#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Relevamiento del perfil de Instagram con Chrome real (channel=chrome).

Instagram bloquea el HTML crudo con muro de registro: lo que devuelve curl no
sirve. Aca se abre el perfil con un navegador de verdad y se guardan:
  - el perfil (bio, seguidores, publicaciones, links externos)
  - el HTML y el JSON embebido, para poder auditar la evidencia despues
  - una captura de pantalla
"""
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

PERFIL = sys.argv[1] if len(sys.argv) > 1 else "https://www.instagram.com/lascaracolas_ar/"
DEST = Path(sys.argv[2] if len(sys.argv) > 2 else ".").resolve()
DEST.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    ctx = b.new_context(
        locale="es-AR",
        viewport={"width": 1440, "height": 1000},
        user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"),
    )
    page = ctx.new_page()
    resp = page.goto(PERFIL, wait_until="domcontentloaded", timeout=60000)
    print(f"HTTP={resp.status if resp else '?'} url={page.url}")
    page.wait_for_timeout(6000)

    html = page.content()
    (DEST / "ig-perfil.html").write_text(html, encoding="utf-8")
    try:
        page.screenshot(path=str(DEST / "ig-perfil.png"), full_page=True)
    except Exception as e:
        print("screenshot fallo:", e)

    # --- datos visibles ---
    datos = {"url_pedida": PERFIL, "url_final": page.url, "title": page.title()}
    for sel, key in [('meta[property="og:description"]', "og_description"),
                     ('meta[name="description"]', "meta_description"),
                     ('meta[property="og:title"]', "og_title"),
                     ('meta[property="og:url"]', "og_url")]:
        el = page.query_selector(sel)
        datos[key] = (el.get_attribute("content") if el else None)

    # --- links externos (link en bio, etc.) ---
    links = page.eval_on_selector_all(
        "a[href]", "els => els.map(e => e.href).filter(h => h && !h.includes('instagram.com'))")
    datos["links_externos"] = sorted(set(links))

    # --- textos clave del perfil ---
    cuerpo = page.inner_text("body")[:4000]
    (DEST / "ig-perfil.txt").write_text(cuerpo, encoding="utf-8")
    datos["texto_inicio"] = cuerpo[:1500]

    # --- JSON embebido: counts reales ---
    for m in re.finditer(r'<script type="application/json"[^>]*>(.*?)</script>', html, re.S):
        blob = m.group(1)
        if "edge_followed_by" in blob or "follower_count" in blob or "biography" in blob:
            (DEST / "ig-json.json").write_text(blob, encoding="utf-8")
            break
    datos["tiene_json_embebido"] = (DEST / "ig-json.json").exists()

    (DEST / "ig-perfil.json").write_text(
        json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in datos.items() if k != "texto_inicio"},
                     ensure_ascii=False, indent=2)[:3000])
    b.close()
