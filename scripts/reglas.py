"""Reglas de construcción que evitan errores medibles al dibujar por código.

Cada función resuelve un fallo que la auditoría de un proyecto real encontró y que no
se ve en una prueba PNG a simple vista (ver references/02, «Comprobación matemática»):

  grosor_traslacion   grosor de un trazo curvo con plumilla de eje inclinado
  eje_en_zona         dónde poner el eje de un trazo para que su BORDE toque la zona
  cerrar_desde_tinta  avance = lateral izq. + anchura real de tinta + lateral der.
  alinear_tiradores   tras redondear a enteros, recupera la continuidad G1 en la rejilla

No sustituye a motor.py ni a trazos.py: se usa junto a ellos.
"""
import math

from fontTools.pens.boundsPen import BoundsPen


def grosor_traslacion(ang, grueso, fino, eje):
    """Grosor de un trazo que avanza en la dirección ang (grados) con contraste de
    traslación: es fino cuando avanza paralelo a la plumilla (ángulo eje respecto a la
    horizontal) y grueso en la perpendicular.

    Ojo: con eje ≠ 0, un trazo horizontal NO mide fino sino
    fino + (grueso − fino)·|sen(eje)|. Colocar su eje con fino/2 desplaza el borde
    (en un proyecto real, rebasamientos de 31 u en lugar de 14)."""
    return fino + (grueso - fino) * abs(math.sin(math.radians(ang - eje)))


def eje_en_zona(y_zona, grosor, arriba=True):
    """Altura del eje de un trazo horizontal cuyo borde exterior debe caer en y_zona.

    arriba=True: el borde superior toca y_zona (curva superior con rebasamiento);
    arriba=False: el borde inferior toca y_zona. grosor es el grosor REAL del trazo en
    ese punto (p. ej. grosor_traslacion(0, ...)), no el fino nominal."""
    return y_zona - grosor / 2 if arriba else y_zona + grosor / 2


def cerrar_desde_tinta(glifo):
    """Fija el avance desde la tinta real, no desde la caja del dibujo.

    glifo: un trazos.Glifo o motor.G ya dibujado (con lsb y rsb). Desplaza los contornos
    para que la tinta empiece en x = 0 y llama a cerrar(anchura de tinta), de modo que
    los laterales son exactamente glifo.lsb y glifo.rsb. Sin esto, cualquier forma cuya
    tinta no empiece en el origen del dibujo (curvas, cortes, uniones) hereda un error de
    lateral; en un proyecto real llegó a −15 u en la e."""
    g = glifo.g
    pen = BoundsPen(None)
    g.draw(pen)
    if pen.bounds is None:
        glifo.cerrar(0)
        return
    x0, _, x1, _ = pen.bounds
    x0r, x1r = round(x0), round(x1)
    if x0r:
        g.move((-x0r, 0))
    glifo.cerrar(x1r - x0r)


def _cruz(a, b):
    return a[0] * b[1] - a[1] * b[0]


def alinear_tiradores(contorno, umbral=6.0):
    """Tras redondear a enteros, en cada nodo liso (tangentes a menos de umbral grados)
    elige para sus tiradores la posición entera a ±1 u que deja las tangentes más
    alineadas. Con tiradores cortos el redondeo crea quiebros de 2–3° que check_sources
    marca y que se ven a gran tamaño. No mueve nodos ni toca rectas con rectas."""
    pts = contorno.points
    n = len(pts)
    for i, p in enumerate(pts):
        if p.type is None:
            continue
        a, b = pts[i - 1], pts[(i + 1) % n]
        if a.type is not None and b.type is not None:
            continue

        def angulo(ax, ay, bx, by):
            u1, u2 = (p.x - ax, p.y - ay), (bx - p.x, by - p.y)
            if math.hypot(*u1) < 1e-9 or math.hypot(*u2) < 1e-9:
                return 180.0
            return abs(math.degrees(math.atan2(_cruz(u1, u2), u1[0] * u2[0] + u1[1] * u2[1])))

        base = angulo(a.x, a.y, b.x, b.y)
        if base == 0 or base > umbral:
            continue
        movs = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
        mov_a = [(0, 0)] if a.type is not None else movs
        mov_b = [(0, 0)] if b.type is not None else movs
        mejor = (base, 0, 0, 0, 0)
        for da in mov_a:
            for db in mov_b:
                ang = angulo(a.x + da[0], a.y + da[1], b.x + db[0], b.y + db[1])
                if ang < mejor[0] - 1e-9:
                    mejor = (ang, *da, *db)
        _, dax, day, dbx, dby = mejor
        a.x, a.y, b.x, b.y = a.x + dax, a.y + day, b.x + dbx, b.y + dby
