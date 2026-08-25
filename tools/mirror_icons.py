#!/usr/bin/env python3
"""A Framer Phosphor-ikonmodulok teljes készletének lokális tükrözése.

A site futásidőben tölti be az ikonokat a framer.com/m/phosphor-icons/
címről; ez a szkript mind az 1494 ikont letölti a docs/m/phosphor-icons/
mappába, a bennük hivatkozott framerusercontent.com modulokat is lokálisra
hozza, majd a shared-lib bundle-ben átírja a betöltő URL-t lokálisra.

Futtatás:  python3 tools/mirror_icons.py   (a mirror.py UTÁN)
"""
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "docs"
ICON_DIR = SITE / "m" / "phosphor-icons"
SHARED_LIB = next(SITE.glob("sites/*/shared-lib.*.mjs"))
VERSION = "@0.0.57"
CDN = "https://framerusercontent.com"
CDN_RE = re.compile(r"https://framerusercontent\.com(/[A-Za-z0-9_\-./~%@]+)")
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) trustfunnel-mirror"}


def fetch(url: str) -> bytes:
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers=UA), timeout=30) as r:
                return r.read()
        except Exception:
            if attempt == 2:
                raise
    raise RuntimeError("unreachable")


def main() -> None:
    text = SHARED_LIB.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"([A-Za-z]+(?:\.[A-Za-z0-9]+){50,})`\.split", text)
    if not m:
        sys.exit("Nem találom az ikonnév-listát a shared-lib bundle-ben.")
    names = m.group(1).split(".")
    print(f"{len(names)} ikon tükrözése...")
    ICON_DIR.mkdir(parents=True, exist_ok=True)

    module_paths: set[str] = set()
    failed: list[str] = []

    def grab_icon(name: str) -> None:
        dest = ICON_DIR / f"{name}.js"
        if dest.exists():
            data = dest.read_bytes()
        else:
            try:
                data = fetch(f"https://framer.com/m/phosphor-icons/{name}.js{VERSION}")
            except Exception as e:
                failed.append(f"{name}: {e}")
                return
            dest.write_bytes(data)
        for mm in CDN_RE.finditer(data.decode("utf-8", errors="replace")):
            module_paths.add(mm.group(1))

    with ThreadPoolExecutor(max_workers=16) as ex:
        list(ex.map(grab_icon, names))
    print(f"Ikonmodulok kész ({len(failed)} hiba); {len(module_paths)} CDN-modul jön.")

    def grab_module(path: str) -> None:
        dest = SITE / path.lstrip("/")
        if dest.exists():
            return
        try:
            data = fetch(CDN + path)
        except Exception as e:
            failed.append(f"{path}: {e}")
            return
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)

    with ThreadPoolExecutor(max_workers=16) as ex:
        list(ex.map(grab_module, sorted(module_paths)))

    # Átírás: az ikon- és modulfájlokban CDN → gyökér-relatív
    for f in list(ICON_DIR.glob("*.js")) + [
        SITE / p.lstrip("/") for p in module_paths
    ]:
        if not f.exists():
            continue
        t = f.read_text(encoding="utf-8", errors="replace")
        n = t.replace(CDN + "/", "/").replace(CDN, "/")
        if n != t:
            f.write_text(n, encoding="utf-8")

    # A shared-lib betöltőjének átírása lokálisra, verziósuffix nélkül
    text = SHARED_LIB.read_text(encoding="utf-8", errors="replace")
    new = text.replace("https://framer.com/m/phosphor-icons/", "/m/phosphor-icons/")
    new = new.replace(f".js{VERSION}", ".js")
    if new != text:
        SHARED_LIB.write_text(new, encoding="utf-8")
        print("shared-lib bundle átírva lokális ikonbetöltésre.")

    if failed:
        print(f"{len(failed)} HIBA:")
        for x in failed[:20]:
            print(" ", x)
        sys.exit(1)
    print("KÉSZ.")


if __name__ == "__main__":
    main()
