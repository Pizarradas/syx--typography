# 07 · Preparar y entregar una fuente propia para la web

Lee esto cuando vayas a exportar una fuente a WOFF2, escribir su `@font-face`, integrarla en un sitio o framework, o revisar por qué pierde features, tarda o desplaza el texto.

**Marcas.** `[verificado 2026-11-07 con fonttools 4.68.0]`: ejecutado aquí con brotli 1.2.1 sobre fuentes de prueba diminutas (comprueba comandos y conducta, no tamaños). `[fuente: X]`: dicho por X, no ejecutado. `[convención]`: práctica habitual sin norma. `[inferencia]`: deducción propia.
**Caducidad.** Los datos de navegadores son de caniuse (uso de octubre de 2026), MDN BCD v8.1.8 (2026-11-02) y web-features, leídos el 2026-11-07. Revísalos antes de citarlos. Almanac es la edición 2025, la última disponible. No hubo navegador para probar: el Chromium headless local no arranca (falta `libnspr4`), de modo que todo lo «de navegador» es fuente, no ensayo.

## Contenido
1 Formatos · 2 Orden · 3 `web_export.py` · 4 Subsetting · 5 Rangos Unicode, U+0301 y NFD · 6 `varLib.instancer` · 7 Variable o estática
8 `@font-face` · 9 Carga · 10 CLS y LCP · 11 `size-adjust` y overrides · 12 `font-variant-*` · 13 Cabeceras HTTP · 14 IFT · 15 COLR
16 Frameworks · 17 Accesibilidad · 18 Presupuestos · 19 Medición · 20 Consejos obsoletos · 21 Checklist final

## 1. Decisión de formatos
- Sirve solo WOFF2: 97,4 % de soporte global, Chrome 36+, Edge 14+, Firefox 39+, Safari 12+ (10–11.1 parcial) [fuente: https://caniuse.com/woff2]. Es Recomendación W3C desde el 8 de agosto de 2024, con tipo `font/woff2` [fuente: https://www.w3.org/TR/WOFF2/].
- No generes `.woff`, `.eot` ni SVG, porque solo sirven a navegadores heredados [fuente: https://web.dev/learn/performance/optimize-web-fonts]. OTF y TTF de escritorio son otro entregable.
- No sirvas colecciones WOFF2 [inferencia]: la especificación admite colecciones, pero dice que ningún agente de usuario las aprovecha aún tras decodificar [fuente: W3C WOFF2].
- No repitas cifras de ahorro como hechos: web.dev dice «hasta 30 %» y el blog W3C de 2026 «hasta 40 %». Dependen de la fuente. Las herramientas confirman el contenedor: `--flavor=woff2` escribe un archivo con firma `wOF2` [verificado 2026-11-07 con fonttools 4.68.0].

## 2. Orden: instanciar, recortar, comprimir
Sigue siempre este orden [fuente: notas de investigación; orden no contradicho]:

1. **Instanciar** con `varLib.instancer`: quitar ejes antes evita arrastrar sus deltas al recorte [inferencia].
2. **Recortar** con `pyftsubset`. Decide glifos, features y nombres.
3. **Comprimir** en el mismo paso con `--flavor=woff2`.
4. **Comprobar**: etiquetas GSUB/GPOS antes y después, conformación y CSS.

Sobre una fuente sin `fvar`, `instancer` falla con `Missing required table fvar` [verificado 2026-11-07 con fonttools 4.68.0]. Parte siempre del TTF variable completo.

## 3. Exportar con `web_export.py`
Es la vía por defecto: encadena instanciación, recorte, WOFF2, comparación de etiquetas y CSS.
```bash
$PY scripts/web_export.py \
  MiTipo-VF.ttf -o web/ --slug mitipo --limitar wght=300:800 --rango latin --version 1
```

Admite varias fuentes estáticas en un mismo CSS. Opciones reales: `-o`, `--slug`, `--limitar` (repetible), `--rango completo|latin|latin-ext|ambos` (por defecto `completo`, un solo WOFF2 con todo el `cmap`), `--ruta-css`, `--hinting`, `--respaldo arial|times`, `--familia-css`, `--version`. Conserva todas las features con `--layout-features=*`, y añade los IDs de nombre 13 y 14. Devuelve JSON con tamaño y features por archivo, `features_ausentes` y `caracteres_excluidos` para el conjunto [verificado 2026-11-07 con fonttools 4.68.0].

Conducta que debes conocer:
- Con `completo` y `ambos`, sale con código 1 si se pierde cualquier carácter o feature. Esto importa: en un ensayo los rangos dejaban fuera ≠ ≈ ≤ ≥, que no pertenecen a `latin` ni a `latin-ext`. Con `latin` o `latin-ext` solo avisa, porque el recorte es deliberado: lee `caracteres_excluidos`.
- Trocear separa U+0307 y U+0327 de sus bases. Para una fuente latina de tamaño medio, usa `completo`.
- Tras exportar, ejecuta `shape_tests.py TTF tests/shaping.json --comparar X.woff2`, que compara avances y desplazamientos, porque los WOFF2 pierden nombres de glifo. Con `--limitar`, las pruebas fuera del rango difieren con razón.
- Con `ambos`, emite `latin` al final, porque la última regla gana en los solapes U+0131, U+0152-0153 y U+2020 [fuente: CSS Fonts 4 §4.5].
- Emite `font-stretch` si queda el eje `wdth`, `oblique` si queda `slnt` e `italic` si la fuente es cursiva.
- `--limitar` en una fuente estática se ignora con un aviso. Pasar el presupuesto da aviso, no error.
- El respaldo ajustado se calcula con la anchura media ponderada medida en `hmtx`, usando una tabla de frecuencias aproximada propia, no la de Chrome. Si faltan letras básicas no se emite. Es una estimación: mide el CLS. Fontpie y Fontaine no se han ejecutado aquí.
- `LATIN_EXT` del script parte del rango de Google, corta en U+20C0 y añade marcas combinantes; `LATIN` añade U+25CC. Son decisiones propias.

## 4. Subsetting y sus trampas
Comando base. Sustituye la lista por las features que tu fuente promete:
```bash
LATIN="U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0300-0304,U+0308,U+0323,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+25CC,U+FEFF,U+FFFD"
pyftsubset MiTipo-wght.ttf --unicodes="$LATIN" \
  --layout-features+=tnum,lnum,onum,pnum,case,ordn,sups,subs,smcp,c2sc,ss01 \
  --no-hinting --notdef-outline --name-IDs+=13,14 \
  --flavor=woff2 --output-file=mitipo-latin-wght-v1.woff2
```

La forma `U+…` separada por comas es válida, igual que `--unicodes-file=rangos.txt`, con comentarios tras `#` [verificado 2026-11-07 con fonttools 4.68.0].

**Features: el recorte falla en silencio.** Sin opciones, `tnum` y `ss01` desaparecieron de GSUB, y HarfBuzz 15.0.0 dejó el `01` con avance 600 en lugar del tabular 620 aun pidiendo `tnum`, sin error ni aviso [verificado 2026-11-07 con fonttools 4.68.0].

| Forma | Qué conserva | Resultado medido |
|---|---|---|
| sin opción | lista por defecto | se pierden `tnum`, `ordn`, `ss01` |
| `--layout-features+=tnum,ordn,ss01` | defecto más esas | conserva todo lo pedido, más `kern`, `mark`, `ccmp`, `liga` |
| `--layout-features='*'` | todas | conserva todo; arrastra los glifos alternativos (23 → 27) |
| `--layout-features=tnum,ss01` | **solo** esas | **pierde `kern`, `mark`, `ccmp`, `liga`**; `ab` pasa de avance 560 a 600 |

Todo [verificado 2026-11-07 con fonttools 4.68.0]. Usa siempre `+=` o `'*'`, salvo que quieras sustituir. El `=` es el error más barato de cometer y el más caro de notar.
- `'*'` afecta solo a las features: **no conserva los name-IDs 13 y 14** [verificado 2026-11-07 con fonttools 4.68.0]. Son dos decisiones separadas.
- La lista por defecto de 4.68.0 tiene 68 etiquetas, no 15: las latinas son `calt ccmp clig curs dnom frac kern liga locl mark mkmk numr rclt rlig rvrn`, y el resto cubre vertical, RTL y escrituras complejas, además de `rand` y `jalt` [verificado 2026-11-07 con fonttools 4.68.0]. Consúltala con `pyftsubset MiTipo.ttf --unicodes=61 '--layout-features=?' --output-file=/dev/null`.
- Fuera quedan `tnum lnum onum pnum case ordn sups subs smcp c2sc zero salt ssNN cvNN aalt dlig hist swsh titl` [verificado 2026-11-07 con fonttools 4.68.0]. `ordn` importa en español por 1.º y 2.ª [inferencia].
- Una feature puede desaparecer con razón: si sus glifos no están en el rango, se poda. `ss02` sobre `ł` no sobrevive en el recorte `latin` [verificado 2026-11-07 con fonttools 4.68.0]. Al comparar antes y después, justifica cada pérdida en lugar de exigir igualdad.
- `--no-layout-closure` con `'*'` dejó GSUB vacío porque no entraron los alternativos [verificado 2026-11-07 con fonttools 4.68.0]. No lo uses salvo que sepas qué pierdes.

**Name-IDs.** Por defecto solo se conservan 0–6: 13 y 14 se fueron sin el flag y se quedaron con `--name-IDs+=13,14` o `--name-IDs='*'` [verificado 2026-11-07 con fonttools 4.68.0]. Los IDs que usan tablas conservadas (`ss01` con nombre, `fvar`, `STAT`) sobreviven sin pedirlos: el ID 256 de `ss01` y los 256–259 de STAT siguieron presentes. Por defecto solo quedan registros en inglés (`--name-languages` = 1033), de modo que un nombre en español se pierde [verificado 2026-11-07 con fonttools 4.68.0].

**Licencia.** Conserva 13 y 14 para que el webfont se identifique. Bajo OFL, recortar normalmente impide usar un Nombre Reservado; evita RFN o concede permiso expreso [fuente: https://openfontlicense.org/ofl-faq/]. Escribe en tu licencia que autorizas self-hosting, recorte y conversión a WOFF2 [inferencia].

**Hinting.** `--no-hinting` quitó `cvt `, `fpgm`, `prep` y las instrucciones de glifo; `gasp` **se conserva** [verificado 2026-11-07 con fonttools 4.68.0]. Lista completa: `cvt cvar fpgm prep hdmx VDMX`. El ahorro «a veces de hasta 30 %» es de la ayuda de fontTools, no medido aquí.
- En variables, no hintes [fuente: https://googlefonts.github.io/gf-guide/hinting.html]; usa `--no-hinting` si el origen trae hints.
- En estáticas de texto para Windows, no quites el hinting a ciegas: la ayuda dice «extremely high-resolution systems» y Google sigue pidiendo hintar estáticas [fuente: https://googlefonts.github.io/gf-guide/statics.html]. Usa `--hinting` en `web_export.py`, que por defecto lo elimina.
- Si publicas sin hinting, revisa tú el `gasp`, porque el recorte no lo toca [inferencia]. Google pide 0x000A en estáticas sin hinting.

**`.notdef`.** Por defecto se vacía su contorno (de 2 contornos a 0); `--notdef-outline` lo mantiene [verificado 2026-11-07 con fonttools 4.68.0]. Consérvalo: cuesta pocos bytes (40 en la prueba) y el glifo 0 debe ser visible [fuente: https://learn.microsoft.com/en-us/typography/opentype/spec/recom]. La ayuda de fontTools dice que no suele hacer falta en un subset web: es un desacuerdo menor, y optamos por el diagnóstico visible [inferencia].

**Otros valores por defecto** [verificado 2026-11-07 con fonttools 4.68.0]:
- `--no-glyph-names`: `post` 3.0, y los alternativos pasan a llamarse `glyphNNNNN`. Compara etiquetas y conformación, no nombres de glifo.
- `--drop-tables`: `JSTF DSIG EBDT EBLC EBSC PCLT LTSH Feat Glat Gloc Silf Sill`. `--layout-scripts`: `*`. Las tablas desconocidas se eliminan salvo `--passthrough-tables`.
- `--recalc-average-width` apagado: `xAvgCharWidth` no refleja el subset.
- `--ignore-missing-unicodes` activo: **pedir un carácter que la fuente no tiene no da error**. Comprueba cobertura aparte con `scripts/coverage.py`.
- `fvar`, `gvar`, `HVAR` y `STAT` sobreviven al recorte de una variable.

**CFF.** En estáticas `.otf` prueba `--desubroutinize` y quédate con el menor: la ayuda solo dice que «se ha informado» de mejor compresión [fuente: fontTools]. El flag funciona [verificado 2026-11-07 con fonttools 4.68.0]. `--with-zopfli` solo afecta a WOFF 1.0: no lo uses.

**glyphhanger.** Sirve para un sitio concreto, porque recorta por lo que encuentra en las páginas. No lo uses en una fuente que se distribuye: necesitas rangos estables y documentados [inferencia; fuente: https://raw.githubusercontent.com/zachleat/glyphhanger/master/README.md]. No se ejecutó.

**Comprueba tras cada recorte:**
```bash
fonttools ttx -l mitipo-latin-wght-v1.woff2
python -c "import sys; from fontTools.ttLib import TTFont as T; f=T(sys.argv[1]); print(sorted({r.FeatureTag for t in ('GSUB','GPOS') if t in f for r in f[t].table.FeatureList.FeatureRecord}), sorted({n.nameID for n in f['name'].names}))" mitipo-latin-wght-v1.woff2
```

## 5. Rangos Unicode para español y latín; U+0301 y NFD
Usa un archivo `latin` y, si procede, otro `latin-ext`. No trocees más ni crees un `es`: Latin-1 son unos 190 caracteres y ahorrarías poco [inferencia]. El troceado rompe reglas entre glifos de archivos distintos [fuente: https://www.w3.org/TR/PFE-evaluation] y `preload` ignora `unicode-range` [fuente: https://web.dev/articles/font-best-practices].

Rangos de Google leídos el 2026-11-07 (cambian y dependen del agente de usuario) [fuente: https://fonts.googleapis.com/css2?family=Inter:wght@400&display=swap]:
- `latin`: `U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD`
- `latin-ext`: `U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF`

Rango propio: el `latin` anterior más `U+0300-0303`, `U+0323` y `U+25CC`, como en `$LATIN` (§ 4). El círculo punteado acompaña a las marcas [fuente: informe, § cobertura].

Cobertura comprobada contra `$LATIN`: todo `á é í ó ú ü ñ Á É Í Ó Ú Ü Ñ ¡ ¿ ª º « » — – ‘ ’ “ ” … €` está dentro, igual que U+0303 y U+02BC. **`ŀ` U+0140 no está**: cae en `latin-ext`, y con él U+A78B [verificado 2026-11-07 con fonttools 4.68.0, cálculo sobre los rangos]. Si el catalán o las lenguas con saltillo importan, usa un solo archivo que una ambos rangos:
```bash
LATIN_EXT="U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C4,U+2113,U+2C60-2C7F,U+A720-A7FF"
pyftsubset MiTipo-wght.ttf --unicodes="$LATIN,$LATIN_EXT" --layout-features='*' \
  --no-hinting --notdef-outline --name-IDs+=13,14 --flavor=woff2 --output-file=mitipo-todo-v1.woff2
```

Un archivo único conserva también el kerning entre ambos grupos, que se pierde entre trozos [inferencia], y encaja mejor con `next/font/local` (§ 16).

**U+0301 y NFD.** U+0301 no está en `latin` ni en `latin-ext` de Google, solo en `vietnamese` y `cyrillic` [fuente: respuesta CSS2 citada]. Por eso el rango propio lo incluye. Ten presente lo que se midió con un subset que tenía `ó` pero no U+0301 (rango de Google), HarfBuzz 15.0.0 [verificado 2026-11-07 con fonttools 4.68.0]:

| Entrada | Rango de Google | Rango con U+0300-0304 |
|---|---|---|
| `ó` precompuesta | `oacute` | `oacute` |
| `o` + U+0301 | `oacute`: HarfBuzz compone | `oacute` |
| `b` + U+0301 (sin precompuesta) | `b` + **`.notdef`** | `b` + `acutecomb` |
| reglas `mark` y `ccmp` de U+0301 | **eliminadas** | conservadas |

Consecuencias:
- El NFD español común no se rompe por sí solo en el conformador si la fuente recibe la secuencia, porque existen las precompuestas. El riesgo real es doble: la descarga de otro trozo o una marca tomada de otro archivo, según el navegador (no probado), y las secuencias **sin precompuesta**, como `g̃` guaraní con U+0303, donde el rango de Google deja la marca fuera.
- Normaliza el contenido a NFC; los nombres de archivo pegados desde macOS son un caso de NFD [fuente: notas]. Incluye marcas con `mark`, `mkmk` y `ccmp`, y prueba siempre con entrada NFD.
- U+02BC, letra en quechua y aimara, está en `latin` y es distinta de U+2019 [fuente: informe].

## 6. Limitar ejes con `varLib.instancer`
```bash
fonttools varLib.instancer MiTipo-VF.ttf wght=300:800 wdth=drop -o MiTipo-wght.ttf
fonttools varLib.instancer MiTipo-VF.ttf wght=500 wdth=100 --static -o MiTipo-Medium.ttf
```

Conducta comprobada [verificado 2026-11-07 con fonttools 4.68.0]:

| Orden | Resultado |
|---|---|
| `wdth=drop` **sin eje `wdth`** | **falla**: `KeyError: 'wdth'`, código 1, sin salida. Igual con `wdth=100` y cualquier etiqueta ausente |
| `wdth=drop` con eje | fija `wdth` en su valor por defecto y elimina el eje |
| `wght=300:800` en fuente 300–700 | recorta en silencio a 300–700: no avisa ni extrapola |
| `wght=350:600` | `fvar` 350/400/600 |
| `wght=500:700` con defecto 400 | **mueve el defecto a 500** y fija `usWeightClass` = 500 |
| `wght=300:500:700` | mueve el defecto a 500 explícitamente |
| `wght=500 --static` | estática con `usWeightClass` 500, pero el nombre sigue `Regular` |
| `--update-name-table` | exige `STAT` **con Axis Value Tables**: falla con `no STAT Axis Values` si la tabla está vacía, como en las fuentes de prueba de `build.py` |

Por tanto:
- **Lista los ejes antes de escribir el comando**, porque copiar un `wdth=drop` genérico rompe en una fuente solo `wght`. El ejemplo publicado en las notas y el informe solo vale con eje `wdth`.
```bash
python -c "import sys; from fontTools.ttLib import TTFont as T; print([(a.axisTag,a.minValue,a.defaultValue,a.maxValue) for a in T(sys.argv[1])['fvar'].axes])" MiTipo-VF.ttf
```

- No mezcles rangos que excluyan el defecto sin revisar el resultado: el default movido cambia lo que ve un entorno sin variación [inferencia].
- Si generas estáticas sin `STAT` poblado, corrige los nombres aparte. Después de limitar, declara en `@font-face` el rango real de `fvar`, no el que pediste.
- Omitir un eje lo deja intacto; `--remove-overlaps` requiere skia-pathops [fuente: https://fonttools.readthedocs.io/en/latest/varLib/instancer.html].

## 7. Variable frente a estática
- Mide los WOFF2 que el diseño usa de verdad. **No hay umbral fiable**: «unos tres estilos» viene de una fuente de baja calidad, sin medidas [fuente: https://madegooddesigns.com/static-vs-variable-fonts/].
- El 88 % de Monotype (12 archivos a uno con 48 estilos) es orientativo y de la época de 2020 [fuente: https://web.dev/articles/variable-fonts]. Un solo Regular puede no reducirse frente a una variable multieje.
- Con uno o dos estilos, prefiere estáticas; con varios, compara. Separa redonda y cursiva en dos variables, para que una página sin cursiva no pague por ella [inferencia].
- Entrega tres cosas [inferencia]: variable completa para licenciatarios, variable web limitada (`wght` y quizá un tramo de `opsz`) y Regular y Bold estáticas.
- Prefiere propiedades de alto nivel: `font-weight`, `font-stretch`, `font-style`, `font-optical-sizing`. `font-variation-settings` es de bajo nivel, sensible a mayúsculas, obliga a redeclarar todos los valores y no respeta los rangos de `@font-face` [fuente: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fonts/Variable_fonts]. Resérvalo para ejes propios como `GRAD`.
- Cuidado con el signo: `font-style: oblique 14deg` equivale a `"slnt" -14` [fuente: MDN].

## 8. `@font-face` completo
```css
/* latin-ext antes: la última regla se comprueba primero */
@font-face {
  font-family: "MiTipo";
  src: url("/fonts/mitipo-latin-ext-v1.woff2") format("woff2");
  font-weight: 300 800; font-stretch: 100%; font-style: normal; font-display: swap;
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+1D00-1DBF,
    U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
@font-face {
  font-family: "MiTipo";
  src: url("/fonts/mitipo-latin-v1.woff2") format("woff2");
  font-weight: 300 800; font-stretch: 100%; font-style: normal; font-display: swap;
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC,
    U+0300-0304, U+0308, U+0323, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193,
    U+2212, U+2215, U+25CC, U+FEFF, U+FFFD;
}
```

- Usa `format("woff2")` también en variables. **Hay desacuerdo**: la guía de variables de MDN llama correcta a `woff2-variations`, su página de `src` la trata como heredada y web.dev la da por obsoleta, con `tech('variations')` entre comillas que no encaja con la gramática de MDN. Tailwind usa `format("woff2")`. La forma simple funciona y evita el descarte de `src` entero en Safari [inferencia].
- Declara `font-weight` como rango en variables, y `font-stretch` solo si conservas `wdth`, con sus valores reales. No uses `font-width`: el descriptor solo existe en Safari 18.4+ [fuente: BCD 8.1.8]. Con eje de inclinación usa `font-style: oblique 0deg 12deg`.
- El mapa efectivo es la intersección de `unicode-range` con el `cmap` [fuente: CSS Fonts 4 §4.5]. `latin` va al final para que gane en los solapes U+0131, U+0152-0153 y U+2020.
- Añade `font-synthesis: none` en el elemento si la familia carece de un estilo, para que no se publique una falsa negrita sin que nadie lo note [inferencia].

## 9. Carga: self-host, preload, `font-display`, fallback
**Self-host.** Aloja en tu origen. La caché compartida entre sitios ya no existe: Safari la desactivó, y Chrome 86 y Firefox 85 la particionaron [fuente: https://csswizardry.com/2019/05/self-host-your-static-assets/]. Web.dev dice que es más rápido «en la mayoría de los casos» con CDN y HTTP/2 o 3, y en otro artículo pide probar antes de cambiar. Las cifras de coste de conexión de ese texto son de 2019 y no de fuentes: úsalas como orden de magnitud.

**Inserción en `<head>`:**
```html
<link rel="preload" href="/fonts/mitipo-latin-v1.woff2" as="font" type="font/woff2" crossorigin>
<style>/* @font-face en línea */</style>
```

- `crossorigin` es obligatorio aunque sea tu mismo origen: las fuentes usan CORS anónimo, y sin él el recurso no se reutiliza [fuente: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel/preload].
- Precarga uno, dos como máximo: el abuso quita ancho de banda a lo crítico [fuente: web.dev]. No precargues trozos que quizá no se usen, porque `preload` ignora `unicode-range`.
- En línea, pon el `@font-face`, nunca la fuente en base64; solo ayuda si el resto del CSS bloqueante también va en línea [fuente: https://web.dev/learn/performance/optimize-web-fonts]. Con terceros, `preconnect` a `fonts.googleapis.com` y a `fonts.gstatic.com` con `crossorigin`.

**`font-display`:**

| Valor | Bloqueo | Intercambio | Usa para |
|---|---|---|---|
| `swap` | ≤ 100 ms (web.dev dice 0: desacuerdo) | infinito | marca y titulares, con fallback ajustado |
| `optional` | solo si está lista para el primer pintado | ninguno | texto de cuerpo donde prima la estabilidad, con preload |
| `fallback` | muy breve | unos 3 s | término medio |
| `block` | unos 3 s | infinito | evítalo en texto |

Periodos de CSS Fonts 4; web.dev recomienda combinar `swap` para marca y `optional` para cuerpo. `optional` con preload es «la forma más eficaz de garantizar que no haya saltos» desde Chrome 83 [fuente: https://web.dev/articles/preload-optional-fonts]. El reloj por defecto de Safari está sin resolver: web.dev dice que bloquea hasta cargar, y Filament Group vio hasta 30 s en iOS.

**Fallback ajustado.** `swap` sin ajuste cambia texto invisible por desplazamiento [inferencia]. Genera las cifras con una herramienta y no las copies a mano:
```css
@font-face { /* forma del bloque, no sus números */
  font-family: "MiTipo Fallback"; src: local("Arial");
  size-adjust: 104.2%; ascent-override: 92%; descent-override: 24%; line-gap-override: 0%;
}
body { font-family: "MiTipo", "MiTipo Fallback", Arial, sans-serif; }
```

- Fórmula: `size-adjust = avgCharWidth(web)/avgCharWidth(respaldo)`, con media **ponderada por frecuencia de letras** de `[a-z\s]`, y `ascent-override = ascent/(UPM × size-adjust)`; `descent` y `line-gap` igual [fuente: https://developer.chrome.com/blog/font-fallbacks].
- **`xAvgCharWidth` no sirve de atajo.** Con una tabla de frecuencias ilustrativa, no la de Chrome, medida en archivos locales: Arial 0,4414 de `xAvgCharWidth` frente a 0,4402 ponderado, pero Segoe UI 0,5386 frente a 0,4416, un 22 % de más, [verificado 2026-11-07 con fonttools 4.68.0]. La causa probable es que depende del juego de glifos [inferencia]. Calcula sobre `hmtx`.
- Herramientas: `npx fontpie ./mitipo.woff2 --name MiTipo` [fuente: https://raw.githubusercontent.com/pixel-point/fontpie/main/README.md]; Fontaine, `FontaineTransform.vite({ fallbacks, resolvePath })`, con CLS de 0,24 a 0,054 en su demo [fuente: https://raw.githubusercontent.com/unjs/fontaine/main/packages/fontaine/README.md]. Ninguna se ejecutó aquí.
- Declara Arial para Windows y Mac, y Roboto para Android, como caras separadas [fuente: Chrome]. Publica los valores para Arial, Times New Roman y Roboto en el paquete de entrega [inferencia].

## 10. CLS y LCP
- Umbrales al percentil 75: LCP bueno ≤ 2,5 s, malo > 4 s; CLS bueno ≤ 0,1, malo > 0,25 [fuente: https://web.dev/articles/lcp, https://web.dev/articles/cls].
- El texto en periodo de bloqueo no se pinta y no puede ser candidato a LCP; un pintado mayor posterior emite una entrada nueva [fuente: web.dev LCP]. Por eso una cara lenta con `block` retrasa el LCP.
- Una fuente que se pinta mayor o menor que su respaldo es causa nombrada de CLS [fuente: web.dev CLS]. Corrígelo con § 9 y con métricas internas sanas: iguala `hhea`, typo y win y activa USE_TYPO_METRICS [inferencia], porque Safari en Mac usa `hhea` y Windows typo o win [fuente: Chrome].
- Mantén exactos `sCapHeight` y `sxHeight`: `text-box`, `font-size-adjust: from-font` y Capsize dependen de ellos [inferencia].

## 11. `size-adjust` y overrides: soporte
Datos de BCD 8.1.8, 2026-11-02; **caducan**.

| Función | Chrome/Edge | Firefox | Safari |
|---|---|---|---|
| `ascent-`, `descent-`, `line-gap-override` | 87 | 89 | solo preview; sin estable, ni iOS |
| `size-adjust` | 92 | 92 | 17 |
| `font-size-adjust` (Baseline, jul. 2024) | 127 | 118 | 17 |
| `text-box` | 133 | 154 | 18.2 |
| `tech()` en `src` | 108 | 107 | 17 |
| `COLRv1` | 98 | 107 | no |
- Safari estable aplica solo `size-adjust`, de modo que el alto de línea allí depende de las métricas internas. Prueba el fallback en Safari.
- `text-box`: web.dev y caniuse lo dan por disponible; web-features aún no marca el grupo porque BCD anota `css.types.text-edge.*` en Firefox como preview. Úsalo como mejora progresiva y prueba Firefox: `text-box: trim-both cap alphabetic`.

## 12. `font-variant-*` frente a `font-feature-settings`
Prefiere `font-variant-*`: da resultados «más eficaces, predecibles y comprensibles», y `font-feature-settings` es de bajo nivel y solo hace falta donde no hay propiedad, como `zero`, `hist` o `ssNN` [fuente: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-feature-settings].
```css
table td, .precio { font-variant-numeric: tabular-nums lining-nums; }
.prosa { font-variant-numeric: oldstyle-nums proportional-nums; }
abbr { font-variant-caps: all-small-caps; letter-spacing: .05em; }
.marca { font-feature-settings: "ss01", "cv03"; } /* sin equivalente de alto nivel */
```

- Baseline: `font-variant-numeric`, `-caps`, `-ligatures`, `-alternates`, `font-kerning` [fuente: web-features].
- `font-variant-position` tiene datos en conflicto: web-features dice solo Firefox, BCD dice Chrome 117, Firefox 34, Safari 9.1. Pruébalo. Las fuentes de esta referencia no fijan la propiedad de `ordn`: consúltala en MDN.
- Ninguna de estas propiedades recupera lo que el recorte quitó: sin `tnum` en el archivo, `tabular-nums` no hace nada y no da error (§ 4).
- No uses por defecto `text-rendering: optimizeLegibility` en artículos, por coste [fuente: MDN], ni `-webkit-font-smoothing: antialiased` en un reset: solo actúa en macOS.
- Para modo oscuro, un eje `GRAD` dúplex cambia el trazo sin cambiar anchos [fuente: https://fonts.google.com/knowledge/choosing_type/exploring_typefaces_with_multiple_weights_or_grades]. El −25 de Material Symbols es de iconos: no lo traslades a texto sin probar.
- Pon `lang="es"`: alimenta `locl` y `hyphens: auto` [fuente: MDN]. Prueba la partición, porque no se confirmó el diccionario español por navegador.

## 13. Cabeceras HTTP
```text
Content-Type: font/woff2
Cache-Control: public, max-age=31536000, immutable
Access-Control-Allow-Origin: https://www.ejemplo.com   # solo si sirves desde otro origen
```

- `Content-Type` es normativo [fuente: W3C WOFF2]; un 6,7 % aún sale como `application/octet-stream` [fuente: Almanac 2025]. Compruébalo con `curl -sI URL`.
- `Cache-Control` es [convención]: web.dev no da valor exacto. Exige nombres con versión o hash. No apliques Brotli ni gzip de servidor a `.woff2`: ya va comprimido [inferencia].
- Configura CORS solo si es de otro origen; mantén `crossorigin` en el preload siempre.

## 14. IFT: estado
Fecha de lectura: 2026-11-07.
- Es Candidate Recommendation Draft del 13 de octubre de 2026 [fuente: https://www.w3.org/TR/IFT/]. Última instantánea CR: 31 de julio de 2025. El objetivo del grupo era el segundo trimestre de 2026 y parece haberse retrasado.
- **No se halló navegador con soporte nativo.** Chromium: en curso, con Intent to Prototype, sin Intent to Ship [fuente: https://groups.google.com/a/chromium.org/g/blink-dev/c/3emvPjUOtaM]. Abril de 2026: «No one appears to be shipping this yet» [fuente: https://github.com/web-platform-dx/web-features/issues/3957]. Mozilla no tiene posición; WebKit lo ve bien, pero sin posición formal. La entrada de chromestatus no se pudo leer: no se excluye una bandera.
- Decisión: no lo entregues ni lo prometas. `unicode-range` sigue siendo la técnica de producción. Beneficiaría a CJK, emoji e iconos, no a una familia latina de 30–100 KB [inferencia].
- Sintaxis prevista: `src: url("MiTipo-Incremental.otf") tech(incremental);`.

## 15. COLR y respaldos
Soporte según BCD 8.1.8 y caniuse (hasta Safari 27.3/TP y iOS 27.2); **caduca**:

| Formato | Chrome/Edge | Firefox | Safari |
|---|---|---|---|
| COLRv0 | 53 | 31 | 11.1 |
| COLRv1 | 98 | 107 | **no** |
| OpenType-SVG | no | 31 | 12.1 |
| sbix | 66 | no | 9.1 |
| CBDT | 66 | no | no |
- COLRv0 es el único formato común a los tres motores. Úsalo como base; una fuente en color necesita siempre un respaldo monocromo [inferencia].
- Desacuerdo: FontLab sugiere WOFF2 COLRv1 más sabor SVG si importa Safari [fuente: https://blog.fontlab.com/2026/05/03/color-fonts-in-2026/].
```css
@font-face {
  font-family: "MiTipo Color";
  src: url("/fonts/mitipo-colrv1.woff2") format("woff2") tech(color-COLRv1),
       url("/fonts/mitipo-contorno.woff2") format("woff2");
}
```

- Detecta con `@supports font-tech(color-COLRv1)` [fuente: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@font-face/src].
- Algunos navegadores descartan todo el `src` si un valor es inválido: BCD da el descarte por elemento en Firefox 109+, parcial en Chrome/Edge 108+ y ausente en Safari. Prueba Safari anterior a 17.
- `pyftsubset` conserva `COLR` y `CPAL` y arrastra las capas. Si recortas fuera el glifo base, ambas tablas desaparecen sin aviso, y queda una fuente monocroma [verificado 2026-11-07 con fonttools 4.68.0]. Comprueba las tablas tras recortar.

## 16. Next.js, Astro, Nuxt, Tailwind
Entrega un WOFF2 limpio y un nombre de variable CSS. Estos datos son de sus documentaciones en noviembre de 2026; revisa la versión. Nada de esto se ejecutó.

**Next.js** [fuente: https://nextjs.org/docs/app/api-reference/components/font, actualizado 2026-09-24]:
```js
import localFont from 'next/font/local'
export const miTipo = localFont({
  src: './fonts/mitipo-latin-v1.woff2', weight: '300 800', display: 'swap',
  adjustFontFallback: 'Arial', variable: '--font-mitipo',
})
```

`display` por defecto es `swap`, `preload` es `true` y `adjustFontFallback` en local es `'Arial'`, y admite `'Times New Roman'` o `false`. Da `weight` con el rango real. Prefiere un solo archivo latino: `src` en lista apunta a peso y estilo, `declarations` se aplica al grupo y no se verificó `unicode-range` por archivo [inferencia].

**Astro** [fuente: https://docs.astro.build/en/guides/fonts/]: matriz `fonts` en la configuración, con `name`, `cssVariable` y proveedor, y `fontProviders.local()` con `options.variants`. En la página, `<Font cssVariable preload />` de `astro:assets`. Por defecto: pesos [400], normal y cursiva, `latin`, `sans-serif`, woff2, y `optimizedFallbacks` activado. Declara pesos y estilos explícitos. La guía no lleva etiqueta de estabilidad y no se halló un anuncio expreso de salida de experimental: compruébalo en el changelog de Astro 6.

**Nuxt** [fuente: https://nuxt.com/modules/fonts/configuration]: `@nuxt/fonts` funciona sin configuración, con proveedor `local`. Por defecto pesos `['400 700']`, normal y cursiva y varios subsets `-ext`: declara lo tuyo. No precarga caras con `unicode-range`, lo que afecta a un `@font-face` troceado.

**Tailwind v4** [fuente: https://tailwindcss.com/docs/font-family]:
```css
@import "tailwindcss";
@font-face { font-family: "MiTipo"; src: url("/fonts/mitipo-latin-v1.woff2") format("woff2"); font-weight: 300 800; font-display: swap; }
@theme { --font-display: "MiTipo", sans-serif; --font-display--font-feature-settings: "ss01"; }
/* con next/font: @theme inline { --font-sans: var(--font-mitipo), system-ui, sans-serif; } */
```

Un `@import` remoto debe ir antes de `@import "tailwindcss"`. Para Vite, `fontless` y `FontaineTransform.vite()` son complementos, no función oficial de Vite.

## 17. Accesibilidad
- **WCAG 1.4.4, Reescalar texto (AA):** hasta 200 % sin tecnología de apoyo y sin perder contenido ni función. **No fija tamaño mínimo** [fuente: https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html]. Evita contenedores fijos en `px` y unidades de viewport mal usadas (fallo F94).
- **WCAG 1.4.12, Espaciado de texto (AA):** nada debe perderse si el usuario pone interlineado 1,5 × tamaño, párrafos 2 ×, letras 0,12 × y palabras 0,16 ×. No hay que usarlos por defecto [fuente: https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html]. El usuario puede además necesitar una familia más ancha.
- Convierte 1.4.12 en prueba de fuente: renderiza un párrafo con `line-height:1.5; letter-spacing:.12em; word-spacing:.16em` y busca colisiones [inferencia].
- 1.4.5: usa texto real; los logotipos son la excepción. No apoyes significado solo en la PUA [inferencia].
- `font-display: block` oculta texto; las fuentes de iconos conviene cambiarlas por SVG, porque su respaldo puede alterar el significado [fuente: web.dev].
- 16 px de cuerpo y 12 px de mínimo son sugerencia sin norma detrás [inferencia].

## 18. Presupuestos propuestos
**Son una propuesta, no una norma.** Ningún organismo publica presupuestos de fuentes. Son juicio propio [inferencia], anclado en Almanac 2025 (por archivo: mediana unos 35–36 KB, p75 mediados de 70, p90 unos 115–116 KB). El Almanac no da totales por página. Ajústalos al proyecto y explica las excepciones.

| Partida | Objetivo | Límite |
|---|---|---|
| Estática latina de un estilo, WOFF2 | 15–30 KB | 40 KB |
| Variable latina solo `wght` | 40–70 KB | 100 KB |
| Variable `wght` + `opsz` | 70–110 KB | 116 KB |
| Bytes de fuente en primera vista | ≤ 100 KB | 150 KB |
| Archivos en primera vista | 2–3 | 4 |
| Familias | 1–2 | 3 |
| Archivos precargados | 1 | 2 |
| `preconnect` para fuentes | 0 con self-host | 1 par con terceros |

Puerta de CI:
```bash
test "$(stat -c%s mitipo-latin-v1.woff2)" -le 100000
```

## 19. Medición
- **Lighthouse:** `font-display` es hoy `font-display-insight`, y `uses-rel-preconnect` pasó a `network-dependency-tree-insight` [fuente: https://developer.chrome.com/blog/moving-lighthouse-to-insights]. Pasan `swap`, `optional` y `fallback` [fuente: https://developer.chrome.com/docs/lighthouse/performance/font-display].
- **DevTools, Performance:** Insights con Font display y ahorro estimado, desde Chrome 136 [fuente: https://developer.chrome.com/blog/new-in-devtools-136].
- **DevTools, Network:** filtra por fuentes y busca dobles descargas por `crossorigin`, tipo y `Cache-Control` [inferencia]. No se documentó el flujo de emulación del panel Rendering.
- **WebPageTest:** la tira de fotogramas muestra el intercambio y resalta desplazamientos; compara con y sin terceros [fuente: https://www.debugbear.com/software/webpagetest].
- **Campo:** decide con CLS y LCP reales al p75, por dispositivo [inferencia]. **Render:** revisa Windows 1x (DirectWrite), macOS (Quartz) y Android o Linux (FreeType) a 12–16 px [fuente: https://googlefonts.github.io/gf-docs/ReviewingFamilies/].

## 20. Consejos obsoletos
No sigas estos consejos, aunque aún circulen:
- **Pila EOT, WOFF, TTF, SVG:** basta WOFF2. **«Google Fonts ya estará en caché»:** falso desde el particionado.
- **Critical FOFT con Data URI como «gold standard» (2016):** histórico. Solo defendible con muchas estáticas. Tampoco uses un cargador JS por defecto.
- **Base64 en CSS:** web.dev pide no hacerlo. **`format("woff2-variations")`:** heredado, aunque la guía de MDN lo cite.
- **«Safari no tiene nada para métricas de respaldo»:** `size-adjust` llegó en Safari 17; los overrides siguen en preview.
- **«`text-box` necesita bandera en Firefox»:** salió en Firefox 154. El texto de Capsize «being implemented» va por detrás.
- **Auditorías Lighthouse `font-display` y `font-size`:** ya no existen como tales en Lighthouse 13.
- **`hyphens` con prefijos o solo en Chrome para macOS:** Chrome 88+, Safari 17 sin prefijo.
- **Soporte de variables según web.dev:** esas afirmaciones son de 2020. **`--with-zopfli` para WOFF2:** no aplica.

Y tres consignas demasiado fuertes [inferencia]: «`swap` lo arregla», porque sin fallback ajustado cambia invisibilidad por CLS; «precarga siempre», y «usa siempre variable». Trata las medidas de 2019–2020 como orientativas.

## 21. Checklist final
- [ ] Ejes listados antes de instanciar; `font-weight` y `font-stretch` tomados del `fvar` final.
- [ ] Solo `.woff2` para web, con `--layout-features+=…` o `'*'`, nunca `=` por descuido.
- [ ] GSUB/GPOS comparados por archivo, y cada pérdida justificada.
- [ ] Name-IDs 13 y 14 presentes, `.notdef` con contorno, hinting y `gasp` decididos según destino.
- [ ] Muestra española con NFC y NFD, más `ŀ` o `g̃` si aplican; cobertura con `scripts/coverage.py`.
- [ ] `latin` definido al final.
- [ ] `@font-face` en `<head>`, un preload con `crossorigin`, sin duplicados en Network.
- [ ] Fallback con media ponderada, no con `xAvgCharWidth`, y probado en Safari.
- [ ] Cabeceras: `font/woff2`, caché larga con nombre versionado, CORS si es otro origen.
- [ ] CLS ≤ 0,1 en 4G limitado, sin texto invisible; bytes en presupuesto o excepción explicada.
- [ ] Pruebas de 200 % y de espaciado 1.4.12; Windows 1x, macOS y Android revisados.
- [ ] Datos de navegador revalidados si esta referencia tiene más de unos meses.
