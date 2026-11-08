#!/usr/bin/env python3
"""Auditoría de la retícula de decisiones: busca medidas ESTRUCTURALES sueltas en el código
de los glifos (references/02-dibujo-y-correcciones.md §4).

  reticula.py PROYECTO                  revisa los .py del proyecto salvo reticula.py
  reticula.py PROYECTO --estricto       código de salida 1 si queda alguna medida suelta
  reticula.py archivo.py [...]          revisa archivos concretos

Qué cuenta como medida estructural suelta (lo que debe salir de la retícula):
  ancho     una anchura de glifo escrita a mano:            w = 470 · ancho = 512
  altura    una altura de unión, barra o arranque como fracción literal de una zona,
            asignada a una variable (yb = CAP * 0.40) o dentro de asta / barra / rect
  lateral   laterales con cifras: lsb=64 / rsb=40, o fracciones literales al crear el glifo
            con la convención nuevo(u, nombre, cp, 1.0, 0.8)

No cuenta la forma: los nodos de una curva (nodo(...), N(...), contorno((...))) siguen el modelo
de escritura y no se ajustan a módulos. Una medida suelta intencionada se declara en su línea con
un comentario «# retícula: motivo» (por ejemplo, una excepción óptica de un solo glifo); queda
listada como declarada y no bloquea.

La auditoría es léxica: encuentra números escritos, no razona sobre geometría. Una retícula sin
medidas sueltas no garantiza buen diseño; garantiza que cada medida estructural tiene un origen
con nombre y que cambiar un papel mueve todos los glifos que lo usan.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ZONAS = r"(?:X|x|CAP|cap|ASC|asc|DESC|desc|alto|xh|alt|P\[\"x\"\]|P\[\"cap\"\]|m\[\"x\"\]|m\[\"cap\"\])"
FRAC = r"0\.\d+"
PATRONES = {
    "ancho": re.compile(r"^\s*(?:w|ancho|anchura)\s*=\s*\d+(?:\.\d+)?\s*(?:#.*)?$"),
    "altura": re.compile(
        rf"^\s*y\w*\s*=\s*{ZONAS}\s*\*\s*{FRAC}\b"                          # yb = CAP * 0.40
        rf"|\.(?:asta|barra|rect)\([^#]*\b{ZONAS}\s*\*\s*{FRAC}"            # g.barra(…, CAP * 0.5 …)
    ),
    "lateral": re.compile(
        r"\b[lr]sb\s*=\s*\d+(?:\.\d+)?\b(?!\s*\*)"                           # lsb=64
        r"|nuevo\(\s*u\s*,\s*[^,]+,\s*[^,]+,\s*\d+(?:\.\d+)?\s*,\s*\d+(?:\.\d+)?\s*\)"   # nuevo(u, n, cp, 1.0, 0.8)
    ),
}
DECLARADA = re.compile(r"#\s*ret[ií]cula\s*:\s*(\S.*)$", re.I)


def revisar(ruta):
    sueltas, declaradas = [], []
    for i, linea in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1):
        codigo = linea.split("#", 1)[0] if not DECLARADA.search(linea) else linea[:DECLARADA.search(linea).start()]
        for tipo, pat in PATRONES.items():
            if pat.search(codigo if tipo != "ancho" else codigo.rstrip()):
                m = DECLARADA.search(linea)
                item = {"archivo": str(ruta), "linea": i, "tipo": tipo, "codigo": linea.strip()}
                if m:
                    item["motivo"] = m.group(1).strip()
                    declaradas.append(item)
                else:
                    sueltas.append(item)
    return sueltas, declaradas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("rutas", nargs="+", type=Path)
    ap.add_argument("--estricto", action="store_true", help="sale con 1 si queda alguna medida suelta")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    archivos = []
    for r in a.rutas:
        if r.is_dir():
            archivos += sorted(p for p in r.glob("*.py") if p.name != "reticula.py")
        else:
            archivos.append(r)
    sueltas, declaradas = [], []
    for f in archivos:
        s, d = revisar(f)
        sueltas += s
        declaradas += d

    if a.json:
        print(json.dumps({"sueltas": sueltas, "declaradas": declaradas}, ensure_ascii=False, indent=1))
    else:
        cuenta = {t: sum(1 for s in sueltas if s["tipo"] == t) for t in PATRONES}
        print(f"Medidas estructurales sueltas: {len(sueltas)} "
              f"(anchos {cuenta['ancho']} · alturas {cuenta['altura']} · laterales {cuenta['lateral']}); "
              f"declaradas: {len(declaradas)}")
        for s in sueltas:
            print(f"  {Path(s['archivo']).name}:{s['linea']:<5} {s['tipo']:8} {s['codigo'][:90]}")
        for d in declaradas:
            print(f"  {Path(d['archivo']).name}:{d['linea']:<5} declarada  {d['motivo'][:70]}")
        if not archivos:
            print("AVISO: no hay archivos .py que revisar")
    sys.exit(1 if a.estricto and sueltas else 0)


if __name__ == "__main__":
    main()
