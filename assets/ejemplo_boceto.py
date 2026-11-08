"""Ejemplo de archivo de boceto: tres direcciones de concepto para comparar.

NO es un diseño: muestra el contrato (VARIANTES + glifos) y cómo el estilo —
tensión, corte, eje del contraste — viaja con cada variante en lugar de heredarse
del motor. Las cifras son de este ejemplo: cada boceto decide las suyas. Uso:
  sketch.py assets/ejemplo_boceto.py -o hoja.png --texto "noon HOHO"
"""
from motor import G, N  # sketch.py añade scripts/ a sys.path

X, CAP, REB = 510, 700, 12

VARIANTES = {
    "A · vertical, tensa": dict(asta=92, fino=80, eje=0, k=0.61, ki=0.63, corte=16,
                                n=400, o=480, H=590, O=670, lat=62),
    "B · eje 14, humanista": dict(asta=96, fino=66, eje=14, k=0.57, ki=0.58, corte=24,
                                  n=410, o=500, H=600, O=690, lat=66),
    "C · negra, cuadrada": dict(asta=150, fino=118, eje=0, k=0.68, ki=0.70, corte=8,
                                n=440, o=530, H=640, O=730, lat=46),
}


def glifos(u, p):
    u.info.unitsPerEm = 1000
    u.info.xHeight, u.info.capHeight = X, CAP
    estilo = dict(corte=p["corte"], k=p["k"], ki=p["ki"])

    g = G(u, "space", 0x20, **estilo)
    g.g.width = 240

    g = G(u, "o", 0x6F, lsb=round(p["lat"] * 0.62), rsb=round(p["lat"] * 0.62), **estilo)
    g.anillo_eje(0, p["o"], -REB, X + REB, p["asta"] * 1.08, p["fino"], eje=p["eje"])
    g.cerrar(p["o"])

    g = G(u, "O", 0x4F, lsb=round(p["lat"] * 0.8), rsb=round(p["lat"] * 0.8), **estilo)
    g.anillo_eje(0, p["O"], -REB, CAP + REB, p["asta"] * 1.22, p["fino"] * 1.06, eje=p["eje"])
    g.cerrar(p["O"])

    g = G(u, "H", 0x48, lsb=round(p["lat"] * 1.3), rsb=round(p["lat"] * 1.3), **estilo)
    s, w = p["asta"] * 1.13, p["H"]
    g.rect(0, 0, s, CAP)
    g.rect(w - s, 0, w, CAP)
    g.rect(s * 0.5, CAP * 0.52 - p["fino"] / 2, w - s * 0.5, CAP * 0.52 + p["fino"] / 2)
    g.cerrar(w)

    g = G(u, "n", 0x6E, lsb=p["lat"], rsb=round(p["lat"] * 0.8), **estilo)
    s, w, f = p["asta"], p["n"], p["fino"]
    g.rect(0, 0, s, X)
    # Arco: asta izquierda -> hombro -> asta derecha, cortado en la línea de base.
    g.trazo([N(s * 0.5, X * 0.30, 90, s * 0.5, s * 0.5),
             N((s + w) * 0.5, X + REB - f * 0.5, 0, f * 0.5, f * 0.5),
             N(w - s * 0.5, 0, -90, s * 0.5, s * 0.5)],
            fin=((0, 0), 0))
    g.cerrar(w)
