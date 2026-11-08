#!/usr/bin/env python3
"""Control de las fuentes (UFO + designspace) antes de compilar.

ERROR bloquea la compilación: incompatibilidad entre másteres, contornos abiertos,
unicodes duplicados, componentes rotos. AVISO requiere criterio: extremos sin nodo,
manejadores nulos, curvas fuera del triángulo mágico, quiebros (uniones casi
colineales) e inflexiones dentro de un segmento. Uso: check_sources.py X.designspace [--json]
"""
import json, math, sys
from collections import Counter
from pathlib import Path

import ufoLib2
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.pens.areaPen import AreaPen


def firma(g):
    cont = tuple(tuple(p.type or "off" for p in c) for c in g.contours)
    comp = tuple(c.baseGlyph for c in g.components)
    anc = tuple(sorted(a.name for a in g.anchors))
    return cont, comp, anc


def area(c, ufo):
    pen = AreaPen(ufo)
    c.draw(pen)
    return pen.value


def segmentos(c):
    """Devuelve las curvas (p0, c1, c2, p3) de un contorno cerrado."""
    pts = list(c.points)
    if not any(p.type for p in pts):
        return
    i0 = next(i for i, p in enumerate(pts) if p.type)
    pts = pts[i0:] + pts[:i0]
    pts.append(pts[0])
    i = 0
    while i < len(pts) - 1:
        if pts[i + 1].type:
            i += 1
            continue
        if i + 3 < len(pts):
            yield pts[i], pts[i + 1], pts[i + 2], pts[i + 3]
        i += 3


def curvatura_cruz(p0, c1, c2, p3, t):
    """Signo de la curvatura de la cúbica en t: el producto cruzado x'y''-y'x''."""
    mt = 1 - t
    d1x = 3 * (mt * mt * (c1.x - p0.x) + 2 * mt * t * (c2.x - c1.x) + t * t * (p3.x - c2.x))
    d1y = 3 * (mt * mt * (c1.y - p0.y) + 2 * mt * t * (c2.y - c1.y) + t * t * (p3.y - c2.y))
    d2x = 6 * (mt * (p0.x - 2 * c1.x + c2.x) + t * (c1.x - 2 * c2.x + p3.x))
    d2y = 6 * (mt * (p0.y - 2 * c1.y + c2.y) + t * (c1.y - 2 * c2.y + p3.y))
    return d1x * d2y - d1y * d2x


def revisar_quiebros(g, avisos):
    """Quiebro: unión casi colineal donde al menos un lado es curva. Una unión
    suave gira 0° y una esquina deliberada gira mucho; el territorio intermedio
    suele ser un manejador mal puesto. Manejadores muy cortos se saltan, porque
    el redondeo a la rejilla ya los desvía unos grados."""
    for c in g.contours:
        pts = list(c.points)
        m = len(pts)
        if m < 3 or pts[0].type == "move":
            continue
        for i, p in enumerate(pts):
            if not p.type:
                continue
            a, b = pts[(i - 1) % m], pts[(i + 1) % m]
            if a.type and b.type:  # línea-línea: es un polígono, no un quiebro
                continue
            v1, v2 = (p.x - a.x, p.y - a.y), (b.x - p.x, b.y - p.y)
            if math.hypot(*v1) < 3 or math.hypot(*v2) < 3:
                continue
            ang = abs(math.degrees(math.atan2(v1[0] * v2[1] - v1[1] * v2[0],
                                              v1[0] * v2[0] + v1[1] * v2[1])))
            if 1.5 < ang < 12:  # más de 12° se ve a simple vista en la prueba: es esquina
                avisos["AVISO"].append(f"{g.name}: quiebro de {ang:.1f}° en ({p.x},{p.y})")


def interseccion(p0, c1, c2, p3):
    d = (c1.x - p0.x) * (p3.y - c2.y) - (c1.y - p0.y) * (p3.x - c2.x)
    if abs(d) < 1e-9:
        return None
    t = ((c2.x - p0.x) * (p3.y - c2.y) - (c2.y - p0.y) * (p3.x - c2.x)) / d
    return p0.x + t * (c1.x - p0.x), p0.y + t * (c1.y - p0.y)


def revisar_glifo(g, ufo, avisos):
    n = g.name
    for ci, c in enumerate(g.contours):
        if c.points and c.points[0].type == "move":
            avisos["ERROR"].append(f"{n}: contorno {ci} abierto")
        for p0, c1, c2, p3 in segmentos(c):
            if (c1.x, c1.y) == (p0.x, p0.y) or (c2.x, c2.y) == (p3.x, p3.y):
                avisos["AVISO"].append(f"{n}: manejador nulo en ({p0.x},{p0.y})")
                continue
            # Extremo sin nodo: la tangente cambia de signo dentro de la curva.
            for eje in ("x", "y"):
                v = [getattr(q, eje) for q in (p0, c1, c2, p3)]
                ext = (max(v[1], v[2]) > max(v[0], v[3]) + 1) or (min(v[1], v[2]) < min(v[0], v[3]) - 1)
                if ext:
                    avisos["AVISO"].append(f"{n}: falta nodo en extremo {eje} cerca de ({p0.x},{p0.y})-({p3.x},{p3.y})")
            x = interseccion(p0, c1, c2, p3)
            if x:
                # Triángulo mágico: el manejador no debe pasar la intersección de tangentes.
                t1 = math.dist((c1.x, c1.y), (p0.x, p0.y)) / (math.dist(x, (p0.x, p0.y)) or 1)
                t2 = math.dist((c2.x, c2.y), (p3.x, p3.y)) / (math.dist(x, (p3.x, p3.y)) or 1)
                if max(t1, t2) > 1.0:
                    avisos["AVISO"].append(f"{n}: manejador fuera del triángulo en ({p0.x},{p0.y})")
            # Inflexión dentro del segmento (regla B4): la curvatura cambia de signo.
            # La ecuación de inflexión de una cúbica es cuadrática: 9 muestras bastan.
            vals = [curvatura_cruz(p0, c1, c2, p3, j / 8) for j in range(9)]
            tope = max(abs(v) for v in vals)
            signos = {v > 0 for v in vals if abs(v) > tope * 1e-3} if tope else set()
            if len(signos) == 2:
                avisos["AVISO"].append(f"{n}: inflexión dentro del segmento ({p0.x},{p0.y})-({p3.x},{p3.y})")
    revisar_quiebros(g, avisos)


def revisar(ds, fuentes=None):
    """fuentes: UFOs ya abiertos en el orden de ds.sources, para no reabrirlos."""
    res = {"ERROR": [], "AVISO": []}
    ufos = list(zip(ds.sources, fuentes)) if fuentes is not None else \
        [(s, ufoLib2.Font.open(s.path)) for s in ds.sources]
    base_s, base = ufos[0]
    nombres = set(base.keys())
    for s, u in ufos[1:]:
        for f in nombres ^ set(u.keys()):
            res["ERROR"].append(f"{f}: no existe en todos los másteres ({s.styleName})")
    for s, u in ufos:
        cnt = Counter(cp for g in u for cp in g.unicodes)
        for cp, k in cnt.items():
            if k > 1:
                res["ERROR"].append(f"U+{cp:04X} asignado a {k} glifos en {s.styleName}")
        for g in u:
            for c in g.components:
                if c.baseGlyph not in u:
                    res["ERROR"].append(f"{g.name}: componente {c.baseGlyph} inexistente")
    for nombre in sorted(nombres):
        fs = {}
        for s, u in ufos:
            if nombre in u:
                fs.setdefault(firma(u[nombre]), []).append(s.styleName)
        if len(fs) > 1:
            res["ERROR"].append(f"{nombre}: incompatible entre másteres {list(fs.values())}")
    for s, u in ufos:
        for g in u:
            revisar_glifo(g, u, res)
    i = base.info
    if ".notdef" not in base:
        res["ERROR"].append("falta .notdef")
    if "space" not in base:
        res["AVISO"].append("falta space")
    for s_, u in ufos[1:]:
        if dict(u.groups) != dict(base.groups):
            res["ERROR"].append(f"grupos de kerning distintos entre másteres ({s_.styleName})")
    tiene_kern = any(len(u.kerning) for _, u in ufos)
    con_anclas = any(a.name.startswith("_") for g in base for a in g.anchors)
    fea = base.features.text or ""
    ruta_fea = Path(base_s.path).parents[1] / "features.fea"
    if ruta_fea.exists():
        fea = ruta_fea.read_text(encoding="utf-8")
    if (tiene_kern or con_anclas) and "languagesystem" not in fea:  # HarfBuzz recurre a DFLT solo mientras no hay kern
        res["ERROR"].append("features.fea sin languagesystem: en cuanto haya kerning, mark no actuará en latín")
    # Letras sin ancla: una marca combinante caería a la derecha de la letra.
    tipos = {a.name[1:] for g in base for a in g.anchors if a.name.startswith("_")}
    for t in sorted(tipos):
        sin = [g.name for g in base if g.unicodes and any(chr(c).isalpha() and ord("A") <= c <= ord("z") for c in g.unicodes)
               and not any(a.name == t for a in g.anchors)]
        if sin:
            res["AVISO"].append(f"letras sin ancla {t}: {' '.join(sin[:30])}")
    for s_, u in ufos:
        if u.info.openTypeOS2WeightClass is None:
            res["AVISO"].append(f"máster {s_.styleName} sin openTypeOS2WeightClass: compilado directo daría 400")
    pesos = {i.styleName: i for i in ds.instances}
    if "Bold" in pesos and "Regular" in pesos and (pesos["Bold"].styleMapStyleName or "") != "bold":
        res["ERROR"].append("la instancia Bold no enlaza con Regular (stylemapstylename): el botón B daría falsa negrita")
    cats = base.lib.get("public.openTypeCategories")
    if con_anclas and cats and "base" not in cats.values():
        res["ERROR"].append("public.openTypeCategories sin bases: no se generará mark sobre base")
    for campo, txt in (("openTypeNameLicense", "licencia"), ("copyright", "copyright"), ("openTypeNameDesigner", "autoría")):
        if not getattr(i, campo):
            res["AVISO"].append(f"sin {txt} en la fuente: la persona debe decidirla antes de publicar")
    faltan = [k for k in ("xHeight", "capHeight", "ascender", "descender") if getattr(i, k) is None]
    if faltan:
        res["ERROR"].append(f"métricas sin definir: {faltan}")
    res["AVISO"] = sorted(set(res["AVISO"]))
    return res, len(ufos), len(nombres)


def informe(res, nu, ng, tope=60):
    print(f"check_sources: {nu} másteres, {ng} glifos, {len(res['ERROR'])} errores, {len(res['AVISO'])} avisos")
    for k in ("ERROR", "AVISO"):
        for m in res[k][:tope]:
            print(f"  {k}: {m}")
        if len(res[k]) > tope:
            print(f"  ... y {len(res[k]) - tope} más ({k})")


def main():
    ds = DesignSpaceDocument.fromfile(sys.argv[1])
    res, nu, ng = revisar(ds)
    if "--json" in sys.argv:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        informe(res, nu, ng)
    sys.exit(1 if res["ERROR"] else 0)


if __name__ == "__main__":
    main()
