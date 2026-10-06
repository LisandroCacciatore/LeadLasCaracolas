#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lee la portada renderizada: lo unico que prueba que «negocio» llega a la hoja."""
import pathlib
import sys
from playwright.sync_api import sync_playwright

TMP = pathlib.Path(sys.argv[1]).resolve()
INFORME = TMP / "00-auditoria" / "informe.html"

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_context().new_page()
    pg.goto(INFORME.as_uri(), wait_until="load")
    pg.wait_for_timeout(4000)
    for sel in (".cover__title", ".cover__subtitle", ".cover__client-sub"):
        els = pg.query_selector_all(sel)
        for i, e in enumerate(els):
            print(f"  {sel}[{i}]: {e.inner_text().strip()!r}")
    b.close()
