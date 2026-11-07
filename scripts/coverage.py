#!/usr/bin/env python3
"""Cobertura lingüística. Uso: coverage.py fuente.ttf [--langs spa,cat,glg,eus,ast,por]

Combina Hyperglot (soporte por idioma) y la lista de glifos faltantes para cada idioma.
Advertencia de Hyperglot: comprueba caracteres, no calidad de diseño ni conformación.
"""
import argparse, json, sys, unicodedata
from pathlib import Path

from fontTools.ttLib import TTFont

from hyperglot.language import Language


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("fuente", type=Path)
    p.add_argument("--langs", default="spa,cat,glg,eus,ast,por,fra,deu,ita")
    p.add_argument("--escritura", default="Latin", help="solo ortografías de esta escritura")
    a = p.parse_args()
    cmap = TTFont(a.fuente, lazy=True).getBestCmap()
    res = {}
    for iso in a.langs.split(","):
        try:
            lg = Language(iso)
            lg.get("name")
        except (KeyError, ValueError):
            res[iso] = {"soportado_base": False, "error": "ISO desconocido en Hyperglot (prueba azj, gug, ayr, nhn)"}
            continue
        base, aux, marcas, punt = set(), set(), set(), set()
        for o in lg.get("orthographies", []):
            if o.get("status", "primary") != "primary" or o.get("script") != a.escritura:
                continue
            for c in (o.get("base") or "").split():
                base.update(c)
            marcas.update(unicodedata.normalize("NFD", o.get("marks") or ""))
            for campo in ("punctuation", "currency", "numerals"):
                punt.update(c for c in (o.get(campo) or "") if not c.isspace())
            for c in (o.get("auxiliary") or "").split():
                aux.update(c)
        # Los acentos pueden llegar precompuestos o como marcas: U+25CC es solo un soporte visual.
        base = {c for c in base if not unicodedata.combining(c) and c != "\u25cc"}
        marcas = {c for c in marcas if unicodedata.combining(c)}
        faltan = sorted(c for c in base if ord(c) not in cmap and not c.isspace())
        res[iso] = {"nombre": lg.get("name"), "soportado_base": not faltan, "faltan_base": "".join(faltan),
                    "faltan_signos": "".join(sorted(c for c in punt if ord(c) not in cmap)),
                    "marcas_ausentes": " ".join(f"U+{ord(c):04X}" for c in sorted(marcas) if ord(c) not in cmap),
                    "faltan_auxiliares": "".join(sorted(c for c in aux if ord(c) not in cmap and not c.isspace()))}
    print(json.dumps(res, ensure_ascii=False, indent=1))
    sys.exit(0 if all(r["soportado_base"] for r in res.values()) else 1)


if __name__ == "__main__":
    main()
