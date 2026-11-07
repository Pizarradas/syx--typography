#!/usr/bin/env python3
"""Registro de procedencia. Mantiene la prueba de autoría y de primera divulgación.

  registro.py glifo PROYECTO n,o,H humano "dibujado a mano en FontLab"
  registro.py glifo PROYECTO a codigo-regla-humana "regla humana del brief, trazos.py"
  registro.py sello PROYECTO "aprobado control n o H O"     hash de sources + commit + registro
  registro.py resumen PROYECTO                               recuento por origen y glifos sin registrar

Orígenes: humano | codigo-regla-humana | ia-modificado-humano | ia-generado | heredado-desconocido
El hash fecha el contenido solo ante quien confíe en el archivo: para valor probatorio,
sella además con un tercero (ver references/08).
"""
import csv, hashlib, subprocess, sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import ufoLib2
from fontTools.designspaceLib import DesignSpaceDocument

ORIGENES = {"humano", "codigo-regla-humana", "ia-modificado-humano", "ia-generado", "heredado-desconocido"}


def hash_fuentes(proj):
    h = hashlib.sha256()
    for f in sorted((proj / "sources").rglob("*")):
        if f.is_file():
            h.update(str(f.relative_to(proj)).encode()); h.update(f.read_bytes())
    return h.hexdigest()


def ahora():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    acc, proj = sys.argv[1], Path(sys.argv[2]).resolve()
    csv_p = proj / "registro" / "procedencia_glifos.csv"
    if acc == "glifo":
        if len(sys.argv) < 5:
            sys.exit(__doc__)
        glifos, origen, detalle = sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else ""
        if origen not in ORIGENES:
            sys.exit(f"Origen no válido. Usa uno de {sorted(ORIGENES)}")
        with csv_p.open("a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            for g in glifos.split(","):
                w.writerow([g, origen, detalle, ahora()])
    elif acc == "sello":
        nota = sys.argv[3] if len(sys.argv) > 3 else ""
        r = subprocess.run(["git", "-C", str(proj), "rev-parse", "HEAD"], capture_output=True, text=True)
        commit = r.stdout.strip() if r.returncode == 0 else "sin-commit"
        sucio = subprocess.run(["git", "-C", str(proj), "status", "--porcelain", "sources"], capture_output=True, text=True).stdout.strip()
        if sucio or commit == "sin-commit":
            print("AVISO: sources/ tiene cambios sin confirmar: confirma en git para que el sello sea trazable.", file=sys.stderr)
        linea = f"{ahora()}\t{hash_fuentes(proj)}\t{commit}{'+sucio' if sucio else ''}\t{nota}\n"
        with (proj / "registro" / "sellos.tsv").open("a", encoding="utf-8") as f:
            f.write(linea)
        print(linea.strip())
    elif acc == "resumen":
        ultimo = {}
        with csv_p.open(encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                ultimo[fila["glifo"]] = fila["origen"]
        ds = DesignSpaceDocument.fromfile(next((proj / "sources").glob("*.designspace")))
        todos = set().union(*(ufoLib2.Font.open(x.path).keys() for x in ds.sources))
        print("Por origen:", dict(Counter(ultimo.values())))
        faltan = sorted(todos - set(ultimo))
        print(f"Sin registrar ({len(faltan)}):", " ".join(faltan[:40]))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
