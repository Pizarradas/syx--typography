"""Motor de trazos: expande esqueletos en contornos compatibles entre másteres.

Un trazo es una cadena de nodos (posición, tangente, ancho a cada lado). Cada lado se
convierte en cúbicas con la misma cantidad de puntos en todos los másteres, así que la
compatibilidad queda garantizada por construcción. Los extremos se recortan con una recta
(el «corte»): se busca dónde cruza cada lado y se parte la curva con De Casteljau.
"""
import math

from trazos import Glifo

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
    """Tensión relativa al cruce de tangentes para un arco que gira theta grados."""
    th = max(min(theta, 170), 1)
    base = (4 / 3) * math.tan(math.radians(th / 4)) / math.tan(math.radians(th / 2))
    return base + (k - CIRC)


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


def t_cruce(s, q, ang):
    """Parámetro donde el segmento cruza la recta; en una línea admite prolongar."""
    if s[0] == "l":
        a, b = lado_recta(s[1], q, ang), lado_recta(s[2], q, ang)
        return a / (a - b) if abs(a - b) > 1e-9 else None
    pasos = 96
    prev = lado_recta(evalua(s, 0), q, ang)
    for i in range(1, pasos + 1):
        act = lado_recta(evalua(s, i / pasos), q, ang)
        if prev == 0 or prev * act < 0:
            lo, hi = (i - 1) / pasos, i / pasos
            fl = prev
            for _ in range(40):
                m = (lo + hi) / 2
                fm = lado_recta(evalua(s, m), q, ang)
                if fl * fm <= 0:
                    hi = m
                else:
                    lo, fl = m, fm
            return (lo + hi) / 2
        prev = act
    return None


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
    """Glifo con primitivas del sistema: asta, barra, diagonal, trazo y anillo."""

    corte = 16.0  # grados: el marco girado de todos los extremos libres

    def __init__(self, ufo, nombre, unicodes=None, lsb=0, rsb=0):
        super().__init__(ufo, nombre, unicodes, lsb, rsb)
        self.ox, self.oy = 0, 0

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

    def lados(self, nodos, k=K, ki=K_INT, cerrado=False):
        pares = list(zip(nodos, nodos[1:] + ([nodos[0]] if cerrado else [])))
        der = [seg(self._t(a.der()), a.ang, self._t(b.der()), b.ang, k) for a, b in pares]
        izq = [seg(self._t(a.izq()), a.ang, self._t(b.izq()), b.ang, ki) for a, b in pares]
        return der, izq

    def trazo(self, nodos, ini=None, fin=None, k=K, ki=K_INT, ini_ang=None):
        """Trazo abierto. ini y fin: (punto, ángulo) de la recta de corte; None = recto."""
        der, izq = self.lados(nodos, k, ki)
        if ini:
            q = self._t(ini[0])
            der, izq = recorta_ini(der, q, ini[1]), recorta_ini(izq, q, ini[1])
        if fin:
            q = self._t(fin[0])
            der, izq = recorta_fin(der, q, fin[1]), recorta_fin(izq, q, fin[1])
        cont = der + [("l", der[-1][-1], izq[-1][-1])] + invierte(izq)
        self.contorno(der[0][1], *a_contorno(cont))

    def anillo(self, xi, xd, yb, yt, ei, ed, eh, ehs=None, k=K, ki=K_INT):
        """Anillo cerrado: exterior antihorario, contraforma horaria."""
        cx, cy = (xi + xd) / 2, (yb + yt) / 2
        ehs = eh if ehs is None else ehs
        ns = [N(cx, yb, 0, eh), N(xd, cy, 90, ed), N(cx, yt, 180, ehs), N(xi, cy, -90, ei)]
        der, izq = self.lados(ns, k, ki, cerrado=True)
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

    def punto(self, cx, cy, r):
        c = 0.5523 * r
        x, y = self._t((cx, cy))
        self.contorno((x, y - r), ((x + c, y - r), (x + r, y - c), (x + r, y)),
                      ((x + r, y + c), (x + c, y + r), (x, y + r)),
                      ((x - c, y + r), (x - r, y + c), (x - r, y)),
                      ((x - r, y - c), (x - c, y - r), (x, y - r)))
