"""Revisa que la carpeta no tenga secretos ni datos personales antes de subirla a GitHub.

Uso:
    python verificar_privacidad.py            # revisa toda la carpeta; código 1 si encuentra algo
    python verificar_privacidad.py --probar   # autoprueba de los patrones

Términos propios (nombres, usuario de GitHub, IDs, dominios): uno por línea en
`.privacidad-local.txt`, que NUNCA se sube (está en .gitignore). Así la lista negra
no se convierte ella misma en una filtración.
"""
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent
LOCAL = RAIZ / ".privacidad-local.txt"
SALTAR = {".git", "node_modules"}
EXTENSIONES = {".md", ".txt", ".py", ".js", ".gs", ".html", ".json", ".yml", ".yaml", ".csv", ".sh", ""}

PATRONES = {
    "correo": r"[\w.+-]+@(?!ejemplo\.com|example\.com)[\w-]+\.[\w.-]+",
    "llave de Google": r"AIza[0-9A-Za-z_-]{35}",
    "token de bot de Telegram": r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b",
    "llave de Groq": r"gsk_[A-Za-z0-9]{20,}",
    "llave tipo sk-": r"\bsk-[A-Za-z0-9_-]{20,}",
    "token de GitHub": r"\bgh[pousr]_[A-Za-z0-9]{30,}",
    "llave privada": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "enlace de Google (Sheet, Drive, script)": r"(docs|drive|script)\.google\.com/\S+",
    "ID de documento de Google": r"\b1[A-Za-z0-9_-]{43}\b",
    "ID de chat/usuario de Telegram": r"(?<![\w.])-?\d{9,13}\b",
    "celular de Colombia": r"(?<!\d)(\+?57[ -]?)?3\d{2}[ -]?\d{3}[ -]?\d{4}(?!\d)",
    "dominio dinámico o túnel": r"\b[\w-]+\.(duckdns\.org|ngrok\.io|ngrok-free\.app|trycloudflare\.com)\b",
}


def terminos_locales():
    if not LOCAL.exists():
        return []
    return [t.strip() for t in LOCAL.read_text(encoding="utf-8").splitlines() if t.strip() and not t.startswith("#")]


def revisar_texto(texto, locales):
    hallazgos = []
    for n, linea in enumerate(texto.splitlines(), 1):
        for nombre, patron in PATRONES.items():
            if re.search(patron, linea):
                hallazgos.append((n, nombre))
        bajo = linea.lower()
        for t in locales:
            if t.lower() in bajo:
                hallazgos.append((n, "término de .privacidad-local.txt"))
    return hallazgos


def revisar_carpeta():
    locales = terminos_locales()
    total = 0
    for ruta in sorted(RAIZ.rglob("*")):
        if not ruta.is_file() or SALTAR & set(ruta.parts) or ruta in (LOCAL, pathlib.Path(__file__).resolve()) or ruta.suffix.lower() not in EXTENSIONES:
            continue
        for n, nombre in revisar_texto(ruta.read_text(encoding="utf-8", errors="replace"), locales):
            # No se imprime el valor encontrado: solo dónde está y de qué tipo es.
            print(f"{ruta.relative_to(RAIZ)}:{n}: {nombre}")
            total += 1
    if not locales:
        print("Aviso: no hay .privacidad-local.txt; solo se revisaron patrones genéricos.")
    print(f"Resultado: {total} hallazgos.")
    return 1 if total else 0


def probar():
    malos = [
        "contacto: alguien@gmail.com",
        "AIza" + "B" * 35,
        "123456789:" + "A" * 35,
        "gsk_" + "x" * 24,
        "https://docs.google.com/spreadsheets/d/abc",
        "chat -1001234567890",
        "llame al 300 123 4567",
        "https://mi-n8n.duckdns.org",
    ]
    buenos = ["socio@ejemplo.com", "Fase 7 · 5–8 sesiones", "733/733 pruebas", "commit 2574f74", "2026-11-14"]
    for m in malos:
        assert revisar_texto(m, []), f"no detectó: {m}"
    for b in buenos:
        assert not revisar_texto(b, []), f"falso positivo: {b}"
    assert revisar_texto("Hola Fulano", ["fulano"])
    print(f"Autoprueba: {len(malos) + len(buenos) + 1}/{len(malos) + len(buenos) + 1} OK")
    return 0


if __name__ == "__main__":
    sys.exit(probar() if "--probar" in sys.argv else revisar_carpeta())
