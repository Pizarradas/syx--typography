#!/usr/bin/env python3
"""Compila un proyecto de forma reproducible y ejecuta las puertas automáticas.

  build.py PROYECTO              compila con gftools builder (fontmake) y verifica
  build.py PROYECTO --rapido     solo variable con fontmake, para iterar
  build.py PROYECTO --con-fontc  además compila con fontc como contraste
  build.py PROYECTO --qa         añade Font Bakery/fontspector (lento); informes en qa/
  build.py PROYECTO --solo-qa    pasa el QA sobre lo ya compilado, sin recompilar

Antes de compilar: copia sources/features.fea a cada máster y recalcula usWinAscent y
usWinDescent con la caja real de la familia (nunca por debajo de typo), para que ningún
máster difiera ni Windows recorte texto mientras la fuente esté incompleta.
Código de salida distinto de 0 si falla una puerta.
"""
import argparse, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

import ufoLib2
from fontTools.designspaceLib import DesignSpaceDocument

import check_sources
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import setMacOverlapFlags

BIN = Path(sys.executable).parent
HERE = Path(__file__).resolve().parent


def run(cmd, cwd=None, quiet=True):
    env = dict(os.environ, PATH=f"{BIN}:{Path.home()}/.local/bin:" + os.environ["PATH"])
    r = subprocess.run([str(c) for c in cmd], cwd=cwd, env=env, text=True, capture_output=quiet)
    return r


def preparar(proj, ds, ufos):
    fea = (proj / "sources" / "features.fea").read_text(encoding="utf-8")
    ymax, ymin = 0, 0
    for u in ufos:
        for g in u:
            pen = BoundsPen(u)
            g.draw(pen)
            if pen.bounds:
                ymin, ymax = min(ymin, pen.bounds[1]), max(ymax, pen.bounds[3])
    ymin, ymax = extremos_con_marcas(ufos, ymin, ymax)
    # usWin cubre la caja real de la familia, pero nunca menos que las métricas de línea
    # (typo): con una fuente aún incompleta (sin descendentes ni acentos) la caja real es
    # pequeña y Windows recorta las letras de RESPALDO que pone otra fuente en pantalla.
    i0 = ufos[0].info
    typo_a = i0.openTypeOS2TypoAscender or 0
    typo_d = abs(i0.openTypeOS2TypoDescender or 0)
    win_a, win_d = max(round(ymax), typo_a), max(round(abs(ymin)), typo_d)
    antes = (ufos[0].info.openTypeOS2WinAscent, ufos[0].info.openTypeOS2WinDescent)
    if antes != (win_a, win_d):
        print(f"AVISO: usWin cambia de {antes} a {(win_a, win_d)}: afecta al interlineado en programas sin USE_TYPO_METRICS")
    for u in ufos:
        i = u.info
        if u.features.text == fea and (i.openTypeOS2WinAscent, i.openTypeOS2WinDescent) == (win_a, win_d):
            continue  # nada que escribir: evita reescribir cientos de .glif por iteración
        u.features.text = fea
        i.openTypeOS2WinAscent, i.openTypeOS2WinDescent = win_a, win_d
        u.save(overwrite=True)
    return {"win": [win_a, win_d]}


def extremos_con_marcas(ufos, ymin, ymax):
    """Win debe cubrir marcas colocadas por GPOS, no solo glifos en reposo (un nivel de pila)."""
    for u in ufos:
        marcas, bases = {}, {}
        for g in u:
            for a in g.anchors:
                if a.name.startswith("_"):
                    pen = BoundsPen(u)
                    g.draw(pen)
                    if pen.bounds:
                        marcas.setdefault(a.name[1:], []).append((a.y, pen.bounds[1], pen.bounds[3]))
                else:
                    bases.setdefault(a.name, []).append(a.y)
        for nombre, lista in marcas.items():
            for y_b in bases.get(nombre, []):
                for y_a, y0, y1 in lista:
                    ymax, ymin = max(ymax, y_b - y_a + y1), min(ymin, y_b - y_a + y0)
    return ymin, ymax


def compilar(proj, ds_path, ds, rapido):
    src = proj / "sources"
    salida = proj / "fonts"
    if rapido:
        (salida / "variable").mkdir(parents=True, exist_ok=True)
        multi = len(ds.sources) > 1
        destino = salida / "variable"
        cmd = [BIN / "fontmake", "-m", ds_path.name, "-o", "variable", "--output-dir", destino] if multi else \
              [BIN / "fontmake", "-u", ds.sources[0].path, "-o", "ttf", "--output-dir", destino]
        r = run(cmd, cwd=src)
        # Mismo nombre que la compilación completa, para no duplicar pruebas ni rutas.
        for f in destino.glob("*-VF.ttf"):
            f.rename(destino / (f.stem[:-3] + "[" + ",".join(sorted(a.tag for a in ds.axes)) + "].ttf"))
        return r.returncode == 0, (r.stderr or r.stdout)[-1500:]
    family = ufoLib2.Font.open(ds.sources[0].path).info.familyName
    tags = [a.tag for a in ds.axes]
    # gftools valida con strictyaml: solo admite YAML de bloque, no JSON.
    variable = "true" if len(ds.sources) > 1 else "false"
    ejes = "".join(f"  - {t}\n" for t in tags)
    (src / "config.yaml").write_text(
        f"sources:\n  - {ds_path.name}\nfamilyName: {family}\naxisOrder:\n{ejes}outputDir: ../fonts\n"
        f"buildVariable: {variable}\nbuildStatic: true\nbuildTTF: true\nbuildOTF: true\n"
        f"buildWebfont: false\nbuildSmallCap: false\nautohintTTF: false\ncleanUp: true\n", encoding="utf-8")
    r = run([BIN / "gftools", "builder", "config.yaml"], cwd=src)
    for residuo in ("build.ninja", ".ninja_log", "instance_ufos"):
        p = src / residuo
        shutil.rmtree(p, ignore_errors=True) if p.is_dir() else p.unlink(missing_ok=True)
    return r.returncode == 0, (r.stdout + r.stderr)[-2500:]


def fuentes(proj):
    return sorted(p for p in (proj / "fonts").rglob("*") if p.suffix in (".ttf", ".otf"))


def marcar_overlap(proj):
    """Activa la marca OVERLAP en las variables: sus contornos conservan los solapes."""
    hechas = []
    for f in sorted((proj / "fonts" / "variable").glob("*.ttf")) if (proj / "fonts" / "variable").exists() else []:
        t = TTFont(f)
        setMacOverlapFlags(t["glyf"])
        t.save(f)
        hechas.append(f.name)
    return hechas


def puerta_ots(fonts):
    fallos = []
    for f in fonts:
        r = run([BIN / "python", "-m", "ots", f])
        if r.returncode != 0:
            fallos.append({"archivo": f.name, "error": (r.stderr or r.stdout)[-400:]})
    return fallos


def puerta_coherencia(fonts):
    """Comprueba en binario lo que la familia debe compartir."""
    fallos, vistos = [], {}
    for f in fonts:
        t = TTFont(f, lazy=True)
        os2, hhea = t["OS/2"], t["hhea"]
        fila = (os2.sTypoAscender, os2.sTypoDescender, os2.sTypoLineGap, hhea.ascent, hhea.descent,
                hhea.lineGap, os2.usWinAscent, os2.usWinDescent)
        vistos.setdefault(fila, []).append(f.name)
        if not os2.fsSelection & (1 << 7):
            fallos.append(f"{f.name}: USE_TYPO_METRICS apagado")
        if (hhea.ascent, hhea.descent, hhea.lineGap) != (os2.sTypoAscender, os2.sTypoDescender, os2.sTypoLineGap):
            fallos.append(f"{f.name}: hhea difiere de typo")
        if ".notdef" != t.getGlyphOrder()[0]:
            fallos.append(f"{f.name}: el glifo 0 no es .notdef")
        if f.stem.endswith("-Bold") and "fvar" not in t:
            n = t["name"]
            if not (os2.fsSelection & 32 and t["head"].macStyle & 1 and n.getDebugName(2) == "Bold"):
                fallos.append(f"{f.name}: sin enlace de negrita (fsSelection, macStyle o nameID 2)")
    regular = next((f for f in fonts if f.stem.endswith("-Regular") and f.suffix == ".ttf"), None)
    bold = next((f for f in fonts if f.stem.endswith("-Bold") and f.suffix == ".ttf"), None)
    if regular and bold:
        id1 = [TTFont(f, lazy=True)["name"].getDebugName(1) for f in (regular, bold)]
        if id1[0] != id1[1] or id1[0].endswith(" Regular"):
            fallos.append(f"Regular y Bold no comparten familia ID 1: {id1}")
    if len(vistos) > 1:
        fallos.append(f"métricas verticales distintas en la familia: {list(vistos)}")
    return fallos


def pasar_qa(proj):
    """Cada carpeta por separado: mezclar estáticas y variable da falsos FAIL de familia.
    Un informe vacío es un error: nunca debe leerse como aprobado."""
    salida, error = [], False
    (proj / "qa").mkdir(exist_ok=True)
    fs = shutil.which("fontspector") or (Path.home() / ".local/bin/fontspector")
    if Path(fs).exists():
        herr = "fontspector"
    elif (BIN / "fontbakery").exists():
        herr = "fontbakery"
    else:
        return [{"ERROR": "ni fontspector ni fontbakery instalados: ejecuta setup_env.sh --qa"}], True
    for carpeta in ("ttf", "variable"):
        rutas = sorted((proj / "fonts" / carpeta).glob("*.ttf"))
        if not rutas:
            continue
        rep = proj / "qa" / f"{herr}_{carpeta}.md"
        rep.unlink(missing_ok=True)
        cmd = [fs, "--profile", "universal", "--ghmarkdown", rep, *rutas] if herr == "fontspector" else \
              [BIN / "fontbakery", "check-universal", "--ghmarkdown", rep, *rutas]
        r = run(cmd)
        texto = rep.read_text(encoding="utf-8") if rep.exists() else ""
        if not texto.strip():
            salida.append({"carpeta": carpeta, "ERROR": "informe vacío: el QA no se ha evaluado", "detalle": (r.stderr or r.stdout)[-400:]})
            error = True
            continue
        motivos = sorted({l.split("</summary>")[0].split("<a ")[0].split("</b>")[-1].strip()
                          for l in texto.splitlines() if "<b>FAIL</b>" in l})
        salida.append({"herramienta": herr, "carpeta": carpeta, "informe": str(rep), "fail": motivos})
    return salida, error


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("proyecto", type=Path)
    p.add_argument("--rapido", action="store_true")
    p.add_argument("--con-fontc", action="store_true")
    p.add_argument("--qa", action="store_true")
    p.add_argument("--solo-qa", action="store_true")
    a = p.parse_args()
    proj = a.proyecto.resolve()
    ds_path = next((proj / "sources").glob("*.designspace"))
    ds = DesignSpaceDocument.fromfile(ds_path)
    if a.solo_qa:
        qa, err = pasar_qa(proj)
        print(json.dumps(qa, ensure_ascii=False, indent=2))
        sys.exit(1 if err else 0)

    # El control y la preparación comparten los UFOs cargados: una sola lectura por iteración.
    ufos = [ufoLib2.Font.open(s.path) for s in ds.sources]
    chk, nu, ng = check_sources.revisar(ds, ufos)
    check_sources.informe(chk, nu, ng)
    if chk["ERROR"]:
        sys.exit("Fuentes con errores bloqueantes: se detiene la compilación.")

    if not a.rapido and not (BIN / "gftools").exists():  # comprobar antes de borrar fonts/
        sys.exit("Falta gftools para la compilación completa: ejecuta setup_env.sh (o usa --rapido).")
    inf = preparar(proj, ds, ufos)
    shutil.rmtree(proj / "fonts", ignore_errors=True)  # sin restos: las puertas solo ven lo recién compilado
    ok, log = compilar(proj, ds_path, ds, a.rapido)
    res = {"compilacion": ok, **inf, "fonts": [str(f.relative_to(proj)) for f in fuentes(proj)]}
    if not ok:
        print(log)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        sys.exit("La compilación ha fallado.")

    fonts = fuentes(proj)
    res["overlap"] = marcar_overlap(proj)
    res["ots"] = puerta_ots(fonts)
    res["coherencia"] = puerta_coherencia(fonts)
    # La variable primero: las pruebas con "variaciones" no actúan sobre una estática.
    principal = next((f for f in fonts if f.parent.name == "variable"), fonts[-1])
    rs = run([BIN / "python", HERE / "shape_tests.py", principal, proj / "tests" / "shaping.json"])
    res["shaping"] = rs.stdout.strip().splitlines()[-1] if rs.stdout.strip() else rs.stderr[-300:]
    fallo = bool(res["ots"] or res["coherencia"] or rs.returncode)

    if a.con_fontc:
        with tempfile.TemporaryDirectory() as t:
            sal = Path(t) / "fontc.ttf"
            r = run([BIN / "fontc", ds_path.name, "-o", sal, "--build-dir", t], cwd=proj / "sources")
            res["fontc"] = "compila" if r.returncode == 0 and sal.exists() else (r.stderr or r.stdout)[-500:]
    if a.qa or a.solo_qa:
        res["qa"], fallo_qa = pasar_qa(proj)
        fallo = fallo or fallo_qa

    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(1 if fallo else 0)


if __name__ == "__main__":
    main()
