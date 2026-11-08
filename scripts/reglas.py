"""Reglas de construcción que evitan errores medibles al dibujar por código.

Cada función resuelve un fallo que la auditoría de un proyecto real encontró y que no
se ve en una prueba PNG a simple vista (ver references/02, «Comprobación matemática»):

  grosor_traslacion   grosor de un trazo curvo con plumilla de eje inclinado
  eje_en_zona         dónde poner el eje de un trazo para que su BORDE toque la zona
  cerrar_desde_tinta  avance = lateral izq. + anchura real de tinta + lateral der.
  alinear_tiradores   tras redondear a enteros, recupera la continuidad G1 en la rejilla
  armonizar_g2        iguala la curvatura a ambos lados de cada nodo liso (G2), con límites

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


# -- curvatura G2 en forma cerrada --------------------------------------------------------
def _resta(a, b):
    return (a[0] - b[0], a[1] - b[1])


def _limite_triangulo(p0, d0, p3, d3):
    """Distancia desde p3 al cruce de las tangentes: p0 con dirección d0 y p3 con d3, ambas
    apuntando hacia el interior de la curva. None si no se cruzan por delante."""
    det = _cruz(d0, d3)
    if abs(det) < 1e-9:
        return None
    t3 = _cruz(_resta(p3, p0), d0) / det
    return t3 if t3 > 0 else None


def _cubica_sana(p0, p1, p2, p3):
    """Sin inflexión y sin extremos H/V interiores que sobresalgan más de 0,5 u."""
    P = [(p.x, p.y) for p in (p0, p1, p2, p3)]
    signos = set()
    for j in range(1, 40):
        t = j / 40
        m = 1 - t
        a = [3 * m * m * (P[1][i] - P[0][i]) + 6 * m * t * (P[2][i] - P[1][i]) + 3 * t * t * (P[3][i] - P[2][i]) for i in (0, 1)]
        b = [6 * m * (P[2][i] - 2 * P[1][i] + P[0][i]) + 6 * t * (P[3][i] - 2 * P[2][i] + P[1][i]) for i in (0, 1)]
        c = a[0] * b[1] - a[1] * b[0]
        if abs(c) > 1e-6:
            signos.add(c > 0)
        pt = [m**3 * P[0][i] + 3 * m * m * t * P[1][i] + 3 * m * t * t * P[2][i] + t**3 * P[3][i] for i in (0, 1)]
        for i in (0, 1):
            if pt[i] > max(P[0][i], P[3][i]) + 0.5 or pt[i] < min(P[0][i], P[3][i]) - 0.5:
                return False
    return len(signos) <= 1


def armonizar_g2(glifo, pasadas=40, lo=0.4, hi=2.0, techo=0.80):
    """Iguala la curvatura a ambos lados de cada nodo liso entre dos cúbicas.

    En el extremo de una cúbica κ = (2/3)·δ/h², con h la longitud del tirador y δ la
    distancia del tirador opuesto a la tangente. Se busca κ* = √(κa·κb) y se despeja
    h = √(2δ / 3κ*), moviendo cada tirador solo a lo largo de su tangente (G1 intacto).
    Límites: lo–hi del tirador original y ≤ techo del cruce de tangentes (tensión
    máxima). Si un cambio crea una inflexión o un extremo interior, retrocede (75, 50, 25,
    0 %). No toca esquinas ni nodos de inflexión. Úsalo sobre el contorno final (tras las
    booleanas) y antes de redondear; después, alinear_tiradores."""
    for c in glifo.contours:
        pts = c.points
        n = len(pts)
        orig = {}
        for _ in range(pasadas):
            for i, p in enumerate(pts):
                if p.type != "curve":
                    continue
                a, b = pts[i - 1], pts[(i + 1) % n]
                if a.type is not None or b.type is not None:
                    continue
                P0, P1, P3 = pts[i - 3], pts[i - 2], p
                Q2, Q3 = pts[(i + 2) % n], pts[(i + 3) % n]
                da, db = _resta((P3.x, P3.y), (a.x, a.y)), _resta((b.x, b.y), (P3.x, P3.y))
                ha, hb = math.hypot(*da), math.hypot(*db)
                if ha < 1e-6 or hb < 1e-6:
                    continue
                ua, ub = (da[0] / ha, da[1] / ha), (db[0] / hb, db[1] / hb)
                if abs(_cruz(ua, ub)) > math.sin(math.radians(1.5)) or ua[0] * ub[0] + ua[1] * ub[1] < 0:
                    continue  # esquina
                ca = _cruz(ua, _resta((P1.x, P1.y), (P3.x, P3.y)))
                cb = _cruz(ub, _resta((Q2.x, Q2.y), (P3.x, P3.y)))
                if ca * cb <= 0 or abs(ca) < 1e-6 or abs(cb) < 1e-6:
                    continue  # inflexión en el nodo (signos opuestos) o tramo recto
                ks = math.sqrt((2 / 3) * abs(ca) / ha**2 * (2 / 3) * abs(cb) / hb**2)
                orig.setdefault(i, (ha, hb))
                ha0, hb0 = orig[i]
                ha_n = min(max(math.sqrt(2 * abs(ca) / (3 * ks)), lo * ha0), hi * ha0)
                hb_n = min(max(math.sqrt(2 * abs(cb) / (3 * ks)), lo * hb0), hi * hb0)
                la = _limite_triangulo((P0.x, P0.y), _resta((P1.x, P1.y), (P0.x, P0.y)), (P3.x, P3.y), (-ua[0], -ua[1]))
                lb = _limite_triangulo((Q3.x, Q3.y), _resta((Q2.x, Q2.y), (Q3.x, Q3.y)), (P3.x, P3.y), ub)
                if la:
                    ha_n = min(ha_n, techo * la)
                if lb:
                    hb_n = min(hb_n, techo * lb)
                for lam in (1.0, 0.75, 0.5, 0.25, 0.0):
                    h1, h2 = ha + (ha_n - ha) * lam, hb + (hb_n - hb) * lam
                    a.x, a.y = P3.x - ua[0] * h1, P3.y - ua[1] * h1
                    b.x, b.y = P3.x + ub[0] * h2, P3.y + ub[1] * h2
                    if _cubica_sana(P0, P1, a, P3) and _cubica_sana(P3, b, Q2, Q3):
                        break
