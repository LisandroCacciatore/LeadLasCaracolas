#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mide el alcance real del feed: por cada publicacion visible, la fecha, los
me gusta y los comentarios tal como Instagram los declara en sus propias metas.
Un seguidor no es un alcance: esto separa los dos numeros."""
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

DEST = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
SHORTCODES = json.loads((DEST / "huecos.json").read_text(encoding="utf-8"))["ig_posts_visibles"]
filas = []

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    ctx = b.new_context(locale="es-AR", user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"))
    pg = ctx.new_page()
    for u in SHORTCODES:
        short = u.rstrip("/").split("/")[-1]
        tipo = "reel" if "/reel/" in u else "post"
        fila = {"shortcode": short, "tipo": tipo, "url": u}
        try:
            pg.goto(u, wait_until="domcontentloaded", timeout=45000)
            pg.wait_for_timeout(4000)
            meta = pg.query_selector('meta[name="description"]') or pg.query_selector('meta[property="og:description"]')
            txt = (meta.get_attribute("content") or "") if meta else ""
            fila["meta"] = txt[:400]
            m = re.match(r"([\d.,]+)\s+likes?,\s+([\d.,]+)\s+comments?\s*-\s*\S+\s+el\s+(\w+\s+\d+,\s+\d+)", txt)
            if m:
                fila["likes"] = int(m.group(1).replace(".", "").replace(",", ""))
                fila["comments"] = int(m.group(2).replace(".", "").replace(",", ""))
                fila["fecha"] = m.group(3)
            t = pg.query_selector("time[datetime]")
            fila["iso"] = t.get_attribute("datetime") if t else None
        except Exception as e:
            fila["error"] = str(e)[:120]
        filas.append(fila)
        print(f"  {short:16} {fila.get('fecha','?'):20} likes={fila.get('likes','?'):>6} com={fila.get('comments','?'):>4}  {(fila.get('meta','') or '')[:70]}")
    b.close()

(DEST / "alcance-feed.json").write_text(json.dumps(filas, ensure_ascii=False, indent=2), encoding="utf-8")
ok = [f for f in filas if "likes" in f]
if ok:
    ls = sorted(f["likes"] for f in ok)
    seg = 56918
    print(f"\npublicaciones medidas: {len(ok)}")
    print(f"me gusta: min={ls[0]} mediana={ls[len(ls)//2]} max={ls[-1]} promedio={sum(ls)/len(ls):.0f}")
    print(f"tasa de interaccion (mediana/seguidores): {ls[len(ls)//2]/seg*100:.3f}%")
    print(f"tasa de interaccion (promedio/seguidores): {sum(ls)/len(ls)/seg*100:.3f}%")
