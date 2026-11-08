#!/usr/bin/env python3
"""Ejemplo mínimo de generador: n o H O + acento, compartiendo parámetros por máster.

Sirve para comprobar la cadena y como patrón de estructura. NO es un diseño: muestra cómo
un conjunto de parámetros produce másteres compatibles. Uso:
  ejemplo_generador.py sources/PruebaSans.designspace
"""
import sys
from pathlib import Path

import ufoLib2
from fontTools.designspaceLib import DesignSpaceDocument

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from trazos import Glifo

# Parámetros por valor de wght. Las astas siguen una curva cóncava, no una recta.
# La tensión (k_ext, k_int) viaja aquí porque es estilo del proyecto, no del motor:
# cada diseño decide la suya en el brief. NO copies estas cifras: son de este ejemplo.
PARAMS = {
    300: dict(asta=66, fino=60, n=380, o=460, H=560, O=640, lat_n=68, k_ext=0.58, k_int=0.56),
    400: dict(asta=92, fino=82, n=400, o=480, H=590, O=670, lat_n=62, k_ext=0.58, k_int=0.56),
    700: dict(asta=168, fino=138, n=440, o=520, H=640, O=720, lat_n=46, k_ext=0.60, k_int=0.58),
}
REB = 12  # rebasamiento


def notdef(u, p, m):
    g = Glifo(u, ".notdef", lsb=50, rsb=50)
    g.rect(0, 0, 400, m["cap"])
    i, a = p["fino"], m["cap"]
    g.contorno((i, i), (i, a - i), (400 - i, a - i), (400 - i, i))
    g.cerrar(400)


def n(u, p, m):
    x, s, f, w = m["x"], p["asta"], p["fino"], p["n"]
    g = Glifo(u, "n", 0x6E, lsb=p["lat_n"], rsb=round(p["lat_n"] * 0.8))
    g.rect(0, 0, s, x)
    top, cx = x + REB, s + (w - 2 * s) * 0.55
    g.contorno((w, 0), (w, x * 0.62),
               ((w, x * 0.86), (cx + (w - cx) * 0.55, top), (cx, top)),
               ((cx - (cx - s * 0.7) * 0.45, top), (s * 0.7 + (cx - s * 0.7) * 0.18, x * 0.74 + (top - x * 0.74) * 0.38), (s * 0.7, x * 0.74)),
               (s * 0.7, x * 0.58),
               ((s * 0.85, x * 0.66), (cx - (cx - s * 0.7) * 0.3, top - f), (cx, top - f)),
               ((cx + (w - s - cx) * 0.55, top - f), (w - s, x * 0.62 + (top - f - x * 0.62) * 0.55), (w - s, x * 0.62)),
               (w - s, 0))
    g.cerrar(w)


def o(u, p, m):
    x, s, f, w = m["x"], p["asta"], p["fino"], p["o"]
    g = Glifo(u, "o", 0x6F, lsb=round(p["lat_n"] * 0.62), rsb=round(p["lat_n"] * 0.62))
    g.ovalo(w / 2, x / 2, w / 2, x / 2 + REB, p["k_ext"], p["k_ext"])
    g.ovalo(w / 2, x / 2, w / 2 - s * 1.1, x / 2 + REB - f, p["k_int"], p["k_int"], horario=True)
    g.ancla("top", w / 2, x + REB)
    g.cerrar(w)


def H(u, p, m):
    c, s, f, w = m["cap"], p["asta"] * 1.13, p["fino"], p["H"]
    g = Glifo(u, "H", 0x48, lsb=round(p["lat_n"] * 1.3), rsb=round(p["lat_n"] * 1.3))
    g.rect(0, 0, s, c); g.rect(w - s, 0, w, c)
    g.rect(s * 0.5, c * 0.52 - f / 2, w - s * 0.5, c * 0.52 + f / 2)
    g.cerrar(w)


def O(u, p, m):
    c, s, f, w = m["cap"], p["asta"] * 1.13, p["fino"], p["O"]
    g = Glifo(u, "O", 0x4F, lsb=round(p["lat_n"] * 0.8), rsb=round(p["lat_n"] * 0.8))
    g.ovalo(w / 2, c / 2, w / 2, c / 2 + REB, p["k_ext"], p["k_ext"])
    g.ovalo(w / 2, c / 2, w / 2 - s * 1.1, c / 2 + REB - f, p["k_int"], p["k_int"], horario=True)
    g.cerrar(w)


def agudo(u, p, m):
    x, s = m["x"], p["asta"]
    g = Glifo(u, "acutecomb", 0x301)
    b, h = x + 70, x + 220
    g.contorno((-s * 0.3, b), (s * 0.5, b), (s * 1.05, h), (s * 0.15, h))
    g.ancla("_top", s * 0.1, x + REB)
    g.g.width = 0


def espacio(u, p, m):
    g = Glifo(u, "space", 0x20)
    g.g.width = 240


def compuesto(u, p, m):
    g = Glifo(u, "oacute", 0xF3)
    o_g = u["o"]
    g.componente("o")
    g.componente("acutecomb", o_g.anchors[0].x - u["acutecomb"].anchors[0].x, 0)
    g.g.width = o_g.width


def main():
    ds = DesignSpaceDocument.fromfile(sys.argv[1])
    for src in ds.sources:
        val = src.location["Weight"]
        u = ufoLib2.Font.open(src.path)
        p = PARAMS[int(val)]
        m = {"x": u.info.xHeight, "cap": u.info.capHeight}
        for f in (notdef, espacio, n, o, H, O, agudo, compuesto):
            f(u, p, m)
        u.lib["public.glyphOrder"] = [".notdef", "space", "H", "O", "n", "o", "oacute", "acutecomb"]
        u.lib["public.postscriptNames"] = {"acutecomb": "uni0301"}
        u.save(overwrite=True)
        print("escrito", src.path)


if __name__ == "__main__":
    main()
