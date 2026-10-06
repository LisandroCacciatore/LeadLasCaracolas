#!/usr/bin/env bash
# Prueba de compatibilidad: el motor nuevo tiene que seguir generando bien una
# config VIEJA (la de Lagos usa `profesion` y `matricula`), y ademas tiene que
# respetar `negocio` cuando esta presente. Se corre sobre una COPIA temporal
# para no tocar el lead entregado.
set -u
TMP="$LOCALAPPDATA/Temp/prueba-negocio"
rm -rf "$TMP"
cp -r /c/Users/Torso/lead-lagos-lisandro "$TMP"
cd "$TMP" || exit 1

echo "=== config de entrada (vieja, con profesion y matricula) ==="
python - <<'PY'
import json, pathlib
p = pathlib.Path("config.json")
c = json.loads(p.read_text(encoding="utf-8"))
m = c["meta"]
print("  profesion:", repr(m.get("profesion")))
print("  matricula:", repr(m.get("matricula")))
print("  negocio  :", repr(m.get("negocio")))
PY

echo
echo "=== PASO 1: generar con la config vieja sin tocar ==="
python scripts/generate.py >/tmp/gen1.log 2>&1 && echo "  generate.py exit=0" || { echo "  ✗ generate.py fallo"; tail -20 /tmp/gen1.log; }
python - <<'PY'
import pathlib, re
for f in ("00-auditoria/informe.html", "01-propuesta/propuesta.html"):
    p = pathlib.Path(f)
    if not p.exists():
        print(f"  {f}: NO EXISTE"); continue
    t = p.read_text(encoding="utf-8")
    print(f"  {f}:")
    print("     viejo: ¿aparece «Psicoanalista»?", "Psicoanalista" in t)
    print("     viejo: ¿aparece la matrícula?", "5677" in t)
    print("     ¿quedó algún {{PLACEHOLDER}} sin sustituir?",
          sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", t)))[:5] or "ninguno")
PY

echo
echo "=== PASO 2: agregar «negocio» y ver si gana ==="
python - <<'PY'
import json, pathlib
p = pathlib.Path("config.json")
c = json.loads(p.read_text(encoding="utf-8"))
c["meta"]["negocio"] = "PRUEBA-NEGOCIO-NUEVO"
p.write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding="utf-8")
print("  agregado meta.negocio = 'PRUEBA-NEGOCIO-NUEVO' (profesion sigue estando)")
PY
python scripts/generate.py >/tmp/gen2.log 2>&1 && echo "  generate.py exit=0" || { echo "  ✗ fallo"; tail -20 /tmp/gen2.log; }
python - <<'PY'
import pathlib
t = pathlib.Path("00-auditoria/informe.html").read_text(encoding="utf-8")
print("  ¿aparece PRUEBA-NEGOCIO-NUEVO?", "PRUEBA-NEGOCIO-NUEVO" in t)
print("  ¿sigue apareciendo Psicoanalista?", "Psicoanalista" in t)
print("  veredicto:",
      "negocio pisa a profesion (correcto)" if "PRUEBA-NEGOCIO-NUEVO" in t
      else "negocio NO se aplicó")
PY
