#!/usr/bin/env python3
"""Crea el esqueleto de un proyecto tipográfico: UFO + designspace + brief + registro.

Ejemplo:
  new_project.py ~/fuentes/mitipo --family "Mi Tipo" --wght 300:400:700 --x-height 510 --cap 700

Sin --wght crea un solo máster Regular. Los másteres van en los extremos del eje; el
valor por defecto solo añade máster si no coincide con un extremo.
"""
import argparse, json, re, shutil, subprocess, sys
from datetime import date
from pathlib import Path

import ufoLib2
from fontTools.designspaceLib import AxisDescriptor, AxisLabelDescriptor, DesignSpaceDocument, InstanceDescriptor, SourceDescriptor

WEIGHT_NAMES = {100: "Thin", 200: "ExtraLight", 300: "Light", 400: "Regular", 500: "Medium",
                600: "SemiBold", 700: "Bold", 800: "ExtraBold", 900: "Black"}
ASSETS = Path(__file__).resolve().parent.parent / "assets"


def slug(family):
    return re.sub(r"[^A-Za-z0-9]", "", family)


def make_master(path, family, style, a, peso=400):
    ufo = ufoLib2.Font()
    i = ufo.info
    i.familyName, i.styleName = family, style
    i.unitsPerEm, i.xHeight, i.capHeight = a.upm, a.x_height, a.cap
    i.ascender, i.descender = a.asc, a.desc
    i.italicAngle = 0
    i.openTypeOS2WeightClass = peso
    if style in ("Regular", "Bold"):
        i.styleMapFamilyName, i.styleMapStyleName = family, style.lower()
    i.versionMajor, i.versionMinor = 0, 1
    # Estrategia por defecto: lineGap 0, hhea = typo, USE_TYPO_METRICS. Los valores win
    # se recalculan con la caja real de la familia en build.py.
    i.openTypeOS2TypoAscender, i.openTypeOS2TypoDescender, i.openTypeOS2TypoLineGap = a.typo_asc, a.typo_desc, 0
    i.openTypeHheaAscender, i.openTypeHheaDescender, i.openTypeHheaLineGap = a.typo_asc, a.typo_desc, 0
    i.openTypeOS2WinAscent, i.openTypeOS2WinDescent = a.typo_asc, abs(a.typo_desc)
    i.openTypeOS2Selection = [7]
    i.openTypeOS2Type = []  # fsType 0: instalable. Una EULA restrictiva puede requerir otro valor.
    if a.licencia == "ofl":
        i.openTypeNameLicense = "This Font Software is licensed under the SIL Open Font License, Version 1.1."
        i.openTypeNameLicenseURL = "https://openfontlicense.org"
    if a.autoria:
        i.openTypeNameDesigner = a.autoria
        i.openTypeOS2VendorID = a.vendor
        i.copyright = f"Copyright {date.today().year} {a.autoria}"
    i.postscriptBlueValues = [-a.overshoot, 0, a.x_height, a.x_height + a.overshoot,
                              a.cap, a.cap + a.overshoot]
    i.postscriptOtherBlues = [a.desc - a.overshoot, a.desc]
    ufo.lib["public.glyphOrder"] = [".notdef", "space"]
    ufo.save(path, overwrite=True)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", type=Path)
    p.add_argument("--family", required=True)
    p.add_argument("--wght", help="min:def:max, p. ej. 300:400:700")
    p.add_argument("--upm", type=int, default=1000)
    p.add_argument("--x-height", type=int, default=500)
    p.add_argument("--cap", type=int, default=700)
    p.add_argument("--asc", type=int, default=750)
    p.add_argument("--desc", type=int, default=-200)
    p.add_argument("--typo-asc", type=int, default=None)
    p.add_argument("--typo-desc", type=int, default=None)
    p.add_argument("--overshoot", type=int, default=12)
    p.add_argument("--vendor", default="NONE", help="ID de fabricante de 4 caracteres")
    p.add_argument("--licencia", choices=["pendiente", "ofl", "propietaria"], default="pendiente",
                   help="la licencia la decide la persona; pendiente deja los campos vacíos y check_sources avisa")
    p.add_argument("--autoria", help="titular del copyright y diseñador")
    a = p.parse_args()

    if a.path.exists() and any(a.path.iterdir()):
        sys.exit(f"{a.path} ya existe y no está vacío; no se sobrescribe.")
    # Interlineado por defecto de 1,25 em con las mayúsculas centradas en él.
    span = round(1.25 * a.upm)
    if a.typo_asc is None:
        a.typo_asc = round((span + a.cap) / 2)
    if a.typo_desc is None:
        a.typo_desc = a.typo_asc - span

    fam = slug(a.family)
    src = a.path / "sources"
    (src / "masters").mkdir(parents=True)
    for d in ("fonts", "proofs", "tests", "registro", "web"):
        (a.path / d).mkdir()

    if a.wght:
        vals = [int(v) for v in a.wght.split(":")]
        lo, de, hi = vals if len(vals) == 3 else (vals[0],) * 3  # «--wght 400»: un solo máster
        master_vals = sorted({lo, de, hi}) if de not in (lo, hi) else sorted({lo, hi})
    else:
        lo = de = hi = 400
        master_vals = [400]

    ds = DesignSpaceDocument()
    ds.formatVersion = "5.0"
    ax = AxisDescriptor()
    ax.name, ax.tag, ax.minimum, ax.default, ax.maximum = "Weight", "wght", lo, de, hi
    # Sin etiquetas, fontmake deja STAT sin valores de eje.
    ax.axisLabels = [AxisLabelDescriptor(name=WEIGHT_NAMES[v], userValue=v, elidable=v == 400,
                                         linkedUserValue=700 if v == 400 and hi >= 700 else None)
                     for v in sorted(WEIGHT_NAMES) if lo <= v <= hi]
    ds.addAxis(ax)
    for v in master_vals:
        style = WEIGHT_NAMES.get(v, f"W{v}")
        rel = f"masters/{fam}-{style}.ufo"
        make_master(src / rel, a.family, style, a, v)
        s = SourceDescriptor()
        s.path, s.filename, s.familyName, s.styleName = str(src / rel), rel, a.family, style
        s.location = {"Weight": v}
        ds.addSource(s)
    for v in sorted(WEIGHT_NAMES):
        if lo <= v <= hi:
            ins = InstanceDescriptor()
            ins.familyName, ins.styleName = a.family, WEIGHT_NAMES[v]
            ins.postScriptFontName = f"{fam}-{WEIGHT_NAMES[v]}"
            # Enlace RIBBI: solo Regular y Bold comparten familia; sin esto el botón B da falsa negrita.
            if v in (400, 700):
                ins.styleMapFamilyName, ins.styleMapStyleName = a.family, WEIGHT_NAMES[v].lower()
            else:
                ins.styleMapFamilyName, ins.styleMapStyleName = f"{a.family} {WEIGHT_NAMES[v]}", "regular"
            ins.location = {"Weight": v}
            ins.filename = f"instances/{fam}-{WEIGHT_NAMES[v]}.ufo"
            ds.addInstance(ins)
    ds.write(src / f"{fam}.designspace")

    (src / "features.fea").write_text(
        "# Fuente única de features. build.py la copia a cada UFO: no edites las copias.\n"
        "# Sin languagesystem, kern y mark solo actúan en DFLT y las marcas no se colocan en latín.\n"
        "languagesystem DFLT dflt;\nlanguagesystem latn dflt;\n", encoding="utf-8")
    shutil.copy(ASSETS / "plantilla_brief.md", a.path / "BRIEF.md")
    shutil.copy(ASSETS / "ejemplo_reticula.py", a.path / "reticula.py")  # se rellena al aprobar la fase 1
    shutil.copy(ASSETS / "plantilla_procedencia.csv", a.path / "registro" / "procedencia_glifos.csv")
    shutil.copy(ASSETS / "shaping_base.json", a.path / "tests" / "shaping.json")
    (a.path / ".gitignore").write_text("fonts/\nproofs/\nweb/\nqa/\nsources/config.yaml\n__pycache__/\n*.pyc\ninstance_ufo/\nmaster_ufo/\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(a.path)], check=False)
    print(json.dumps({"proyecto": str(a.path), "designspace": str(src / f"{fam}.designspace"),
                      "masteres": master_vals, "typo": [a.typo_asc, a.typo_desc]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
