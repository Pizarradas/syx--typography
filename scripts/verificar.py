#!/usr/bin/env python3
"""Auditoría matemática de contornos: lo que una prueba PNG no deja ver.

  verificar.py FUENTE.ufo|FAMILIA.designspace [--config verificar.json] [--json salida.json]
  verificar.py --meta        autoprueba: inyecta defectos y comprueba que se detectan

Complementa a check_sources.py (compatibilidad, avisos de Bézier): aquí cada
comprobación tiene tolerancia explícita y es ERROR salvo que se diga aviso. Los solapes
entre contornos se permiten (se eliminan al exportar); se informan en las medidas.

Siempre (sin configuración):
  T  topología: sentido por anidamiento real (exterior antihorario), autocruces de cada
     contorno por XOR exacto, islas sueltas, micro-segmentos (< 4 u) y espolones (recta < 15 u entre dos esquinas)
  X  ningún extremo H/V interior que sobresalga más de 0,6 u de los nodos
  Q  sin quiebros: en nodos casi lisos (< 12°) la tangente es continua salvo el error de
     redondear a la rejilla, calculado para cada nodo con la longitud de sus tiradores
  M  tiradores dentro del triángulo (no pasan el cruce de tangentes), sin tiradores nulos;
     aviso si la tensión supera 0,85 (curva casi en esquina)
  I  sin inflexiones dentro de un segmento, salvo glifos declarados
  K  aviso: salto de curvatura (G2) > ×3 en un nodo liso
  Z  zonas: si un borde superior o inferior cae a menos de 2 rebasamientos de una zona,
     debe caer EXACTAMENTE (±1 u) en ella o en su rebasamiento (BlueValues del UFO);
     no se aplica a marcas combinantes (glifos con anclas «_»); un borde inferior entre la
     línea base y el descendente («tierra de nadie») es error salvo en "zonas_libres"
  L  métricas: BlueValues coherentes con xHeight/capHeight; avisos de usWin

Con verificar.json (reglas del diseño, todas opcionales):
  {"tolerancia": 1.0,
   "zonas_extra": {"730": ["h", "d"]},          altura → glifos ("*" = todos)
   "zonas_libres": ["Q", "comma"],             bordes inferiores entre línea base y descendente
   "inflexiones": ["S", "s"],                  también lib["com.syx.curvas.inflexion"]
   "astas": {"H": [175, 129.6]},               glifo → [y de la horizontal, grosor]
   "contraste": {"O": {"eje": 20, "fino": 40.3}},   eje del fino desde la vertical
   "cincel": {"angulo": 26, "excluir": ["A"]},  corte = perpendicular al trazo + ángulo
   "laterales": {"H": [77, 77]}}               glifo → [izquierdo, derecho]

Código de salida 1 si hay errores. Una auditoría sin errores demuestra conformidad con
estas reglas, no calidad de diseño: las pruebas PNG siguen siendo obligatorias.
"""
import json
import math
import sys
from pathlib import Path

import pathops
import ufoLib2
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.misc.bezierTools import solveQuadratic

REJILLA = 0.5 * math.sqrt(2)  # error máximo al redondear un punto a enteros
LIB_INFLEXION = "com.syx.curvas.inflexion"


class Informe:
    def __init__(self, prefijo=""):
        self.errores, self.avisos, self.medidas, self.prefijo = [], [], {}, prefijo

    def err(self, g, cod, msg):
        self.errores.append(f"{self.prefijo}{g:8} {cod}  {msg}")

    def aviso(self, g, cod, msg):
        self.avisos.append(f"{self.prefijo}{g:8} {cod}  {msg}")

    def medida(self, g, clave, valor):
        self.medidas.setdefault(g, {})[clave] = valor


# -- geometría ---------------------------------------------------------------------------
def segmentos(c):
    pts = list(c.points)
    if not any(p.type for p in pts):
        return []
    i0 = next(i for i, p in enumerate(pts) if p.type)
    pts = pts[i0 + 1:] + pts[:i0 + 1]
    segs, prev, pend = [], (pts[-1].x, pts[-1].y), []
    for p in pts:
        if p.type is None:
            pend.append((p.x, p.y))
            continue
        q = (p.x, p.y)
        if p.type == "line":
            segs.append(("l", prev, q))
        elif p.type == "curve":
            segs.append(("c", prev, pend[0], pend[1], q))
        else:
            raise ValueError(f"tipo de punto no admitido: {p.type} (convierte a cúbicas)")
        prev, pend = q, []
    return segs


def B(s, t):
    if s[0] == "l":
        return tuple(s[1][i] + (s[2][i] - s[1][i]) * t for i in range(2))
    m = 1 - t
    return tuple(m**3 * s[1][i] + 3 * m * m * t * s[2][i] + 3 * m * t * t * s[3][i] + t**3 * s[4][i] for i in range(2))


def d1(s, t):
    if s[0] == "l":
        return tuple(s[2][i] - s[1][i] for i in range(2))
    m = 1 - t
    return tuple(3 * m * m * (s[2][i] - s[1][i]) + 6 * m * t * (s[3][i] - s[2][i]) + 3 * t * t * (s[4][i] - s[3][i]) for i in range(2))


def d2(s, t):
    if s[0] == "l":
        return (0.0, 0.0)
    m = 1 - t
    return tuple(6 * m * (s[3][i] - 2 * s[2][i] + s[1][i]) + 6 * t * (s[4][i] - 2 * s[3][i] + s[2][i]) for i in range(2))


def curv(s, t):
    a, b = d1(s, t), d2(s, t)
    n = math.hypot(*a)
    return (a[0] * b[1] - a[1] * b[0]) / n**3 if n > 1e-9 else 0.0


def tang_ini(s):
    for q in s[2:]:
        if math.dist(q, s[1]) > 1e-9:
            return (q[0] - s[1][0], q[1] - s[1][1]), math.dist(q, s[1])
    return (1.0, 0.0), 0.0


def tang_fin(s):
    fin = s[-1]
    for q in reversed(s[1:-1]):
        if math.dist(q, fin) > 1e-9:
            return (fin[0] - q[0], fin[1] - q[1]), math.dist(q, fin)
    return (1.0, 0.0), 0.0


def ang(v):
    return math.degrees(math.atan2(v[1], v[0]))


def dif(a, b):
    return abs((a - b + 180) % 360 - 180)


def poligono(c, n=24, n_recta=1):
    """Contorno aplanado. n_recta > 1 también muestrea a lo largo de las rectas
    (necesario para decidir contención: los vértices solos engañan)."""
    out = []
    for seg in segmentos(c):
        k = n_recta if seg[0] == "l" else n
        out += [B(seg, j / k) for j in range(k)]
    return out


def area(c):
    pol = poligono(c, 48)
    return sum(pol[i - 1][0] * pol[i][1] - pol[i][0] * pol[i - 1][1] for i in range(len(pol))) / 2


def dentro(pt, pol):
    x, y, ins = pt[0], pt[1], False
    for i in range(len(pol)):
        (x1, y1), (x2, y2) = pol[i], pol[i - 1]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            ins = not ins
    return ins


def caja(g):
    p = pathops.Path()
    g.draw(p.getPen())
    return p.bounds


# -- T X Q M I K -------------------------------------------------------------------------
def _path(contornos):
    p = pathops.Path()
    pen = p.getPen()
    for c in contornos:
        c.draw(pen)
    return p


def topologia(g, inf):
    """Sentido por anidamiento real y autocruces por contorno.

    Los solapes ENTRE contornos se permiten: la skill los conserva en las fuentes y los
    elimina al exportar (references/02, regla 8). Por eso el anidamiento se decide por
    contención completa (todos los puntos dentro), no por un punto: una barra que solapa
    un asta es hermana del asta, no su contraforma."""
    cs = list(g.contours)
    if not cs:
        return
    pols = [poligono(c, 24, 12) for c in cs]
    areas = [area(c) for c in cs]
    total = sum(abs(a) for a in areas)
    for i, c in enumerate(cs):
        prof = sum(1 for j in range(len(cs)) if j != i and abs(areas[j]) > abs(areas[i])
                   and all(dentro(p, pols[j]) for p in pols[i]))
        if (prof % 2 == 0) != (areas[i] > 0):
            inf.err(g.name, "T", f"contorno {i} con sentido erróneo (área {areas[i]:.0f}, profundidad {prof})")
        # Autocruce: un contorno solo, simplificado, debe quedar igual.
        p = _path([c])
        s = pathops.simplify(p, clockwise=areas[i] < 0)
        x = pathops.op(p, s, pathops.PathOp.XOR)
        if abs(x.area) > 0.5 or len(list(s.contours)) != 1:
            inf.err(g.name, "T", f"contorno {i} se cruza consigo mismo (XOR {abs(x.area):.1f} u²)")
        # Isla: contorno pequeño que no toca a ningún otro.
        if len(cs) > 1 and abs(areas[i]) < 0.03 * total:
            otros = _path([cs[j] for j in range(len(cs)) if j != i])
            if pathops.op(p, otros, pathops.PathOp.INTERSECTION).area == 0 and prof == 0:
                inf.err(g.name, "T", f"isla suelta: contorno {i} de {abs(areas[i]):.0f} u² ({100 * abs(areas[i]) / total:.1f} % de la tinta)")
    solapes = abs(_path(cs).area - pathops.simplify(_path(cs), clockwise=False).area) if len(cs) > 1 else 0
    if solapes > 0.5:
        inf.medida(g.name, "solapes", "sí (se eliminan al exportar)")


def curvas(g, inf, inflexion_ok=False):
    g2 = []
    for ci, c in enumerate(g.contours):
        segs = segmentos(c)
        for si, s in enumerate(segs):
            cuerda = math.dist(s[1], s[-1])
            pos = tuple(round(v) for v in s[1])
            if cuerda < 4:
                inf.err(g.name, "T", f"c{ci} s{si}: micro-segmento de {cuerda:.1f} u en {pos}")
            elif s[0] == "l" and cuerda < 15:
                a_in = dif(ang(tang_fin(segs[si - 1])[0]), ang(tang_ini(s)[0]))
                a_out = dif(ang(tang_fin(s)[0]), ang(tang_ini(segs[(si + 1) % len(segs)])[0]))
                if a_in > 12 and a_out > 12:
                    inf.err(g.name, "T", f"c{ci} s{si}: espolón (recta de {cuerda:.1f} u entre dos esquinas) en {pos}")
            if s[0] != "c":
                continue
            for eje in (0, 1):  # X: extremos interiores
                a = -s[1][eje] + 3 * s[2][eje] - 3 * s[3][eje] + s[4][eje]
                b = 2 * (s[1][eje] - 2 * s[2][eje] + s[3][eje])
                cc = s[2][eje] - s[1][eje]
                for t in solveQuadratic(3 * a, 3 * b, 3 * cc):
                    if 0.02 < t < 0.98:
                        v = B(s, t)[eje]
                        lo, hi = min(s[1][eje], s[4][eje]), max(s[1][eje], s[4][eje])
                        sobra = max(v - hi, lo - v)
                        if sobra > 0.6:
                            inf.err(g.name, "X", f"c{ci} s{si}: extremo {'xy'[eje]} interior en t={t:.2f} ({sobra:.1f} u fuera de los nodos)")
            h0, h1 = math.dist(s[1], s[2]), math.dist(s[3], s[4])  # M
            if h0 < 1e-9 or h1 < 1e-9:
                inf.err(g.name, "M", f"c{ci} s{si}: tirador nulo")
            else:
                u, v = tang_ini(s)[0], tang_fin(s)[0]
                det = u[0] * v[1] - u[1] * v[0]
                if abs(det) > 1e-6:
                    q = (s[4][0] - s[1][0], s[4][1] - s[1][1])
                    t0 = (q[0] * v[1] - q[1] * v[0]) / det   # P0 + t0·u = P3 − t1·v
                    t1 = (u[0] * q[1] - u[1] * q[0]) / det
                    L0, L1 = t0 * math.hypot(*u), t1 * math.hypot(*v)
                    if L0 > 0 and L1 > 0:
                        if h0 > L0 + REJILLA or h1 > L1 + REJILLA:
                            inf.err(g.name, "M", f"c{ci} s{si}: tirador fuera del triángulo ({h0:.0f}/{L0:.0f}, {h1:.0f}/{L1:.0f})")
                        elif max(h0 / L0, h1 / L1) > 0.85:
                            inf.aviso(g.name, "M", f"c{ci} s{si}: tensión {max(h0 / L0, h1 / L1):.2f} (> 0,85: curva casi en esquina)")
            ks = [curv(s, j / 40) for j in range(1, 40)]  # I
            tope = max(abs(k) for k in ks)
            signos = {k > 0 for k in ks if abs(k) > tope * 1e-3} if tope else set()
            if len(signos) == 2 and not inflexion_ok:
                inf.err(g.name, "I", f"c{ci} s{si}: inflexión no declarada")
        for si in range(len(segs)):  # Q y K
            a, b = segs[si - 1], segs[si]
            ta, la = tang_fin(a)
            tb, lb = tang_ini(b)
            d = dif(ang(ta), ang(tb))
            tol = math.degrees(math.atan(REJILLA / max(min(la, lb), 1))) * 2 + 0.05
            if tol < d < 12:
                inf.err(g.name, "Q", f"c{ci} nodo {si} {tuple(round(v) for v in b[1])}: quiebro de {d:.1f}° (tolerancia de rejilla {tol:.2f}°)")
            if a[0] == "c" and b[0] == "c" and d < 2:
                ka, kb = abs(curv(a, 1)), abs(curv(b, 0))
                if min(ka, kb) > 1e-6:
                    g2.append(max(ka, kb) / min(ka, kb))
    if g2:
        inf.medida(g.name, "G2_max", round(max(g2), 2))
        if max(g2) > 3:
            inf.aviso(g.name, "K", f"salto de curvatura G2 hasta ×{max(g2):.1f} en un nodo liso")


# -- Z L -----------------------------------------------------------------------------------
def zonas_ufo(u):
    i = u.info
    bv = list(i.postscriptBlueValues or [])
    ob = list(i.postscriptOtherBlues or [])
    bordes = set(bv + ob)
    for v in (0, i.xHeight, i.capHeight, i.descender):
        if v is not None:
            bordes.add(v)
    pares = [abs(b - a) for a, b in zip(bv[::2], bv[1::2])] + [abs(b - a) for a, b in zip(ob[::2], ob[1::2])]
    reb = max(pares) if pares else 15
    return bordes, reb


def zonas(g, inf, bordes, reb, extra, tol, libres=()):
    if not g.contours or any(a.name.startswith("_") for a in g.anchors):
        return  # las marcas combinantes flotan por diseño: se juzgan con sus anclas
    _, y0, _, y1 = caja(g)
    propios = set(bordes) | {z for z, gs in extra.items() if "*" in gs or g.name in gs}
    inf.medida(g.name, "y", [round(y0, 2), round(y1, 2)])
    # Tierra de nadie: un borde inferior claramente bajo la línea base que tampoco llega al
    # descendente es casi siempre un trazo mal colocado (una U que cuelga), no una forma.
    desc = min(propios)
    if g.name not in libres and desc + 2 * reb < y0 < -2 * reb:
        inf.err(g.name, "Z", f"borde inferior en {y0:.1f}: bajo la línea base sin llegar al descendente "
                              f"({desc}); si es intencionado, decláralo en \"zonas_libres\"")
    for v, nom in ((y0, "inferior"), (y1, "superior")):
        cerca = [z for z in propios if abs(v - z) <= 2 * reb]
        if cerca and min(abs(v - z) for z in cerca) > tol:
            z = min(cerca, key=lambda z: abs(v - z))
            inf.err(g.name, "Z", f"borde {nom} en {v:.1f}: a {abs(v - z):.1f} u de la zona {z}, fuera de tolerancia")


def metricas(u, inf):
    i = u.info
    bv = list(i.postscriptBlueValues or [])
    for nombre, v in (("xHeight", i.xHeight), ("capHeight", i.capHeight)):
        if v is not None and bv and v not in bv:
            inf.err("info", "Z", f"{nombre} {v} no es un borde de BlueValues {bv}")
    if i.openTypeOS2WinDescent is not None and i.descender is not None and i.openTypeOS2WinDescent < abs(i.descender):
        inf.aviso("info", "L", f"usWinDescent {i.openTypeOS2WinDescent} < descendente {abs(i.descender)}: correcto si cubre "
                               "los glifos existentes, pero Windows recortará las letras de respaldo")


# -- reglas del diseño (verificar.json) -----------------------------------------------------
def astas(u, inf, conf, tol):
    for nombre, (y, obj) in conf.items():
        if nombre not in u:
            continue
        g = u[nombre]
        xs = []
        for c in g.contours:
            pol = poligono(c, 48)
            for k in range(len(pol)):
                (xa, ya), (xb, yb) = pol[k - 1], pol[k]
                if (ya > y) != (yb > y):
                    xs.append(xa + (y - ya) * (xb - xa) / (yb - ya))
        xs.sort()
        w = [xs[k + 1] - xs[k] for k in range(0, len(xs) - 1, 2)]
        inf.medida(nombre, "astas", [round(v, 1) for v in w])
        for v in w:
            if abs(v - obj) > tol and v < obj * 1.5:
                inf.err(nombre, "A", f"asta de {v:.1f} a y={y}; la regla da {obj:.1f}")


def contraste(u, inf, conf):
    for nombre, regla in conf.items():
        if nombre not in u:
            continue
        cs = sorted(u[nombre].contours, key=lambda c: -abs(area(c)))
        if len(cs) < 2:
            inf.err(nombre, "E", "sin contraforma: no se puede medir el eje")
            continue
        ext, cont = poligono(cs[0], 200), poligono(cs[1], 200)
        cx = (min(p[0] for p in ext) + max(p[0] for p in ext)) / 2
        cy = (min(p[1] for p in ext) + max(p[1] for p in ext)) / 2

        def radio(pol, a):
            d = (math.cos(a), math.sin(a))
            mejor = 0
            for i in range(len(pol)):
                p, q = pol[i - 1], pol[i]
                e = (q[0] - p[0], q[1] - p[1])
                det = d[0] * (-e[1]) + d[1] * e[0]
                if abs(det) < 1e-12:
                    continue
                w = (p[0] - cx, p[1] - cy)
                t = (w[0] * (-e[1]) + w[1] * e[0]) / det
                v = (d[0] * w[1] - d[1] * w[0]) / det
                if t > 0 and 0 <= v <= 1:
                    mejor = max(mejor, t)
            return mejor
        gros = [(radio(ext, math.radians(k / 2)) - radio(cont, math.radians(k / 2)), k / 2) for k in range(360)]
        gmin, amin = min(gros)
        eje = amin - 90
        inf.medida(nombre, "eje", round(eje, 1))
        inf.medida(nombre, "fino", round(gmin, 1))
        if "eje" in regla and abs(eje - regla["eje"]) > 1.0:
            inf.err(nombre, "E", f"eje del contraste medido {eje:.1f}° ≠ {regla['eje']}°")
        if "fino" in regla and abs(gmin - regla["fino"]) > 1.5:
            inf.err(nombre, "E", f"fino medido {gmin:.1f} ≠ {regla['fino']}")


def cincel(u, inf, conf):
    """Rectas de corte de terminal (no H/V, 8–260 u): deben formar +ángulo (antihorario)
    con la perpendicular al trazo, cuyo eje es la bisectriz de los dos bordes que llegan."""
    angulo, excluir = conf["angulo"], set(conf.get("excluir", []))
    lmin, lmax = conf.get("largo_min", 8), conf.get("largo_max", 260)
    for g in u:
        if g.name in excluir or not g.contours:
            continue
        medidos = []
        for c in g.contours:
            segs = segmentos(c)
            for si, s in enumerate(segs):
                if s[0] != "l":
                    continue
                L = math.dist(s[1], s[2])
                a = ang((s[2][0] - s[1][0], s[2][1] - s[1][1])) % 180
                if not (lmin <= L <= lmax) or min(a, 180 - a) < 0.5 or abs(a - 90) < 0.5:
                    continue
                (v_prev, l_prev), (v_next, l_next) = tang_fin(segs[si - 1]), tang_ini(segs[(si + 1) % len(segs)])
                t_prev = math.radians(ang(v_prev))
                t_next = math.radians(ang(v_next) + 180)
                eje = math.degrees(math.atan2(math.sin(t_prev) + math.sin(t_next), math.cos(t_prev) + math.cos(t_next)))
                desvio = (a - (eje + 90) % 180 + 90) % 180 - 90
                medidos.append(round(desvio, 1))
                # Redondear a enteros desvía una dirección entre dos puntos hasta atan(2·REJILLA/largo):
                # el corte por su largo, el eje por la media de los dos tiradores que lo definen.
                def err(largo):
                    return math.degrees(math.atan(2 * REJILLA / max(largo, 1)))
                tol = 1.0 + err(L) + (err(l_prev) + err(l_next)) / 2
                if abs(desvio - angulo) > tol:
                    inf.err(g.name, "C", f"corte en {tuple(round(v) for v in s[1])} a {desvio:+.1f}° de la perpendicular al trazo; la regla es +{angulo}°")
        if medidos:
            inf.medida(g.name, "cincel", medidos)


def laterales(u, inf, conf, tol):
    for nombre, (li, ld) in conf.items():
        if nombre not in u or not u[nombre].contours:
            continue
        g = u[nombre]
        x0, _, x1, _ = caja(g)
        inf.medida(nombre, "laterales", [round(x0), round(g.width - x1)])
        if abs(x0 - li) > tol:
            inf.err(nombre, "L", f"lateral izquierdo {x0:.0f} ≠ {li}")
        if abs(g.width - x1 - ld) > tol:
            inf.err(nombre, "L", f"lateral derecho {g.width - x1:.0f} ≠ {ld}")


# -- conjunto ------------------------------------------------------------------------
def auditar(u, conf, inf):
    tol = conf.get("tolerancia", 1.0)
    bordes, reb = zonas_ufo(u)
    extra = {float(k): set(v) for k, v in conf.get("zonas_extra", {}).items()}
    decl = set(conf.get("inflexiones", []))
    for g in u:
        if not g.contours:
            continue
        topologia(g, inf)
        curvas(g, inf, inflexion_ok=g.name in decl or bool(g.lib.get(LIB_INFLEXION)))
        zonas(g, inf, bordes, reb, extra, tol, set(conf.get("zonas_libres", [])))
    metricas(u, inf)
    if "astas" in conf:
        astas(u, inf, conf["astas"], tol)
    if "contraste" in conf:
        contraste(u, inf, conf["contraste"])
    if "cincel" in conf:
        cincel(u, inf, conf["cincel"])
    if "laterales" in conf:
        laterales(u, inf, conf["laterales"], tol)
    return inf


def fuentes(ruta):
    ruta = Path(ruta)
    if ruta.suffix == ".designspace":
        ds = DesignSpaceDocument.fromfile(ruta)
        return [(Path(s.path).stem + " ", ufoLib2.Font.open(s.path)) for s in ds.sources]
    return [("", ufoLib2.Font.open(ruta))]


# -- autoprueba -------------------------------------------------------------------------
def meta():
    """Cada defecto inyectado debe detectarse con su código, y lo limpio debe pasar."""
    u = ufoLib2.Font()

    def glifo(nombre, contornos):
        g = u.newGlyph(nombre)
        pen = g.getPen()
        for c in contornos:
            pen.moveTo(c[0])
            for s in c[1:]:
                pen.curveTo(*s) if isinstance(s[0], tuple) else pen.lineTo(s)
            pen.closePath()
        return g

    casos = {
        "sentido": ([[(0, 0), (0, 100), (100, 100), (100, 0)]], "T"),
        "autocruce": ([[(0, 0), (100, 100), (100, 0), (0, 100)]], "T"),
        "barra_cw": ([[(0, 0), (60, 0), (60, 300), (0, 300)], [(200, 0), (260, 0), (260, 300), (200, 300)],
                      [(30, 140), (30, 160), (230, 160), (230, 140)]], "T"),
        "isla": ([[(0, 0), (400, 0), (400, 400), (0, 400)], [(500, 0), (510, 0), (510, 10), (500, 10)]], "T"),
        "micro": ([[(0, 0), (200, 0), (202, 1), (200, 200), (0, 200)]], "T"),
        "espolon": ([[(0, 0), (200, 0), (200, 10), (190, 10), (190, 200), (0, 200)]], "T"),
        "extremo": ([[(0, 0), ((100, -60), (200, -60), (300, 0)), (300, 200), (0, 200)]], "X"),
        "triangulo": ([[(0, 0), (100, 0), ((100, 150), (50, 100), (0, 100))]], "M"),
        "quiebro": ([[(0, 0), (100, 0), ((100, 60), (100, 100), (100, 100)), ((90, 160), (60, 200), (0, 200))]], "Q"),
        "inflexion": ([[(0, 0), (300, 0), ((300, 100), (0, 100), (0, 300))]], "I"),
    }
    limpios = {
        "cuadrado": [[(0, 0), (100, 0), (100, 100), (0, 100)]],
        "H_solape": [[(0, 0), (60, 0), (60, 300), (0, 300)], [(200, 0), (260, 0), (260, 300), (200, 300)],
                     [(30, 140), (230, 140), (230, 160), (30, 160)]],
        "o": [[(100, 0), ((155, 0), (200, 45), (200, 100)), ((200, 155), (155, 200), (100, 200)),
               ((45, 200), (0, 155), (0, 100)), ((0, 45), (45, 0), (100, 0))],
              [(100, 40), ((67, 40), (40, 67), (40, 100)), ((40, 133), (67, 160), (100, 160)),
               ((133, 160), (160, 133), (160, 100)), ((160, 67), (133, 40), (100, 40))]],
        "circulo": [[(100, 0), ((155, 0), (200, 45), (200, 100)), ((200, 155), (155, 200), (100, 200)),
                     ((45, 200), (0, 155), (0, 100)), ((0, 45), (45, 0), (100, 0))]],
    }
    ok = True
    for nombre, (cs, cod) in casos.items():
        inf = Informe()
        g = glifo(nombre, cs)
        topologia(g, inf)
        curvas(g, inf)
        hit = any(f" {cod}  " in e for e in inf.errores)
        ok &= hit
        print(f"  {nombre:10} espera {cod}: {'detectado' if hit else 'NO DETECTADO'}")
    for nombre, cs in limpios.items():
        inf = Informe()
        g = glifo(nombre, cs)
        topologia(g, inf)
        curvas(g, inf)
        ok &= not inf.errores
        print(f"  {nombre:10} espera limpio: {'limpio' if not inf.errores else inf.errores}")
    # Zonas: un rebasamiento de 31 u sobre una zona de 14 debe fallar; uno exacto, pasar.
    for y1, debe in ((484, False), (498, True)):
        inf = Informe()
        zonas(glifo(f"z{y1}", [[(0, -14), (100, -14), (100, y1), (0, y1)]]), inf, {0, -14, 470, 484}, 14, {}, 1.0)
        hit = bool(inf.errores)
        ok &= hit == debe
        print(f"  zona {y1:<5} espera {'Z' if debe else 'limpio'}: {'detectado' if hit else 'limpio'}")
    # Cincel: asta vertical cortada a +26° pasa; a +31° (5° fuera, por encima del margen de
    # redondeo de un corte de 111 u) debe fallar.
    for y_der, debe in ((300 + round(100 * math.tan(math.radians(26))), False),
                        (300 + round(100 * math.tan(math.radians(31))), True)):
        uc, inf = ufoLib2.Font(), Informe()
        g = uc.newGlyph("asta")
        pen = g.getPen()
        for i, q in enumerate([(0, 0), (100, 0), (100, y_der), (0, 300)]):
            pen.moveTo(q) if i == 0 else pen.lineTo(q)
        pen.closePath()
        cincel(uc, inf, {"angulo": 26})
        hit = bool(inf.errores)
        ok &= hit == debe
        print(f"  cincel {y_der:<4} espera {'C' if debe else 'limpio'}: {'detectado' if hit else 'limpio'}")
    # Tierra de nadie: una U cuyo trazo inferior cuelga 69 u (caso real de Lacre) debe fallar.
    inf = Informe()
    zonas(glifo("U_cuelga", [[(0, -83), (100, -83), (100, 700), (0, 700)]]), inf, {0, -14, 700, 714, -220}, 14, {}, 1.0)
    ok &= bool(inf.errores)
    print(f"  U cuelga   espera Z: {'detectado' if inf.errores else 'NO DETECTADO'}")
    print("AUTOPRUEBA:", "OK" if ok else "FALLA")
    return ok


def main():
    args = sys.argv[1:]
    if "--meta" in args:
        sys.exit(0 if meta() else 1)
    if not args or args[0].startswith("--"):
        sys.exit(__doc__)
    conf = {}
    if "--config" in args:
        conf = json.loads(Path(args[args.index("--config") + 1]).read_text(encoding="utf-8"))
    total = Informe()
    for prefijo, u in fuentes(args[0]):
        inf = auditar(u, conf, Informe(prefijo))
        total.errores += inf.errores
        total.avisos += inf.avisos
        total.medidas[prefijo.strip() or "fuente"] = inf.medidas
    print(f"ERRORES ({len(total.errores)})")
    print("\n".join(total.errores) or "  ninguno")
    print(f"\nAVISOS ({len(total.avisos)})")
    print("\n".join(total.avisos) or "  ninguno")
    if "--json" in args:
        Path(args[args.index("--json") + 1]).write_text(json.dumps(
            {"errores": total.errores, "avisos": total.avisos, "medidas": total.medidas}, ensure_ascii=False, indent=1))
    sys.exit(1 if total.errores else 0)


if __name__ == "__main__":
    main()
