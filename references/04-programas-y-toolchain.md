# Programas y cadena de herramientas

Léelo al arrancar un proyecto, al elegir editor o si falla la compilación.
Precios y versiones: comprobados en noviembre de 2026; caducan rápido, revísalos antes de recomendar una compra.

## Qué programa usar

| Situación | Programa | Motivo |
|---|---|---|
| Agente en Linux/WSL, por código | Python con UFO + designspace, en git | Abierto, reproducible, verificado de principio a fin con esta skill |
| Persona en Windows, sin presupuesto | Fontra Pak (gratis, GPL-3.0) | Lee `.designspace` y `.ufo`; sigue «en desarrollo» |
| Persona en Windows, profesional | FontLab 9 (499 $ o 139 $ por 129 días; prueba de 10 días) | Salió el 2026-11-05: pruébalo antes de comprometerte |
| Persona en macOS, profesional | Glyphs 4 (319 €; Mini 2, 49 €) | Referencia en macOS. Mantén `.glyphs` formato 3 o exporta UFO |
| Fundición muy basada en Python, macOS | RoboFont 4.6 (precio sin verificar) | Trabaja sobre UFO |
| Tareas heredadas | FontForge | Gratis y multiplataforma; UI y flujo antiguos |
| Presupuesto bajo en Windows/macOS | FontCreator 16 (desde 49 $) | Flojo para flujos con agente |

Glyphs y RoboFont no corren de forma nativa en Windows. Runebender es una alfa sin instalador para Windows.

**Decisión por defecto para Windows 11 + WSL2:** fuente de verdad en UFO + designspace dentro del ext4 de WSL, compilación con esta skill y revisión humana en Fontra o FontLab.

## Dónde guardar los archivos

Trabaja en el sistema de archivos de WSL (`~/...`), nunca en `/mnt/c`: Microsoft desaconseja cruzar sistemas, e inotify no entrega bajo `/mnt/c` los cambios hechos por programas de Windows. Desde Windows, abre los archivos por `\\wsl$\<distro>\home\...`.

## Cadena verificada

Comprobado el 2026-11-07 con un proyecto de 3 másteres `wght`, en `~/.local/share/type-design/venv`:

| Herramienta | Versión | Papel | Resultado |
|---|---|---|---|
| fontTools | 4.68.0 | subset, instancer, feaLib | Funciona |
| ufoLib2 | 0.19.1 | Lectura y escritura de UFO | Funciona |
| fontmake | 3.12.2 | Compilador de publicación | Funciona |
| gftools builder | 0.9.996 | Orquesta variable, TTF, OTF, STAT | Funciona |
| fontc | 1.0.0 | Compilador de contraste | Compila; no es la vía de publicación |
| Font Bakery | 1.1.0 | QA | Funciona |
| fontspector | 1.9.0 | QA más rápido | Opcional: ver abajo |
| OTS (`python -m ots`) | opentype-sanitizer | Filtro de navegadores | Funciona |
| uharfbuzz + Pillow con Raqm | 0.57.0 | Conformación y pruebas PNG | Funciona |
| Hyperglot | PyPI | Cobertura por idioma | Funciona |

### Trampas comprobadas

- `gftools builder` copia los UFO a `instance_ufos/`, así que `include(../features.fea)` falla al compilar estáticas. Por eso `build.py` copia `sources/features.fea` a cada máster. Edita solo el archivo compartido.
- `config.yaml` debe ser YAML de bloque: strictyaml rechaza JSON.
- `build.py` nombra el variable `Familia[wght].ttf` en las dos vías. Si compilas con fontmake a mano saldrá `Familia-VF.ttf`.
- Font Bakery sobre estáticas y variable a la vez da FAIL falsos de familia; `build.py --qa` pasa cada carpeta por separado y guarda los informes en `qa/`, porque `fonts/` se borra en cada compilación.
- En un ensayo, `fontbakery --ghmarkdown` se cayó con `UnboundLocalError` y dejó el informe vacío; no se reprodujo después. `build.py` trata un informe vacío como error, no como aprobado.
- Con másteres incompatibles, `fontmake -i` puede compilar y deformar las instancias intermedias sin error: la variable falla, las estáticas no. Ejecuta siempre `check_sources.py`.
- Sin navegador: Chromium y Playwright pueden no arrancar aquí (falta `libnspr4.so`, y el servidor MCP no conecta). Declara que el CSS no se ha probado en navegador si es el caso.
- `usWinAscent/Descent` deben ser la caja real: valores mayores que typo sin motivo dan FAIL.
- `.glyphs` formato 4 no se abre con glyphsLib (`TypeError`), y su mantenedor dijo el 2026-09-30 que no prevé soportarlo ahí. Si el origen es Glyphs 4, exporta UFO o conserva formato 3.

### Instalación de QA opcional

`fontspector` es un binario externo: instálalo solo si la persona lo pide (`cargo binstall fontspector` o desde sus publicaciones en GitHub). `build.py --qa` lo usa si existe y si no, Font Bakery. Las banderas de `fontspector` no se han comprobado en esta skill: revísalas con `--help`.

Interpreta el QA con criterio: Font Bakery marca FAIL en una fuente incompleta (p. ej., sin NBSP o sin pares de caja). Un paso limpio prueba conformidad, no calidad de diseño.

## Sin verificar

- Fontra servido desde WSL y abierto en el navegador de Windows: la combinación no está documentada ni se ha probado. El paquete de PyPI está obsoleto (0.5.2, 2024); Fontra Pak es la vía fácil en Windows.
- FontLab 9 con UFO y designspace: su [página de producto](https://www.fontlab.com/font-editor/fontlab/) lista UFO 2 y 3 y designSpace, pero la documentación disponible es de versiones anteriores. Allí UFO es formato de intercambio: guardar es exportar y [puede perder datos](https://help.fontlab.com/fontlab-vi/Files/) (esquinas inteligentes, nodos genius, notas). El formato nativo es VFC/VFJ. No se ha probado el viaje de ida y vuelta: compruébalo con un glifo antes de confiar en él.
- MCP de FontLab 9 (puerto, transporte, acceso desde WSL): trátalo como mejora opcional. Requiere la aplicación abierta y no sustituye a la compilación reproducible.

## Formato de intercambio con un editor

1. La persona abre el `.designspace` o los `.ufo`.
2. Edita, guarda en el mismo sitio y confirma en git.
3. El agente ejecuta `check_sources.py`, que detecta incompatibilidades entre másteres al instante.
4. Si el editor cambia la estructura (orden de puntos, nodos añadidos), repara la compatibilidad antes de continuar.

Si un generador por código produce un glifo que la persona ha retocado a mano, márcalo en el generador como congelado: la siguiente generación no debe sobrescribir trabajo humano. Protege esa lista antes de volver a generar y revisa `git diff` tras cada ejecución.
