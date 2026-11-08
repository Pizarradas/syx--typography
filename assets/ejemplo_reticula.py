"""Plantilla de retícula de decisiones (references/02-dibujo-y-correcciones.md §4).

Copia este archivo al proyecto como reticula.py cuando la fase 1 esté aprobada. Cada valor
se DERIVA de un glifo aprobado y lleva su origen en el comentario; las funciones de glifo
solo usan estos nombres. Salirse de la retícula exige una entrada en CORRECCIONES.
Los números de abajo son de ejemplo: sustitúyelos por las medidas de tus glifos aprobados.
"""
P = dict(x=500, cap=700, asta=100, lat=60, n=470, o=520, d=500, e=480, s=400, H=640, O=720, A=700, E=500)
X, CAP, S = P["x"], P["cap"], P["asta"]

ALTURAS = {               # fracción de la zona (X en minúscula, CAP en versal y cifras)
    "rama": 0.30,         # el arco sale del asta (n h m r); u usa 1 − rama al girar n
    "hombro": 0.52,       # el arco se vuelve pierna (n h m); u usa 1 − hombro
    "panza_sup": 0.80,    # la panza se une al asta (d; b p q g)
    "remate_inf": 0.24,   # terminal abierto inferior (c e; 3 5)
    "remate_sup": 0.70,   # terminal abierto superior (a; 2 3)
    "cintura": 0.53,      # división óptica alta (barra de e, espina de S, B 3 8)
    "barra": 0.50,        # barra de H E F; apoyo de la barra de G
    "union": 0.40,        # uniones bajas (P R panza; K k Y; arranque de U J)
}


def y(papel, zona=CAP):
    return zona * ALTURAS[papel]


CORRECCIONES = {          # motivo + cantidad; cada una se juzga en una prueba concreta
    "contra_m": 0.92,     # contraformas de m algo más estrechas que la de n (Briem) · `minimum`
}

ANCHOS = {                # familias derivadas; los factores por letra son decisión de diseño
    "recta": P["n"],                                       # n h u x
    "arcada": 3 * S + 2 * CORRECCIONES["contra_m"] * (P["n"] - 2 * S),   # m
    "mixta": P["d"],                                       # b d p q g
    "abierta": P["e"],                                     # e; c ≈ 0,92
    "diagonal": (P["n"] + P["o"]) / 2,                     # v y; w ≈ 1,55
    "estrecha": P["s"],                                    # s z; r ≈ 0,78 recta
    "V_recta": P["H"], "V_redonda": P["O"], "V_estrecha": P["E"], "V_diagonal": P["A"],
}

LATERAL = {               # clase de borde → fracción de P["lat"] (de n, o, e y A aprobadas)
    "asta": 1.0, "hombro": 0.8, "redondo": 0.7, "panza": 0.65, "abierto": 0.45,
    "diagonal": 0.12, "V_asta": 1.2, "V_redondo": 0.7, "V_diagonal": 0.12,
}
