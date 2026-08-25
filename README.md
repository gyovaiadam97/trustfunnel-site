# Trustfunnel.hu — önállóan hostolt statikus oldal

A www.trustfunnel.hu céges weboldal Framerről lementett, teljesen önálló
statikus másolata. Cél: a Framer-előfizetés (évi ~60e Ft) kiváltása —
az oldal GitHub Pages-en fut ingyen.

## Felépítés

- `docs/` — a kész statikus oldal, ezt szolgálja ki a GitHub Pages
  (main ág, `/docs` mappa). Két oldal: `/` és `/kontakt`.
- `tools/mirror.py` — az eredeti Framer-oldal tükrözése: HTML + minden
  framerusercontent.com asset letöltése, hivatkozások gyökér-relatívra
  írása, Framer-analitika és szerkesztősáv eltávolítása.
- `tools/mirror_icons.py` — a futásidőben betöltött Phosphor-ikonmodulok
  (1494 db) teljes készletének lokális tükrözése + a betöltő átírása.

## Fontos tudnivalók

- Az oldal "befagyott" másolat: tartalommódosítás a `docs/` HTML/asset
  fájljainak szerkesztésével történik (Claude-dal), nem a Framerben.
- Külső függések szándékosan megtartva: Google Fonts (fonts.gstatic.com)
  és YouTube-beágyazások. Framer-függés NINCS.
- A `docs/CNAME` fájl köti a www.trustfunnel.hu domaint a Pages-hez.
- A tükröző szkriptek csak addig futtathatók újra, amíg az eredeti
  Framer-oldal él; utána a `docs/` a tartalom egyetlen forrása.

## Deploy

Commit + push a `main` ágra → a GitHub Pages automatikusan frissül
(1-2 perc). Ellenőrzés: https://www.trustfunnel.hu
