**Cuándo leer este archivo:** al fijar el género en el brief, y otra vez antes de la fase de calidad, para saber qué pruebas exige ese género y qué partes carecen de fuente.

# Restricciones y pruebas por género

El género cambia las pruebas más que el proceso. Lee aquí lo que añade cada género a `01-brief-y-parametros.md`, `02-dibujo-y-correcciones.md` y `03-espaciado-y-kerning.md`.

Etiquetas: [dato] medición, [fuente: X] tutorial o autor, [convención], [inferencia]. `(extracto)` significa visto solo en un resumen de búsqueda.

## 1. Mapa de fiabilidad

Antes de aplicar una regla, mira de dónde viene. **Sin fuente del género** significa que la investigación no halló ninguna fuente autorizada para ese género: lo que aparece son transferencias razonadas de otros temas, marcadas como [inferencia]. No las presentes como práctica establecida.

| Género | Estado | Restricción central | Prueba decisiva |
|---|---|---|---|
| Texto | Sin fuente del género; datos generales buenos | Color uniforme a cuerpo de lectura | Párrafos en papel a 8–12 pt |
| Interfaz | Sin fuente del género; datos de pantalla y WCAG | Claridad a tamaños pequeños en pantalla | Pantalla de baja densidad, ambas polaridades |
| Titular | Sin fuente del género | Carácter a gran tamaño | Cascada de 36 a 96 pt |
| Monoespaciada | Fuentes parciales, con disputa | Avance fijo y desambiguación | Código real a 12 px |
| Señalética | Fuentes parciales; normas no recuperadas | Distancia y vistazo | Distancia real en ambas polaridades |
| Color | Fuentes técnicas; soporte cambiante | Respaldo monocromo | Tres motores |
| Script | Fuentes parciales | Alternancia determinista con `calt` | Palabras con letras repetidas |
| Marca | Fuentes de proceso parciales | Investigación, contrato | Uso real del cliente |
| Píxel | **Sin fuente** | No determinada | No determinada; ver §10 |
| Stencil | **Sin fuente** | Puentes que sobreviven al medio [inferencia] | Prueba física; ver §11 |

Tampoco se recuperaron cifras de las normas ADA, MUTCD o DIN 1450, y no se verificó el avance de 600 unidades en monoespaciadas.

## 2. Texto

**Estado:** no hubo fuente autorizada específica del género. Lo siguiente aplica datos generales.

Restricciones:

- Prioriza el color: «Even color and texture is probably the most important quality of a good text typeface» ([fuente: Monotype](https://www.myfonts.com/pages/fontscom-learning-fyti-typographic-tips-good-text-face-part-one)).
- Exige coherencia en todo el conjunto (misma fuente).
- Altura x de 0,42 a 0,45 en libro; sube en prensa, con media medida de 0,48 [dato] ([Legge y Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264)).
- Conserva la a de dos pisos y aperturas abiertas sin exagerar; evita letras muy estrechas, sobre todo f, i, j, l, t. Sube x protegiendo astas [inferencia], a partir de los estudios en `01-brief-y-parametros.md`.
- Decide las serifas por concepto: no tienen efecto apreciable en legibilidad [dato] ([Arditi y Cho 2005](https://lists.w3.org/Archives/Public/w3c-wai-gl/2007JulSep/0173.html)).
- Asume kerning apagado en Word ([fuente: Glyphs](https://glyphsapp.com/learn/localize-your-font-catalan-punt-volat)): los laterales deben aguantar solos.
- Serifa expresiva de texto: tarea de mano humana. El agente es débil en curvas y texto expresivo.

Pruebas:

| Prueba | Cómo | Criterio |
|---|---|---|
| Color | `proof.py fuente.ttf --pagina texto` y desenfoque | Sin manchas oscuras ni claras |
| Lectura en papel | Párrafo a 9–12 pt, en láser | Se lee sin esfuerzo; el juicio a 8–12 pt lo recoge [Amado](https://typedesign.fba.up.pt/?p=571) |
| Columna | Texto corrido en columna real | «Funciona en columna» ([LettError](https://letterror.com/archive/badtype)) |
| Baja resolución y luego alta | Pantalla antigua, pantalla densa, imprenta ([TypeDrawers](https://typedrawers.com/discussion/4724/what-software-do-you-test-in), extracto) | Sin pérdida de finos |
| Aplicación real de maquetación y Word | Documento con párrafos | Sin recortes; negrita correcta |

## 3. Interfaz

**Estado:** sin fuente autorizada del género. Se apoya en datos de pantalla, en WCAG y en la práctica de hinting.

Restricciones:

- Altura x cerca de 0,52, contraste bajo, anchura moderada a ancha, aperturas abiertas, espaciado moderado o mayor [inferencia], sobre una media medida de 0,52.
- Compara siempre a igual altura x, no a igual cuerpo ([fuente: Herrmann](https://typography.guru/journal/what-makes-letters-legible-r37/)).
- Prioriza la desambiguación: `Il1`, `O0`, `rn`/m ([fuente: Bohm](https://typography.guru/journal/letters-symbols-misrecognition/), secundaria).
- Las cifras de una tabla necesitan `tnum`; usa glifos nuevos y desactiva el kerning.
- Tolera el texto reespaciado. WCAG no fija tamaño mínimo, pero exige reescalar al 200 % y soportar interlineado de 1,5, 0,12 em entre letras y 0,16 em entre palabras ([1.4.4](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html), [1.4.12](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html)). Son exigencias a la página, pero la fuente no debe romperse con ellas.
- Modo oscuro: un eje `GRAD` cambia el trazo sin cambiar anchuras ([fuente: Google Fonts](https://fonts.google.com/knowledge/choosing_type/exploring_typefaces_with_multiple_weights_or_grades)). El valor de −25 viene de una fuente de iconos y no vale de forma universal para texto: pruébalo. `GRAD` no está registrado en Microsoft.
- Hinting: importa sobre todo en Windows de baja densidad. Para interfaz corporativa en Windows, presupuesta VTT aparte; para variables nuevas, sin hinting es la práctica de Google ([fuente: Google Fonts](https://googlefonts.github.io/gf-guide/hinting.html); esa URL dio 404 en otra sesión).

Pruebas:

| Prueba | Cómo | Criterio |
|---|---|---|
| Tamaños pequeños | `--pagina cascada` y `--pt-control 12` | Letras distinguibles a 8–12 pt |
| Polaridad | `--pagina oscuro` | No se adelgaza ni brilla en exceso; ajusta `GRAD` si existe |
| Desambiguación | `--pagina control --texto "Il1 O0 rn m cl d"` | Sin confusión |
| Pantalla real | Windows 1x, macOS, Linux | Lectura correcta; `proof.py` no sustituye al renderizador real |
| Espaciado WCAG | Página web con los valores anteriores | Sin solapes ni cortes |

## 4. Titular

**Estado:** sin fuente autorizada para titular ni póster.

Restricciones:

- La libertad es amplia: altura x a menudo menor (0,42 a 0,46 como hipótesis), contraste puede subir, espaciado baja [inferencia].
- Rebasamiento cerca de 10 u. sobre x de 500 ([fuente: Glyphs](https://glyphsapp.com/learn/sketching)); lados de o menores que en texto ([fuente: Glyphs](https://glyphsapp.com/learn/spacing)).
- El carácter no excusa la coherencia: la misma regla, en todas las letras.
- Las grandes tallas se optimizan para elegancia más que para legibilidad ([Larson y Carter 2015](https://www.microsoft.com/en-us/research/uploads/prod/2021/06/Larson-Carter-2015-Sitka.pdf), extracto).
- Una decisión estilística puede tomarse en nombre del buen espaciado ([fuente: Ohno](https://ohnotype.co/blog/the-process-of-ohno-blazeface), extracto).
- A gran tamaño se ven las curvas: extrema el cuidado Bézier [inferencia].

Pruebas:

| Prueba | Cómo | Criterio |
|---|---|---|
| Curvas | `--pagina cascada`, a 96 pt | Sin bultos ni quiebros |
| Kerning fino | `--texto "AVATAR Tote Yoga"` a gran tamaño | Sin huecos ni choques |
| Palabras reales | `--pagina palabras` con textos del brief | El concepto se transmite |
| Invertido | `--pagina oscuro` | Espaciado desigual controlado |
| Mayúsculas | Títulos en caja alta, con `case` si hay | ¿ ¡ « y guiones bien alineados |

## 5. Monoespaciada y código

**Estado:** fuentes parciales, con una disputa abierta. **El avance de 600 unidades no se verificó**: elige el avance por prueba, no por costumbre.

Restricciones:

- Avance fijo, incluidos acentuados y glifos de cajas [inferencia].
- Distingue 0/O, 1/l/I, `rn`/m, `{}[]()`, y la comilla invertida de la recta. Un ejemplo documentado usa x alta y cero con punto ([fuente: Rightfont](https://rightfontapp.com/family/jetbrains+mono)); es dato, no objetivo.
- Redibuja para distinguir: Butterick acepta esto aunque rechace ligaduras ([fuente: Practical Typography](https://practicaltypography.com/ligatures-in-programming-fonts-hell-no.html)).

**Desacuerdo sobre ligaduras.** Butterick las rechaza: pueden representar mal el código, chocan con Unicode (`!=` frente a `≠`) y no conocen el contexto. Una posición contraria dice que son puro renderizado y siguen siendo ASCII ([fuente: Fira Code](https://gitea.suzanne.soy/suzanne.soy/FiraCode/src/commit/c616e0dfc7b0742b847216079ecd6d2907701c1b)).

Por defecto: opcionales, desactivadas, con una versión sin ligaduras. Razón: quien no las quiere no debe recibirlas y el texto de código se copia y se revisa. Consecuencia técnica [inferencia]: HarfBuzz activa `calt` y `liga` por defecto, así que para que queden apagadas deben ir en un conjunto opcional.

Un estudio con 48 adultos con dislexia halló mejoras con estilos monoespaciados, visto vía revisión ([UCL](https://discovery.ucl.ac.uk/10173561/2/L.Broadbent%20EdD%20thesis.pdf); original no leído). No lo uses como afirmación.

La construcción es buen primer proyecto: la generación programática es madura para formas monoespaciadas.

Pruebas:

| Prueba | Cómo | Criterio |
|---|---|---|
| Avance fijo | Inspeccionar `hmtx`, salvo marcas de avance cero | Sin desviaciones |
| Desambiguación | `--pagina control --pt-control 6 --texto "0O 1lI rn m {}[]()"`, más la comilla invertida y la recta (6 pt se rasterizan a 12 px) | Sin confusión a 12 px |
| Código real | Bloques de código en editor | Columnas alineadas, sin choques |
| Sin ligaduras | Versión sin ligaduras compilada | Glifos idénticos, sin regla activa |

## 6. Señalética y orientación

**Estado:** fuentes parciales; las cifras normativas de ADA, MUTCD y DIN 1450, y los equivalentes europeos, **no se recuperaron**. No des alturas, relaciones de trazo ni contrastes normativos: consúltalos en la norma aplicable.

Hechos disponibles:

- Clearview publica versiones por contraste, positiva y negativa, seis pesos en cada una, para conductores mayores y nocturnos ([fuente: Clearview](https://www.clearviewhwy.com/home/anatomy/)).
- Sus desarrolladores alegan hasta 40 % más distancia: cifra de parte interesada.
- Un estudio de 2017 halló umbrales inferiores a Highway Gothic en todas las condiciones, pero indica que no es óptima para toda la señalización [dato] ([TRID](https://trid.trb.org/View/1438904)).
- **Conflicto normativo**: una fuente la da por aprobada ([Typographica](https://typographica.org/?p=10035)) y un resumen posterior dice que la FHWA revocó la aprobación provisional ([SAGE](https://journals.sagepub.com/doi/abs/10.3141/2624-01)). El estado actual no se confirmó. No lo presentes como vigente.

Restricciones [inferencia]:

- Aperturas amplias y contraformas grandes.
- Corrige el trazo por separado para texto invertido: claro sobre oscuro y oscuro sobre claro se leen distinto a distancia (Clearview). El texto invertido parece más fino ([fuente: Paper Mill Store](https://blog.thepapermillstore.com/design-techniques-reversed-type), extracto).
- Distingue caracteres: una señal mal leída no tiene contexto que la salve.

Pruebas:

| Prueba | Cómo | Criterio |
|---|---|---|
| Distancia real | Impresión a escala, observadores a la distancia de uso | Lectura correcta a un vistazo |
| Polaridades | `--pagina oscuro` más prueba física | Ambas igual de legibles |
| Noche o retroiluminación | Prueba física con halación | Contraformas abiertas |
| Palabras reales | `--texto` con topónimos y destinos | Identificación por letra |

`proof.py` no simula distancia ni halación. Sirve para detectar problemas gruesos, no para aprobar.

## 7. Color

**Estado:** fuentes técnicas, con soporte cambiante; compruébalo antes de decidir.

Hechos:

- Existen cuatro formatos, sbix, CBDT/CBLC, COLR/CPAL y OT-SVG, con soporte desigual ([fuente: FontLab](https://blog.fontlab.com/2026/05/03/color-fonts-in-2026/)).
- Solo 0,05–0,06 % de sitios las usan [dato] ([Almanac 2025](https://almanac.httparchive.org/en/2025/fonts)).
- Safari no tiene COLRv1 hasta 27.3/TP según [caniuse](https://caniuse.com/colr-v1), y BCD lo confirma. Fuentes secundarias decían otra cosa y ceden ante ambas. COLRv0 es el único formato común a los tres motores ([BCD](https://cdn.jsdelivr.net/npm/@mdn/browser-compat-data/data.json)). Las notas de géneros dejaban el asunto sin confirmar en noviembre de 2026: revalida.

**Desacuerdo.** FontLab sugiere WOFF2 COLRv1 más sabor SVG si importa Safari; la opción base aquí es COLRv0. Por defecto: COLRv0 con respaldo monocromo, porque es lo común a los tres motores y evita mantener dos sabores. Usa COLRv1 si el degradado lo exige y Safari no importa.

Restricciones:

- **Respaldo monocromo siempre**, seleccionable con `tech()`.
- Construye con nanoemoji ([repositorio](https://github.com/googlefonts/nanoemoji)); picosvg normaliza SVG ([repositorio](https://github.com/googlefonts/picosvg)).
- La política de Google Fonts sobre formatos de color **no se halló**.

Pruebas:

| Prueba | Cómo | Criterio |
|---|---|---|
| Respaldo | `proof.py` con la fuente monocroma | Legible sin color |
| Motores | Chrome, Firefox, Safari reales | Renderizado esperado o respaldo limpio |
| Tamaño | Peso del WOFF2 | Aceptable para el uso |

`proof.py` produce imágenes en escala de grises: no sirve para juzgar paleta ni color.

## 8. Script y manuscrita

**Estado:** fuentes parciales, centradas en OpenType. **No se halló fuente sobre diseño de conexiones.**

Restricciones:

- La lógica de posición va por `calt`, porque `init/medi/fina` no están activas por defecto en latín ([fuente: High-Logic](https://www.high-logic.com/font-editor/fontcreator/tutorials/creating-handwritten-fonts-with-contextual-alternates)).
- Alternancia determinista, no aleatoria, con rotación tipo `.between1/.between2`. Dos variantes suelen bastar (ídem). La seudoaleatoria existe desde 2005 ([fuente: Shinn](https://ilovetypography.com/2011/04/01/engaging-contextuality/)).
- `calt` debe estar activo en aplicaciones Adobe ([fuente: FontShop](https://www.fontshop.com/content/enable-contextual-alternates)). Compruébalo en cada aplicación de destino.
- Si se escribe con útil real, el dibujo humano es la base. Potrace captura mapas de bits, pero no da contornos finales ([fuente: Potrace](https://potrace.sourceforge.net/)). El agente es débil en caligrafía.

Pruebas:

| Prueba | Cómo | Criterio |
|---|---|---|
| Repetición | `--texto "llenar bebé ooo mamá"` | Sin dobles idénticos si se busca variedad |
| Conexión | `--pagina palabras` | Trazos que empalman en todos los pares frecuentes |
| Sin `calt` | Compilación o aplicación con `calt` apagado | Texto aceptable, sin rotura |
| Español | `--pagina idiomas` | Tildes y ñ no chocan con los trazos |

## 9. Marca corporativa

**Estado:** fuentes de proceso parciales. **No se hallaron el proceso completo paso a paso, presupuestos ni plazos típicos.** Nada de esto es asesoramiento jurídico.

Restricciones:

- Empieza por investigación y taller con el cliente ([fuente: Creative Bloq](https://creativebloq.com/features/the-secrets-of-custom-font-development), [Creative Review](https://www.creativereview.co.uk/dalton-maag-custom-font-bbc-reith/)).
- Propiedad: Dalton Maag declara que el cliente posee toda la propiedad intelectual tras la entrega ([fuente: Dalton Maag](https://daltonmaag.com/services/custom-font-design.html)). En España los derechos morales son irrenunciables y deben tratarse aparte.
- Contrato [inferencia]: cesión, derechos morales, exclusividad, nombre, idiomas, licencia a agencias y expediente de procedencia.
- Partir de una fuente de biblioteca es modificarla y exige permiso de la fundición [inferencia].
- Comprueba el nombre como marca antes de incrustarlo, porque cambiarlo después rompe documentos.
- Niégate a clonar. Si el cliente pide «igual que X», reformula en requisitos y dirección propios.

Pruebas:

| Prueba | Cómo | Criterio |
|---|---|---|
| Uso real | Aplicaciones del cliente: web, ofimática, señalética, redes | Funciona donde se usará |
| Idiomas | `--pagina idiomas` y revisión | Cubre el alcance pactado |
| Similitud | Auditoría de `08-originalidad-licencias-ia.md` | Sin combinación distintiva compartida |
| Sistemas | Word, PowerPoint, navegador | Enlace de estilos correcto |

## 10. Píxel y bitmap

**Estado: no hubo fuente fiable.** No se dispone de reglas sobre retículas, tamaños de píxel, antialiasing, tamaño nativo ni conversión. No inventes cifras.

Lo poco transferible [inferencia]:

- La generación programática es madura para formas de píxel: los pens de fontTools sobre ufoLib2 escriben contornos directamente. Es un buen candidato a construcción por agente.
- Haz explícito en el brief el tamaño nativo y la retícula, justificados por el uso, y regístralos como hipótesis propias.
- El requisito común sigue: `check_sources.py`, `build.py PROYECTO --rapido`, pruebas de lectura y desambiguación.

Pruebas [inferencia]:

| Prueba | Cómo | Criterio |
|---|---|---|
| Lectura | `--pagina texto` y `cascada` | Se lee al tamaño nativo |
| Desambiguación | `--texto "Il1 O0 rn m"` | Sin confusión con pocos píxeles |
| Destino real | Pantalla o soporte previsto | Sin difuminado inaceptable |

Antes de un encargo de este género, busca fuentes y documéntalas.

## 11. Stencil

**Estado: no hubo fuente fiable.** Solo hay una inferencia general: stencil y póster necesitan puentes o formas que sobrevivan al medio. **No se hallaron anchuras de puente, posiciones ni reglas.** Tampoco hay datos sobre stencil de corte físico frente a estilo de pantalla.

Lo razonable [inferencia]:

- Decide si el stencil es **funcional** (se cortará) o **estilístico**: cambia las restricciones. Solo el primero depende del material.
- Convierte los puentes en la lógica de forma: una regla en una frase, igual que el útil, aplicada a todas las contraformas cerradas.
- Vigila que un puente no borre rasgos de identificación: las terminaciones llevan carga de identificación ([Typography.Guru](https://typography.guru/journal/what-makes-letters-legible-r37/), secundaria).

Pruebas [inferencia]:

| Prueba | Cómo | Criterio |
|---|---|---|
| Contraformas | Revisión de a, b, d, e, g, o, p, q, A, B, D, O, P, Q, R, 0, 4, 6, 8, 9 | Toda isla tiene puente |
| Material | Corte físico si es funcional | Sobrevive al corte y al uso |
| Lectura | `--pagina texto` y `palabras` | Los puentes no rompen la lectura |
| Coherencia | `--pagina glifos` | La regla es visible en todo el conjunto |

## 12. Casos cercanos

- **Iconos**: entrega SVG en la web. Las críticas son de práctica, con objeciones: lectores de pantalla y anulación de fuentes ([fuente: Stop Using Icon Fonts](https://frontendfoc.us/link/104057/web)). Cerca de 54 % de sitios cargan fuentes con PUA [dato] ([Almanac 2025](https://almanac.httparchive.org/en/2025/fonts)). Si haces una, usa Unicode real cuando sea posible [inferencia].
- **Accesibilidad y baja visión**: no es un género aparte, sino un requisito. Ver evidencia y afirmaciones permitidas en `01-brief-y-parametros.md`. Prueba con personas del grupo destinatario. Promete «diseñada para diferenciar caracteres, probada con X lectores», nunca que cure nada. No se halló evaluación independiente de las tipografías de referencia en este campo.
- **Revival**: ver `08-originalidad-licencias-ia.md`; exige fuente identificada, derechos y trabajo desde impresos, nunca una digitalización ajena.
