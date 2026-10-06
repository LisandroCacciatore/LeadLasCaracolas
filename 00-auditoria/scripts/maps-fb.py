#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Maps + Facebook con Chrome real: lo que el curl no puede leer."""
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

DEST = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
DEST.mkdir(parents=True, exist_ok=True)
out = {}

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    ctx = b.new_context(locale="es-AR", viewport={"width": 1440, "height": 1000},
                        user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"))
    page = ctx.new_page()

    # --- 1. Google Maps: ficha del negocio ---
    try:
        page.goto("https://www.google.com/maps/search/Las+Caracolas+pescaderia+Corrientes+1402+Rosario/",
                  wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(7000)
        page.screenshot(path=str(DEST / "maps-caracolas.png"), full_page=False)
        txt = page.inner_text("body")
        (DEST / "maps-caracolas.txt").write_text(txt, encoding="utf-8")
        out["maps_texto"] = txt[:2200]
        out["maps_url"] = page.url
    except Exception as e:
        out["maps_error"] = str(e)

    # --- 2. Facebook ---
    try:
        page.goto("https://www.facebook.com/lascaracolas.ar/",
                  wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(6000)
        page.screenshot(path=str(DEST / "fb-caracolas.png"), full_page=False)
        meta = page.eval_on_selector_all("meta", "els => els.map(e => [e.getAttribute('property')||e.getAttribute('name'), e.getAttribute('content')]).filter(x=>x[0]&&x[1])")
        out["fb_meta"] = dict(meta)
        out["fb_title"] = page.title()
        out["fb_texto"] = page.inner_text("body")[:1200]
    except Exception as e:
        out["fb_error"] = str(e)

    b.close()

(DEST / "maps-fb.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2)[:4000])
