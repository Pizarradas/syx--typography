#!/usr/bin/env python3
"""Genera pruebas PNG de una fuente. Mirar estas pruebas es obligatorio: sin ojo no hay diseño.

  proof.py fuente.ttf -o proofs/ --pagina control palabras texto cascada glifos pesos idiomas oscuro

Páginas: control (cadenas de espaciado), palabras (palabras de diseño), texto (párrafos a
tamaños de lectura), cascada (mismas palabras de 8 a 96 pt), glifos (rejilla con métricas),
pesos (cada instancia), idiomas (español y vecinos), oscuro (claro sobre oscuro).
--texto "..." sustituye las palabras, --var wght=700 fija una variación, --feat tnum activa features.
Solo se muestran los caracteres que existen; lo que falta se informa, no se oculta.
"""
import argparse, re
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont, features as pil_features

DPI = 144
ESC = DPI / 72  # 1 pt = 2 px: las pruebas se juzgan a tamaño real ampliado 2x

CONTROL = ["nnnnnnnn", "nnonnonno", "noononno", "oooooooo", "HHHHHHHH", "HHOHHOHH", "HOHOHOHO", "OOOOOOOO",
           "nanbncndnenfngnhninjnknlnmn", "oaobocodoeofogohoiojokolomo",
           "HAHBHCHDHEHFHGHIHJHKHLHMH", "OAOBOCODOEOFOGOIOJOKOLOMO", "H0H1H2H3H4 n,n.n;n:n¿n¡n"]
PALABRAS = ["adhesion", "hamburgefonstiv", "minimum", "Tipografía", "Hamburgefonstiv", "ÑANDÚ", "cigüeña"]
ES = ("La tipografía no se dibuja letra a letra: se construye como un sistema en el que cada forma "
      "responde a las demás. ¿Qué hace que un texto se lea sin esfuerzo? El ritmo regular de blancos y "
      "negros, la apertura de las formas y un espaciado paciente. ¡Ñandú, cigüeña, pingüino y vergüenza "
      "ponen a prueba los acentos! En 1984 costaba 12,50 €, y el 3.º de 2.ª fila pagó «a escote».")
IDIOMAS = {
    "Español": "¿Dónde está el pingüino? ¡Aquí, señor! Años, cañón, ÑANDÚ, 1.º, 2.ª, «comillas»",
    "Català": "Col·legi, paral·lel, COL·LEGI, PARAL·LEL, plaça, Ç, l·l",
    "Galego": "Ourense, Galiza, nación, viaxe, señor, lingua",
    "Euskara": "Euskal Herria, ñabardura, txakolina, zuhaitz",
    "Asturianu": "Asturies, ḷḷuna, ḥoguera, xente",
    "Português": "Coração, ação, São João, além, ç, ã, õ",
    "Français": "Œuvre, cœur, Noël, naïve, « bientôt »",
    "Deutsch": "Straße, Größe, Übung, Äpfel, ẞ",
    "Polski": "Żółć, gęś, jaźń, Łódź, ą, ę",
    "Čeština": "Příliš žluťoučký kůň, ďábel, ť, ľ",
    "Română": "Șapte, țară, ȘȚ, și",
    "Türkçe": "İstanbul, ılık, fıstık, fi, ĞŞ",
    "Tiếng Việt": "Tiếng Việt, Ắ, Ầ, Ễ, ệ, ử",
}


def cargar(fuente, pt, var=None):
    f = ImageFont.truetype(str(fuente), round(pt * ESC), layout_engine=ImageFont.Layout.RAQM)
    if var:
        ejes = f.get_variation_axes()
        vals = []
        for e in ejes:
            nom = e["name"].decode() if isinstance(e["name"], bytes) else e["name"]
            tag = {"Weight": "wght", "Width": "wdth", "Optical Size": "opsz", "Slant": "slnt", "Italic": "ital"}.get(nom, nom)
            vals.append(var.get(tag, e["default"]))
        f.set_variation_by_axes(vals)
    return f


def lienzo(alto, ancho=1600, fondo="white"):
    return Image.new("L", (ancho, alto), fondo)


def recortar(im, fondo=255, margen=40):
    from PIL import ImageChops
    caja = ImageChops.difference(im, Image.new("L", im.size, fondo)).getbbox()
    if not caja:
        return im
    return im.crop((0, 0, im.width, min(im.height, caja[3] + margen)))


def _fuente_etiqueta():
    # La fuente por defecto de Pillow no tiene acentos.
    for ruta in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf"):
        if Path(ruta).exists():
            return ImageFont.truetype(ruta, 14)
    return ImageFont.load_default(14)


ETIQUETA = _fuente_etiqueta()


def etiqueta(d, xy, txt, color=120):
    d.text(xy, txt, fill=color, font=ETIQUETA)


def ajustar(texto, font, ancho, feats):
    lineas, act = [], ""
    for w in texto.split():
        prueba = (act + " " + w).strip()
        if font.getlength(prueba, features=feats) > ancho and act:
            lineas.append(act)
            act = w
        else:
            act = prueba
    return lineas + [act]


def existe(cmap, texto):
    return all(ord(c) in cmap or c.isspace() for c in texto)


FALTANTES = set()


def filtrar(cmap, texto):
    FALTANTES.update(c for c in texto if ord(c) not in cmap and not c.isspace())
    return "".join(c if ord(c) in cmap or c.isspace() else "" for c in texto)


def pag_control(a):
    im = lienzo(2400); d = ImageDraw.Draw(im); y = 30
    f = cargar(a.fuente, a.pt_control, a.var)
    for s in a.textos_control:
        s = filtrar(a.cmap, s)
        if not s:
            continue
        d.text((40, y), s, fill=0, font=f, features=a.feat); y += round(a.pt_control * ESC * 1.45)
    return recortar(im)


def pag_palabras(a):
    im = lienzo(2200); d = ImageDraw.Draw(im); y = 30
    for pt in (72, 36):
        f = cargar(a.fuente, pt, a.var)
        for s in a.palabras:
            s = filtrar(a.cmap, s)
            if s:
                d.text((40, y), s, fill=0, font=f, features=a.feat); y += round(pt * ESC * 1.3)
    return recortar(im)


def pag_texto(a, fondo=255, tinta=0):
    im = lienzo(2600, fondo=fondo); d = ImageDraw.Draw(im); y = 30
    cuerpo = filtrar(a.cmap, a.parrafo)
    for pt, col in ((9, 700), (10.5, 760), (12, 860), (16, 1100), (24, 1500)):
        etiqueta(d, (40, y), f"{pt} pt", color=128); y += 22
        f = cargar(a.fuente, pt, a.var)
        for li in ajustar(cuerpo, f, col, a.feat):
            d.text((40, y), li, fill=tinta, font=f, features=a.feat); y += round(pt * ESC * 1.4)
        y += 30
    return recortar(im, fondo)


def pag_cascada(a):
    im = lienzo(2000); d = ImageDraw.Draw(im); y = 30
    s = filtrar(a.cmap, a.palabras[0] + " " + a.palabras[-1])
    for pt in (8, 9, 10, 12, 14, 18, 24, 36, 48, 72, 96):
        f = cargar(a.fuente, pt, a.var)
        etiqueta(d, (40, y), f"{pt}")
        d.text((90, y), s, fill=0, font=f, features=a.feat); y += round(pt * ESC * 1.35) + 8
    return recortar(im)


def pag_glifos(a):
    t = TTFont(a.fuente, lazy=True)
    upm = t["head"].unitsPerEm
    os2 = t["OS/2"]
    cps = sorted(c for c in a.cmap if c > 32)
    celda, pt = 150, 44
    cols = 1560 // celda
    filas = len(cps) // cols + 1
    im = lienzo(min(filas * 210 + 60, 6000)); d = ImageDraw.Draw(im)
    f = cargar(a.fuente, pt, a.var)
    px = pt * ESC / upm
    for i, cp in enumerate(cps):
        x = 20 + (i % cols) * celda
        y = 20 + (i // cols) * 210
        base = y + 150
        for alt, col in ((0, 170), (getattr(os2, "sxHeight", 0) or 0, 215), (getattr(os2, "sCapHeight", 0) or 0, 215)):
            yy = base - alt * px
            d.line([(x, yy), (x + celda - 10, yy)], fill=col)
        d.text((x + 16, base), chr(cp), fill=0, font=f, anchor="ls")
        etiqueta(d, (x + 4, y + 176), f"{cp:04X}", color=120)
    return recortar(im)


def pag_pesos(a):
    t = TTFont(a.fuente, lazy=True)
    if "fvar" not in t:
        return None
    im = lienzo(2200); d = ImageDraw.Draw(im); y = 30
    s = filtrar(a.cmap, a.palabras[0] + " " + a.palabras[-1])
    for ins in t["fvar"].instances:
        var = {k: v for k, v in ins.coordinates.items()}
        f = cargar(a.fuente, 44, var)
        etiqueta(d, (40, y), str(var)); y += 20
        d.text((40, y), s, fill=0, font=f, features=a.feat); y += 96
    return recortar(im)


def pag_idiomas(a):
    im = lienzo(1800); d = ImageDraw.Draw(im); y = 30
    f = cargar(a.fuente, 20, a.var)
    for nom, s in IDIOMAS.items():
        faltan = sorted({c for c in s if not c.isspace() and ord(c) not in a.cmap})
        etiqueta(d, (40, y), nom + (f"  ·  FALTAN: {''.join(faltan)}" if faltan else ""), color=60 if faltan else 130)
        y += 20
        d.text((40, y), filtrar(a.cmap, s), fill=0, font=f, features=a.feat); y += 58
    return recortar(im)


def pag_oscuro(a):
    return pag_texto(a, fondo=0, tinta=255)


PAGS = dict(control=pag_control, palabras=pag_palabras, texto=pag_texto, cascada=pag_cascada,
            glifos=pag_glifos, pesos=pag_pesos, idiomas=pag_idiomas, oscuro=pag_oscuro)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("fuente", type=Path)
    p.add_argument("-o", "--salida", type=Path, default=Path("proofs"))
    p.add_argument("--pagina", nargs="*", default=["control", "palabras", "texto", "cascada", "glifos", "pesos", "idiomas", "oscuro"])
    p.add_argument("--texto", help="palabras separadas por espacios")
    p.add_argument("--var", action="append", default=[], help="eje=valor")
    p.add_argument("--feat", action="append", default=[], help="tag, p. ej. tnum")
    p.add_argument("--pt-control", type=float, default=24)
    a = p.parse_args()
    if not pil_features.check("raqm"):
        raise SystemExit("Pillow sin Raqm: no aplicaría kerning ni features.")
    a.var = {k: float(v) for k, v in (s.split("=") for s in a.var)}
    a.cmap = TTFont(a.fuente, lazy=True).getBestCmap()
    a.palabras = a.texto.split() if a.texto else PALABRAS
    a.textos_control = [a.texto] + CONTROL if a.texto else CONTROL
    a.parrafo = ES
    a.salida.mkdir(parents=True, exist_ok=True)
    base = re.sub(r"\[.*\]|-VF$", "-var", a.fuente.stem)
    for nombre in a.pagina:
        im = PAGS[nombre](a)
        if im is None:
            print(f"(sin {nombre}: fuente estática)")
            continue
        destino = a.salida / f"{base}-{nombre}.png"
        im.save(destino)
        print(destino)
    if FALTANTES:
        print(f"AVISO: caracteres sin glifo, omitidos en las pruebas: {''.join(sorted(FALTANTES))}")
    if FALTANTES:
        print(f"AVISO: caracteres sin glifo, omitidos en las pruebas: {''.join(sorted(FALTANTES))}")


if __name__ == "__main__":
    main()
