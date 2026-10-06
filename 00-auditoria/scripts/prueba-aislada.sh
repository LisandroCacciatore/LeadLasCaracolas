#!/usr/bin/env bash
# Verificacion aislada: se reemplazan SOLO las plantillas del motor actual en la
# copia temporal, para que lo que se pruebe sea el print.js nuevo y no el viejo
# que el lead tiene pegado adentro.
set -u
TMP="$LOCALAPPDATA/Temp/prueba-negocio"
M="/c/Users/Torso/motor-leads"
cd "$TMP" || exit 1

echo "=== que print.js tenia el lead vs el del motor ==="
grep -n "cover__subtitle" templates/print.js | head -2
echo "  --- motor ---"
grep -n "cover__subtitle" "$M/templates/print.js" | head -2

echo
echo "=== reemplazo las plantillas del motor actual ==="
cp -f "$M"/templates/* templates/
cp -f "$M"/scripts/generate.py scripts/
echo "  listo"

echo
echo "=== config: negocio presente + profesion todavia presente ==="
python - <<'PY'
import json, pathlib
c = json.loads(pathlib.Path("config.json").read_text(encoding="utf-8"))
print("  negocio  :", repr(c["meta"].get("negocio")))
print("  profesion:", repr(c["meta"].get("profesion")))
PY

python scripts/generate.py >/tmp/g3.log 2>&1 || { echo "generate fallo"; tail -15 /tmp/g3.log; exit 1; }
echo "  generate ok"
echo
echo "=== portada renderizada (con el print.js NUEVO) ==="
python "C:/Users/Torso/audit-caracolas-scratch/leer-portada.py" "$TMP"

echo
echo "=== ahora quito «negocio»: tiene que caer a «profesion» ==="
python - <<'PY'
import json, pathlib
p = pathlib.Path("config.json")
c = json.loads(p.read_text(encoding="utf-8"))
c["meta"].pop("negocio", None)
p.write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding="utf-8")
print("  negocio eliminado; profesion queda:", repr(c["meta"].get("profesion")))
PY
python scripts/generate.py >/tmp/g4.log 2>&1 && echo "  generate ok" || { echo "  fallo"; tail -10 /tmp/g4.log; }
python "C:/Users/Torso/audit-caracolas-scratch/leer-portada.py" "$TMP"
