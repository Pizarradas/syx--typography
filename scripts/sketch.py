#!/usr/bin/env python3
"""Bocetos rápidos de tipografía: de los parámetros al PNG, sin proyecto ni compilación.

Un archivo de boceto define VARIANTES (nombre -> parámetros) y glifos(ufo, p), que
dibuja con las primitivas de motor.py y trazos.py sobre un UFO en memoria (patrón:
assets/ejemplo_boceto.py). Cada variante se renderiza como un panel con las líneas
pedidas y todas se apilan en una hoja única, para comparar de un vistazo.

  sketch.py BOCETO.py -o hoja.png --texto "noon HOHO" [--texto "otra línea"]

Un boceto juzga FORMA y COLOR, no espaciado: los avances son los declarados por cada
glifo y no hay kerning ni conformación. Nada de aquí se publica: el camino a la
fuente real es new_project.py y las mismas funciones de glifo en el generador.
"""
import argparse
import importlib.util
import sys
from pathlib import Path

import ufoLib2
from fontTools.pens.recordingPen import DecomposingRecordingPen
from PIL import Image, ImageDraw, ImageFont

CLARO = dict(placa=(250, 248, 243, 255), tinta=(17, 17, 17, 255), gris=(138, 132, 120, 255))
OSCURO = dict(placa=(22, 19, 16, 255), tinta=(236, 230, 219, 255), gris=(150, 143, 130, 255))


def cargar_boceto(ruta):
    spec = importlib.util.spec_from_file_location("boceto", ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["boceto"] = mod
    spec.loader.exec_module(mod)
    if not hasattr(mod, "VARIANTES") or not hasattr(mod, "glifos"):
        raise SystemExit(f"{ruta}: un archivo de boceto define VARIANTES y glifos(ufo, p)")
    return mod


def _etiqueta_fuente():
    for ruta in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                 "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf"):
        if Path(ruta).exists():
            return ImageFont.truetype(ruta, 20)
    return ImageFont.load_default()


def poligonos(u, nombre, pasos=28):
    """Contornos del glifo (componentes resueltos) aplanados a polígonos."""
    pen = DecomposingRecordingPen(u)
    u[nombre].draw(pen)
    polis, cur = [], []
    for op, args in pen.value:
        if op == "moveTo":
            cur = [args[0]]
        elif op == "lineTo":
            cur.append(args[0])
        elif op == "curveTo":
            p0, (c1, c2, p3) = cur[-1], args
            for j in range(1, pasos + 1):
                t = j / pasos
                mt = 1 - t
                cur.append((mt**3 * p0[0] + 3 * mt * mt * t * c1[0] + 3 * mt * t * t * c2[0] + t**3 * p3[0],
                            mt**3 * p0[1] + 3 * mt * mt * t * c1[1] + 3 * mt * t * t * c2[1] + t**3 * p3[1]))
        elif op == "closePath":
            if len(cur) > 2:
                polis.append(cur)
            cur = []
    return polis


def area(p):
    return sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1]
               for i in range(len(p))) / 2


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("archivo", type=Path, help="archivo de boceto (VARIANTES + glifos)")
    p.add_argument("-o", "--salida", type=Path, default=Path("boceto.png"))
    p.add_argument("--texto", action="append", help="línea de palabras; repetible")
    p.add_argument("--variantes", help="subconjunto por nombre, separado por comas")
    p.add_argument("--cuerpo", type=float, default=150, help="píxeles por em (150)")
    p.add_argument("--oscuro", action="store_true", help="paleta clara sobre placa oscura")
    a = p.parse_args()

    mod = cargar_boceto(a.archivo.resolve())
    nombres = [s.strip() for s in a.variantes.split(",")] if a.variantes else list(mod.VARIANTES)
    for nv in nombres:
        if nv not in mod.VARIANTES:
            raise SystemExit(f"variante desconocida: {nv} (hay: {', '.join(mod.VARIANTES)})")
    lineas = a.texto or ["noon HOHO"]
    col = OSCURO if a.oscuro else CLARO
    fuente_et = _etiqueta_fuente()
    faltan = set()

    # Prepara cada variante: dibuja el UFO en memoria y aplana sus glifos.
    paneles = []
    for nv in nombres:
        u = ufoLib2.Font()
        mod.glifos(u, dict(mod.VARIANTES[nv]))
        upm = u.info.unitsPerEm or 1000
        esc = a.cuerpo / upm
        cmap = {cp: g.name for g in u for cp in (g.unicodes or [])}
        cache = {}

        def glifo(nombre):
            if nombre not in cache:
                cache[nombre] = [(pl, area(pl)) for pl in poligonos(u, nombre)]
            return cache[nombre]

        filas, ymin, ymax = [], 0.0, upm * 0.72
        for linea in lineas:
            pen_x, dibujos = 0.0, []
            for ch in linea:
                if ch.isspace():
                    pen_x += u["space"].width if "space" in u else upm * 0.3
                    continue
                gn = cmap.get(ord(ch))
                if gn is None:
                    faltan.add(ch)
                    continue
                for pl, ar in glifo(gn):
                    dibujos.append(([(x + pen_x, y) for x, y in pl], ar))
                    ys = [q[1] for q in pl]
                    ymin, ymax = min(ymin, min(ys)), max(ymax, max(ys))
                pen_x += u[gn].width
            filas.append((dibujos, pen_x))
        paneles.append((nv, filas, esc, ymin, ymax))

    # Composición de la hoja.
    MX, ETIQ, ENTRE = 56, 44, 30
    ancho = max(int(f[1] * pn[2]) for pn in paneles for f in pn[1]) + 2 * MX
    altos = []
    for nv, filas, esc, ymin, ymax in paneles:
        alto_linea = (ymax - ymin) * esc + 18
        altos.append(int(ETIQ + len(filas) * alto_linea + 18))
    hoja = Image.new("RGBA", (ancho, sum(altos) + ENTRE * (len(paneles) - 1) + 2 * 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(hoja)
    d.rounded_rectangle([0, 0, hoja.width - 1, hoja.height - 1], 26, fill=col["placa"])
    y0 = 14
    for (nv, filas, esc, ymin, ymax), alto in zip(paneles, altos):
        d.text((MX, y0 + 8), nv, fill=col["gris"], font=fuente_et)
        alto_linea = (ymax - ymin) * esc + 18
        for i, (dibujos, _) in enumerate(filas):
            base = y0 + ETIQ + i * alto_linea + ymax * esc
            for pl, ar in sorted(dibujos, key=lambda t: -abs(t[1])):
                d.polygon([(MX + x * esc, base - y * esc) for x, y in pl],
                          fill=col["tinta"] if ar > 0 else col["placa"])
        y0 += alto + ENTRE
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    hoja.save(a.salida)
    print(a.salida)
    print("boceto: juzga forma y color; sin espaciado real ni kerning, no publicable")
    if faltan:
        print(f"AVISO: caracteres sin glifo en el boceto, omitidos: {''.join(sorted(faltan))}")


if __name__ == "__main__":
    main()
