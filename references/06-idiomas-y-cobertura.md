**Cuándo leer este archivo:** al fijar el conjunto de glifos, al dibujar diacríticos y al preparar anclajes, marcas y pruebas para cada idioma del brief.

# Idiomas y cobertura

## Contenido

1. [Cómo leer las etiquetas](#1-cómo-leer-las-etiquetas)
2. [Qué significa dar soporte a un idioma](#2-qué-significa-dar-soporte-a-un-idioma)
3. [Niveles y conjuntos de glifos](#3-niveles-y-conjuntos-de-glifos)
4. [Herramientas de cobertura](#4-herramientas-de-cobertura)
5. [Español: requisitos y RAE](#5-español-requisitos-y-rae)
6. [Lenguas ibéricas](#6-lenguas-ibéricas)
7. [Casos de localización](#7-casos-de-localización)
8. [Lenguas indígenas americanas](#8-lenguas-indígenas-americanas)
9. [Reglas de diacríticos](#9-reglas-de-diacríticos)
10. [Cómo declarar anclajes y marcas](#10-cómo-declarar-anclajes-y-marcas)
11. [Cifras, moneda y puntuación](#11-cifras-moneda-y-puntuación)
12. [Cuándo exigir revisor nativo](#12-cuándo-exigir-revisor-nativo)
13. [Escrituras no latinas](#13-escrituras-no-latinas)

## 1. Cómo leer las etiquetas

- **[verificado 2026-11-07 con fonttools 4.68.0]**: ejecutado ese día, con Hyperglot 0.8.2, glyphsets 1.1.0, gflanguages 0.7.7, fontmake 3.12.2 y uharfbuzz 0.57.0.
- **[fuente: X]**: lo dice esa fuente; no es comprobable aquí.
- **[convención]** y **[inferencia]**: práctica sin norma, y razonamiento propio.

Los datos de Hyperglot llevan su grado: `verified`, `preliminary`, `draft`. Hyperglot los ofrece «AS IS», y los de las lenguas indígenas salen en parte de Wikipedia: son punto de partida y requieren revisión comunitaria.

En los comandos, `V=~/.local/share/type-design/venv/bin`.

## 2. Qué significa dar soporte a un idioma

El soporte es granular, no un sí o no: glifos, marcas, conformación, puntuación y formas locales son capas distintas, y puede fallar una sola, como versalitas sin una letra [fuente: [TypeDrawers](https://typedrawers.com/discussion/comment/67728)]. Un checker que pasa solo demuestra que están los caracteres. Exige las cinco capas:

| Capa | Prueba | Herramienta |
|---|---|---|
| Caracteres base | Están codificados | `coverage.py`, `hyperglot` |
| Marcas combinantes | Se posicionan sobre cada base del idioma | `shape_tests.py` |
| Formas locales | `locl` actúa con idioma y lo crítico sin él | `shape_tests.py` |
| Puntuación y moneda | Propias del idioma | `hyperglot -c punctuation,currency` |
| Lectura real | Texto corrido en el idioma | `proof.py --pagina idiomas`, lector nativo |

Declara por escrito qué ortografías probaste y cuáles están revisadas. No anuncies soporte por un pase de checker [inferencia].

## 3. Niveles y conjuntos de glifos

Son objetivos de planificación, no certificaciones.

**Adobe Latin** [fuente: [Adobe](https://raw.githubusercontent.com/adobe-type-tools/adobe-latin-charsets/master/README.md)]. Acumulativos e «informativos, no normativos».

| Nivel | Cubre |
|---|---|
| AL1 | Europa occidental, vasco, catalán sin ŀ, irlandés, suajili |
| AL2 | Mínimo para fuentes Std |
| AL3 | Mínimo Pro occidental: Europa central y oriental, turco, serbio latino, **ŀ catalana** |
| AL4 | Esperanto, maltés, maorí, vietnamita, galés, yoruba, zulú |
| AL5 | Navajo, hausa, malgache, wolof, IPA, transliteración; abierto |

**Google** medido con el paquete `glyphsets` [verificado 2026-11-07 con fonttools 4.68.0]. Discrepa de las notas en dos cifras:

| Conjunto | Glifos medidos | Con Unicode | Notas / comentario |
|---|---|---|---|
| GF Latin Kernel | 116 | 116 | Igual. Solo inglés |
| GF Latin Core | 324 | 319 | Igual |
| GF Latin Plus | 141 | 110 | Igual. Cifras, matemáticas, moneda, flechas |
| GF Latin Vietnamese | 239 | 231 | Igual. Se suma a Core |
| GF Latin PriAfrican | **177** | 177 | Las notas decían 175 |
| GF Latin African | **522** | 522 | Las notas decían 557 |
| GF Latin Beyond | 134 | 134 | Igual |

**Desacuerdo sobre GF Latin Core.** «Unos 200 idiomas» en [la guía](https://googlefonts.github.io/gf-guide/requirements.html), 27 en GLYPHSETS.md, **26 en los datos instalados** [verificado 2026-11-07 con fonttools 4.68.0]. No es que la guía mienta: una lista enumera idiomas objetivo y otra los que cubre de facto [inferencia].

**Underware Latin Plus:** 446 caracteres, 219 idiomas, con verificador en línea y exigencia alta, como IJacute [fuente: [Underware](https://www.underware.nl/latin_plus/info/)].

**Lo que GF Latin Core no trae** [verificado 2026-11-07 con fonttools 4.68.0]. Sí incluye `periodcentered.loclCAT`, `.case`, `idotaccent`, `caroncomb.alt`, ȷ, ẞ, ș ț, U+0303 y U+0326–0328. Faltan, frente a Hyperglot (`base` + `auxiliary`):

| Idioma | Faltan en Core |
|---|---|
| Catalán | Ŀ ŀ |
| Asturiano | Ḥ ḥ Ḷ ḷ |
| Rumano | Ţ ţ (auxiliares) |
| Neerlandés | Ĳ ĳ |
| Azerí norte | Ə ə ʼ |
| Guaraní paraguayo | Ĩ ĩ Ũ ũ Ẽ ẽ Ỹ ỹ ʼ |
| Náhuatl central | Ō ō Ȳ ȳ |
| Quechua | Ĉ ĉ (auxiliares) |
| Mam | Ẍ ẍ |
| Kaqchikel | ʼ |
| Mixteco de Metlatónoc | Ɨ ɨ |
| Vietnamita | 96 caracteres |

Tampoco están `◌` U+25CC, № U+2116 ni U+A78B/C. Español, gallego, vasco, portugués, aragonés, occitano, turco, polaco, lituano, aimara, mapudungun, maya yucateco y wayuu no tienen huecos.

**Objetivo por defecto** [inferencia]:
1. Base: GF Latin Core o AL3.
2. Suma el mercado hispano: Ŀ ŀ Ḥ ḥ Ḷ ḷ Ō ō Ȳ ȳ Ĩ ĩ Ũ ũ Ẽ ẽ Ỹ ỹ Ẍ ẍ Ĳ ĳ Ţ ţ, U+02BC, U+A78B/C, U+25CC, U+2116.
3. Añade vietnamita si es viable: marca el techo métrico por Ắ (`05-ingenieria-opentype.md`).
4. `.case`, tabulares, elzevirianas y versalitas si el diseño lo justifica.

## 4. Herramientas de cobertura

```bash
$V/python scripts/coverage.py FUENTE.ttf --langs spa,cat,glg,eus,ast,por
$V/hyperglot FUENTE.ttf
$V/hyperglot -c base,auxiliary -d FUENTE.ttf
$V/hyperglot-report FUENTE.ttf
$V/hyperglot -m --validity verified -o primary FUENTE.ttf
$V/glyphsets coverage FUENTE.ttf
$V/glyphsets find 'ŀ'
```

Todos ejecutados [verificado 2026-11-07 con fonttools 4.68.0]. Hyperglot tiene 806 idiomas en esta versión.

**Contradicciones con las notas:**
- Las notas decían 783 idiomas: son 806 en Hyperglot 0.8.2.
- Decían `-m union`: no existe. `-m` es `--marks` (exige todas las marcas) y no lleva argumento.
- Decían filtro por defecto `preliminary`: es `draft`.
- `-c` admite `base, auxiliary, punctuation, numerals, currency, all`; `-d` acepta base + marca en vez de precompuesto; `-o` selecciona ortografía; `-s`, estado.

**Limitaciones medidas de `coverage.py`** [verificado 2026-11-07 con fonttools 4.68.0]:
- Filtra por escritura con `--escritura`, por defecto `Latin`.
- Usa ISO de Hyperglot. **No existen** `aze`, `grn`, `aym`, `nah` ni `qxo`, y `coverage.py` los marca con `error`. Usa `azj` (azerí norte), `gug` (guaraní paraguayo), `ayr`/`ayc` (aimara), `nhn` (náhuatl central) y `que`.
- `kaz` y `tat` solo tienen ortografía cirílica en Hyperglot: las latinas no se pueden medir aquí, aunque `locl` las atienda.
- `glyphsets print-unicodes` falla con `FileNotFoundError` en esta instalación: no lo uses.

Para probar `locl` usa el código BCP 47 en `lang`: `ca tr az crh ro nl pl lt`. HarfBuzz los mapea a `CAT TRK AZE CRT ROM NLD PLK LTH`; `mo` y `ro-MD` también activaron `locl` rumano [verificado 2026-11-07 con fonttools 4.68.0]. Son los nombres del registro [fuente: [languagetags](https://learn.microsoft.com/en-us/typography/opentype/spec/languagetags)].

## 5. Español: requisitos y RAE

**No necesita `locl`:** no se encontró caso específico en las fuentes leídas, y Hyperglot (`spa`, `verified`) no lo pide. Lo que exige es dibujo y puntuación propios.

| Elemento | Caracteres | Requisito |
|---|---|---|
| Letras | Á É Í Ñ Ó Ú Ü y minúsculas | En `base` de Hyperglot [verificado 2026-11-07 con fonttools 4.68.0] |
| Signos de apertura | ¿ ¡ | Obligatorios: van donde empieza la pregunta, y omitirlos a la inglesa es incorrecto [fuente: [RAE](https://www.rae.es/dpd/signos%20de%20interrogaci%C3%B3n%20y%20exclamaci%C3%B3n)] |
| Comillas | « » “ ” ‘ ’ | En impresos, primero las angulares y las otras para anidar [fuente: [RAE](https://www.rae.es/dpd/comillas)] |
| Ordinales | ª º | Texto de la RAE sobre ellos no recuperado; `1.º` y `2.ª` llevan punto [convención] |
| Moneda | € | U+20AC, dibujado para la fuente |
| Puntuación Hyperglot | … · ° § ¶ • ′ ″ ¤ ‰ ± ÷ × ≈ ≠ | `spa`, grupos `punctuation`, `numerals`, `currency` [verificado 2026-11-07 con fonttools 4.68.0] |

El punto va tras la comilla de cierre, y el de abreviatura se mantiene ante ? [fuente: [RAE](https://www.rae.es/libro-estilo-lengua-espa%C3%B1ola/puntuaci%C3%B3n)].

**Exigencias de diseño** [inferencia, salvo la fuente citada]:
- ¿ ¡ no son ? ! girados: caen mayormente bajo la línea de base en caja baja. Ajusta el alineado óptico y dales formas `.case` para `¿QUÉ?`. El `case` de `05` ya las sustituye.
- Kerna `¿A`, `¡T`, `«A`, `A»`, `¿V`.
- La tilde de ñ debe ser de la familia y no chocar con ascendentes.
- ª º deben armonizar con `ordn` y leerse como abreviatura a tamaño de texto.
- € no se copia del logotipo de la Comisión: cada fuente necesita el suyo, como el que Microsoft redibujó [fuente: [Microsoft](https://learn.microsoft.com/en-us/typography/develop/euro)]. Parte de tu C u O, ajusta las barras a la altura de cifra y dibújalo también en tabular.

**Texto de prueba:** `¿Qué año? ¡AÑO! «Él» 1.º 2.ª pingüino CAMIÓN NÚÑEZ €20`.

## 6. Lenguas ibéricas

Datos de Hyperglot [verificado 2026-11-07 con fonttools 4.68.0]:

| Lengua | ISO | Grado | Específicas en `base` | `auxiliary` |
|---|---|---|---|---|
| Español | `spa` | verified | Á É Í Ñ Ó Ú Ü ¡ ¿ | — |
| Catalán | `cat` | verified | À Ç È É Í Ï Ò Ó Ú Ü | Ŀ ŀ |
| Gallego | `glg` | preliminary | Á É Í Ñ Ó Ú Ü | — |
| Vasco | `eus` | verified | Ñ Ü | — |
| Asturiano | `ast` | verified | Á É Í Ñ Ó Ú Ü **Ḥ Ḷ**; sin J, K, W | — |
| Portugués | `por` | verified | À Á Â Ã Ç È É Ê Í Ò Ó Ô Õ Ú | Ü ü |
| Aragonés | `arg` | verified | Á É Í Ñ Ó Ú | — |
| Occitano | `oci` | preliminary | À Á Ç È É Ë Í Ï Ò Ó Ú Ü | — |

**Contradicciones con las notas:**
- *Asturiano:* las notas decían que Ḷ Ḥ no estaban confirmadas y que el listado de [Evertype](https://evertype.com/alphabets/asturian.pdf) no las muestra. Hyperglot `verified` las pone en `base`. Inclúyelas: es barato.
- *Gallego:* las notas lo daban como español más ï, de conocimiento general. Hyperglot no lo incluye. Inclúyelo igual (ya está en Core).
- *Vasco:* las notas añadían ç para préstamos. Hyperglot no. Ninguna fuente específica lo confirma.
- *Catalán:* Ŀ ŀ quedan en `auxiliary`, de modo que `hyperglot` da soporte sin ellas con `-c base`. Inclúyelas igualmente: Adobe las exige en AL3.

Portugués y catalán prefieren una cedilla conectada; Microsoft sugiere sustitución por idioma [fuente: [Microsoft](https://learn.microsoft.com/en-us/typography/develop/character-design-standards/diacritics)]. Francés puede llevarla sin conectar.

## 7. Casos de localización

Las reglas de catalán, turco y rumano están en la plantilla `locl` de `05-ingenieria-opentype.md`, sección 8, y las de `calt` y `ccmp` también. Aquí, el porqué y lo que falta.

**Regla general.** `locl` solo actúa si la aplicación pasa el idioma, y el motor de texto de Mac lo ignoraba según el autor del tutorial [fuente: [Glyphs](https://glyphsapp.com/learn/localize-your-font-catalan-punt-volat)]. El glifo por defecto debe ser siempre aceptable y lo crítico necesita vía sin idioma [inferencia].

**Catalán: ela geminada.** La entrada es `l` U+00B7 `l` [fuente: Glyphs]. Sustituye el punto por un glifo más estrecho:
- Resuelve por espaciado, no por ligadura ni kerning: la ligadura `L_periodcentered_L.loclCAT` falla con tracking y sin idioma; el kerning falla en Word, donde va apagado por defecto [fuente: Glyphs].
- Excluye estos glifos de grupos de kerning.
- Construye `Ldot` U+013F y `ldot` U+0140 con los componentes `.loclCAT`.
- El punto se centra en altura de mayúscula en L·L y suele pedir tamaño propio [fuente: Microsoft].
- La sustitución puede romper la búsqueda en PDF [fuente: [TypeDrawers](https://typedrawers.com/discussion/comment/16136)].
- Prueba: `paral·lel`, `COL·LEGI`, y con `smcp`. Funciona con `ca`, con `es` y sin idioma gracias a `calt`; `a·b` queda intacto [verificado 2026-11-07 con fonttools 4.68.0].

**Turco, azerí, tártaro de Crimea, kazajo, tártaro.** Necesitas `dotlessi` U+0131, `Idotaccent` U+0130 y un `idotaccent` sin codificar construido con `dotlessi` + punto [fuente: [Glyphs](https://glyphsapp.com/learn/localize-your-font-turkish)]. Protege `fi`: `liga` debe ir tras `locl`.
- Con `tr`: `i` → `idotaccent`, `fi` → `f idotaccent`, `ffi` → `f_f idotaccent`, `ı` intacta, `smcp` correcto. Con `es` o sin idioma, `fi` liga [verificado 2026-11-07 con fonttools 4.68.0].
- Azerí norte (`azj`) añade Ə ə U+018F/0259 y ʼ.
- La ş turca lleva cedilla conectada de verdad: nunca la cambies por coma salvo en `ROM`/`MOL`. Con `tr`, `ş` queda intacta [verificado 2026-11-07 con fonttools 4.68.0].

**Rumano y moldavo.** Coma debajo en Ș ș Ț ț U+0218–021B; el texto antiguo usa U+015E/F y U+0162/3, por eso `locl` los convierte [fuente: [Glyphs](https://glyphsapp.com/learn/localize-your-font-romanian-and-moldovan)]. Hyperglot pone Ș Ț en `base` y Ş Ţ en `auxiliary`.
- Sin idioma, `ş` no cambia: es lo correcto para turco. Por eso U+0218–021B deben existir.
- **Desacuerdo:** para la Ţ U+0162, unos ponen la coma bajo el código de la cedilla y otros mantienen cedilla dibujada; los diseñadores rumanos se dividen, y el método coma pareció más popular en una encuesta informal [fuente: Glyphs].
- La coma también vale en K L N R T [fuente: Microsoft].

**Neerlandés: IJ acentuada.** Hyperglot pone Ĳ ĳ en `base`; Glyphs aconseja no confiar en ellos porque son compatibilidad y casi nadie los teclea [fuente: [Glyphs](https://glyphsapp.com/learn/localize-your-font-accented-dutch-ij)]. **No hay contradicción práctica:** inclúyelos y añade la regla contextual. Con `nl`, `íj` → `iacute jacute` y `ÍJ` → `Iacute Jacute`; con `es`, `íj` no cambia [verificado 2026-11-07 con fonttools 4.68.0]. Underware exige IJacute como glifo.

**Polaco: kreska.** Más inclinada que el agudo, desplazada a la derecha, centro visual bajo, y más plana sobre mayúsculas [fuente: [Twardoch](https://www.twardoch.com/download/polishhowto/kreska.html)]. Microsoft respalda el sustituto por idioma. Con `pl`, `ó` → `oacute.loclPLK` y con `es` no cambia [verificado 2026-11-07 con fonttools 4.68.0]. Añade Ó y ćńśź.

**Lituano.** La i conserva el punto ante acento [fuente: Adobe]. El `ccmp` de `05` deja sin `SIN_PUNTO` el idioma `LTH`: `i` U+0307 U+0301 queda intacto con `lt`, y sin idioma pasa a `dotlessi` [verificado 2026-11-07 con fonttools 4.68.0].

Añade este bloque tras el `locl` de `05`, y recorta los idiomas que no cubras:

```fea
feature locl {
    script latn;
    language NLD;
        lookup NEERLANDES {
            sub iacute j' by jacute;
            sub Iacute J' by Jacute;
        } NEERLANDES;
    language PLK;
        lookup POLACO { sub oacute by oacute.loclPLK; } POLACO;
} locl;
```

**Forma publicada que no compila.** El tutorial de Glyphs abre con `lookup locl_latn_1 { script latn; language CAT; ...}`. feaLib lo rechaza fuera de un `feature`. Dentro de `feature locl { }` compila y actúa solo en `ca` [verificado 2026-11-07 con fonttools 4.68.0].

**Pruebas.** Copia en `tests/shaping.json`. Ejecutadas tal cual sobre la fuente de prueba: 12/12 [verificado 2026-11-07 con fonttools 4.68.0]. Sustituye nombres si los tuyos difieren.

```json
[
  {"nombre": "catalán con idioma", "texto": "l·l", "lang": "ca", "espera_glifos": ["l", "periodcentered.loclCAT", "l"]},
  {"nombre": "catalán sin idioma", "texto": "l·l", "espera_glifos": ["l", "periodcentered.loclCAT", "l"]},
  {"nombre": "catalán mayúsculas", "texto": "L·L", "espera_glifos": ["L", "periodcentered.loclCAT.case", "L"]},
  {"nombre": "punto medio común intacto", "texto": "a·b", "espera_glifos": ["a", "periodcentered", "b"]},
  {"nombre": "turco fi", "texto": "fi", "lang": "tr", "espera_glifos": ["f", "idotaccent"]},
  {"nombre": "español fi", "texto": "fi", "lang": "es", "espera_glifos": ["fi"]},
  {"nombre": "rumano", "texto": "şţ", "lang": "ro", "espera_glifos": ["uni0219", "uni021B"]},
  {"nombre": "turco conserva cedilla", "texto": "ş", "lang": "tr", "espera_glifos": ["scedilla"]},
  {"nombre": "fracción", "texto": "1/2", "features": {"frac": true}, "espera_glifos": ["one.numr", "fraction", "two.dnom"]},
  {"nombre": "g tilde", "texto": "g̃", "espera_glifos": ["g", "tildecomb"]},
  {"nombre": "G tilde case", "texto": "G̃", "espera_glifos": ["G", "tildecomb.case"]},
  {"nombre": "neerlandés", "texto": "íj", "lang": "nl", "espera_glifos": ["iacute", "jacute"]}
]
```

## 8. Lenguas indígenas americanas

Planifícalas desde el primer día: dependen de marcas combinantes y letras modificadoras, no solo de precompuestos. Datos de Hyperglot [verificado 2026-11-07 con fonttools 4.68.0]:

| Lengua | ISO | Grado | Específicas | Apóstrofo |
|---|---|---|---|---|
| Guaraní paraguayo | `gug` | preliminary | Ã Ẽ **G̃** Ĩ Ñ Õ Ũ Ỹ | ʼ U+02BC |
| Quechua | `que` | verified | Ñ; aux. Č Ĉ Š Ž | no listado |
| Aimara central y sur | `ayr`, `ayc` | verified | Ä Ï Ñ Ü | ’ U+2019 |
| Náhuatl central | `nhn` | verified | Ā Ē Ī Ō Ū Ȳ Ü | no listado |
| Mapudungun | `arn` | preliminary | Ñ Ü | no listado |
| Wayuu | `guc` | verified | Ñ Ü | no listado |
| Maya yucateco | `yua` | preliminary | Á À É È Ó Ò Ú Ù | ' U+0027 |
| K'iche' | `quc` | preliminary | — | ' U+0027 |
| Mam | `mam` | preliminary | Ẍ | ' U+0027 |
| Kaqchikel | `cak` | preliminary | Ä Ë Ï Ö Ü | ʼ U+02BC |
| Tzotzil | `tzo` | verified | — | ’ U+2019 |
| Zapoteco | `zap` | verified | Á À È É Ë Ì Ü y marcas ◌̨ ◌̌ | no listado |
| Otomí del Mezquital | `ote` | preliminary | Ã Ï Ö Ü y marca U+0331 | no listado |
| Mixteco de Metlatónoc | `mxv` | preliminary | Ñ Ɨ ɨ | ' U+0027 |

**Contradicción con las notas e informe.** Sostenían que las eyectivas apuntan a U+02BC como letra. La opción es correcta en Unicode: U+02BC es letra (Lm) y U+2019 puntuación [fuente: [Wikipedia](https://www.wikiwand.com/en/articles/Modifier_letter_apostrophe)]. Pero los datos muestran tres caracteres según la lengua: U+02BC, U+2019 y U+0027. **Trata los tres como apóstrofo de lengua:** forma de apóstrofo, y kerning y espaciado que funcionen entre letras. No alteres bases para fingir eyectivas [inferencia].

**Guaraní.** G̃ no tiene precompuesto: es G o g + U+0303, y los usuarios caen en ĝ o la omiten si la fuente falla [fuente: [Wikipedia](https://www.wikipedia.org/wiki/G%CC%83)]. Lo que la hace funcionar son los anclajes `top` en g y G y la marca `_top`, no un glifo. Con el `ccmp` de `05`, `G`+U+0303 usa `tildecomb.case` con desplazamiento −310 y `g`+U+0303, −250 [verificado 2026-11-07 con fonttools 4.68.0].

**Quechua y aimara.** Eyectivas con apóstrofo (p', t', ch', k', q'), aspiradas con h. Perú adoptó alfabeto en 1975 y tres vocales en 1985; hay diccionarios con cinco. Ecuador y Bolivia usan j donde va h [fuente: [Wikipedia](https://en.wikipedia.org/wiki/Quechuan_and_Aymaran_spelling_shift)]. Prueba los dígrafos `p' t' ch' k' q'` con los tres apóstrofos.

**Náhuatl.** Macrones en la ortografía neoclásica; saltillo como h, o U+A78B/C. Carochi usó macrones con grave y circunflejo. Muchas ortografías no marcan ninguno [fuente: [Wikipedia](https://en.wikipedia.org/wiki/Nahuatl_orthography)]. Hyperglot no incluye el saltillo; las notas lo documentan desde Unicode 5.1, en uso por ejemplo en tlapaneco, con forma recta por defecto [fuente: [Wikipedia](https://en.wikipedia.org/wiki/Saltillo_(linguistics))]. Incluye U+A78B/C.

**Sin revisar.** Normas INALI y alfabeto oficial aimara no se leyeron. Las lenguas mayas, mapudungun, zapoteco, otomí y mixteco de esta tabla vienen solo de Hyperglot, y en `preliminary` puede haber errores. Hay muchas ortografías por variante: pregunta qué comunidad es el público.

## 9. Reglas de diacríticos

Los diacríticos pertenecen a la construcción de la fuente. Diséñalos en este orden [inferencia]: agudo, grave, circunflejo, carón, tilde, diéresis, anillo, macrón, breve y punto como una familia; luego `.case`; luego excepciones por idioma; por último pilas `mkmk`.

**Generales** [fuente: [GF](https://googlefonts.github.io/gf-guide/diacritics.html)]:
- Misma construcción, contraste, terminales e inclinación que la letra.
- Formas relacionadas parecidas, y sin cambiarlas entre sí: un breve no es un carón.
- Misma distancia a la base; centrado en el centro óptico.
- Muy cerca crea manchas; muy lejos se separa.

**Medidas** [fuente: [Microsoft](https://learn.microsoft.com/en-us/typography/develop/character-design-standards/diacritics)]:
- Hueco sobre el rebasamiento de minúscula: 5–10 % del em, típico. Palatino 130 unidades sobre o y 98 sobre O (a 2048); Georgia 96 y 54.
- En mayúsculas va más cerca.
- Agudo: 1/3 del negro a la izquierda del eje, 2/3 a la derecha; grave, espejo. Luego ajusta a ojo.

**`.case`.** Históricamente, los acentos de mayúscula eran más cortos y robustos; un solo juego es un compromiso [fuente: Microsoft]. Dibuja marcas `.case` sobre la altura de mayúscula [fuente: [Glyphs](https://glyphsapp.com/learn/diacritics)].

**Formas específicas:**

| Forma | Regla | Fuente / desacuerdo |
|---|---|---|
| Ogonek | Parte del glifo, no acento; llega a la línea de descendentes; nunca excede el borde derecho; en A sale del asta o serifa interior | Twardoch. **Desacuerdo:** en e cerca del borde derecho (Twardoch), algo a la derecha del centro (Microsoft) |
| Carón vertical | Ľ ľ ď ť, cuña estrecha «no una coma ni apóstrofo curvo», nombre `caroncomb.alt` | GF. **Desacuerdo:** Microsoft prefiere el apóstrofo en d y t. Sigue a GF, más explícito |
| Coma debajo | Ș ș Ț ț; válida en K L N R T | Microsoft |
| Cedilla | Cuelga de la línea base; conectada en turco | Glyphs, Microsoft |
| Tilde y circunflejo de espaciado | Algo mayores y bajos que los combinantes | Glyphs |
| Punto | El mismo en i, j, ė, ċ, ż | Glyphs |
| Marca de pila vietnamita | `.case` más anchas, cortas y planas; anclaje propio tipo `top_viet` | GF |

**Vietnamita.** Precompuestos U+1EA0–1EF9 más Ă ă Đ đ Ĩ ĩ Ũ ũ Ơ ơ Ư ư, y mantén marcas y anclajes para texto NFD: U+0300, 0301, 0303, 0309, 0323, 0302, 0306, 031B. Las pilas genéricas chocan: necesitan diseño propio [inferencia]. No se leyó ninguna fuente nativa sobre posición de tonos. Prueba `Ắ Ặ Ỗ Ẫ` bajo interlineado apretado.

Respeta al lector: «Disregarding the reader's habits ends up being counterproductive» [fuente: [Alphabettes](https://www.alphabettes.org/language-as-design-criteria-part-iii/)]. Recursos: Diacritics Project de Blažek, *Manual of Diacritics*.

## 10. Cómo declarar anclajes y marcas

Escribe anclajes en el UFO: ufo2ft genera `mark`, `mkmk` y mark-to-ligature, y varían por máster. Requisitos previos en `05-ingenieria-opentype.md` sección 7: `languagesystem` en `features.fea`, y `public.openTypeCategories` ausente o completo.

| Anclaje | Va en | Genera |
|---|---|---|
| `top`, `bottom` | base | mark-to-base con `_top`, `_bottom` |
| `_top`, `_bottom` | marca | clase de marca |
| `top` + `_top` | marca | mark-to-mark (`mkmk`), pilas |
| `top_1`, `top_2` | ligadura | mark-to-ligature |
| `ogonek` + `_ogonek` | base + marca | Clase propia: cualquier nombre sirve |

Con `ogonek`/`_ogonek`, `a`+U+0328 se posicionó, y `b`, sin ese anclaje, no [verificado 2026-11-07 con fonttools 4.68.0]. Las notas sugieren `top_viet` [fuente: GF]: es este mismo mecanismo, aunque no se probó ese nombre.

**Con ufoLib2**, en el generador. Ejecutado [verificado 2026-11-07 con fonttools 4.68.0]:

```python
from pathlib import Path

import ufoLib2

X, CAP, DESC = 500, 700, -200
fuente = ufoLib2.Font()
fuente.info.unitsPerEm = 1000

g = fuente.newGlyph("g")
g.width = 520
g.unicodes = [0x67]
g.appendAnchor({"name": "top", "x": 260, "y": X + 12})
g.appendAnchor({"name": "bottom", "x": 260, "y": DESC})

G = fuente.newGlyph("G")
G.width = 680
G.unicodes = [0x47]
G.appendAnchor({"name": "top", "x": 340, "y": CAP + 12})

tilde = fuente.newGlyph("tildecomb")
tilde.width = 0  # Toda marca combinante lleva avance 0.
tilde.unicodes = [0x303]
tilde.appendAnchor({"name": "_top", "x": 0, "y": X + 12})
tilde.appendAnchor({"name": "top", "x": 0, "y": X + 200})  # Permite apilar otra marca encima.

tilde_case = fuente.newGlyph("tildecomb.case")
tilde_case.width = 0
tilde_case.appendAnchor({"name": "_top", "x": 0, "y": CAP + 12})
tilde_case.appendAnchor({"name": "top", "x": 0, "y": CAP + 130})

circulo = fuente.newGlyph("uni25CC")  # Soporte de marcas sueltas: lleva todos los anclajes.
circulo.width = 500
circulo.unicodes = [0x25CC]
circulo.appendAnchor({"name": "top", "x": 250, "y": X + 12})
circulo.appendAnchor({"name": "bottom", "x": 250, "y": 0})

fuente.save(Path("prueba_anclajes.ufo"), overwrite=True)
```

**Cómo queda en el `.glif`** (salida real del código anterior, sin contorno):

```xml
<?xml version='1.0' encoding='UTF-8'?>
<glyph name="tildecomb" format="2">
  <unicode hex="0303"/>
  <anchor x="0" y="512" name="_top"/>
  <anchor x="0" y="700" name="top"/>
  <outline>
  </outline>
</glyph>
```

**Reglas:**
- El mismo conjunto de anclajes en todos los másteres. `check_sources.py` da ERROR si difieren: forman parte de la firma de compatibilidad.
- Coloca `_top` donde la marca debe tocar el anclaje de la base, no en su origen.
- Da avance 0 a las marcas: HarfBuzz lo anula con clase GDEF, pero `hmtx` conservaría otro valor [verificado 2026-11-07 con fonttools 4.68.0].
- Los compuestos no heredan anclajes: si admites marca sobre `á`, añádelos a mano o genéralos [verificado 2026-11-07 con fonttools 4.68.0].
- Incluye U+25CC con todos los anclajes [fuente: GF]. Con `top`, `◌`+U+0301 se posicionó.
- Combina: precompuesto para lo que el idioma necesita + marcas y anclajes para el resto [inferencia].
- i y j sin punto ante marca superior, por `ccmp` [fuente: GF]. Plantilla en `05`.

**Por qué importa `languagesystem`.** Sin kerning, HarfBuzz recurre a `DFLT` y las marcas se mueven; en cuanto hay un solo par de kerning, una fuente con anclajes correctos y sin `languagesystem` deja `x`+U+0301 sin mover. `new_project.py` lo incluye y `check_sources.py` da ERROR si falta. `espera_glifos` no mira posiciones: usa `"marca_movida": true` en `tests/shaping.json`, o este script para una comprobación detallada, que falló sin `languagesystem` y pasó con él [verificado 2026-11-07 con fonttools 4.68.0]:

```python
import uharfbuzz as hb

cara = hb.Face(hb.Blob.from_file_path("fonts/variable/Familia[wght].ttf"))
fuente = hb.Font(cara)
buf = hb.Buffer()
buf.add_str("g\u0303")
buf.guess_segment_properties()
hb.shape(fuente, buf, {})
assert buf.glyph_positions[1].x_offset != 0, "la marca no se posiciona"
```

## 11. Cifras, moneda y puntuación

- `tnum` debe llevar € y $ con el mismo avance que las cifras [inferencia].
- `1.º`, `2.ª` y la fracción mixta `2 1/4`: plantillas `ordn` y `frac` en `05`.
- El griego usa `;` como interrogación, y su punto y coma es un punto alto [fuente: [TypeTogether](https://www.type-together.com/greek-type-anatomy)].
- Latin Plus añade cifras, matemáticas, moneda, flechas y viñetas [fuente: GF requirements].
- No se encontró fuente autorizada sobre cifras tabulares o de moneda, ni la lámina de construcción del euro de la Comisión. Las reglas de espacio de no separación y colocación del euro solo aparecieron en páginas SEO: quedan fuera.

## 12. Cuándo exigir revisor nativo

Exígelo, remunerado y acreditado, desde el inicio y no como comprobación final, en estos casos [inferencia, a partir de las fuentes de la sección siguiente]:

| Caso | Requisito |
|---|---|
| Cualquier escritura que el equipo no lee | Revisor nativo o, si no, etiqueta «sin revisar» |
| Lenguas indígenas anunciadas como soporte | Hablante o institución de esa comunidad y esa ortografía |
| Rumano, vietnamita, polaco o checo anunciados como soporte de calidad | Lector nativo de las formas específicas |
| Datos en `preliminary` o `draft` | Comprobar con fuente primaria o comunidad |
| Encargo institucional o educativo | Contrato con la revisión incluida |

Basta el proceso normal para español, catalán, gallego y portugués si un hablante del equipo lee las pruebas [inferencia].

**Ética mínima** [inferencia]: crédito y retribución acordados antes de empezar; pruebas con lectores; no inventar formas «expresivas» latinizando. **El agente no sustituye al revisor:** etiqueta lo que produzca en una escritura no latina como no revisado.

Lo que dicen las fuentes: los lectores nativos tienen un ojo que a un no nativo le lleva años [fuente: [Commarts](https://www.commarts.com/columns/multilingual-scripts)]; colabora con diseñadores o calígrafos nativos y prueba con textos nativos [fuente: [Jolicia Type](https://joliciatype.com/designing-fonts-without-borders-a-complete-guide-to-creating-multilingual-multi-script-typefaces/)]; Sharp Type hace que sean «the filter» [fuente: [Print](https://www.printmag.com/type-tuesday/sharp-type-season-two/)]; debe haber un hablante nativo en cliente y equipo [fuente: [Futuress](https://futuress.org/stories/letters-words-stories/)].

## 13. Escrituras no latinas

«Similar letters are just that — similar, but not the same», y los lectores nativos «will always be able to tell» [fuente: [TypeTogether](https://www.typetogether.com/multiscript-typography-guide)]. Igual cuerpo y grosor no dan igual tamaño ni peso visual. Empieza por la escritura más compleja.

| Escritura | Requisitos conocidos | Fuente |
|---|---|---|
| Griego | Minúscula no comparte forma con latina: «a misconception borne of poor research, bad design process» | [Leonidas](https://leonidas.net/greek-type-design/typophile-greek-type-design-standards/) |
| Griego, tonos | **Desacuerdo:** idéntico al agudo (obras griegas) o mayor y más vertical (foro) | [Leonidas](https://medium.com/@gerryleonidas/designing-greek-typefaces-eac0de7767cc), [TypeDrawers](https://typedrawers.com/discussion/comment/16686) |
| Cirílico | Formas bulgaras y serbias por `locl` | [features_ko](https://learn.microsoft.com/en-us/typography/opentype/otspec150/features_ko) |
| Griego, latino, cirílico | Mayúsculas parecidas en glifos separados: sus grupos de kerning difieren | [Glyphs](https://handbook.glyphsapp.com/en/single-page/) |
| Hebreo | Mark-to-base; unicase: tamaño entre x y mayúscula junto al latín | FontForge, TypeTogether |
| Devanagari | Reserva interlínea; conjuntos por conformación; ra en cuatro formas | TypeTogether, ISO/IEC TR 15285 |
| Árabe | Más de cuatro formas por letra, alternantes contextuales, kerning RTL | [FontLab](https://blog.fontlab.com/2025/09/02/beyond-the-latin-sandbox-global-typography/), FontForge |
| CJK | Decenas de miles de glifos frente a unos 500 en latín | FontLab |

Hyperglot tiene comprobaciones de conformación limitadas: solo para hindi/devanagari en conjuntos [fuente: [Hyperglot](https://github.com/rosettatype/hyperglot)], y no evalúa diseño. Google tiene conjuntos con `glyphsets`: GF_Greek_Core, GF_Cyrillic_Core, GF_Arabic_Core, además de Plus, Pro y Expert donde existen [verificado 2026-11-07 con fonttools 4.68.0]. No existe Pro para latín [fuente: GLYPHSETS.md], y la lista instalada lo confirma.

Sin revisor no hay soporte: declara «no revisado por lector nativo» en la documentación y no lo anuncies.
