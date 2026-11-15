"""Checks that this folder has no secrets or personal data before pushing it to GitHub.

Usage:
    python check_privacy.py          # scans the whole folder; exit code 1 if anything is found
    python check_privacy.py --test   # self-test of the patterns

Project-specific terms (names, IDs, domains): one per line in `.privacy-local.txt`,
which is NEVER pushed (it is in .gitignore), so the denylist itself is not a leak.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
LOCAL = ROOT / ".privacy-local.txt"
SKIP = {".git", "node_modules"}
EXTENSIONS = {".md", ".txt", ".py", ".js", ".gs", ".html", ".json", ".yml", ".yaml", ".csv", ".sh", ""}

PATTERNS = {
    "email": r"[\w.+-]+@(?!example\.com|ejemplo\.com)[\w-]+\.[\w.-]+",
    "Google API key": r"AIza[0-9A-Za-z_-]{35}",
    "Telegram bot token": r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b",
    "Groq key": r"gsk_[A-Za-z0-9]{20,}",
    "sk- style key": r"\bsk-[A-Za-z0-9_-]{20,}",
    "GitHub token": r"\bgh[pousr]_[A-Za-z0-9]{30,}",
    "private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "Google link (Sheet, Drive, script)": r"(docs|drive|script)\.google\.com/\S+",
    "Google document ID": r"\b1[A-Za-z0-9_-]{43}\b",
    "Telegram chat/user ID": r"(?<![\w.])-?\d{9,13}\b",
    "Colombian mobile number": r"(?<!\d)(\+?57[ -]?)?3\d{2}[ -]?\d{3}[ -]?\d{4}(?!\d)",
    "dynamic DNS or tunnel domain": r"\b[\w-]+\.(duckdns\.org|ngrok\.io|ngrok-free\.app|trycloudflare\.com)\b",
}


def local_terms():
    if not LOCAL.exists():
        return []
    return [t.strip() for t in LOCAL.read_text(encoding="utf-8").splitlines() if t.strip() and not t.startswith("#")]


def check_text(text, terms):
    findings = []
    for n, line in enumerate(text.splitlines(), 1):
        for name, pattern in PATTERNS.items():
            if re.search(pattern, line):
                findings.append((n, name))
        low = line.lower()
        for t in terms:
            if t.lower() in low:
                findings.append((n, "term from .privacy-local.txt"))
    return findings


def check_folder():
    terms = local_terms()
    total = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or SKIP & set(path.parts) or path in (LOCAL, pathlib.Path(__file__).resolve()) or path.suffix.lower() not in EXTENSIONS:
            continue
        for n, name in check_text(path.read_text(encoding="utf-8", errors="replace"), terms):
            # The matched value is never printed: only where it is and what kind it is.
            print(f"{path.relative_to(ROOT)}:{n}: {name}")
            total += 1
    if not terms:
        print("Warning: no .privacy-local.txt found; only generic patterns were checked.")
    print(f"Result: {total} findings.")
    return 1 if total else 0


def self_test():
    bad = [
        "contact: someone@gmail.com",
        "AIza" + "B" * 35,
        "123456789:" + "A" * 35,
        "gsk_" + "x" * 24,
        "https://docs.google.com/spreadsheets/d/abc",
        "chat -1001234567890",
        "call 300 123 4567",
        "https://my-n8n.duckdns.org",
    ]
    good = ["partner@example.com", "Phase 7 · 5–8 sessions", "733/733 tests", "commit 2574f74", "2026-11-14"]
    for b in bad:
        assert check_text(b, []), f"not detected: {b}"
    for g in good:
        assert not check_text(g, []), f"false positive: {g}"
    assert check_text("Hello Fulano", ["fulano"])
    n = len(bad) + len(good) + 1
    print(f"Self-test: {n}/{n} OK")
    return 0


if __name__ == "__main__":
    sys.exit(self_test() if "--test" in sys.argv else check_folder())
