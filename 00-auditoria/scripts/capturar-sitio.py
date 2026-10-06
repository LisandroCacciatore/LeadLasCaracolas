#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Captura el sitio servido: escritorio y celular, para mirarlo antes de mostrarlo."""
import subprocess
import sys
from pathlib import Path

DEST = Path(sys.argv[1]).resolve()
DEST.mkdir(parents=True, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
URL = "http://127.0.0.1:8942/"

for nombre, ancho, alto in (("desktop.png", 1440, 3000), ("mobile.png", 390, 2600)):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
                    "--hide-scrollbars", "--virtual-time-budget=8000",
                    f"--window-size={ancho},{alto}", f"--screenshot={DEST / nombre}", URL],
                   capture_output=True, text=True, errors="replace")
    p = DEST / nombre
    print(f"  {nombre}: {p.stat().st_size // 1024} KB" if p.exists() else f"  {nombre}: FALLO")
