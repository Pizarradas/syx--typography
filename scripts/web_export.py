#!/usr/bin/env python3
"""Prepara una fuente para la web: instancia, recorta, comprime, VERIFICA y genera el CSS.

  web_export.py fuente.ttf [otra.ttf ...] -o web/ --slug mitipo [--limitar wght=300:800]
                [--rango completo|latin|latin-ext|ambos] [--ruta-css /fonts/] [--hinting] [--respaldo arial|times]

--rango completo (por defecto) da un solo WOFF2 con todo el cmap: es lo sensato para una
fuente latina de tamaño medio, porque trocear rompe kerning y marcas entre archivos.
Con varias estáticas, escribe un solo CSS con todos los @font-face.
Falla si en el conjunto se pierde algún carácter o feature.

Conserva todas las features de la fuente (pyftsubset por defecto eliminaría tnum, onum,
case, ordn, smcp o ssNN sin avisar) y comprueba las etiquetas GSUB/GPOS antes y después.
El rango latino incluye U+0300-0304 y U+0323: Google no pone U+0301 en latin ni latin-ext,
y un texto NFD pediría la marca a otro archivo.
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

from fontTools.ttLib import TTFont

BIN = Path(sys.executable).parent
LATIN = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0300-0304,U+0308,U+0323,U+0329,"
         "U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+25CC,U+FEFF,U+FFFD")
LATIN_EXT = ("U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0305-0307,U+0309-0322,U+0324-0328,"
             "U+032A-036F,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,"
             "U+A720-A7FF")
# Frecuencia aproximada de letras (español e inglés, con espacio) para la anchura media:
# xAvgCharWidth no sirve, porque en muchas fuentes es la media de todos los glifos.
FRECUENCIA = {" ": 18, "e": 12, "a": 10, "o": 8, "n": 7, "s": 7, "r": 6, "i": 6, "t": 6, "l": 5, "d": 4.5,
              "c": 3.8, "u": 3.5, "m": 2.8, "p": 2.3, "h": 2, "g": 1.5, "b": 1.4, "f": 1.3, "y": 1.3,
              "v": 1, "w": 0.8, "k": 0.4, "q": 0.6, "j": 0.4, "z": 0.4, "x": 0.3}
# Anchura media (em) de los respaldos con esa misma tabla y sus métricas.
RESPALDOS = {"arial": ("Arial", 0.4496), "times": ("Times New Roman", 0.404)}
PRESUPUESTO_KB = {"estatica": (30, 40), "wght": (70, 100), "multi": (110, 116)}


def tags(f):
    t = TTFont(f, lazy=True)
    res = set()
    for tb in ("GSUB", "GPOS"):
        if tb in t and t[tb].table.FeatureList:
            res |= {r.FeatureTag for r in t[tb].table.FeatureList.FeatureRecord}
    return res


def anchura_media(t):
    """Anchura media ponderada en em, medida en hmtx."""
    cm, hm, upm = t.getBestCmap(), t["hmtx"], t["head"].unitsPerEm
    pares = [(hm[cm[ord(c)]][0], w) for c, w in FRECUENCIA.items() if ord(c) in cm]
    if len(pares) < 10:
        return None
    return sum(a * w for a, w in pares) / sum(w for _, w in pares) / upm


def ejecutar(cmd):
    r = subprocess.run([str(c) for c in cmd], text=True, capture_output=True)
    if r.returncode:
        sys.exit(f"Falló {' '.join(map(str, cmd[:3]))}:\n{r.stderr[-1500:]}")


def cubre(cmap, rango):
    out = 0
    for tr in rango.split(","):
        a, _, b = tr[2:].partition("-")
        lo, hi = int(a, 16), int(b or a, 16)
        out += sum(1 for c in cmap if lo <= c <= hi)
    return out


def exportar(fuente, a, css, informe, sufijo):
    origen, t = fuente, TTFont(fuente, lazy=True)
    variable = "fvar" in t
    if a.limitar and not variable:
        print("AVISO: --limitar ignorado: la fuente es estática", file=sys.stderr)
    if a.limitar and variable:
        inst = a.salida / f"_{a.slug}{sufijo}-instanciada.ttf"
        ejecutar([BIN / "fonttools", "varLib.instancer", origen, *a.limitar, "-o", inst])
        origen = inst
    feats_antes, cmap = tags(origen), TTFont(origen, lazy=True).getBestCmap()
    t2 = TTFont(origen, lazy=True)
    rangos = {"latin": LATIN, "latin-ext": LATIN_EXT, "completo": "U+0000-10FFFF"}
    # latin va al final: en los solapes de unicode-range gana la última regla.
    usados = ["latin-ext", "latin"] if a.rango == "ambos" else [a.rango]
    familia = a.familia_css or t2["name"].getBestFamilyName()
    ej = {x.axisTag: x for x in t2["fvar"].axes} if "fvar" in t2 else {}
    w = ej.get("wght")
    peso = f"{w.minValue:g} {w.maxValue:g}" if w else str(t2["OS/2"].usWeightClass)
    decl = [f"font-weight: {peso};"]
    if "wdth" in ej:
        decl.append(f"font-stretch: {ej['wdth'].minValue:g}% {ej['wdth'].maxValue:g}%;")
    if "slnt" in ej:
        # slnt es negativo a la derecha y CSS usa grados positivos.
        lo, hi = sorted((abs(ej["slnt"].minValue), abs(ej["slnt"].maxValue)))
        decl.append(f"font-style: oblique {lo:g}deg {hi:g}deg;")
    elif t2["post"].italicAngle != 0 or t2["OS/2"].fsSelection & 1:
        decl.append("font-style: italic;")
    else:
        decl.append("font-style: normal;")
    decl_css = "\n  ".join(decl)
    conservadas, cubiertos = set(), set()
    for nombre in usados:
        rango = rangos[nombre]
        if cubre(cmap, rango) == 0:
            informe.append({"rango": nombre, "omitido": "la fuente no tiene glifos en este rango"})
            continue
        etiqueta = "" if nombre == "completo" else f"-{nombre}"
        destino = a.salida / f"{a.slug}{sufijo}{etiqueta}-v{a.version}.woff2"
        cmd = [BIN / "pyftsubset", origen, "--layout-features=*", "--name-IDs+=13,14", "--notdef-outline",
               "--flavor=woff2", f"--output-file={destino}"]
        cmd.append("--unicodes=*" if nombre == "completo" else f"--unicodes={rango}")
        cmd.append("--hinting" if a.hinting else "--no-hinting")
        ejecutar(cmd)
        despues = tags(destino)
        conservadas |= despues
        cubiertos |= set(TTFont(destino, lazy=True).getBestCmap())
        kb = destino.stat().st_size / 1024
        tipo = "estatica" if "fvar" not in t2 else ("wght" if len(t2["fvar"].axes) == 1 else "multi")
        obj, lim = PRESUPUESTO_KB[tipo]
        informe.append({"archivo": destino.name, "kb": round(kb, 1), "objetivo_kb": obj, "limite_kb": lim,
                        "excede": kb > lim, "features": sorted(despues)})
        ur = "" if nombre == "completo" else f"\n  unicode-range: {rango.replace(',', ', ')};"
        css.append(f"""@font-face {{
  font-family: "{familia}";
  src: url("{a.ruta_css}{destino.name}") format("woff2");
  {decl_css}
  font-display: swap;{ur}
}}""")
    perdidos = sorted(set(cmap) - cubiertos)
    m = TTFont(origen, lazy=True)
    if origen != fuente:
        Path(origen).unlink()
    return m, familia, sorted(feats_antes - conservadas), perdidos


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("fuentes", type=Path, nargs="+")
    p.add_argument("-o", "--salida", type=Path, required=True)
    p.add_argument("--slug", required=True)
    p.add_argument("--limitar", action="append", default=[], help="wght=300:800; solo ejes que existan")
    p.add_argument("--rango", choices=["completo", "latin", "latin-ext", "ambos"], default="completo")
    p.add_argument("--ruta-css", default="/fonts/", help="prefijo de las URL en el CSS")
    p.add_argument("--hinting", action="store_true", help="conserva hinting (estáticas de texto para Windows)")
    p.add_argument("--respaldo", choices=list(RESPALDOS), default="arial")
    p.add_argument("--familia-css", default=None)
    p.add_argument("--version", default="1")
    a = p.parse_args()
    a.salida.mkdir(parents=True, exist_ok=True)
    css, informe, perdidas, perdidos = [], [], [], []
    for f in a.fuentes:
        sufijo = "" if len(a.fuentes) == 1 else "-" + f.stem.split("-")[-1].lower()
        m, familia, pf, pc = exportar(f, a, css, informe, sufijo)
        perdidas += pf; perdidos += pc
    upm, os2, hhea = m["head"].unitsPerEm, m["OS/2"], m["hhea"]
    xa, cap = getattr(os2, "sxHeight", 0) or 0, getattr(os2, "sCapHeight", 0) or 0
    nombre_r, ancho_r = RESPALDOS[a.respaldo]
    media = anchura_media(m)
    if media is None:
        css.append("/* Sin respaldo ajustado: la fuente no tiene aún las letras básicas para medirla. */")
    else:
        ajuste = media / ancho_r
        css.append(f"""/* Respaldo ajustado: anchura media ponderada medida en hmtx frente a {nombre_r}.
   Es una estimación: mide el CLS real. Safari estable solo aplica size-adjust. */
@font-face {{
  font-family: "{familia} Fallback";
  src: local("{nombre_r}");
  size-adjust: {ajuste * 100:.2f}%;
  ascent-override: {hhea.ascent / upm / ajuste * 100:.2f}%;
  descent-override: {abs(hhea.descent) / upm / ajuste * 100:.2f}%;
  line-gap-override: {hhea.lineGap / upm / ajuste * 100:.2f}%;
}}
/* body {{ font-family: "{familia}", "{familia} Fallback", system-ui, sans-serif; }} */""")
    (a.salida / f"{a.slug}.css").write_text("\n\n".join(css) + "\n", encoding="utf-8")
    for r in informe:
        if r.get("excede"):
            print(f"AVISO: {r['archivo']} supera el presupuesto propuesto de {r['limite_kb']} KB", file=sys.stderr)
    txt = "".join(chr(c) for c in sorted(set(perdidos)))
    res = {"informe": informe, "css": str(a.salida / f"{a.slug}.css"), "metricas": {"upm": upm, "x": xa, "cap": cap},
           "features_ausentes": sorted(set(perdidas)), "caracteres_excluidos": txt}
    print(json.dumps(res, ensure_ascii=False, indent=2))
    grave = a.rango in ("completo", "ambos") and (perdidas or perdidos)
    if perdidas or perdidos:
        print(f"AVISO: fuera de lo exportado: features {sorted(set(perdidas))}, caracteres {txt!r}", file=sys.stderr)
    sys.exit(1 if grave else 0)


if __name__ == "__main__":
    main()
