**Cuándo leer este archivo:** al convertir los dibujos en una fuente que funcione: métricas, nombres, features `.fea`, variable, hinting, QA y paquete final.

# Ingeniería OpenType

## Contenido

[1 Etiquetas](#1-cómo-leer-las-etiquetas) · [2 Anatomía](#2-anatomía-de-la-fuente) · [3 Contornos y salidas](#3-contornos-y-salidas) · [4 Métricas](#4-métricas-verticales) · [5 Nombres](#5-nombres-y-estilo) · [6 AGLFN](#6-nombres-de-glifo-y-aglfn) · [7 Kerning y marcas](#7-kerning-y-marcas-desde-el-ufo) · [8 Plantillas](#8-plantillas-fea) · [9 Sintaxis](#9-sintaxis-qué-acepta-fealib) · [10 Variables](#10-variables) · [11 Hinting](#11-hinting) · [12 Color](#12-color) · [13 QA](#13-qa-por-capas) · [14 Paquete](#14-paquete-final)

## 1. Cómo leer las etiquetas

- **[verificado 2026-11-07 con fonttools 4.68.0]**: ejecutado ese día. Pila: fontmake 3.12.2, ufo2ft 3.11.0, gftools 0.9.996, fontc 1.0.0, uharfbuzz 0.57.0 (HarfBuzz 15.0.0), Font Bakery 1.1.0. Cada bloque `fea` de este archivo se compiló con feaLib y con fontmake, y `fontc` compiló el conjunto.
- **[fuente: X]**: lo dice esa fuente, sin comprobar aquí. **[convención]**: práctica sin norma. **[inferencia]**: razonamiento propio.

En los comandos, `V=~/.local/share/type-design/venv/bin`; el `$PY` de `SKILL.md` es `$V/python`. `hb-shape` y `hb-view` no están instalados. Usa `scripts/shape_tests.py`, que llama a HarfBuzz por uharfbuzz. fontspector tampoco: `build.py --qa` recurre a Font Bakery.

## 2. Anatomía de la fuente

**Especificación.** OpenType 1.9.1 (mayo de 2024) [fuente: [OpenType](https://learn.microsoft.com/en-us/typography/opentype/spec/changes)]; ISO/IEC 14496-22:2026 va por delante según un resumen de búsqueda. avar2 funciona en Safari, Firefox y Chrome 148 (extracto) y no consta en DirectWrite: no dependas de él sin respaldo. VARC y más de 64k glifos no aportan a una familia latina [inferencia].

**Tablas obligatorias:** `cmap head hhea hmtx maxp name OS/2 post`, más `glyf`+`loca`, `CFF ` o `CFF2` [fuente: [otff](https://learn.microsoft.com/en-us/typography/opentype/spec/otff)]. Layout: `GSUB GPOS GDEF`. Variación: `fvar STAT gvar avar HVAR MVAR`.

| | `glyf` | `CFF ` | `CFF2` |
|---|---|---|---|
| Curvas | cuadráticas | cúbicas | cúbicas |
| Precisión; variación | 1 unidad; `gvar` | 1/65536; no | 1/65536; en la tabla |
| Solapes | sí | no | sí |
| Hinting | instrucciones | zonas y astas por glifo | zonas por grupo y astas |

[fuente: [comparación](https://learn.microsoft.com/en-us/typography/opentype/spec/glyphformatcomparison)]

**Reglas:** glifo 0 = `.notdef` visible [fuente: [recom](https://learn.microsoft.com/en-us/typography/opentype/spec/recom)]. Evita compuestos anidados [fuente: [glyf](https://learn.microsoft.com/en-us/typography/opentype/spec/glyf)]. Nada de tabla `kern`: no varía, usa GPOS [fuente: recom]. UPM 1000 o 2048 es lo habitual [fuente: [Glyphs](https://glyphsapp.com/learn/vertical-metrics)], sin fuente primaria para elegir; `glyf` redondea a enteros, así que uno mayor gana fidelidad y pierde tamaño [inferencia]. `macStyle` debe coincidir con `fsSelection`, y Windows lee la versión del ID 5, no de `head.fontRevision` [fuente: [head](https://learn.microsoft.com/en-us/typography/opentype/spec/head)].

## 3. Contornos y salidas

Compila siempre con `scripts/build.py`. Para probar a mano, estas son las opciones reales de fontmake (`-o`: `ufo otf otf-cff2 ttf ttf-interpolatable otf-interpolatable variable variable-cff2`):
```bash
cd sources
$V/fontmake -m Familia.designspace -o variable --output-dir ../salida
$V/fontmake -m Familia.designspace -o variable-cff2 --output-dir ../salida
$V/fontmake -m Familia.designspace -i "Familia Medium" -o ttf otf --output-dir ../salida
$V/fontmake -u masters/Familia-Regular.ufo -o ttf --output-path ../salida/rapida.ttf
rm -rf instance_ufo
```

Medido [verificado 2026-11-07 con fonttools 4.68.0]:
| Salida | Tablas de contorno y variación | `post` | Solapes |
|---|---|---|---|
| `-o variable` | `glyf gvar fvar HVAR STAT`; `avar` si hay `<map>`; `MVAR` si varían métricas | 2.0 | Se conservan, **sin flag OVERLAP** |
| `-o variable-cff2` | `CFF2 fvar HVAR STAT`, y `avar` | 2.0 | Se conservan |
| `-o ttf` estática | `glyf` | 2.0 | Fusiona contornos; **los componentes solapados siguen** y sin flag |
| `-o otf` | `CFF ` | 3.0 | Fusiona y descompone todo |

Consecuencias:
- Evita componentes que se cubran en TTF estática: no se fusionan. Si un acento debe solapar la base, dibuja el glifo como contorno [inferencia].
- `-o variable` crea `Familia-VF.ttf`; `gftools builder` crea `Familia[wght].ttf`. Google prohíbe el sufijo VF y Microsoft lo sugiere [fuente: [GF](https://googlefonts.github.io/gf-guide/variable.html), recom].
- `gftools builder` toma el nombre de archivo de las instancias, no de la familia: salió `Ing-Bold.ttf` con PostScript `PruebaIng-Bold`. `new_project.py` los hace coincidir [verificado 2026-11-07 con fonttools 4.68.0].
- **Familia SC no pedida.** `buildSmallCap` vale `true` por defecto en `gftools builder`: `feature smcp` generaría además `Familia SC` en todas las salidas. `build.py` lo fija a `false`.

## 4. Métricas verticales

Existen tres juegos: `hhea`, `OS/2 sTypo*`, `OS/2 usWin*`. El núcleo común de todas las recomendaciones modernas: activa USE_TYPO_METRICS (bit 7 de `fsSelection`), iguala `hhea` a typo, haz que win cubra la caja y usa los mismos valores en toda la familia. GDI recorta lo que sobresalga de win [fuente: [OS/2](https://learn.microsoft.com/en-us/typography/opentype/spec/os2)].

| Estrategia | typo y hhea | win | lineGap | Comentario |
|---|---|---|---|---|
| **Por defecto en esta skill** | span 1,25 em con mayúsculas centradas | caja real | 0 | Lo más predecible entre plataformas |
| Google [fuente: [GF](https://googlefonts.github.io/gf-guide/metrics.html)] | asc ≥ yMax de Ắ (U+1EAE); `typoAsc − capHeight ≈ |typoDesc|`; 120–130 % UPM | caja de la familia | 0 | Su ejemplo 1015/−315 es 133 % y la guía lo llama quizá holgado |
| Glyphs webfont 2019 [fuente: [Glyphs](https://glyphsapp.com/learn/vertical-metrics)] | cubre diacríticos clave | extremos | 10–20 % del span | Avisa de que seguir a Google al pie puede bajar el texto en caja mixta |
| Microsoft A / B [fuente: recom] | A: asc − desc = UPM; B: iguales a win | A: span + gap, o mayor; B: igual o mayor | A: se admite; B: 0 | El em exacto es «a menudo apropiado», no obligatorio |

**Desacuerdos.** Si `lineGap` es 0 (Google, esta skill) o no (Glyphs, Minion de Microsoft), y si el span debe ser un em. Cambia sobre todo dónde cae el espacio en la caja de línea CSS, no el interlineado total [inferencia]; los navegadores reparten el gap arriba y abajo [fuente: Glyphs].

**Automatizado.** `new_project.py` fija gap 0, hhea = typo, USE_TYPO_METRICS y span 1,25 em; con cap 700 da 975/−275 [verificado 2026-11-07 con fonttools 4.68.0]. `build.py` recalcula win con la caja de todos los glifos de todos los másteres.

**Qué sigue siendo tuyo:**
1. Comprueba que typoAsc cubra Ắ si habrá vietnamita. Sube el span si hace falta.
2. `build.py` calcula win con los glifos y con un nivel de marca colocada sobre cada base con ancla. Las pilas de dos o más marcas quedan fuera, y la norma pide considerarlas en fuentes nuevas [fuente: OS/2]. Si las admites, mide el `y_offset` máximo con HarfBuzz y revisa el resultado.
3. No varíes métricas entre másteres: si cambias `xHeight` o el ascendente en la Bold, aparece MVAR (medido: `hasc stro xhgt`) [verificado 2026-11-07 con fonttools 4.68.0]. La puerta de coherencia de `build.py` compara typo, hhea y win entre archivos, no `xHeight`.
4. Con USE_TYPO_METRICS, Office ignora posición y grosor de subrayado [fuente: Glyphs]. Registra los valores en el changelog: cambiarlos tras publicar reordena documentos ajenos y cuenta como versión mayor [inferencia].

## 5. Nombres y estilo

Tres modelos paralelos conviven: IDs 1/2 (grupo RIBBI de cuatro), 16/17 (tipográfico, ilimitado) y 21/22 (WWS, solo si hay un atributo no WWS) [fuente: [name](https://learn.microsoft.com/en-us/typography/opentype/spec/name)].

| ID | Contenido | Regla |
|---|---|---|
| 0, 7 | Copyright, marca | Marca solo si es real y con consejo legal |
| 1, 2 | Familia, subfamilia | Máximo cuatro fuentes por ID 1 |
| 3, 4 | ID único, nombre completo | `1.000;VEND;Familia-Estilo`; sin «Regular» residual |
| 5, 6 | Versión, PostScript | `Version 1.000`; ASCII 33–126 sin `[ ] ( ) { } < > / %` |
| 8, 9, 11, 12 | Fabricante, diseñador, URL | Con protocolo |
| 13, 14 | Licencia y URL | Vigila subset (`07-web.md`) |
| 16, 17 | Familia y subfamilia tipográficas | 17 único en la familia |
| 25; 256+ | Prefijo PostScript de variaciones; propios | Solo alfanumérico ASCII; 256+ los usan `fvar`, `STAT`, `featureNames` |

**RIBBI** [fuente: [GF statics](https://googlefonts.github.io/gf-guide/statics.html)]:
| Estilo | fsSelection | macStyle | ID 1 | ID 2 | 16 / 17 |
|---|---|---|---|---|---|
| Regular | bit 6 | 0 | Familia | Regular | — |
| Bold | bit 5 | bit 0 | Familia | Bold | — |
| Italic | bit 0 | bit 1 | Familia | Italic | — |
| Bold Italic | bits 0 y 5 | bits 0 y 1 | Familia | Bold Italic | — |
| Otro peso (cursiva) | bit 6 (bit 0) | 0 (bit 1) | Familia Light | Regular (Italic) | Familia / Light (Light Italic) |

Con `stylemapfamilyname` y `stylemapstylename` en el designspace, `gftools builder` reproduce la tabla: Bold con ID 1 de familia, fsSelection `0b10100000`, macStyle 1; Medium con ID 1 `Prueba Ing Medium`, ID 2 `Regular` y 16/17 [verificado 2026-11-07 con fonttools 4.68.0].

- **Cursiva.** `italicAngle` no activa los bits de estilo: una variable cursiva salió sin bit 0 y macStyle 0. Con `styleMapStyleName = "italic"` en el UFO, bit 0 y macStyle 2 [verificado 2026-11-07 con fonttools 4.68.0]. Define también `italicAngle` negativo.
- **fsType.** Sin `openTypeOS2Type`, ufo2ft da 4 (solo vista previa e impresión) en variables, y las instancias salieron con 8: incoherente. Con `[]` ambos dan 0 [verificado 2026-11-07 con fonttools 4.68.0]. `new_project.py` ya lo fija; revisa proyectos anteriores y la licencia.
- **Versión.** `versionMajor=1`, `versionMinor=234` da `Version 1.234` en ID 5, `1.234;NONE;Familia-Regular` en ID 3 y `head.fontRevision` ≈ 1.234 [verificado 2026-11-07 con fonttools 4.68.0]. Google: cambio que rompe 1.230 → 2.000; juego nuevo → 1.330; pocos glifos → 1.240; solo `name` → 1.231 [fuente: [GF](https://googlefonts.github.io/gf-guide/requirements.html)]. Nunca reutilices un número.

**Desacuerdos:**
- *Límite del ID 6:* 63 en `name`; 127 recomendado en `recom`; lectores de 63 y 29 según [Glyphs](https://glyphsapp.com/learn/naming); familia + estilo ≤ 32 en Google. Quédate bajo 29 si puedes [inferencia].
- *Semibold y peso mínimo:* el ejemplo Caslon de la especificación enlaza Semibold como negrita de Regular; Google no. Glyphs aconseja `usWeightClass` ≥ 250 por el emboldado viejo de Office; Microsoft y Google usan 100.
- *Nombres Mac:* no hacen falta, y a la vez se piden 1/0/0 y 3/1/0x409 iguales para el ID 6 [fuente: recom]. fontmake escribe solo plataforma 3, y OTS lo acepta [verificado 2026-11-07 con fonttools 4.68.0].
- *Orden de estilo:* Glyphs ordena peso, anchura, inclinación, tamaño óptico; STAT deja anchura, peso e itálica al final.
- Antes de incrustar el nombre, comprueba que no sea marca ajena: cambiarlo después rompe documentos [inferencia].

## 6. Nombres de glifo y AGLFN

Usa solo `A–Z a–z 0–9 . _`, sin empezar por dígito o punto salvo `.notdef`, con 63 caracteres como máximo [fuente: [AGL](https://raw.githubusercontent.com/adobe-type-tools/agl-specification/master/README.md)]. Lo que sigue al primer punto no cuenta para Unicode: `periodcentered.loclCAT` da `·`. Usa AGLFN si existe y `uniXXXX` en mayúsculas si no: `uni20ac` no mapea a nada [verificado 2026-11-07 con fonttools 4.68.0].

`fontTools.agl.AGL2UV` contiene AGLFN; `toUnicode()` usa además el AGL antiguo. De ahí esta tabla [verificado 2026-11-07 con fonttools 4.68.0]:
| Carácter | Nombre seguro | Trampa |
|---|---|---|
| Ș ș U+0218/9 | `uni0218`, `uni0219` | `Scommaaccent` no está en AGLFN (en el AGL antiguo sí da U+0218) |
| Ț ț U+021A/B | `uni021A`, `uni021B` | **`Tcommaaccent` da U+0162 Ţ, con cedilla**: es otro carácter |
| Ţ ţ U+0162/3; Ş ş U+015E/F | `uni0162`, `uni0163`; `Scedilla`, `scedilla` | `Tcedilla` no está en AGLFN; `Scedilla` sí |
| ı U+0131 | `dotlessi` | `idotless` no mapea a nada |
| İ U+0130 | `Idotaccent` | `idotaccent` (la i turca con punto) no tiene Unicode: es correcto, se usa por `locl` |
| ȷ U+0237 | `uni0237` | `dotlessj` no está en AGLFN |
| ﬁ, ﬂ, ¹ ² ³ | `fi`, `fl`, `onesuperior`… | Solo en el AGL antiguo; mapean bien por `toUnicode`. Son convención, no AGLFN |
| µ U+00B5 / μ U+03BC | `mu` / `uni03BC` | `mu` es el signo micro |
| ʼ U+02BC, ꞌ U+A78C | `uni02BC`, `uniA78C` | Sin nombre AGLFN |

**Nombres de producción.** Con `public.postscriptNames` en `lib.plist`, fontmake renombra (`a.ss01 → a.alt`, `fi → uniFB01`) y `--no-production-names` lo desactiva [verificado 2026-11-07 con fonttools 4.68.0]. Lo más simple es nombrar ya con la tabla de arriba y no usar la clave. La extracción de texto de PDF depende del visor: compruébalo si importa [inferencia].

## 7. Kerning y marcas desde el UFO

Escribe kerning y anclajes en el UFO, no en `.fea`: así varían por máster solos. ufo2ft los convierte en GPOS.

`public.kern1.X` agrupa los que van **primero** en el par (por su lado derecho) y `public.kern2.X` los que van **segundo** (por su lado izquierdo). El par (`public.kern1.T`, `public.kern2.o`) = −80 afecta a `To` y no a `oT`. Medido [verificado 2026-11-07 con fonttools 4.68.0]:
- Otros prefijos, como `MMK_L_T`, se ignoran sin aviso. Un glifo en dos grupos del mismo lado: ufoLib2 no guarda («occurs in too many kerning groups»). Una excepción glifo-grupo (`T`, `oacute` = −20) gana a la clase (−80).
- **Par ausente en un máster, sin clase:** vale 0 ahí. `A V` solo en Regular (−70) dio 0 en 300 y 700, y −35 en 550. **Excepción ausente:** usa la clase de ese máster: `T e` = 0 solo en Regular dio −80, 0 y −120.
- **Grupos distintos entre másteres:** compila; ufo2ft avisa con un INFO («Reconciling kerning groups») y deja fuera del grupo al glifo discrepante. Mantén grupos idénticos.

**Contradicción con las notas:** decían que los pares ausentes podían romper la interpolación [fuente: [Glyphs](https://glyphsapp.com/learn/creating-a-variable-font)]. Con esta pila no rompen, pero el valor cae a 0 y hace una joroba: da valor en todos los másteres.

**`# Automatic Code`.** ufo2ft salta lo que encuentre escrito a mano:
| En `features.fea` | Resultado medido |
|---|---|
| Sin `feature kern` | Genera todo el kerning del UFO |
| `feature kern { pos A A -33; } kern;` | **Descarta todo el kerning del UFO sin aviso** (`To` pasó de −80 a 0) |
| Igual con `# Automatic Code` dentro | Conserva ambos, y **se suman**: manual −5 + UFO −80 en `To` = −85 |

Lo mismo con `mark`: un `feature mark` a mano elimina los automáticos [verificado 2026-11-07 con fonttools 4.68.0].

- **`languagesystem` es obligatorio.** Sin él, y en cuanto hay kerning, `mark` y `mkmk` quedan solo en `DFLT` mientras `kern` crea `latn`. HarfBuzz elige `latn` y **las marcas no se posicionan** (`x`+U+0301 con desplazamiento 0, frente a −250 con las líneas `languagesystem`) [verificado 2026-11-07 con fonttools 4.68.0].
- **`public.openTypeCategories`.** Sin la clave, ufo2ft infiere GDEF de los anclajes y todo funciona. Con ella, solo participan los glifos listados: sin bases **no genera mark-to-base**, y una marca no listada deja de posicionarse. O no la pongas, o lista todo (`base`, `mark`, `ligature`) [verificado 2026-11-07 con fonttools 4.68.0].

**Resto de `mark`** [verificado 2026-11-07 con fonttools 4.68.0]. `top` en la base + `_top` en la marca da `mark`; ambos en la misma marca dan `mkmk`; `top_1`, `top_2` en una ligadura dan mark-to-ligature. Los compuestos no heredan anclajes: `acomp` con U+0323 no se posiciona; con `--filter ... --filter PropagateAnchorsFilter` en fontmake sí, pero `build.py` no lo pasa, así que escribe los anclajes en el generador. Una marca con avance 200 y clase `mark` queda a 0 en HarfBuzz y `hmtx` conserva 200: dale avance 0, como exige Google [fuente: [GF](https://googlefonts.github.io/gf-guide/diacritics.html)]. Declaración completa en `06-idiomas-y-cobertura.md`.

## 8. Plantillas `.fea`

Escribe en `sources/features.fea`; `build.py` lo copia a cada máster. **El orden del archivo es el orden de aplicación:** HarfBuzz aplica los lookups por índice. Conserva el orden, elimina lo que no uses y recorta las clases a tus glifos, porque feaLib falla ante un glifo inexistente. Sufijos [convención]: `.tf` tabular, `.osf` elzeviriana, `.tosf` tabular elzeviriana, `.numr`, `.dnom`, `.sc`, `.case`, `.loclCAT`, `.ssNN`, `.cvNN`. Las cifras por defecto se suponen proporcionales de caja alta, como exige Google [fuente: [GF](https://googlefonts.github.io/gf-guide/requirements.html)]; la especificación dice que las tabulares suelen serlo. Si eliges tabulares, intercambia los papeles.

Cada bloque se compiló aislado con feaLib y el conjunto con fontmake y fontc; las pruebas son de HarfBuzz sobre la variable resultante [verificado 2026-11-07 con fonttools 4.68.0]:
| Bloque | Por qué y qué se probó |
|---|---|
| Preámbulo | `DFLT` debe ir primero: feaLib da error si no |
| `ccmp` | `.case` sobre mayúsculas sin precompuesto (G̃) y sin punto en i, j ante marca alta. En lituano la i conserva el punto: `LTH` va sin `SIN_PUNTO`. Probado `G`+U+0303, dos marcas seguidas, `i`+U+0306, `lt` |
| `locl` | Casos explicados en `06-idiomas-y-cobertura.md`, con neerlandés y polaco. Probado `ca tr az crh kk tt ro mo` |
| `frac` | Solo toca cifras pegadas a la barra. La plantilla de las notas volvía numeradores todas las cifras y estropeaba `2 1/4`; esta usa `rsub`. Probado `1/2`, `11/17`, `2 1/4`, `a/b` intacto. **U+2044 activa la fracción sin pedir `frac`**, pues HarfBuzz aplica `numr` y `dnom`. Limitación: `12/03/2026` sale mal, aplica `frac` solo a la selección |
| `ordn` | Conserva el punto de `1.º`. Probado `1.o`, `2.a`, `12a`, `No` → `uni2116`, `ao` intacto. No cubre `1.er`. Dos lookups: uno con nombre no admite tipos distintos |
| `sups`, `subs` | Glifos codificados, que se copian bien |
| Cifras | `onum`+`tnum` da `.tosf`. `onum`/`lnum` y `pnum`/`tnum` son excluyentes [fuente: [features](https://learn.microsoft.com/en-us/typography/opentype/spec/features_ko)]: a la vez gana el último del archivo. `zero`+`tnum` da `zero.tf.zero`; `zero` no afecta a `onum`. No metas `.tf` en grupos de kerning: `11` con −50 pasó a avance fijo con `tnum` |
| `case` | Sube puntuación y anula `onum` [fuente: [features_ae](https://learn.microsoft.com/en-us/typography/opentype/spec/features_ae)]; va tras las cifras. Las formas de ¿ ¡ son las que más importan en español |
| `smcp`, `c2sc` | Genera las clases desde Unicode, no a mano. Con `tr`: `i` → `idotaccent.sc`, `ı` → `dotlessi.sc`, `İ` → `idotaccent.sc`. **Activa la familia SC: ver sección 3** |
| `ss01`, `cv01` | `ss` para un conjunto con nombre, `cv` para un carácter. Sin `featureNames` se ve «Stylistic Set 1». feaLib crea IDs ≥ 256: 0x409 con la cadena sin idioma (ponla en inglés) y 0x0C0A con la española. `cv01=1` da `a.cv01`, `cv01=2` da `a.cv02` |
| `liga` | Las largas se aplican antes aunque las escribas después |
| `calt` | Vía catalana sin idioma: `locl` solo actúa si la aplicación lo pasa. Probado sin idioma, `es`, `ca`, mayúsculas, `smcp`, `c2sc`; `a·b` intacto |

```fea
languagesystem DFLT dflt;
languagesystem latn dflt;
languagesystem latn CAT; languagesystem latn NLD; languagesystem latn PLK; languagesystem latn LTH;
languagesystem latn TRK; languagesystem latn AZE; languagesystem latn CRT;
languagesystem latn KAZ; languagesystem latn TAT; languagesystem latn ROM; languagesystem latn MOL;

@fig      = [zero one two three four five six seven eight nine];
@fig_tf   = [zero.tf one.tf two.tf three.tf four.tf five.tf six.tf seven.tf eight.tf nine.tf];
@fig_osf  = [zero.osf one.osf two.osf three.osf four.osf five.osf six.osf seven.osf eight.osf nine.osf];
@fig_tosf = [zero.tosf one.tosf two.tosf three.tosf four.tosf five.tosf six.tosf seven.tosf eight.tosf nine.tosf];
@fig_numr = [zero.numr one.numr two.numr three.numr four.numr five.numr six.numr seven.numr eight.numr nine.numr];
@fig_dnom = [zero.dnom one.dnom two.dnom three.dnom four.dnom five.dnom six.dnom seven.dnom eight.dnom nine.dnom];
@marcas_arriba = [gravecomb acutecomb uni0302 tildecomb uni0304 uni0306 uni0307 uni0308 uni030A uni030C hookabovecomb];
@marcas_arriba_case = [gravecomb.case acutecomb.case uni0302.case tildecomb.case uni0304.case uni0306.case uni0307.case uni0308.case uni030A.case uni030C.case hookabovecomb.case];
@mayusculas = [A - Z];
@min = [a - z aacute eacute iacute oacute uacute udieresis ntilde agrave egrave igrave ograve ugrave idieresis ccedilla];
@min_sc = [a.sc - z.sc aacute.sc eacute.sc iacute.sc oacute.sc uacute.sc udieresis.sc ntilde.sc agrave.sc egrave.sc igrave.sc ograve.sc ugrave.sc idieresis.sc ccedilla.sc];
@may = [A - Z Aacute Eacute Iacute Oacute Uacute Udieresis Ntilde Ccedilla];
@may_sc = [a.sc - z.sc aacute.sc eacute.sc iacute.sc oacute.sc uacute.sc udieresis.sc ntilde.sc ccedilla.sc];
feature ccmp {
    lookup MARCAS_CASE { sub @mayusculas @marcas_arriba' by @marcas_arriba_case; sub @marcas_arriba_case @marcas_arriba' by @marcas_arriba_case; } MARCAS_CASE;
    lookup SIN_PUNTO { sub [i j]' @marcas_arriba by [dotlessi uni0237]; } SIN_PUNTO;
    script latn; language LTH exclude_dflt; lookup MARCAS_CASE;
} ccmp;
lookup TURCO { sub i by idotaccent; } TURCO;
lookup RUMANO { sub Scedilla by uni0218; sub scedilla by uni0219; sub uni0162 by uni021A; sub uni0163 by uni021B; } RUMANO;
feature locl {
    script latn;
    language CAT;
        lookup CATALAN {
            sub l periodcentered' l by periodcentered.loclCAT;
            sub L periodcentered' L by periodcentered.loclCAT.case;
        } CATALAN;
    language TRK; lookup TURCO;  language AZE; lookup TURCO;  language CRT; lookup TURCO;
    language KAZ; lookup TURCO;  language TAT; lookup TURCO;
    language ROM; lookup RUMANO; language MOL; lookup RUMANO;
} locl;
feature numr { sub @fig by @fig_numr; } numr;
feature dnom { sub @fig by @fig_dnom; } dnom;
feature frac {
    lookup FRAC_BARRA { sub @fig slash' @fig by fraction; } FRAC_BARRA;
    lookup FRAC_NUMR { rsub @fig' fraction by @fig_numr; rsub @fig' @fig_numr by @fig_numr; } FRAC_NUMR;
    lookup FRAC_DNOM { sub [fraction @fig_dnom] @fig' by @fig_dnom; } FRAC_DNOM;
} frac;
feature ordn {
    lookup ORDN_LETRA { sub @fig [a o]' by [ordfeminine ordmasculine]; sub @fig period [a o]' by [ordfeminine ordmasculine]; } ORDN_LETRA;
    lookup ORDN_NUMERO { sub N o by uni2116; } ORDN_NUMERO;
} ordn;
feature sups { sub @fig by [uni2070 onesuperior twosuperior threesuperior uni2074 uni2075 uni2076 uni2077 uni2078 uni2079]; } sups;
feature subs { sub @fig by [uni2080 uni2081 uni2082 uni2083 uni2084 uni2085 uni2086 uni2087 uni2088 uni2089]; } subs;
feature pnum { sub @fig_tf by @fig; sub @fig_tosf by @fig_osf; } pnum;
feature tnum { sub @fig by @fig_tf; sub @fig_osf by @fig_tosf; } tnum;
feature lnum { sub @fig_osf by @fig; sub @fig_tosf by @fig_tf; } lnum;
feature onum { sub @fig by @fig_osf; sub @fig_tf by @fig_tosf; } onum;
feature zero { sub zero by zero.zero; sub zero.tf by zero.tf.zero; } zero;
feature case {
    sub [hyphen endash emdash parenleft parenright bracketleft bracketright braceleft braceright exclamdown questiondown guillemotleft guillemotright guilsinglleft guilsinglright at slash periodcentered]
     by [hyphen.case endash.case emdash.case parenleft.case parenright.case bracketleft.case bracketright.case braceleft.case braceright.case exclamdown.case questiondown.case guillemotleft.case guillemotright.case guilsinglleft.case guilsinglright.case at.case slash.case periodcentered.case];
    sub @fig_osf by @fig; sub @fig_tosf by @fig_tf;
} case;
feature smcp { sub @min by @min_sc; sub dotlessi by dotlessi.sc; sub idotaccent by idotaccent.sc; } smcp;
feature c2sc { sub @may by @may_sc; sub Idotaccent by idotaccent.sc; } c2sc;
feature ss01 {
    featureNames { name "Alternates for a and g"; name 3 1 0x0C0A "Alternativas de a y g"; };
    sub a by a.ss01; sub g by g.ss01;
} ss01;
feature cv01 {
    cvParameters {
        FeatUILabelNameID { name "Variants of a"; name 3 1 0x0C0A "Variantes de a"; };
        Character 0x0061;
    };
    sub a from [a.cv01 a.cv02];
} cv01;
feature liga { sub f f i by f_f_i; sub f f l by f_f_l; sub f f by f_f; sub f i by fi; sub f l by fl; } liga;
feature calt {
    lookup CATALAN_SIN_IDIOMA {
        sub l periodcentered' l by periodcentered.loclCAT;
        sub L periodcentered' L by periodcentered.loclCAT.case;
        sub l.sc periodcentered' l.sc by periodcentered.loclCAT.sc;
    } CATALAN_SIN_IDIOMA;
} calt;
```

**Qué rompe el orden** [verificado 2026-11-07 con fonttools 4.68.0]:
| Si pones | Resultado |
|---|---|
| `liga` antes de `locl` | Turco `fi` → ligadura: se pierde la i con punto |
| `liga` antes de `smcp` | `fi` con `smcp` sigue siendo la ligadura de caja baja |
| Cifras antes de `frac` | `frac`+`onum` deja `one.osf slash two.osf`: sin fracción |
| `case` antes de cifras | `case` no anula `onum` |
| `calt` antes de `smcp` | `l·l` con `smcp` conserva el punto sin `.sc` |

Las notas proponían `sub f [i idotaccent] by fi;` para turco: compila y en turco da `fi` [verificado 2026-11-07 con fonttools 4.68.0]. Solo vale si tu `fi` muestra el punto.

**`kern` y `mark` a mano.** Solo si no caben en el UFO. Este bloque **sustituye** al kerning y las marcas automáticos: añade `# Automatic Code` para conservar los del UFO, y recuerda que se suman. `IgnoreMarks` mantiene el par en `T`+marca+`o`. Los pares sueltos preceden a las clases y ganan (`Tó` −20, `To` −80); `enum` expande a pares; `subtable;` corta si una clase desborda. Las marcas de este bloque **no varían** con el peso: `g`+U+0303 dio −250 en 300 y en 700; en variables usa anclajes [verificado 2026-11-07 con fonttools 4.68.0]. Límite de GPOS: 64 KB, y `useExtension` para lookups grandes [fuente: [Glyphs](https://glyphsapp.com/learn/kerning)].

```fea
feature kern {
    lookupflag IgnoreMarks;
    pos T oacute -20;
    enum pos T [semicolon colon] -30;
    pos [T V] [a o] -80;
    subtable;
    pos [A] [T V] -60;
} kern;
markClass [gravecomb acutecomb tildecomb] <anchor 0 512> @TOP;
markClass dotbelowcomb <anchor 0 0> @BOTTOM;
feature mark {
    lookup MARCA_BASE { pos base [a o] <anchor 250 512> mark @TOP <anchor 250 0> mark @BOTTOM; pos base g <anchor 250 512> mark @TOP; } MARCA_BASE;
} mark;
feature mkmk {
    lookup MARCA_MARCA {
        lookupflag UseMarkFilteringSet [gravecomb acutecomb tildecomb];
        pos mark [gravecomb acutecomb tildecomb] <anchor 0 700> mark @TOP;
    } MARCA_MARCA;
} mkmk;
```

## 9. Sintaxis: qué acepta feaLib

La gramática de Adobe es la 1.27 [fuente: [AFDKO](https://adobe-type-tools.github.io/afdko/OpenTypeFeatureFileSpecification.html)]. Diferencias reales con feaLib [verificado 2026-11-07 con fonttools 4.68.0]. **`fontc` es más permisivo: compila `wght=700u`, `(-20 wght=700u:-40)` y el escalar sin máster por defecto, que feaLib rechaza; ambos rechazan `locationDef`.** Por eso `--con-fontc` no sustituye a fontmake como prueba:
| Escritura | Resultado | Haz esto |
|---|---|---|
| `lookup X { script latn; language CAT; ... } X;` fuera de `feature` (forma publicada por Glyphs) | **Error** feaLib: «Script statements are not allowed within standalone lookup blocks» | Mételo en `feature locl { }`: así compila y actúa solo en `ca` |
| `lookup X {...} X;` fuera de `feature`, sin referencia | Compila, pero no actúa | Referéncialo con `lookup X;` |
| `[zero - nine]` | **Error**: los rangos son alfabéticos | Escribe la lista |
| `[a-c]`, `[a - c]`, `[a.sc - z.sc]`, `[uni2081 - uni2082]` | Compilan | Prefiere con espacios: un guion puede formar parte del nombre |
| `locationDef`, `wght=700u`, `wght=300d`, `wght=-1n` (AFDKO) | **Error** | Usa `wght=700:valor` |
| `(-20 wght=700u:-40)` (valor por defecto implícito de AFDKO) | **Error** | Da todas las posiciones |
| `(wght=300:-10 wght=700:-40)` sin el máster por defecto | **Error**: «Failed to compute deltas» | Incluye la posición por defecto |
| Tipos mezclados en lookup con nombre | **Error**: «all rules must be of the same lookup type» | Separa lookups |
| Tipos mezclados en `feature` sin nombre; dos bloques `feature ordn` | Compilan: separa o acumula | Aceptable |
| `sub a by NULL;`, `rsub`, `ignore sub`, `enum pos`, `pos cursive`, `<anchor NULL>`, `useExtension`, `aalt`, `table GDEF`, `table STAT`, `table head/hhea/OS/2/name`, `required` | Compilan | Las notas decían que `required` no estaba implementado: feaLib lo acepta. No lo uses |
| `markClass` tras su uso | **Error** | Declara antes |
| `language TRK` sin `languagesystem latn TRK`; acentos en `name`, directos o con `\00E9` | Compilan | Declara el idioma igualmente |

**Un solo archivo, igual en todos los másteres.** `include(calt.fea);` falla tras la copia, porque el camino queda relativo al UFO; `--fea-include-dir .` lo resuelve, pero `build.py` no lo pasa. Con `.fea` distintas por máster, fontmake falla al fusionar («Couldn't merge the fonts») [verificado 2026-11-07 con fonttools 4.68.0].

## 10. Variables

`fvar` y `STAT` son obligatorias; `HVAR` recomendada en TrueType y obligatoria en CFF2 [fuente: [otvar](https://learn.microsoft.com/en-us/typography/opentype/spec/otvaroverview)]. fontmake crea las tres y cumple bit 1 de `head.flags` y lsb = xMin [verificado 2026-11-07 con fonttools 4.68.0]. Solo `ital opsz slnt wdth wght` están registrados; los propios van en mayúsculas y dígitos [fuente: [registro](https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxisreg)].

| Eje | Escala | Regla |
|---|---|---|
| `wght` | 1–1000, como `usWeightClass` | Google exige incluir 400 |
| `wdth` | % de la normal; 100 = normal | `usWidthClass` coincide con el defecto |
| `opsz` | puntos | Mín. y máx. = objetivos reales; defecto 10–16 en texto |
| `slnt` | grados; a la derecha, negativo | Google: solo si no hay cursiva |
| `ital` | 0–1 | Una variable redonda y otra cursiva, enlazadas por STAT |
| `GRAD` | no registrado | No debe cambiar avances [fuente: extracto de GF] |

Expón solo lo que puedas dibujar y probar. Regular como defecto es lo más compatible [inferencia]. Hudson pide un máster en cada extremo de eje, no en cada esquina; la especificación avisa de que los ejes combinados a menudo las necesitan [fuente: extracto de [TypeDrawers](https://typedrawers.com/discussion/3612/what-is-best-practise-in-variable-font-development), otvar].

**Designspace.** Probado tal cual: con `<labels>` fontmake escribe STAT completo sin gftools, `<map>` genera `avar`, `postscriptfontname` llena `postScriptNameID` y `processing="last"` pone la regla en `rclt` (`first` en `rvrn`) [verificado 2026-11-07 con fonttools 4.68.0]. El `xvalue` va en coordenadas de diseño: el 500 de usuario es 480. Añade una `<instance>` por estilo.

```xml
<?xml version='1.0' encoding='UTF-8'?>
<designspace format="5.0">
  <axes elidedfallbackname="Regular">
    <axis tag="wght" name="Weight" minimum="300" maximum="700" default="400">
      <labelname xml:lang="en">Weight</labelname>
      <map input="300" output="300"/><map input="400" output="400"/>
      <map input="500" output="480"/><map input="700" output="700"/>
      <labels ordering="0">
        <label uservalue="300" name="Light"/><label uservalue="500" name="Medium"/><label uservalue="700" name="Bold"/>
        <label uservalue="400" name="Regular" elidable="true" linkeduservalue="700"/>
      </labels>
    </axis>
  </axes>
  <rules processing="last">
    <rule name="a.gruesa"><conditionset><condition name="Weight" minimum="600" maximum="700"/></conditionset><sub name="a" with="a.ss01"/></rule>
  </rules>
  <sources>
    <source filename="masters/Familia-Light.ufo" stylename="Light"><location><dimension name="Weight" xvalue="300"/></location></source>
    <source filename="masters/Familia-Regular.ufo" stylename="Regular"><location><dimension name="Weight" xvalue="400"/></location></source>
    <source filename="masters/Familia-Bold.ufo" stylename="Bold"><location><dimension name="Weight" xvalue="700"/></location></source>
  </sources>
  <instances>
    <instance familyname="Familia" stylename="Medium" postscriptfontname="Familia-Medium" filename="instances/Familia-Medium.ufo"><location><dimension name="Weight" xvalue="480"/></location></instance>
    <instance familyname="Familia" stylename="Bold" postscriptfontname="Familia-Bold" filename="instances/Familia-Bold.ufo"><location><dimension name="Weight" xvalue="700"/></location></instance>
  </instances>
</designspace>
```

**Quién crea qué** [verificado 2026-11-07 con fonttools 4.68.0]:
| Elemento | `fontmake -o variable` sin `<labels>` | Con `<labels>` y `postscriptfontname` | `gftools builder` |
|---|---|---|---|
| STAT | v1.1, **solo eje, sin AxisValue**: Font Bakery da FAIL | fmt 1 + fmt 3 en Regular → 700 | fmt 1 + fmt 3 |
| `postScriptNameID` | 0xFFFF (ausente) | Presente | Presente |
| Instancias `fvar` | Las del designspace | Las del designspace | **Las regenera**: añadió SemiBold no declarada |
| ID 25, `gasp`, `prep` | No | No | Sí |
| IDs 16/17; flags OVERLAP | **No** | **No** | **No** |

`new_project.py` escribe `<labels>`, `postscriptfontname` y el enlace RIBBI de Regular y Bold. Si añades instancias o ejes a mano, mantén los tres.

**Contradicciones con las notas:** daban por presentes las flags de solape, y ni fontmake ni gftools builder las ponen; una variable con solapes puede verse oscura en los bordes [fuente: [Glyphs](https://glyphsapp.com/learn/creating-a-variable-font)]. Además, `recom` exige IDs 16/17 en variables y ningún compilador los escribe si el defecto es Regular; `check-universal` no lo marcó.

**OVERLAP.** `build.py` lo activa en las variables tras compilar. Dos vías probadas: `public.truetype.overlap = True` en el `lib` de cada glifo, o tras compilar `setMacOverlapFlags(fuente["glyf"])` de `fontTools.varLib.instancer`. Ambas dan 0x41 en simples; la segunda da 0x404 en el primer componente, y OTS pasa [verificado 2026-11-07 con fonttools 4.68.0]. `fonttools varLib.instancer FUENTE wght=500 -o salida.ttf` activa las flags (345 simples y 2 compuestos en la prueba); con `--remove-overlaps` fusiona; una instancia parcial no las activa [verificado 2026-11-07 con fonttools 4.68.0].

**Cursiva.** Con eje `ital` discreto y `<variable-fonts>`, fontmake generó dos archivos con `fvar` solo de `wght` y STAT con `wght` e `ital` (redonda fmt 3, 0 → 1, elidible; cursiva fmt 1, valor 1) [verificado 2026-11-07 con fonttools 4.68.0]. Declara `<axis tag="ital" name="Italic" values="0 1" default="0">` con `<labels>` y un `<axis-subset name="Italic" uservalue="0"/>` por fuente, y `styleMapStyleName` (sección 5). Google no admite `ital` como variación en un archivo y Microsoft no lo espera común [fuente: GF variable, [ital](https://learn.microsoft.com/en-us/typography/opentype/spec/dvaraxistag_ital)].
**avar.** Usa `<map>` para espaciar pesos perceptivamente sin añadir másteres [fuente: GF variable; inferencia]. Si un eje tiene mapas, debe incluir −1, 0 y 1 [fuente: [avar](https://learn.microsoft.com/en-us/typography/opentype/spec/avar)]; varLib los pone (`{-1: -1, 0: 0, 1: 1}` más tus puntos) [verificado 2026-11-07 con fonttools 4.68.0].

**`.fea` variable.** Las coordenadas de feaLib son de usuario, incluso con `avar`. Es la forma que ufo2ft escribe al generar kerning. Da siempre el máster por defecto [verificado 2026-11-07 con fonttools 4.68.0].

```fea
markClass acutecomb <anchor 0 (wght=300:500 wght=400:512 wght=700:530)> @T_VAR;
feature kern { pos A V (wght=300:-10 wght=400:-20 wght=700:-40); } kern;
feature mark { pos base x <anchor (wght=300:200 wght=400:250 wght=700:300) 512> mark @T_VAR; } mark;
conditionset gruesa { wght 600 700; } gruesa;
variation rvrn gruesa { sub a by a.ss01; } rvrn;
```

**Desacuerdos.** Sufijo VF (sección 3). Familia distinta para la variable: Microsoft y Glyphs la sugieren si conviven con estáticas, Google usa una. `opsz` en STAT: formato 2 con rangos (Microsoft) o 3 (Google). Sigue a Google solo si le entregas la fuente.

## 11. Hinting

| Caso | Decisión |
|---|---|
| Titular o display | Sin hinting |
| Variable nueva | Sin hinting; prueba Windows a 100 % |
| Texto, venta general | ttfautohint con opciones probadas, o sin hinting si Windows empeora |
| Interfaz corporativa en Windows, cuerpo pequeño | VTT, presupuestado aparte |
| CFF estática | Zonas y astas con autohinter de AFDKO; revisar |

[inferencia, a partir de las notas]. macOS ignora hints [fuente: [GF](https://googlefonts.github.io/gf-docs/ReviewingFamilies/)]. FreeType v40 ignora las instrucciones horizontales y reproduce en gran parte DirectWrite [fuente: [FreeType](https://freetype.org/freetype2/docs/hinting/subpixel-hinting.html)]. **Desacuerdo sin resolver:** un resumen de Typotheque dice lo contrario sobre DirectWrite y no hay documento primario de Microsoft; da prioridad al implementador. Google publica las nuevas sin hinting. `gasp` [fuente: [gasp](https://learn.microsoft.com/en-us/typography/opentype/spec/gasp)]: 0x0001 GRIDFIT, 0x0002 DOGRAY, 0x0004 SYMMETRIC_GRIDFIT, 0x0008 SYMMETRIC_SMOOTHING; último rango 0xFFFF.

**Medido** [verificado 2026-11-07 con fonttools 4.68.0]:
- `fontmake` solo: sin `gasp` ni `prep`, y Font Bakery da FAIL «smart dropout». `gftools fix-nonhinting`: añade `gasp` {65535: 0x000F} y `prep` `PUSHW 511 SCANCTRL PUSHB 4 SCANTYPE`. Funciona en estática y variable. Crea una copia `-backup-fonttools-prep-gasp.ttf` salvo con `--no-backup`.
- `gftools builder` con `autohintTTF: false` (como lo configura `build.py`) aplica lo mismo a TTF, variable **y OTF**, que acaba con `gasp` y `prep`, tablas TrueType, en un CFF. OTS lo acepta.
- ttfautohint añade `cvt fpgm prep gasp`, deja `gasp` 0x000F y `head.flags` 0b111, sin el bit 3 que la especificación recomienda en fuentes hintadas [fuente: head].
- **`ttfautohint` acepta una variable con código 0** y conserva `gvar`, pero sin `cvar`: sus hints no siguen el eje. No lo uses en variables [inferencia sobre el efecto].
- `fontmake -a` ejecuta ttfautohint, solo en TTF. `gftools fix-gasp --set 15` no modifica el archivo: escribe `.fix` al lado.

**Contradicción:** el 0x000F que las notas daban de memoria queda confirmado, pero Google pide 0x000A para estáticas sin hinting [fuente: [GF statics](https://googlefonts.github.io/gf-guide/statics.html)]: guía y herramienta discrepan. Sigue la herramienta salvo que Google te lo pida.

```bash
$V/gftools fix-nonhinting --no-backup entrada.ttf salida.ttf
$V/python -m ttfautohint -W -n entrada.ttf salida.ttf
```

`-W` añade zonas en win para evitar recortes [fuente: [ttfautohint](https://freetype.org/ttfautohint/doc/ttfautohint.html)], `-n` no escribe en el ID 5. Según `--help`: `-a` modo de asta (defecto `qsq`), `-l` y `-r` rango, `-G` límite (200), `-x` altura x (14), `-X` excepciones, `-d` deshintar.

- **CFF.** AFDKO no está instalado: no hay `otfautohint`. `postscriptBlueValues` llega a la OTF (`[-12, 0, 510, 522, 700, 712]`), pero sin `StdVW` ni astas [verificado 2026-11-07 con fonttools 4.68.0]. Para hinting CFF real, pide permiso para instalar AFDKO y prueba `autohintOTF` en `config.yaml`, que existe en gftools y no se ejecutó.
- **VTT en variables.** Light Latin Autohinter y `cvar` manual; sin hinting bajo 9 ppem; evita compuestos volteados o escalados [fuente: [cómo hintar](https://googlefonts.github.io/how-to-hint-variable-fonts)].

## 12. Color

Hazlo solo si el brief lo pide. COLRv0 apila capas con colores de CPAL; COLRv1 añade degradados, transformaciones y composición. 0xFFFF es el color de primer plano [fuente: [COLR](https://learn.microsoft.com/en-us/typography/opentype/spec/colr)].

Soporte: Safari no tiene COLRv1 hasta 27.3/TP [fuente: [caniuse](https://caniuse.com/colr-v1)]; COLRv0 es el único formato común a los tres motores [fuente: BCD]. Por eso: base COLRv0, y siempre respaldo monocromo. Detalles de `tech()` en `07-web.md`.

`fontTools.colorLib.builder.buildCPAL([[(r, g, b, a)]])` y `buildCOLR({"a": [("n", 0), ("o", 0xFFFF)]})` generan v0 con paso de OTS; con una pintura sale v1 [verificado 2026-11-07 con fonttools 4.68.0]. Para partir de SVG, `nanoemoji --color_format glyf_colr_0`, `glyf_colr_1`, `cff_colr_0` u otros (según `--helpfull`; no se compiló una fuente con él).

## 13. QA por capas

Cada capa atrapa algo que la anterior no ve. **Que todas pasen demuestra conformidad, no belleza.**

1. Fuente: `check_sources.py`, revisión en editor (compatibilidad, contornos, extremos).
2. Compilación: `build.py`, `--con-fontc` (sintaxis, glifos ausentes).
3. Conformidad: `build.py --qa` (metadatos, STAT, tablas). 4. Navegador: OTS, dentro de `build.py`.
5. Conformación: `shape_tests.py` (reglas que compilan y no actúan). 6. Idiomas: `coverage.py`, `hyperglot`.
7. Regresión: `diffenator2`. 8. Render real: Windows 100 %, macOS, Linux, Word, navegador, papel.

Compilar no basta. **Toda regla necesita una prueba en `tests/shaping.json`.**

```bash
$V/python scripts/build.py PROYECTO --con-fontc
$V/python scripts/build.py PROYECTO --qa
$V/python scripts/shape_tests.py "fonts/variable/Familia[wght].ttf" tests/shaping.json
$V/python -m ots "fonts/variable/Familia[wght].ttf"
$V/fontbakery check-universal --ghmarkdown informe.md -l FAIL "fonts/variable/Familia[wght].ttf"
$V/ttx -q -t OS/2 -t hhea -t name -o - "fonts/variable/Familia[wght].ttf"
$V/ttx -l "fonts/variable/Familia[wght].ttf"
$V/diffenator2 diff -fb antigua.ttf -fa "fonts/variable/Familia[wght].ttf" -o difs --no-diffbrowsers
```

Todas ejecutadas [verificado 2026-11-07 con fonttools 4.68.0]. Interpretación:
- `build.py` pasa las pruebas contra la variable si existe. En estáticas no actúan las `variaciones`.
- Font Bakery devolvió código 1 también sin FAIL en `check-opentype`: lee el informe, no el código. `case_mapping` da FAIL real en un juego parcial. Avisa de que falta `shaperglot`, así que `shape_languages` del perfil de Google no corre.
- Font Validator no se mantiene; existe el fork de HinTak [fuente: [Microsoft](https://raw.githubusercontent.com/microsoft/Font-Validator/master/README.md)]. No se confirmó qué usa Google al incorporar fuentes.

| Síntoma | Causa | Corrección | Estado |
|---|---|---|---|
| Marcas sin posicionar | Sin `languagesystem`, o `public.openTypeCategories` sin bases | `check_sources.py` da ERROR; preámbulo de la sección 8 | verificado |
| Desaparece el kerning del UFO | `feature kern` a mano | Añade `# Automatic Code` | verificado |
| Kerning doble, o 0 en un peso | Manual y UFO a la vez; par ausente en un máster | Elimina una; valor en todos | verificado |
| `fi` oculta el punto en turco; fracción sin efecto con `onum` | `liga` antes de `locl`; cifras antes de `frac` | Orden de la sección 8 | verificado |
| `2 1/4` con el 2 pequeño | `frac` sobre todas las cifras | Plantilla con `rsub` | verificado |
| Ș con cedilla; `Tcommaaccent` da Ţ | Sin `locl` o sin U+0218; AGL antiguo | Ambos; `uni021A` | verificado |
| Cursiva no enlaza; instalación restringida | Sin `styleMapStyleName`; fsType 4 u 8 | UFO; `openTypeOS2Type = []` | verificado |
| Falla «Couldn't merge» o `include()` | `.fea` distinta por máster, o incluida | Una sola `features.fea` | verificado |
| Instancias mal en apps; FAIL de STAT | Sin `<labels>` | Añádelas o `gftools builder` | verificado |
| FAIL «smart dropout» | Sin `prep` | `fix-nonhinting` | verificado |
| FAIL de nombres de familia; aparece `FamiliaSC` | `feature smcp` con `buildSmallCap` activo | Sección 3 | verificado |
| Puntos oscuros en solapes | Flag ausente | Sección 10 | flag verificada; render [inferencia] |
| Acentos recortados en Windows | win pequeño | Caja + pilas | [fuente: OS/2] |
| Interlineado distinto Mac/Windows | hhea ≠ typo o flag apagada | Igualar y activar | [inferencia] |
| Falsa negrita; pesos fundidos en Office | Enlace de estilo; ID 1 compartido, ID 4 o 6 duplicado | Sección 5 | [inferencia] |
| Quiebro al interpolar; versalitas sin acentuadas | Puntos incompatibles; clase incompleta | `check_sources.py`; clases desde Unicode | [inferencia] |

## 14. Paquete final

Entrega por destinatario [inferencia]: OTF estática para impresión y maquetación (cúbicas, solapes fusionados); TTF u OTF con RIBBI para oficina; TTF variable con `HVAR` y `STAT` para apps; WOFF2 para web (`07-web.md`); TTF hintada para Windows a cuerpo pequeño.

Árbol [inferencia, adaptado de [GF upstream](https://googlefonts.github.io/gf-guide/upstream.html)]: `LICENSE.txt README.md CHANGELOG.md BRIEF.md`, `sources/` (designspace, `masters/`, `features.fea`, `config.yaml`), `fonts/` (`otf ttf variable webfonts`), `tests/shaping.json`, `proofs/`, `registro/`.

**Reproducible.** Con `SOURCE_DATE_EPOCH` fijo, dos compilaciones dieron el mismo hash, y `head.created` y `modified` tomaron ese valor [verificado 2026-11-07 con fonttools 4.68.0].

```bash
SOURCE_DATE_EPOCH=1760000000 $V/fontmake -m Familia.designspace -o variable --output-path Familia-VF.ttf
```

**Lista de salida:**
- [ ] Toda regla con prueba en `tests/shaping.json`, con y sin idioma; marcas comprobadas por posición.
- [ ] Sin FAIL no explicados en `--qa`; OTS limpio en todas las salidas; sin `FamiliaSC` no querida.
- [ ] ID 5, `head.fontRevision`, etiqueta git y changelog coinciden; `fsType` e IDs 13 y 14 según licencia.
- [ ] STAT con todos los valores, `postScriptNameID` presente y OVERLAP activado si hay solapes.
- [ ] Windows a 100 %, macOS, Word y navegador; diff con la versión anterior.
- [ ] Revisión humana firmada, auditoría de similitud y búsqueda de marca (`08-originalidad-licencias-ia.md`).

## Fuentes en Word y Office

Instala las TTF estáticas de los pesos que vayas a usar, y desinstala antes las versiones anteriores: Office trata mal las variables y el enlace de estilos depende de IDs 1/2 [inferencia, sin probar en Word]. Solo Regular y Bold (o Italic y Bold Italic) se enlazan: en Light, Medium y SemiBold, el botón B seguirá dando negrita sintética. Eso es normal, no un fallo.

`gftools builder` solo reproduce el enlace RIBBI si el designspace o el UFO traen `stylemapfamilyname` y `stylemapstylename`: sin ellos dio ID 1 `Familia Regular`. `new_project.py` los escribe y `build.py` comprueba que Regular y Bold compartan ID 1, bits y `macStyle`.
