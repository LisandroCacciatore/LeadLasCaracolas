#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""¿El sitio se adapta al celular? Medido con viewport real, no con --window-size.

Chrome en Windows no baja de ~500px de ventana, así que una captura con
--window-size=390 sale recortada y parece un bug de layout que no existe.
Playwright sí aplica el viewport de verdad, y además mide el desborde.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8942/"
DEST = Path(sys.argv[1]).resolve()
DEST.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for nombre, w, h in (("movil-390", 390, 844), ("tablet-768", 768, 1024),
                         ("desktop-1440", 1440, 900)):
        ctx = b.new_context(viewport={"width": w, "height": h},
                            device_scale_factor=1, is_mobile=(w < 500),
                            has_touch=(w < 500), locale="es-AR")
        pg = ctx.new_page()
        pg.goto(URL, wait_until="load")
        pg.wait_for_timeout(2500)
        m = pg.evaluate("""() => {
            const de = document.documentElement;
            const desbordan = [];
            document.querySelectorAll('body *').forEach(el => {
                const r = el.getBoundingClientRect();
                if (r.width > 0 && (r.right > de.clientWidth + 1 || r.left < -1)) {
                    desbordan.push(el.tagName.toLowerCase() +
                        (el.className && typeof el.className === 'string'
                          ? '.' + el.className.split(' ')[0] : '') +
                        ' → ' + Math.round(r.left) + '..' + Math.round(r.right));
                }
            });
            return {
                viewport: de.clientWidth,
                scrollWidth: de.scrollWidth,
                desborde_horizontal: de.scrollWidth > de.clientWidth + 1,
                elementos_desbordados: desbordan.slice(0, 8),
                n_desbordados: desbordan.length,
                alto_total: document.body.scrollHeight,
            };
        }""")
        print(f"\n=== {nombre} (viewport {m['viewport']}px) ===")
        print(f"  scrollWidth: {m['scrollWidth']}  →  desborde horizontal: "
              f"{'SÍ' if m['desborde_horizontal'] else 'no'}")
        print(f"  alto total: {m['alto_total']}px")
        if m["n_desbordados"]:
            print(f"  {m['n_desbordados']} elemento(s) se salen:")
            for d in m["elementos_desbordados"]:
                print(f"    - {d}")
        pg.screenshot(path=str(DEST / f"{nombre}.png"), full_page=True)
        ctx.close()
    b.close()
