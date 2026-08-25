#!/usr/bin/env python3
"""Trustfunnel.hu Framer-oldal tükrözése lokális, önálló statikus oldallá.

Letölti a HTML-oldalakat és az összes framerusercontent.com assetet
(képek, fontok, JS-modulok, rekurzívan a JS-ből hivatkozottakat is),
majd a hivatkozásokat gyökér-relatívra írja át. A Framer-analitikát
és a szerkesztő-scriptet eltávolítja.

Futtatás:  python3 tools/mirror.py
Kimenet:   docs/ mappa (index.html, kontakt/index.html, images/, sites/, assets/ ...)
"""
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "docs"
ORIGIN = "https://www.trustfunnel.hu"
CDN = "https://framerusercontent.com"

PAGES = {
    "/": SITE / "index.html",
    "/kontakt": SITE / "kontakt" / "index.html",
}

# framerusercontent URL-ek (query nélkül — a GitHub Pages úgyis eldobja a query-t)
CDN_RE = re.compile(r"https://framerusercontent\.com(/[A-Za-z0-9_\-./~%@]+)")
# relatív .mjs importok a JS-chunkokban
REL_IMPORT_RE = re.compile(r"""["'](\./[A-Za-z0-9_\-.]+\.mjs)["']""")

UA = {"User-Agent": "Mozilla/5.0 (Macintosh) trustfunnel-mirror"}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception as e:
            if attempt == 2:
                raise
            print(f"  ÚJRA ({e}): {url}", file=sys.stderr)
            time.sleep(2)
    raise RuntimeError("unreachable")


def local_path(cdn_path: str) -> Path:
    return SITE / cdn_path.lstrip("/")


def main() -> None:
    SITE.mkdir(parents=True, exist_ok=True)

    htmls: dict[Path, str] = {}
    queue: list[str] = []  # CDN path-ek (pl. /images/xxx.png)
    seen: set[str] = set()

    for page, dest in PAGES.items():
        print(f"Oldal letöltése: {page}")
        html = fetch(ORIGIN + page).decode("utf-8")
        htmls[dest] = html
        for m in CDN_RE.finditer(html):
            p = m.group(1)
            if p not in seen:
                seen.add(p)
                queue.append(p)

    downloaded = 0
    failed: list[str] = []
    while queue:
        p = queue.pop()
        dest = local_path(p)
        if not dest.exists():
            try:
                data = fetch(CDN + p)
            except Exception as e:
                print(f"  HIBA: {p} — {e}", file=sys.stderr)
                failed.append(p)
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            downloaded += 1
            if downloaded % 25 == 0:
                print(f"  {downloaded} asset kész, {len(queue)} a sorban...")
        else:
            data = dest.read_bytes()

        # JS-fájlokból további hivatkozások kigyűjtése
        if p.endswith((".mjs", ".js", ".json", ".css")):
            text = data.decode("utf-8", errors="replace")
            for m in CDN_RE.finditer(text):
                np = m.group(1)
                if np not in seen:
                    seen.add(np)
                    queue.append(np)
            base = p.rsplit("/", 1)[0]
            for m in REL_IMPORT_RE.finditer(text):
                np = base + "/" + m.group(1)[2:]
                if np not in seen:
                    seen.add(np)
                    queue.append(np)

    print(f"Összesen {downloaded} asset letöltve, {len(failed)} hiba.")
    if failed:
        print("Sikertelen letöltések:")
        for p in failed:
            print(f"  {p}")

    # A Framer szerkesztősáv betöltője helyett üres modul (soha ne aktiválódjon)
    NOOP_EDITOR = "data:text/javascript,export const createEditorBar=()=>()=>null"

    # JS/CSS/JSON fájlokban az abszolút CDN-hivatkozások átírása gyökér-relatívra
    rewritten = 0
    for f in SITE.rglob("*"):
        if f.suffix in {".mjs", ".js", ".json", ".css"} and f.is_file():
            text = f.read_text(encoding="utf-8", errors="replace")
            new = text.replace("https://framer.com/edit/init.mjs", NOOP_EDITOR)
            new = new.replace(CDN + "/", "/").replace(CDN, "/")
            if new != text:
                f.write_text(new, encoding="utf-8")
                rewritten += 1
    print(f"{rewritten} JS/CSS fájlban átírva a CDN-hivatkozás.")

    # HTML-ek átírása és mentése
    for dest, html in htmls.items():
        # Framer-analitika és szerkesztő-init eltávolítása
        html = re.sub(r'<script[^>]*events\.framer\.com[^>]*>\s*</script>', "", html)
        html = re.sub(r'<script[^>]*events\.framer\.com[^>]*/?>', "", html)
        html = re.sub(r'<link[^>]*framer\.com/edit/init\.mjs[^>]*/?>', "", html)
        html = re.sub(r'<script>[^<]*framer\.com/edit/init\.mjs[^<]*</script>', "", html)
        html = html.replace("<!-- Made in Framer · framer.com ✨ -->", "")
        # CDN → gyökér-relatív (a query stringek maradhatnak, a Pages eldobja őket)
        html = html.replace(CDN + "/", "/").replace(CDN, "/")
        # saját abszolút linkek relatívvá
        html = html.replace(ORIGIN + "/", "/").replace(ORIGIN, "/")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        print(f"Mentve: {dest.relative_to(ROOT)}")

    print("KÉSZ.")


if __name__ == "__main__":
    main()
