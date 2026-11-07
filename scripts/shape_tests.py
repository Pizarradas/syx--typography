#!/usr/bin/env python3
"""Pruebas de conformación con HarfBuzz. Uso: shape_tests.py fuente.ttf tests/shaping.json

Cada prueba: {"nombre", "texto", "lang" (opcional), "features" (opcional, {"tnum": true}),
"variaciones" (opcional, {"wght": 700}), y una o más expectativas:
  "espera_glifos": ["n", "o"]        nombres de glifo exactos
  "contiene_glifo": "ccaron"          aparece ese glifo
  "kern_distinto_de_cero": true       algún avance difiere del avance propio del glifo
  "avance_igual": true                todos los glifos del texto tienen el mismo avance
  "marca_movida": true                alguna marca recibe desplazamiento (mark actúa)
  "espera_offset": [x, y]             desplazamiento exacto del último glifo

Tras recortar, compara la conformación con la fuente de origen:
  shape_tests.py fuente.ttf tests/shaping.json --comparar web/x.woff2
Los WOFF2 pierden nombres de glifo: por eso se comparan avances y desplazamientos, no nombres.
"""
import io, json, sys
from pathlib import Path

import uharfbuzz as hb


def conformar(font, blob_face, prueba):
    buf = hb.Buffer()
    buf.add_str(prueba["texto"])
    buf.guess_segment_properties()
    if "lang" in prueba:
        buf.language = prueba["lang"]
    if "variaciones" in prueba:
        font.set_variations(prueba["variaciones"])
    hb.shape(font, buf, prueba.get("features", {}))
    nombres = [font.glyph_to_string(i.codepoint) for i in buf.glyph_infos]
    avances = [p.x_advance for p in buf.glyph_positions]
    pos = [(p.x_advance, p.x_offset, p.y_offset) for p in buf.glyph_positions]
    return nombres, avances, [font.get_glyph_h_advance(i.codepoint) for i in buf.glyph_infos], pos


def abrir(ruta):
    """HarfBuzz no lee WOFF2: se descomprime a un TTF temporal."""
    if str(ruta).endswith(".woff2"):
        from fontTools.ttLib import TTFont
        t = TTFont(ruta)
        t.flavor = None
        b = io.BytesIO()
        t.save(b)
        return hb.Face(hb.Blob(b.getvalue()))
    return hb.Face(hb.Blob.from_file_path(str(ruta)))


def main():
    ruta, tests = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    face = abrir(ruta)
    otra = abrir(sys.argv[sys.argv.index("--comparar") + 1]) if "--comparar" in sys.argv else None
    fallos = 0
    for t in tests:
        font = hb.Font(face)
        nombres, avances, propios, pos = conformar(font, face, t)
        desplazado = any(x or y for _, x, y in pos)
        err = []
        if "espera_glifos" in t and nombres != t["espera_glifos"]:
            err.append(f"esperaba {t['espera_glifos']}, obtuvo {nombres}")
        if "contiene_glifo" in t and t["contiene_glifo"] not in nombres:
            err.append(f"falta {t['contiene_glifo']} en {nombres}")
        if t.get("kern_distinto_de_cero") and avances == propios:
            err.append(f"sin kerning: {nombres}")
        if t.get("avance_igual") and len(set(avances)) > 1:
            err.append(f"avances desiguales: {avances}")
        if t.get("marca_movida") and not desplazado:
            err.append(f"marca sin posicionar: {nombres}")
        if "espera_offset" in t and list(pos[-1][1:]) != t["espera_offset"]:
            err.append(f"esperaba offset {t['espera_offset']}, obtuvo {list(pos[-1][1:])}")
        if otra is not None:
            _, _, _, pos2 = conformar(hb.Font(otra), otra, t)
            if pos2 != pos:
                err.append(f"difiere de la fuente comparada: {pos} / {pos2}")
        if ".notdef" in nombres:
            err.append("aparece .notdef")
        if err:
            fallos += 1
            print(f"FALLA  {t['nombre']}: {'; '.join(err)}")
        else:
            print(f"ok     {t['nombre']}")
    print(f"shaping: {len(tests) - fallos}/{len(tests)} superadas")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
