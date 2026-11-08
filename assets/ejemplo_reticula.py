"""Retícula de decisiones del proyecto (references/02-dibujo-y-correcciones.md §4).

new_project.py copia esta plantilla como reticula.py. Rellénala al aprobar la fase 1, con las
medidas de los glifos aprobados, y desde la fase 2 dibuja solo con sus nombres:

    from reticula import reticula
    R = reticula(p, m)            # p: parámetros del máster; m: métricas (x, cap…)
    yb = R.y("union")             # en lugar de yb = CAP * 0.40
    w = R.ancho["mixta"]          # en lugar de w = 490
    Glifo(u, "b", 0x62, lsb=R.lat("asta"), rsb=R.lat("panza"))

`reticula.py PROYECTO` (de la skill) lista las medidas estructurales que aún no salen de aquí.
Cada valor lleva su ORIGEN (el glifo aprobado del que se midió). Los números de abajo son de
ejemplo: sustitúyelos por los tuyos. Salirse de la retícula exige una entrada en CORRECCIONES.
"""
from types import SimpleNamespace

# -- alturas: fracción de su zona (x en minúscula, versal en mayúsculas y cifras) ----------
# Son proporciones: valen para todos los másteres. Si un peso necesita otra, es una corrección.
ALTURAS = {
    "rama": 0.30,         # origen: n · el arco sale del asta (n h m r); u usa 1 − rama al girar n
    "hombro": 0.52,       # origen: n · el arco se vuelve pierna (n h m); u usa 1 − hombro
    "panza_sup": 0.80,    # origen: d · la panza se une al asta (b p q g)
    "remate_inf": 0.24,   # origen: e · terminal abierto inferior (c; cifras 3 5)
    "remate_sup": 0.70,   # origen: a · terminal abierto superior (cifras 2 3)
    "cintura": 0.53,      # origen: e (barra) y S (espina) · B 3 8
    "barra": 0.50,        # origen: H · E F; apoyo de la barra de G
    "union": 0.40,        # origen: P · panza de R; brazos de K k; horquilla de Y; arranque de U J
}

# -- correcciones ópticas declaradas: motivo, cantidad y la prueba que la juzga ----------------
CORRECCIONES = {
    "contra_m": 0.92,     # contraformas de m algo más estrechas que la de n (Briem) · `minimum`
}

# -- laterales: clase de borde → fracción del lateral de n (origen: n, o, e, A aprobadas) ------
LATERAL = {
    "asta": 1.0, "hombro": 0.8, "redondo": 0.7, "panza": 0.65, "abierto": 0.45, "diagonal": 0.12,
    "V_asta": 1.2, "V_redondo": 0.7, "V_diagonal": 0.12,
}


def reticula(p, m):
    """p: parámetros del máster (asta, n, o, d, e, s, H, O, E, A, lat…); m: métricas (x, cap)."""
    s = p["asta"]
    ancho = {   # familias derivadas de los aprobados; los factores por letra son decisión de diseño
        "recta": p["n"],                                                    # n h u x
        "arcada": 3 * s + 2 * CORRECCIONES["contra_m"] * (p["n"] - 2 * s),  # m
        "mixta": p["d"],                                                    # b d p q g
        "abierta": p["e"],                                                  # e; c ≈ 0,92
        "diagonal": (p["n"] + p["o"]) / 2,                                  # v y; w ≈ 1,55
        "estrecha": p["s"],                                                 # s z; r ≈ 0,78 recta
        "V_recta": p["H"], "V_redonda": p["O"], "V_estrecha": p["E"], "V_diagonal": p["A"],
    }
    zona = {"x": m["x"], "cap": m["cap"]}
    return SimpleNamespace(
        ancho=ancho,
        correccion=CORRECCIONES,
        y=lambda papel, z="cap": zona[z] * ALTURAS[papel],
        lat=lambda clase: round(p["lat"] * LATERAL[clase]),
    )
