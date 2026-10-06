#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dónde aparece cada dato repetido, con su contexto, en la propuesta generada."""
import re
from pathlib import Path

P = Path("01-propuesta/propuesta.html")
t = P.read_text(encoding="utf-8")

for dato in ("0,19", "64,8", "56.918", "741", "107"):
    ocurrencias = [m.start() for m in re.finditer(re.escape(dato), t)]
    print(f"\n=== «{dato}»: {len(ocurrencias)} aparición(es) en la propuesta ===")
    for i in ocurrencias:
        frag = t[max(0, i - 130):i + 70]
        frag = re.sub(r"\s+", " ", frag)
        # ubicar la sección más cercana hacia atrás
        seccion = ""
        m = re.findall(r'id="([a-z\-]+)"|data-seccion="([^"]+)"|class="seccion[^"]*"', t[:i])
        if m:
            seccion = " ".join(x for tupla in m[-1] for x in tupla if x)[:28]
        print(f"  [{i:6}] ({seccion or '—'}) …{frag}…")
