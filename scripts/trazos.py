"""Ayudas para dibujar glifos por código en UFO con compatibilidad por construcción.

Regla central: cada glifo es una función de un diccionario de parámetros y emite SIEMPRE
la misma secuencia de puntos. Así todos los másteres son interpolables sin reparaciones.
No uses condicionales que cambien el número de puntos según el máster.

Convención UFO/PostScript: contorno exterior antihorario, contraforma horaria.
"""
K_CIRCULO = 0.5523  # tensión de un círculo; las curvas tipográficas suelen ir de 0,55 a 0,76


def _r(v):
    return round(v)


class Glifo:
    def __init__(self, ufo, nombre, unicodes=None, lsb=0, rsb=0):
        self.g = ufo.newGlyph(nombre) if nombre not in ufo else ufo[nombre]
        self.g.clearContours(); self.g.clearComponents(); self.g.clearAnchors()
        if unicodes is not None:
            self.g.unicodes = [unicodes] if isinstance(unicodes, int) else list(unicodes)
        self.pen = self.g.getPen()
        self.lsb, self.rsb = lsb, rsb
        self.negro = 0  # anchura de negro declarada

    # -- contornos -----------------------------------------------------------------
    def contorno(self, inicio, *segmentos):
        """segmentos: (x, y) es línea; ((c1x,c1y),(c2x,c2y),(x,y)) es curva cúbica."""
        p = self.pen
        p.moveTo((_r(inicio[0]), _r(inicio[1])))
        for s in segmentos:
            if len(s) == 2 and not isinstance(s[0], (tuple, list)):
                p.lineTo((_r(s[0]), _r(s[1])))
            else:
                p.curveTo(*[(_r(x), _r(y)) for x, y in s])
        p.closePath()

    def rect(self, x0, y0, x1, y1):
        self.contorno((x0, y0), (x1, y0), (x1, y1), (x0, y1))

    def ovalo(self, cx, cy, rx, ry, kx=K_CIRCULO, ky=None, horario=False):
        """Óvalo con cuatro nodos en los extremos. kx, ky: tensión; más de 0,55 = más cuadrado."""
        ky = kx if ky is None else ky
        hx, hy = rx * kx, ry * ky
        if not horario:
            self.contorno((cx, cy - ry),
                          ((cx + hx, cy - ry), (cx + rx, cy - hy), (cx + rx, cy)),
                          ((cx + rx, cy + hy), (cx + hx, cy + ry), (cx, cy + ry)),
                          ((cx - hx, cy + ry), (cx - rx, cy + hy), (cx - rx, cy)),
                          ((cx - rx, cy - hy), (cx - hx, cy - ry), (cx, cy - ry)))
        else:
            self.contorno((cx, cy - ry),
                          ((cx - hx, cy - ry), (cx - rx, cy - hy), (cx - rx, cy)),
                          ((cx - rx, cy + hy), (cx - hx, cy + ry), (cx, cy + ry)),
                          ((cx + hx, cy + ry), (cx + rx, cy + hy), (cx + rx, cy)),
                          ((cx + rx, cy - hy), (cx + hx, cy - ry), (cx, cy - ry)))

    def componente(self, base, dx=0, dy=0):
        self.pen.addComponent(base, (1, 0, 0, 1, _r(dx), _r(dy)))

    def ancla(self, nombre, x, y):
        self.g.appendAnchor({"name": nombre, "x": _r(x), "y": _r(y)})

    def cerrar(self, ancho_negro):
        """Fija el avance. Los contornos se dibujan desde x=0 y aquí se desplazan a lsb."""
        lsb = _r(self.lsb)  # sin esto quedarían coordenadas decimales en el UFO
        self.g.move((lsb, 0))
        self.g.width = _r(lsb + ancho_negro + self.rsb)
