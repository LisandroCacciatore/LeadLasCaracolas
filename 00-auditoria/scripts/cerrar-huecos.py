#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cierra los huecos: las dos tiendas de PedidosYa y la actividad real del feed."""
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

DEST = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
out = {}

URLS_PY = [
    ("sushi", "https://www.pedidosya.com.ar/restaurantes/rosario/las-caracolas-sushi-fe0e6153-d0f3-4720-95f2-ea69c36c73bb-menu"),
    ("roti-frescos", "https://www.pedidosya.com.ar/restaurantes/rosario/las-caracolas-1bde2c3f-3cb5-47dc-a3fc-718399d924a6-menu"),
]

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    ctx = b.new_context(locale="es-AR", viewport={"width": 1440, "height": 1000},
                        user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"))
    page = ctx.new_page()

    for nombre, url in URLS_PY:
        try:
            r = page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(7000)
            txt = page.inner_text("body")
            (DEST / f"pedidosya-{nombre}.txt").write_text(txt, encoding="utf-8")
            page.screenshot(path=str(DEST / f"pedidosya-{nombre}.png"))
            out[nombre] = {
                "status": r.status if r else None,
                "url_final": page.url,
                "texto": " ".join(txt.split())[:1400],
            }
        except Exception as e:
            out[nombre] = {"error": str(e)[:200]}

    # --- actividad del feed de Instagram ---
    try:
        page.goto("https://www.instagram.com/lascaracolas_ar/", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(6000)
        # cerrar el modal si aparece
        for sel in ['div[role="dialog"] svg[aria-label="Cerrar"]', 'div[role="dialog"] button']:
            el = page.query_selector(sel)
            if el:
                try: el.click()
                except Exception: pass
                break
        page.wait_for_timeout(2000)
        # bajar para cargar publicaciones
        for _ in range(4):
            page.mouse.wheel(0, 2500)
            page.wait_for_timeout(1800)
        hrefs = page.eval_on_selector_all("a[href*='/p/'], a[href*='/reel/']",
                                          "els => els.map(e => e.href)")
        unicos = []
        for h in hrefs:
            c = h.split("?")[0].rstrip("/")
            if c not in unicos:
                unicos.append(c)
        out["ig_posts_visibles"] = unicos[:24]
        out["ig_posts_visibles_n"] = len(unicos)
        out["ig_link_bio"] = page.eval_on_selector_all(
            "header a[href^='http'], main a[href^='http'][href*='linktr'], a[href*='l.instagram.com']",
            "els => els.map(e => e.href)")
        page.screenshot(path=str(DEST / "ig-perfil-scroll.png"), full_page=False)
    except Exception as e:
        out["ig_error"] = str(e)[:200]

    b.close()

(DEST / "huecos.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2)[:5000])
