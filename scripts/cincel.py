"""Terminales a cincel con una regla única para rectas y curvas.

Regla: la recta de corte forma `angulo` grados (antihorario) con la perpendicular al
trazo, y el eje del trazo es la BISECTRIZ de los dos bordes reales que llegan al corte.
Medir respecto a la tangente del esqueleto o respecto a la vertical da ángulos distintos
en cada letra (en un proyecto real, de −22° a +44° para una regla de 26°).

El corte lo hace el propio motor (`G.trazo(..., ini=, fin=)`, raíz exacta de la cúbica),
sin booleanas: no quedan astillas ni la punta puede morder otra parte de la letra. Como
los bordes reales dependen del ángulo del corte, el ángulo se resuelve por punto fijo
(converge en 2–4 iteraciones a < 0,005°).

Requisito del motor: la recta de corte debe cruzar ambos bordes dentro del primer (ini)
o último (fin) tramo. Si falla en una letra pequeña o un peso negro, alarga ese tramo del
esqueleto más allá del corte (p. ej. empieza el arco antes): la punta sobrante no existe,
porque el motor recorta.
"""
import math

import pathops
from fontTools.pens.recordingPen import RecordingPen

from motor import evalua, seg


def _segmentos(path):
    """Segmentos de un pathops.Path por contorno: ('l', p0, p1) o ('c', p0, c1, c2, p3)."""
    rec = RecordingPen()
    path.draw(rec)
    conts, cur, ini, prev = [], [], None, None
    for op, args in rec.value:
        if op == "moveTo":
            cur, ini, prev = [], args[0], args[0]
        elif op == "lineTo":
            cur.append(("l", prev, args[0]))
            prev = args[0]
        elif op == "curveTo":
            cur.append(("c", prev, *args))
            prev = args[-1]
        elif op in ("closePath", "endPath"):
            if prev != ini:
                cur.append(("l", prev, ini))
            conts.append(cur)
    return conts


def _tangente(sg, fin):
    pts = sg[1:]
    if fin:
        for q in reversed(pts[:-1]):
            if math.dist(q, pts[-1]) > 1e-9:
                return math.degrees(math.atan2(pts[-1][1] - q[1], pts[-1][0] - q[0]))
    for q in pts[1:]:
        if math.dist(q, pts[0]) > 1e-9:
            return math.degrees(math.atan2(q[1] - pts[0][1], q[0] - pts[0][0]))


def _bisectriz(conts, q, phi, punta):
    """Eje del trazo en el corte: bisectriz de los bordes que llegan a la recta de corte,
    orientados hacia la punta."""
    u = (math.cos(math.radians(phi)), math.sin(math.radians(phi)))
    for cont in conts:
        for k, sg in enumerate(cont):
            if sg[0] != "l" or math.dist(sg[1], sg[2]) < 5:
                continue
            if max(abs((p[0] - q[0]) * u[1] - (p[1] - q[1]) * u[0]) for p in sg[1:]) > 0.6:
                continue
            sx = sy = 0.0
            for tg in (_tangente(cont[k - 1], True), _tangente(cont[(k + 1) % len(cont)], False) + 180):
                tx, ty = math.cos(math.radians(tg)), math.sin(math.radians(tg))
                if tx * punta[0] + ty * punta[1] < 0:
                    tx, ty = -tx, -ty
                sx, sy = sx + tx, sy + ty
            return math.degrees(math.atan2(sy, sx))
    raise ValueError("no se encontró la recta de corte en el trazo")


class _Corte:
    def __init__(self, nodos, i, t, hacia_inicio, k, angulo):
        a, b = nodos[i], nodos[i + 1]
        sg = seg((a.x, a.y), a.ang, (b.x, b.y), b.ang, k)
        self.q, q2 = evalua(sg, t), evalua(sg, t + 1e-4)
        self.tau = math.degrees(math.atan2(q2[1] - self.q[1], q2[0] - self.q[0])) + (180 if hacia_inicio else 0)
        self.phi = self.tau + 90 + angulo  # primera estimación: eje = tangente del esqueleto


def trazo_con_cincel(g, nodos, angulo, ini=None, fin=None, iteraciones=12):
    """Dibuja en el glifo g (motor.G) un trazo con terminales a cincel.

    nodos: los N del trazo; angulo: grados respecto a la perpendicular al trazo;
    ini / fin: parámetro t (0–1) del primer / último tramo del esqueleto donde cortar.
    Devuelve los ángulos finales de las rectas de corte, por si se quieren registrar."""
    cortes = {}
    if ini is not None:
        cortes["ini"] = _Corte(nodos, 0, ini, True, g.k, angulo)
    if fin is not None:
        cortes["fin"] = _Corte(nodos, len(nodos) - 2, fin, False, g.k, angulo)

    def dibuja():
        p = pathops.Path()
        viejo = g.pen
        g.pen = p.getPen()
        try:
            g.trazo(nodos, ini=(cortes["ini"].q, cortes["ini"].phi) if "ini" in cortes else None,
                    fin=(cortes["fin"].q, cortes["fin"].phi) if "fin" in cortes else None)
        finally:
            g.pen = viejo
        return p

    for _ in range(iteraciones):
        conts = _segmentos(dibuja())
        cambio = 0.0
        for c in cortes.values():
            punta = (math.cos(math.radians(c.tau)), math.sin(math.radians(c.tau)))
            eje = _bisectriz(conts, c.q, c.phi, punta)
            delta = (eje + 90 + angulo - c.phi + 90) % 180 - 90
            c.phi += delta
            cambio = max(cambio, abs(delta))
        if cambio < 0.005:
            break
    dibuja().draw(g.g.getPen())
    return {k: c.phi for k, c in cortes.items()}
