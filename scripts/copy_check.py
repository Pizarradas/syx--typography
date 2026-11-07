#!/usr/bin/env python3
"""Prueba de copia entre dos fuentes compiladas: ¿comparten puntos de control?

  copy_check.py mia.ttf otra.ttf

Lleva cada glifo a su propia caja (anula escala, anchura y desplazamiento), prueba
inclinaciones de -14° a 14° y mide los puntos que coinciden a menos de 6 milésimas, en
ambos sentidos. Solo compara letras y cifras: los símbolos se comparten con frecuencia.
En una variable solo mide el máster por defecto; exporta otras instancias para el resto.

Es una alarma, no un certificado. Una coincidencia alta en muchos glifos indica calco
(razonamiento de Adobe v. Southern Software). Una baja NO prueba originalidad: un redibujo
sigue pasando. Usa solo fuentes que tengas derecho a abrir.
"""
import math, statistics, sys, unicodedata

from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont

INCLINACIONES = [math.tan(math.radians(g)) for g in range(-14, 15, 2)]
TOLERANCIA = 6  # sobre una caja de 1000


def puntos(gs, nombre):
    pen = DecomposingRecordingPen(gs)
    gs[nombre].draw(pen)
    return [p for _, args in pen.value for p in args if p]


def normalizar(pts, inc=0):
    pts = [(x + y * inc, y) for x, y in pts]
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    w, h = (x1 - x0) or 1, (y1 - y0) or 1
    return [((x - x0) * 1000 / w, (y - y0) * 1000 / h) for x, y in pts]


def rejilla(pts):
    return {(round(x / TOLERANCIA), round(y / TOLERANCIA)) for x, y in pts}


def coincidencia(a, b):
    r = rejilla(b)
    hits = 0
    for x, y in a:
        cx, cy = round(x / TOLERANCIA), round(y / TOLERANCIA)
        if any((cx + i, cy + j) in r for i in (-1, 0, 1) for j in (-1, 0, 1)):
            hits += 1
    return hits / len(a)


def mejor(pa, pb):
    na = normalizar(pa)
    res = 0
    for inc in INCLINACIONES:
        res = max(res, coincidencia(na, normalizar(pb, inc)), coincidencia(normalizar(pa, inc), normalizar(pb)))
    return res


def cargar(ruta):
    f = TTFont(ruta, lazy=True)
    return f.getGlyphSet(), f.getBestCmap()


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    gsa, cma = cargar(sys.argv[1])
    gsb, cmb = cargar(sys.argv[2])
    resultados = []
    for cp in sorted(set(cma) & set(cmb)):
        if unicodedata.category(chr(cp))[0] not in "LN":
            continue
        pa, pb = puntos(gsa, cma[cp]), puntos(gsb, cmb[cp])
        if len(pa) < 8 or len(pb) < 8:
            continue
        resultados.append((mejor(pa, pb), chr(cp)))
    if not resultados:
        sys.exit("Sin glifos comparables.")
    resultados.sort(reverse=True)
    print(f"Glifos comparados: {len(resultados)}  ·  mediana de puntos coincidentes: {statistics.median(r[0] for r in resultados):.0%}")
    print("Más coincidentes:", ", ".join(f"{c} {v:.0%}" for v, c in resultados[:15]))
    altos = [r for r in resultados if r[0] >= 0.7]
    print(f"Glifos con 70 % o más de coincidencia: {len(altos)}")
    if len(altos) > max(3, len(resultados) * 0.1):
        print("ALARMA: patrón compatible con calco. Detén el trabajo y revisa el origen.")
        sys.exit(1)


if __name__ == "__main__":
    main()
