#!/usr/bin/env python3
"""Donna: bot de Telegram de CEREBRO (escenario B, hibrido).

Carriles:
  1. Saludos y gracias -> banco de frases (FRASES.json). Instantaneo, sin modelos.
  2. Tareas, compromisos, estados, ideas, notas -> Gemma local clasifica; el codigo
     escribe la confirmacion y calcula las fechas. Ningun modelo puede inventar hechos.
  3. Charla -> Fledge (OpenCode) con limite de tiempo; si falla, Gemma; si falla, el banco.
  4. Fotos/documentos/voz/video -> se guardan siempre en 00_INBOX/adjuntos.

Todo se captura primero en 00_INBOX. Nada se borra. Solo responde al dueño.
"""
import base64
import collections
import datetime
import json
import os
import queue
import random
import re
import threading
import time
import urllib.request
from pathlib import Path

if os.environ.get("CEREBRO_SOLO_IPV4", "0") == "1":  # activar solo si el log muestra llamadas lentas a Telegram
    import socket
    _gai = socket.getaddrinfo
    socket.getaddrinfo = lambda host, port, family=0, type=0, proto=0, flags=0: _gai(host, port, socket.AF_INET, type, proto, flags)

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OWNER = os.environ.get("CEREBRO_OWNER_ID", "").strip()
RAIZ = Path(os.environ.get("CEREBRO_RAIZ", "/srv/cerebro"))
INBOX = Path(os.environ.get("CEREBRO_INBOX", str(RAIZ / "00_INBOX")))
LOGS = Path(os.environ.get("CEREBRO_LOGS", str(RAIZ / "_SISTEMA" / "logs")))
DONNA = Path(os.environ.get("CEREBRO_DONNA", str(RAIZ / "_SISTEMA" / "donna")))
MODELO = os.environ.get("CEREBRO_MODELO", "gemma4:e2b-it-qat")
OLLAMA = os.environ.get("CEREBRO_OLLAMA", "http://127.0.0.1:11434/api/chat")
VOZ = os.environ.get("CEREBRO_VOZ", "opencode")  # "opencode" (con respaldo Gemma) o "gemma"
OPENCODE_URL = os.environ.get("CEREBRO_OPENCODE_URL", "http://127.0.0.1:49374")
OPENCODE_MODELO = os.environ.get("CEREBRO_OPENCODE_MODELO", "opencode/fledge-alpha-free")
OPENCODE_TIMEOUT = float(os.environ.get("CEREBRO_OPENCODE_TIMEOUT", "8"))
CHISPA = float(os.environ.get("CEREBRO_CHISPA", "0.35"))  # probabilidad de comentario en ideas/notas
AVISO_RECORDATORIO = os.environ.get("CEREBRO_AVISO_RECORDATORIO", "1") == "1"
API = "https://api.telegram.org/bot" + TOKEN + "/"

TIPOS = ["tarea", "compromiso_mio", "compromiso_de_otro", "idea", "nota", "estado", "charla"]
ESQUEMA = {"type": "object", "properties": {
    "tipo": {"type": "string", "enum": TIPOS},
    "persona": {"type": "string"}, "fecha_texto": {"type": "string"},
    "proyecto": {"type": "string"}, "bloqueo": {"type": "string"},
    "animo": {"type": "string", "enum": ["normal", "agobiado"]}},
    "required": ["tipo", "persona", "fecha_texto", "proyecto", "bloqueo", "animo"]}

SISTEMA_DEFECTO = """Clasificas notas en español. Responde solo JSON.
tipo: tarea = algo que yo debo hacer, con una acción concreta; compromiso_mio = algo que yo prometí a otra persona; compromiso_de_otro = algo que otra persona me prometió a mí; idea = una ocurrencia o propuesta creativa, sin obligación; nota = información que conviene guardar y no pide acción; estado = algo que cambió en mi situación (se acabó algo, algo se rompió, algo llegó); charla = saludo, pregunta o mensaje dirigido al asistente, sin nada que anotar.
Si dudas entre tarea y nota, elige nota.
persona: la persona involucrada, o "" si no hay.
fecha_texto: la expresión de fecha tal como aparece (por ejemplo "el lunes", "el día 15", "mañana"), sin convertirla. "" si no hay.
proyecto: solo el nombre de un proyecto, cliente o marca (por ejemplo wagency o Lily). Nunca objetos ni entregables como "la canción" o "el logo". "" si no hay.
bloqueo: lo que impide avanzar, o "" si nada.
animo: "agobiado" si el mensaje expresa agobio, cansancio o sentirse desbordado; si no, "normal".
Ejemplo: "enviar la factura a Ana el miércoles" -> {"tipo":"compromiso_mio","persona":"Ana","fecha_texto":"el miércoles","proyecto":"","bloqueo":"","animo":"normal"}
Ejemplo: "Luis me debe el boceto para el martes" -> {"tipo":"compromiso_de_otro","persona":"Luis","fecha_texto":"el martes","proyecto":"","bloqueo":"","animo":"normal"}
Ejemplo: "idea: sesión de fotos en la panadería" -> {"tipo":"idea","persona":"","fecha_texto":"","proyecto":"","bloqueo":"","animo":"normal"}
Ejemplo: "se acabó el café" -> {"tipo":"estado","persona":"","fecha_texto":"","proyecto":"","bloqueo":"","animo":"normal"}
Ejemplo: "pagar el hosting el viernes" -> {"tipo":"tarea","persona":"","fecha_texto":"el viernes","proyecto":"","bloqueo":"","animo":"normal"}
Ejemplo: "no puedo más, tengo todo atrasado" -> {"tipo":"charla","persona":"","fecha_texto":"","proyecto":"","bloqueo":"","animo":"agobiado"}"""

DEFECTO = {
    "saludo": {"madrugada": ["Aquí estoy. ¿Qué traes?"], "manana": ["Buenos días. ¿Qué toca?"],
               "tarde": ["Buenas tardes. ¿Qué toca?"], "noche": ["Buenas noches. ¿Qué toca?"]},
    "espera": ["Un segundo, lo ubico."],
    "calma": ["Una cosa a la vez. Escoge la que más quema y empezamos por ahí."],
    "comentario": ["Me gusta por dónde va."],
    "gracias": ["Para eso estoy."],
    "charla_respaldo": ["Aquí estoy. Cuéntame más."],
}

PROHIBIDAS = ["mi amor", "cariño", "cielo", "de nuevo", "otra vez", "como siempre"]
BASE = {"tarea": "Tarea anotada", "compromiso_mio": "Compromiso tuyo anotado",
        "compromiso_de_otro": "Compromiso de otra persona anotado", "idea": "Idea guardada",
        "nota": "Nota guardada", "estado": "Estado anotado"}
DIAS = {"lunes": 0, "martes": 1, "miércoles": 2, "miercoles": 2, "jueves": 3,
        "viernes": 4, "sábado": 5, "sabado": 5, "domingo": 6}
DIAS_ES = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
EXT_OK = {".jpg", ".jpeg", ".png", ".webp", ".pdf", ".txt", ".md", ".docx", ".xlsx", ".csv",
          ".ogg", ".oga", ".mp3", ".m4a", ".mp4"}
MAX_ADJUNTO = 19 * 1024 * 1024

cola = queue.Queue()
candado = threading.Lock()


# ---------------------------------------------------------------- Telegram
def api(metodo, _timeout=60, **params):
    t0 = time.time()
    try:
        req = urllib.request.Request(API + metodo, json.dumps(params).encode(),
                                     {"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=_timeout) as r:
            return json.load(r)
    finally:
        dur = time.time() - t0
        if dur > 5 and metodo != "getUpdates":
            log("telegram_lento", {"metodo": metodo, "segundos": round(dur, 1)})


def decir(chat, texto):
    return api("sendMessage", chat_id=chat, text=texto)


def responder(chat, texto, msg_id):
    return api("sendMessage", _timeout=20, chat_id=chat, text=texto,
               reply_parameters={"message_id": int(msg_id), "allow_sending_without_reply": True})


def entregar(chat, ack_id, texto, msg_id):
    """Edita el acuse inicial con la respuesta final; si no se puede, manda mensaje nuevo."""
    if ack_id:
        try:
            api("editMessageText", _timeout=20, chat_id=chat, message_id=ack_id, text=texto)
            return
        except Exception:
            pass
    responder(chat, texto, msg_id)


def log(accion, detalle):
    try:
        LOGS.mkdir(parents=True, exist_ok=True)
        linea = {"cuando": datetime.datetime.now().isoformat(timespec="seconds"),
                 "accion": accion, "detalle": detalle}
        with open(LOGS / "ia.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(linea, ensure_ascii=False) + "\n")
    except Exception as e:
        print("no pude escribir el log:", type(e).__name__, flush=True)


# ---------------------------------------------------------------- Banco de frases
_recientes = collections.defaultdict(lambda: collections.deque(maxlen=3))


def frases():
    try:
        return json.loads((DONNA / "FRASES.json").read_text(encoding="utf-8"))
    except Exception:
        return DEFECTO


def elegir(clave, lista):
    lista = [x for x in lista if isinstance(x, str) and x.strip()]
    if not lista:
        return ""
    rec = _recientes[clave]
    opciones = [x for x in lista if x not in rec] or lista
    x = random.choice(opciones)
    rec.append(x)
    return x


def banco(cat, sub=None):
    for fuente in (frases(), DEFECTO):
        try:
            v = fuente[cat]
            if sub is not None:
                v = v[sub]
            f = elegir(cat + (sub or ""), v)
            if f:
                return f
        except Exception:
            continue
    return ""


def periodo(h):
    if h < 5:
        return "madrugada"
    if h < 12:
        return "manana"
    if h < 19:
        return "tarde"
    return "noche"


GREET = (r"(?:hola+|holi+|buenas(?:\s+(?:tardes|noches|dias|días))?|buen(?:os)?\s+d[ií]as?|"
         r"hey+|ey+|saludos|qu[eé]\s+tal|qu[eé]\s+hubo|qu[eé]\s+onda)")
NOMBRE = r"(?:[\s,]*(?:donna|dona|jefe|jefa|amiga|asistente))?"
COLA = r"(?:[\s,¿]*(?:qu[eé]\s+tal|c[oó]mo\s+est[aá]s|c[oó]mo\s+va|c[oó]mo\s+andas))?"
FIN = r"[\s!¡.¿?,]*"


def es_saludo(t):
    return bool(re.fullmatch(r"[¡¿\s]*" + GREET + NOMBRE + COLA + FIN, t.strip(), re.I))


def es_gracias(t):
    return bool(re.fullmatch(r"(?:muchas\s+)?gracias(?:\s+por\s+todo)?" + NOMBRE + FIN, t.strip(), re.I))


# ---------------------------------------------------------------- Fechas (las calcula el codigo)
def resolver_fecha(texto, hoy):
    t = texto.lower()
    if not t.strip():
        return ""
    d = datetime.timedelta
    if "pasado mañana" in t or "pasado manana" in t:
        return (hoy + d(days=2)).isoformat()
    if re.search(r"\bhoy\b|esta (?:mañana|manana|tarde|noche)", t):
        return hoy.isoformat()
    for nombre, n in DIAS.items():
        if nombre in t:
            return (hoy + d(days=((n - hoy.weekday()) % 7) or 7)).isoformat()
    if "mañana" in t or "manana" in t:
        return (hoy + d(days=1)).isoformat()
    m = re.search(r"(\d{1,2})\s*/\s*(\d{1,2})", t)
    if m:
        dia, mes = int(m.group(1)), int(m.group(2))
        for anio in (hoy.year, hoy.year + 1):
            try:
                f = datetime.date(anio, mes, dia)
            except ValueError:
                return ""
            if f >= hoy:
                return f.isoformat()
        return ""
    m = re.search(r"(?:d[ií]a|el)\s+(\d{1,2})\b", t)
    if m:
        dia, mes, anio = int(m.group(1)), hoy.month, hoy.year
        for _ in range(2):
            try:
                f = datetime.date(anio, mes, dia)
            except ValueError:
                f = None
            if f and f >= hoy:
                return f.isoformat()
            mes += 1
            if mes > 12:
                mes, anio = 1, anio + 1
    return ""


MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]


def fecha_bonita(f):
    try:
        d = datetime.date.fromisoformat(f)
        hoy = datetime.date.today()
        base = DIAS_ES[d.weekday()] + " " + str(d.day) + " de " + MESES[d.month - 1]
        if d == hoy:
            return "hoy, " + base
        if d == hoy + datetime.timedelta(days=1):
            return "mañana, " + base
        return "el " + base
    except Exception:
        return f


# ---------------------------------------------------------------- Inbox (Markdown con frontmatter)
def escribir(ruta, datos, texto):
    lineas = ["---"] + [k + ": " + json.dumps(v, ensure_ascii=False) for k, v in datos.items()]
    lineas += ["---", "", texto, ""]
    tmp = ruta.with_suffix(".tmp")
    tmp.write_text("\n".join(lineas), encoding="utf-8")
    tmp.replace(ruta)


def leer(ruta):
    _, fm, resto = ruta.read_text(encoding="utf-8").split("---", 2)
    datos = {}
    for linea in fm.strip().splitlines():
        k, v = linea.split(": ", 1)
        datos[k] = json.loads(v)
    return datos, resto.strip()


def guardar(msg):
    ahora = datetime.datetime.now()
    stem = ahora.strftime("%Y%m%d-%H%M%S") + "-" + str(msg["message_id"])
    datos = {"origen": "telegram", "capturado_en": ahora.isoformat(timespec="seconds"),
             "chat": msg["chat"]["id"], "estado": "recibido",
             "enviado_en": datetime.datetime.fromtimestamp(msg["date"]).isoformat(timespec="seconds")}
    INBOX.mkdir(parents=True, exist_ok=True)
    with candado:
        escribir(INBOX / (stem + ".md"), datos, msg["text"])
    return stem


def actualizar(stem, **cambios):
    ruta = INBOX / (stem + ".md")
    with candado:
        datos, texto = leer(ruta)
        datos.update(cambios)
        escribir(ruta, datos, texto)


# ---------------------------------------------------------------- Modelos
def sistema():
    try:
        return (DONNA / "CLASIFICADOR.md").read_text(encoding="utf-8")
    except Exception:
        return SISTEMA_DEFECTO


def ficha():
    return (DONNA / "FICHA_CORTA.md").read_text(encoding="utf-8")


def clasificar(texto):
    cuerpo = {"model": MODELO, "stream": False, "think": False, "format": ESQUEMA,
              "keep_alive": "10m", "options": {"temperature": 0},
              "messages": [{"role": "system", "content": sistema()},
                           {"role": "user", "content": texto}]}
    req = urllib.request.Request(OLLAMA, json.dumps(cuerpo).encode(),
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        r = json.loads(json.load(r)["message"]["content"])
    out = {"tipo": r.get("tipo") if r.get("tipo") in TIPOS else "nota",
           "persona": str(r.get("persona") or ""), "fecha_texto": str(r.get("fecha_texto") or ""),
           "proyecto": str(r.get("proyecto") or ""), "bloqueo": str(r.get("bloqueo") or ""),
           "animo": "agobiado" if r.get("animo") == "agobiado" else "normal"}
    return out


def voz_gemma(f, entrada):
    cuerpo = {"model": MODELO, "stream": False, "think": False, "keep_alive": "10m",
              "options": {"temperature": 0.8, "num_predict": 100},
              "messages": [{"role": "system", "content": f}, {"role": "user", "content": entrada}]}
    req = urllib.request.Request(OLLAMA, json.dumps(cuerpo).encode(),
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["message"]["content"]


def _opencode(metodo, ruta, datos=None):
    cab = {"Content-Type": "application/json"}
    try:
        svc = json.loads((Path.home() / ".config" / "opencode" / "service.json").read_text(encoding="utf-8"))
        if svc.get("password"):
            cab["Authorization"] = "Basic " + base64.b64encode(("opencode:" + svc["password"]).encode()).decode()
    except Exception:
        pass
    req = urllib.request.Request(OPENCODE_URL + ruta, json.dumps(datos or {}).encode(), cab, method=metodo)
    with urllib.request.urlopen(req, timeout=OPENCODE_TIMEOUT) as r:
        return json.load(r)


def voz_opencode(f, entrada):
    proveedor, _, modelo = OPENCODE_MODELO.partition("/")
    sid = _opencode("POST", "/api/session", {"model": {"providerID": proveedor, "id": modelo}})["data"]["id"]
    return _opencode("POST", "/api/session/" + sid + "/generate",
                     {"prompt": f + "\n\nENTRADA:\n" + entrada})["data"]["text"]


def validar(crudo):
    t = " ".join((crudo or "").split()).strip('"')
    if not t or len(t) > 320 or any(p in t.lower() for p in PROHIBIDAS):
        return None
    frases_ = re.split(r"(?<=[.!?])\s+", t)
    return " ".join(frases_[:2]).strip() or None


def conversar(texto):
    ahora = datetime.datetime.now()
    entrada = "MODO: CHARLA | MENSAJE: " + texto + " | hora=" + ahora.strftime("%H:%M")
    try:
        f = ficha()
    except Exception:
        return banco("charla_respaldo")
    for via in (["opencode", "gemma"] if VOZ == "opencode" else ["gemma"]):
        t0 = time.time()
        try:
            crudo = voz_opencode(f, entrada) if via == "opencode" else voz_gemma(f, entrada)
            out = validar(crudo)
            if out:
                log("voz", {"via": via, "segundos": round(time.time() - t0, 1), "respuesta": out})
                return out
            log("voz_descartada", {"via": via, "crudo": (crudo or "")[:160]})
        except Exception as e:
            log("voz_error", {"via": via, "error": type(e).__name__, "segundos": round(time.time() - t0, 1)})
    return banco("charla_respaldo")


# ---------------------------------------------------------------- Respuestas con hechos (las escribe el codigo)
def confirmar(r, fecha):
    t = BASE.get(r["tipo"], "Anotado")
    if r["persona"]:
        t += " con " + r["persona"]
    if r["proyecto"] and r["proyecto"].strip().lower() != r["persona"].strip().lower():
        t += " (" + r["proyecto"] + ")"
    if fecha:
        t += " para " + fecha_bonita(fecha)
    t += ". Queda en el inbox."
    if AVISO_RECORDATORIO and fecha and r["tipo"] in ("tarea", "compromiso_mio", "compromiso_de_otro"):
        t += " Ojo: aún no te aviso ese día."
    return t


# ---------------------------------------------------------------- Proceso
def escribiendo(chat):
    try:
        api("sendChatAction", _timeout=5, chat_id=chat, action="typing")
    except Exception:
        pass


def procesar(stem, chat, ack_id):
    ruta = INBOX / (stem + ".md")
    with candado:
        datos, texto = leer(ruta)
    msg_id = stem.rsplit("-", 1)[1]
    t0 = time.time()
    threading.Thread(target=escribiendo, args=(chat,), daemon=True).start()
    try:
        r = clasificar(texto)
    except Exception as e:
        log("clasificar_error", {"archivo": stem, "error": type(e).__name__})
        actualizar(stem, estado="sin_clasificar")
        entregar(chat, ack_id, "Quedó guardado en el inbox, pero no pude clasificarlo ahora.", msg_id)
        return
    fecha = resolver_fecha(r["fecha_texto"], datetime.date.today())
    log("clasificar", {"archivo": stem, "modelo": MODELO, "segundos": round(time.time() - t0, 1),
                       "propuesta": r, "fecha_calculada": fecha})
    if r["tipo"] == "charla":
        actualizar(stem, tipo="charla", estado="charla", animo=r["animo"])
        resp = banco("calma") if r["animo"] == "agobiado" else conversar(texto)
        entregar(chat, ack_id, resp, msg_id)
        return
    actualizar(stem, tipo=r["tipo"], persona=r["persona"], fecha_texto=r["fecha_texto"], fecha=fecha,
               proyecto=r["proyecto"], bloqueo=r["bloqueo"], animo=r["animo"], estado="propuesto")
    resp = confirmar(r, fecha)
    if r["animo"] == "agobiado":
        resp += " " + banco("calma")
    elif r["tipo"] in ("idea", "nota") and random.random() < CHISPA:
        resp += " " + banco("comentario")
    entregar(chat, ack_id, resp, msg_id)


def trabajador():
    while True:
        stem, chat, ack_id = cola.get()
        try:
            procesar(stem, chat, ack_id)
        except Exception as e:
            print("error procesando:", type(e).__name__, e, flush=True)


# ---------------------------------------------------------------- Adjuntos
def guardar_adjunto(msg, chat):
    msg_id = msg["message_id"]
    info = msg["photo"][-1] if msg.get("photo") else (msg.get("document") or msg.get("voice") or msg.get("video"))
    if info.get("file_size", 0) > MAX_ADJUNTO:
        responder(chat, "Ese archivo pesa demasiado para bajarlo por Telegram. Ponlo directo en la carpeta.", msg_id)
        return
    try:
        remota = api("getFile", file_id=info["file_id"])["result"]["file_path"]
        ext = os.path.splitext(remota)[1].lower()
        if ext not in EXT_OK:
            ext = ".bin"
        req = urllib.request.Request("https://api.telegram.org/file/bot" + TOKEN + "/" + remota)
        with urllib.request.urlopen(req, timeout=60) as r:
            binario = r.read(MAX_ADJUNTO + 1)
        if len(binario) > MAX_ADJUNTO:
            raise ValueError("grande")
    except Exception as e:
        log("adjunto_error", {"error": type(e).__name__})
        responder(chat, "No pude bajar ese archivo. Mándamelo otra vez o ponlo directo en la carpeta.", msg_id)
        return
    caption = (msg.get("caption") or "").strip()
    m = dict(msg)
    m["text"] = caption or "(adjunto sin descripción)"
    stem = guardar(m)
    nombre = stem + ext
    carpeta = INBOX / "adjuntos"
    carpeta.mkdir(parents=True, exist_ok=True)
    (carpeta / nombre).write_bytes(binario)
    cambios = {"adjunto": "adjuntos/" + nombre, "nombre_original": (msg.get("document") or {}).get("file_name", "")}
    if not caption:
        cambios["estado"] = "adjunto"
    actualizar(stem, **cambios)
    log("adjunto", {"archivo": stem, "tipo": ext, "bytes": len(binario), "con_descripcion": bool(caption)})
    if caption:
        ack = responder(chat, banco("espera"), msg_id)
        cola.put((stem, chat, ack["result"]["message_id"]))
    else:
        responder(chat, "Guardado en el inbox. Si me dices de qué va, lo clasifico.", msg_id)


def manejar(u):
    msg = u.get("message")
    if not msg or msg["chat"]["type"] != "private":
        return
    uid, chat = str(msg["from"]["id"]), msg["chat"]["id"]
    texto = msg.get("text")
    if not OWNER:
        if texto and texto.startswith("/start"):
            decir(chat, "Tu ID de Telegram es " + uid + ". Guárdalo en el servidor y reinicia el bot.")
        return
    if uid != OWNER:
        return
    if texto is None:
        if msg.get("photo") or msg.get("document") or msg.get("voice") or msg.get("video"):
            guardar_adjunto(msg, chat)
        else:
            decir(chat, "Eso no lo sé guardar todavía. Prueba con texto, fotos o documentos.")
        return
    if texto.startswith("/start"):
        decir(chat, banco("saludo", periodo(datetime.datetime.now().hour)))
        return
    stem = guardar(msg)
    if es_saludo(texto) or es_gracias(texto):
        frase = banco("gracias") if es_gracias(texto) else banco("saludo", periodo(datetime.datetime.now().hour))
        actualizar(stem, tipo="charla", estado="charla")
        responder(chat, frase, msg["message_id"])
        log("saludo", {"archivo": stem, "via": "banco"})
        return
    ack_id = None
    try:
        ack_id = responder(chat, banco("espera"), msg["message_id"])["result"]["message_id"]
    except Exception:
        pass
    cola.put((stem, chat, ack_id))


def reencolar_pendientes():
    for ruta in sorted(INBOX.glob("2*.md")):
        try:
            datos, _ = leer(ruta)
            if datos.get("origen") == "telegram" and datos.get("estado") in ("recibido", "sin_clasificar"):
                cola.put((ruta.stem, datos["chat"], None))
        except Exception:
            pass


def main():
    INBOX.mkdir(parents=True, exist_ok=True)
    reencolar_pendientes()
    threading.Thread(target=trabajador, daemon=True).start()
    offset = None
    print("bot en marcha; dueño configurado:", bool(OWNER), "| voz:", VOZ, flush=True)
    while True:
        try:
            params = {"timeout": 30, "allowed_updates": ["message"]}
            if offset:
                params["offset"] = offset
            for u in api("getUpdates", **params).get("result", []):
                offset = u["update_id"] + 1
                try:
                    manejar(u)
                except Exception as e:
                    print("error manejando:", type(e).__name__, e, flush=True)
        except Exception as e:
            print("error de red:", type(e).__name__, flush=True)
            time.sleep(5)


if __name__ == "__main__":
    main()
