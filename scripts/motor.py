"""Motor de trazos: expande esqueletos en contornos compatibles entre másteres.

Un trazo es una cadena de nodos (posición, tangente, ancho a cada lado). Cada lado se
convierte en cúbicas con la misma cantidad de puntos en todos los másteres, así que la
compatibilidad queda garantizada por construcción. Los extremos se recortan con una recta
(el «corte»): se busca dónde cruza cada lado y se parte la curva con De Casteljau.
"""
import math

from fontTools.misc.bezierTools import solveCubic

from trazos import Glifo

# Valores por defecto del módulo. La tensión y el corte son decisiones de estilo:
# cada proyecto debe fijarlos en su brief y pasarlos al constructor de G.
K = 0.575        # tensión del borde exterior
K_INT = 0.59     # tensión del borde interior: algo más tensa
CIRC = 0.5523


def dir_(a):
    r = math.radians(a)
    return (math.cos(r), math.sin(r))


def nor_izq(a):
    c, s = dir_(a)
    return (-s, c)


def suma(p, d, t=1):
    return (p[0] + d[0] * t, p[1] + d[1] * t)


def resta(a, b):
    return (a[0] - b[0], a[1] - b[1])


def punto(a, b):
    return a[0] * b[0] + a[1] * b[1]


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def cruce(p, d, q, e):
    det = d[0] * e[1] - d[1] * e[0]
    if abs(det) < 1e-9:
        return None
    t = ((q[0] - p[0]) * e[1] - (q[1] - p[1]) * e[0]) / det
    return suma(p, d, t)


def giro(a0, a1):
    d = (a1 - a0 + 180) % 360 - 180
    return abs(d)


def k_para(theta, k):
    """Tensión relativa al cruce de tangentes para un arco que gira theta grados.

    base es la aproximación exacta del arco circular: (4/3)·tan(th/4)/tan(th/2).
    El factor k/CIRC conserva el significado de la tensión en cualquier ángulo
    (con k = CIRC el arco es circular en todo theta). El tope < 1 garantiza el
    triángulo mágico por construcción: el manejador nunca pasa el cruce."""
    th = max(min(theta, 170), 1)
    base = (4 / 3) * math.tan(math.radians(th / 4)) / math.tan(math.radians(th / 2))
    return min(base * (k / CIRC), 0.995)


class N:
    """Nodo: (x, y), tangente en grados y ancho a izquierda y derecha del avance."""

    def __init__(self, x, y, ang, wl=0, wr=0):
        self.x, self.y, self.ang, self.wl, self.wr = x, y, ang, wl, wr

    def izq(self):
        return suma((self.x, self.y), nor_izq(self.ang), self.wl)

    def der(self):
        return suma((self.x, self.y), nor_izq(self.ang), -self.wr)


def seg(p0, a0, p1, a1, k):
    if giro(a0, a1) < 0.01:
        return ("l", p0, p1)
    d0, d1 = dir_(a0), dir_(a1)
    i = cruce(p0, d0, p1, d1)
    t0 = punto(resta(i, p0), d0) if i else -1
    t1 = punto(resta(p1, i), d1) if i else -1
    if not i or t0 <= 0 or t1 <= 0:
        l = math.dist(p0, p1) / 3
        return ("c", p0, suma(p0, d0, l), suma(p1, d1, -l), p1)
    kk = k_para(giro(a0, a1), k)
    return ("c", p0, lerp(p0, i, kk), lerp(p1, i, kk), p1)


def evalua(s, t):
    if s[0] == "l":
        return lerp(s[1], s[2], t)
    a = lerp(s[1], s[2], t); b = lerp(s[2], s[3], t); c = lerp(s[3], s[4], t)
    d = lerp(a, b, t); e = lerp(b, c, t)
    return lerp(d, e, t)


def parte(s, t):
    if s[0] == "l":
        m = lerp(s[1], s[2], t)
        return ("l", s[1], m), ("l", m, s[2])
    p0, p1, p2, p3 = s[1:]
    a = lerp(p0, p1, t); b = lerp(p1, p2, t); c = lerp(p2, p3, t)
    d = lerp(a, b, t); e = lerp(b, c, t); m = lerp(d, e, t)
    return ("c", p0, a, d, m), ("c", m, e, c, p3)


def lado_recta(p, q, ang):
    return punto(resta(p, q), nor_izq(ang))


def arcos_elipse(m, cx, cy, k):
    """Cuatro arcos cúbicos de la elipse M·círculo con nodos en sus extremos H/V.

    La aproximación de Bézier de un arco circular es invariante afín: se calcula
    sobre el círculo unidad con la fórmula canónica (4/3)·tan(d/4), se escala la
    tensión con k/CIRC y se transforma por M. Una elipse rotada conserva así los
    nodos en los extremos horizontales y verticales reales (regla B1). Devuelve
    los segmentos en antihorario empezando por el extremo inferior."""
    m00, m01, m10, m11 = m

    def P(t):
        return (cx + m00 * math.cos(t) + m01 * math.sin(t),
                cy + m10 * math.cos(t) + m11 * math.sin(t))

    tx = math.atan2(m01, m00)   # parámetros donde la tangente es vertical u horizontal
    ty = math.atan2(m11, m10)
    angs = sorted(a % (2 * math.pi) for a in (tx, tx + math.pi, ty, ty + math.pi))
    i0 = min(range(4), key=lambda i: P(angs[i])[1])
    angs = angs[i0:] + [a + 2 * math.pi for a in angs[:i0]] + [angs[i0] + 2 * math.pi]
    segs = []
    for t0, t1 in zip(angs, angs[1:]):
        h = (4 / 3) * math.tan((t1 - t0) / 4) * (k / CIRC)
        c1u = (math.cos(t0) - h * math.sin(t0), math.sin(t0) + h * math.cos(t0))
        c2u = (math.cos(t1) + h * math.sin(t1), math.sin(t1) - h * math.cos(t1))
        tr = lambda p: (cx + m00 * p[0] + m01 * p[1], cy + m10 * p[0] + m11 * p[1])
        segs.append(("c", P(t0), tr(c1u), tr(c2u), P(t1)))
    return segs


def tapa_seg(a, b, f):
    """Tapa entre los dos lados de un trazo: recta con f=0, cúbica abombada si no.

    El abombado apunta hacia fuera del trazo (a→b girado -90°). La profundidad es
    0,75·f·|ab|: con f=2/3 la tapa aproxima un semicírculo; negativo = cóncava."""
    if not f:
        return ("l", a, b)
    v = resta(b, a)
    d = (v[1], -v[0])
    return ("c", a, suma(a, d, f), suma(b, d, f), b)


def t_cruce(s, q, ang):
    """Parámetro donde el segmento cruza la recta; en una línea admite prolongar.

    En la cúbica se resuelve en forma cerrada: la distancia con signo a la recta es
    un polinomio cúbico en t (base de Bernstein) y solveCubic da todas sus raíces,
    sin el caso ciego de dos cruces dentro de un paso de muestreo."""
    if s[0] == "l":
        a, b = lado_recta(s[1], q, ang), lado_recta(s[2], q, ang)
        return a / (a - b) if abs(a - b) > 1e-9 else None
    s0, s1, s2, s3 = (lado_recta(p, q, ang) for p in s[1:])
    a3, a2, a1, a0 = -s0 + 3 * s1 - 3 * s2 + s3, 3 * (s0 - 2 * s1 + s2), 3 * (s1 - s0), s0
    validas = sorted(t for t in solveCubic(a3, a2, a1, a0) if -1e-9 <= t <= 1 + 1e-9)
    if not validas:
        return None
    t = min(max(validas[0], 0.0), 1.0)
    for _ in range(3):  # pulido de Newton: deja la raíz en precisión de máquina
        df = (3 * a3 * t + 2 * a2) * t + a1
        if abs(df) < 1e-12:
            break
        t = min(max(t - (((a3 * t + a2) * t + a1) * t + a0) / df, 0.0), 1.0)
    return t


def recorta_ini(lado, q, ang):
    """Recorta el primer segmento. Exige cruce ahí para no cambiar el número de puntos."""
    s = lado[0]
    t = t_cruce(s, q, ang)
    if t is None:
        raise ValueError("el corte inicial no cruza el primer segmento")
    lado[0] = ("l", lerp(s[1], s[2], t), s[2]) if s[0] == "l" else parte(s, t)[1]
    return lado


def recorta_fin(lado, q, ang):
    s = lado[-1]
    t = t_cruce(s, q, ang)
    if t is None:
        raise ValueError("el corte final no cruza el último segmento")
    lado[-1] = ("l", s[1], lerp(s[1], s[2], t)) if s[0] == "l" else parte(s, t)[0]
    return lado


def invierte(lado):
    out = []
    for s in reversed(lado):
        out.append(("l", s[2], s[1]) if s[0] == "l" else ("c", s[4], s[3], s[2], s[1]))
    return out


def a_contorno(lados):
    pts = []
    for s in lados:
        if s[0] == "l":
            pts.append(s[2])
        else:
            pts.append((s[2], s[3], s[4]))
    return pts


class G(Glifo):
    """Glifo con primitivas del sistema: asta, barra, diagonal, trazo y anillo.

    corte, k y ki son estilo: pásalos en el constructor desde los parámetros del
    proyecto en lugar de aceptar los valores por defecto del módulo."""

    corte = 16.0  # grados: el marco girado de todos los extremos libres

    def __init__(self, ufo, nombre, unicodes=None, lsb=0, rsb=0, corte=None, k=None, ki=None):
        super().__init__(ufo, nombre, unicodes, lsb, rsb)
        self.ox, self.oy = 0, 0
        if corte is not None:
            self.corte = corte
        self.k = K if k is None else k
        self.ki = K_INT if ki is None else ki

    @property
    def tan(self):
        return math.tan(math.radians(self.corte))

    def _t(self, p):
        return (p[0] + self.ox, p[1] + self.oy)

    def poli(self, *pts):
        pts = [self._t(p) for p in pts]
        self.contorno(pts[0], *pts[1:])

    def rect(self, x0, y0, x1, y1):
        self.poli((x0, y0), (x1, y0), (x1, y1), (x0, y1))

    def lados(self, nodos, k=None, ki=None, cerrado=False):
        k = self.k if k is None else k
        ki = self.ki if ki is None else ki
        pares = list(zip(nodos, nodos[1:] + ([nodos[0]] if cerrado else [])))
        der = [seg(self._t(a.der()), a.ang, self._t(b.der()), b.ang, k) for a, b in pares]
        izq = [seg(self._t(a.izq()), a.ang, self._t(b.izq()), b.ang, ki) for a, b in pares]
        return der, izq

    def trazo(self, nodos, ini=None, fin=None, k=None, ki=None, ini_ang=None, tapa=0, tapa_ini=0):
        """Trazo abierto. ini y fin: (punto, ángulo) de la recta de corte; None = recto.
        tapa y tapa_ini curvan el extremo final e inicial: 2/3 ≈ semicírculo,
        menos = más plano, negativo = cóncavo (ver tapa_seg)."""
        der, izq = self.lados(nodos, k, ki)
        if ini:
            q = self._t(ini[0])
            der, izq = recorta_ini(der, q, ini[1]), recorta_ini(izq, q, ini[1])
        if fin:
            q = self._t(fin[0])
            der, izq = recorta_fin(der, q, fin[1]), recorta_fin(izq, q, fin[1])
        cont = der + [tapa_seg(der[-1][-1], izq[-1][-1], tapa)] + invierte(izq)
        if tapa_ini:
            cont.append(tapa_seg(izq[0][1], der[0][1], tapa_ini))
        self.contorno(der[0][1], *a_contorno(cont))

    def anillo(self, xi, xd, yb, yt, ei, ed, eh, ehs=None, k=None, ki=None):
        """Anillo cerrado: exterior antihorario, contraforma horaria."""
        cx, cy = (xi + xd) / 2, (yb + yt) / 2
        ehs = eh if ehs is None else ehs
        ns = [N(cx, yb, 0, eh), N(xd, cy, 90, ed), N(cx, yt, 180, ehs), N(xi, cy, -90, ei)]
        der, izq = self.lados(ns, k, ki, cerrado=True)
        self.contorno(der[0][1], *a_contorno(der))
        inv = invierte(izq)
        self.contorno(inv[0][1], *a_contorno(inv))

    def anillo_eje(self, xi, xd, yb, yt, grueso, fino, eje=0, k=None, ki=None):
        """Anillo con eje de contraste inclinado: el contrapunzón es una elipse rotada.

        eje gira los puntos finos respecto de la vertical (grados, antihorario, el
        modelo de traslación de la plumilla). El exterior es la elipse de la caja;
        el interior, una elipse girada eje grados cuyos semiejes dejan exactamente
        fino en la dirección del eje y grueso en su perpendicular (la construcción
        clásica del contrapunzón humanista). Ambos contornos llevan cuatro nodos en
        sus extremos H/V reales y la misma estructura en todos los másteres."""
        k = self.k if k is None else k
        ki = self.ki if ki is None else ki
        cx, cy = self._t(((xi + xd) / 2, (yb + yt) / 2))
        rx, ry = (xd - xi) / 2, (yt - yb) / 2

        def radio(ang):  # radio de la elipse exterior en la dirección ang (grados)
            c, s = dir_(ang)
            return rx * ry / math.hypot(ry * c, rx * s)

        der = arcos_elipse((rx, 0, 0, ry), cx, cy, k)
        a_in, b_in = radio(90 + eje) - fino, radio(eje) - grueso
        if min(a_in, b_in) <= 0:
            raise ValueError("anillo_eje: el grosor no cabe en la caja")
        ce, se = dir_(eje)
        izq = arcos_elipse((b_in * ce, -a_in * se, b_in * se, a_in * ce), cx, cy, ki)
        self.contorno(der[0][1], *a_contorno(der))
        inv = invierte(izq)
        self.contorno(inv[0][1], *a_contorno(inv))

    def asta(self, x0, x1, y0, y1, sup=True, inf=False):
        """Asta vertical. sup: corte que sube a la derecha; inf: corte paralelo abajo."""
        d = (x1 - x0) * self.tan
        self.poli((x0, y0), (x1, y0 + (d if inf else 0)), (x1, y1), (x0, y1 - (d if sup else 0)))

    def barra(self, x0, x1, y0, y1, izq=False, der=True):
        """Barra horizontal. Los extremos libres se inclinan hacia la izquierda arriba."""
        d = (y1 - y0) * self.tan
        self.poli((x0 + (d if izq else 0), y0), (x1, y0), (x1 - (d if der else 0), y1), (x0, y1))

    def diag(self, xb, xt, wb, y0, y1, sup=True, wt=None):
        """Diagonal: xb y xt son el borde izquierdo abajo y arriba; wb y wt, su ancho."""
        wt = wb if wt is None else wt
        drop = wt * self.tan if sup else 0
        f = (y1 - drop - y0) / (y1 - y0)
        tl = xb + (xt - xb) * f
        self.poli((xb, y0), (xb + wb, y0), (xt + wt, y1), (tl, y1 - drop))

    def punto(self, cx, cy, r, k=CIRC):
        """Punto o gota: solapado al extremo de un trazo hace de terminal de bulbo
        (los solapes se conservan en la fuente y se eliminan al exportar)."""
        c = k * r
        x, y = self._t((cx, cy))
        self.contorno((x, y - r), ((x + c, y - r), (x + r, y - c), (x + r, y)),
                      ((x + r, y + c), (x + c, y + r), (x, y + r)),
                      ((x - c, y + r), (x - r, y + c), (x - r, y)),
                      ((x - r, y - c), (x - c, y - r), (x, y - r)))

    def losa(self, cx, y0, ancho, alto):
        """Serifa de losa: rectángulo centrado en cx, solapado al extremo del asta."""
        self.rect(cx - ancho / 2, y0, cx + ancho / 2, y0 + alto)
