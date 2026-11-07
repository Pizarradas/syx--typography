**Cuándo leer este archivo:** antes de espaciar el primer par de letras, cada vez que entre un grupo nuevo de glifos, y antes de tocar el kerning.

# Espaciado y kerning

Etiquetas: [dato] medición, [fuente: X] tutorial o autor, [convención], [inferencia]. `(extracto)` significa visto solo en un resumen de búsqueda y `(foro)`, opinión de practicante. Toda cifra es una hipótesis que se confirma en la prueba indicada.

## 1. Principios

- **Espaciado y dibujo avanzan juntos**, no uno detrás de otro ([fuente: RoboFont](https://www.robofont.com/documentation/tutorials/spacing-intro)). Los laterales cambian cómo se ven las formas, de modo que un dibujo sin espaciar no está evaluado.
- **El espaciado es el fallo principiante más citado** ([fuente: TypeDrawers](https://typedrawers.com/discussion/comment/59302), foro; opinión, no prueba).
- **El kerning no arregla un mal espaciado** ([fuente: RoboFont](https://www.robofont.com/documentation/tutorials/spacing-intro)). Kernear un par es tratar un caso; cambiar un lateral arregla todos los pares de esa letra.
- **Espacia al cuerpo de uso.** Trabajar con zoom produce espaciado demasiado apretado ([fuente: Glyphs](https://glyphsapp.com/learn/spacing)). Usa `proof.py fuente.ttf --pagina control --pt-control 12` para texto; el valor por defecto es 24 pt y dibuja 1 pt como 2 px.
- **Conviene que aguante sin kerning**: el kerning está desactivado por defecto en Word ([fuente: Glyphs](https://glyphsapp.com/learn/localize-your-font-catalan-punt-volat)). Revisa también el texto sin kerning: `proof.py fuente.ttf --pagina texto --feat=-kern`.
- **Una lógica común.** Todos los sistemas fijan a tamaño de lectura una recta y una redonda, propagan por forma de borde, añaden diagonales y resuelven el resto a ojo.

Recuerda el motivo perceptivo: los espacios entre palabras guían los sacádicos y el amontonamiento se rige por el espaciado centro a centro [dato] ([Larson 2004](https://learn.microsoft.com/en-us/typography/develop/word-recognition); [Legge y Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264)). El objetivo es un gris uniforme en el texto, porque el mal espaciado interrumpe el ritmo.

## 2. Siembra numérica

Siembra de [Glyphs, Spacing](https://glyphsapp.com/learn/spacing), válida para diseños de texto:

| Letra | Valor inicial | Modificadores | Prueba |
|---|---|---|---|
| o | Lados iguales, cerca de **1/3 de su contraforma** | Más en cuerpos pequeños o panzas planas; menos en titulares o panzas muy redondas | `noononno` |
| n | Cerca de **1,5 × el lado de o**, sin contar serifas | Las serifas reducen el lateral efectivo. El hombro deja espacio extra a la derecha: compensa desplazando el glifo | `noononno` |

Ejemplo [inferencia]: contraforma de o de 320 → lado de o ≈ 107 → lado de n ≈ 160. Con la n asimétrica de Briem (izquierda ≈ 14 % mayor), los 320 totales de la n se reparten en unos 170 y 150. Con una contraforma de n de 310, el hueco entre astas de nn (320) queda parecido a la contraforma.

**Es generosa a propósito.** Un tercio y 1,5× dan huecos entre astas cercanos a la contraforma [inferencia]. El tutorial acepta que lo holgado se corrige mejor que lo apretado. **No se confirmó cuánto se aleja de fuentes comerciales de texto**: espera apretar y mide contra referencias del género, solo para orientarte.

En serifa o cursiva, mide desde las astas, no desde los bordes exteriores ([fuente: RoboFont](https://www.robofont.com/documentation/tutorials/spacing-intro)). Para diseños geométricos erguidos ayuda una lógica matemática con laterales redondos iguales entre sí y menores que los planos, pero centra siempre a la vista ([fuente: Microsoft](https://learn.microsoft.com/en-us/typography/develop/character-design-standards/lowercase)).

Para mayúsculas no hay siembra numérica en las fuentes: imprime tiras de H y O a varias anchuras y elige ([fuente: Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/5-0-spacing/briem-5-03-capitals/)).

Orden recomendado por RoboFont: cadena de n → o → transferir → v → resto de minúsculas → H → O → cifras con 0 como base. Reconoce tres grupos de borde: recto, redondo y angulado (v w y x; V W Y A X).

## 3. Propagación por forma de borde

Glifo a glifo. **G** = [Glyphs](https://glyphsapp.com/learn/spacing); **B** = Briem, siguiendo a Tracy según su lectura ([minúsculas](https://help.fontlab.com/fontlab/8/tutorials/briem/5-0-spacing/briem-5-04-lower-case/), [mayúsculas](https://help.fontlab.com/fontlab/8/tutorials/briem/5-0-spacing/briem-5-03-capitals/)). «n izq.» es el lado izquierdo de n; «—» significa que la fuente no lo da; «+5–10 %» significa algo mayor que la referencia y «ojo», sin regla. La columna Decisión es el valor por defecto de esta skill, explicado en §4.

### Minúsculas

| Glifo | Izq. G | Izq. B | Der. G | Der. B | Decisión |
|---|---|---|---|---|---|
| a | — | ojo | n der. | ojo | Der. como G, luego ojo |
| b | n izq. | n izq. | o | o | Coinciden |
| c | o | o | — | o +5–10 % | Izq. o; der. +5–10 % |
| d | o | o | — | n izq. | Coincide lo dado |
| e | o | o | — | o +5–10 % | Izq. o; der. +5–10 % |
| f | — | ojo | — | ojo | Ojo, entre n y o |
| g | o | ojo | — | ojo | Izq. o como semilla; ojo |
| h | n izq. | n izq. +5–10 % | n der. | n der. | G en sans; B en serifa |
| i | n izq. | n izq. +5–10 % | — | n izq. | Ídem; der. n izq. |
| j | — | n izq. | — | n izq., medido desde el asta | B |
| k | n izq. | n izq. +5–10 % | — | mínima | Izq. como h; der. mínima |
| l | n izq. | n izq. +5–10 % | — | n izq. | Como i |
| m | n izq. | = n | n der. | = n | Coinciden |
| p | n izq. | n izq. +5–10 % | o | o | Izq. como h |
| q | o | o | — | n izq. | Coincide lo dado |
| r | n izq. | n izq. | — | mínima | Coincide; der. mínima |
| s, t, z | — | ojo | — | ojo | Ojo, entre n y o |
| u | — | n izq. | — | n der. | B |
| v, w, x, y | — | mínima | — | mínima | Mínima; v como referencia |

Las notas de RoboFont añaden v como referencia angulada. Ni Sousa ni Tracy, según un extracto, ofrecen guía para a, f, g, s, t, z, S más allá del juicio visual ([JGED](https://jged.uns.ac.rs/index.php/jged/article/download/541/615/1285), extracto).

### Mayúsculas

| Glifo | Izq. G | Izq. B | Der. G | Der. B | Decisión |
|---|---|---|---|---|---|
| B, E, F, P, R | H | H | — | ver nota | Izq. H; der. a ojo |
| D | H | H | O | O | Coinciden |
| I | H | H | H | H | Coinciden |
| K, L | H | H | — | mínima | Izq. H; der. mínima |
| M | H | H −5–10 % | H | H | Izq.: H en sans, −5 % en serifa |
| N | H | H −5–10 % | H | H −5–10 % | Ver §4 |
| U | — | H | — | H −5–10 % | B |
| C, G | O | O | — | C: ver nota; G: H −5–10 % | Izq. O; der. a ojo |
| Q | O | O | O | O | Coinciden |
| O | referencia | referencia | referencia | referencia | Tiras |
| H | referencia | referencia | referencia | referencia | Tiras |
| J | — | mínima | — | H | B; RoboFont también da J der. = H |
| A, T, V, W, X, Y | — | mínima | — | mínima | Mínima |
| S | — | ojo | — | ojo | Ojo, entre H y O |
| Z | — | ≈ 1/2 H | — | ≈ 1/2 H | B |

Nota: según Briem, el lado derecho de B, C, E, F ≈ 1/2 de H, y el derecho de P = izquierdo de O; R tiene derecha mínima. Comprobación final de Briem: hueco G-H frente a H-I, y ambos lados de Q.

Pruebas por grupo: `HAHBHCHDHEHFHGHIHJHKHLHMH`, `OAOBOCODOEOFOGOIOJOKOLOMO` (ya en `--pagina control`); `nanbncndnenfngnhninjnknlnmn`, `oaobocodoeofogohoiojokolomo`.

### Cifras, puntuación y otros

No se halló procedimiento autorizado para puntuación.

| Grupo | Regla | Origen | Prueba |
|---|---|---|---|
| Cifras | Cero como base | [fuente: RoboFont](https://www.robofont.com/documentation/tutorials/spacing-intro) | `H0H1H2H3H4`, `0n0` |
| Punto, coma, dos puntos, punto y coma | Mismo avance, centrados a la vista entre n y o | [fuente: Microsoft](https://learn.microsoft.com/en-us/typography/develop/character-design-standards/punctuation) | `n,n.n;n:n` |
| Compuestos | Heredan el espaciado del componente base | [fuente: Glyphs](https://glyphsapp.com/learn/spacing) | Comprobar `Á Ñ ü` en `--pagina idiomas` |
| Espacio | Un espacio demasiado ancho es «all too common». **No se halló cifra autorizada** | [fuente: TypeDrawers](https://typedrawers.com/discussion/comment/59302), foro | `--pagina texto`: el espacio separa sin agujerear |
| Catalán | La ela geminada se resuelve con espaciado, no con ligadura | [fuente: Glyphs](https://glyphsapp.com/learn/localize-your-font-catalan-punt-volat) | `COL·LEGI`, `paral·lel` |

Multiplicadores de la muestra de HT Letterspacer, por categoría: minúscula 1; versalita 1,4; cifras 1,2–1,5; paréntesis 1,8; comillas 3; guiones 1,5; moneda 1,6; superiores 0,8; mayúscula 2 en la muestra frente a 1,25 en el texto, incoherencia del propio tutorial. Describen una muestra de una herramienta, no proporciones universales ([tutorial](https://letterspacer.htfonts.com/tutorial/en.html)). Por defecto, mayúscula 1,25, porque es la cifra del texto explicativo; ajusta porque las mayúsculas suelen verse apretadas.

## 4. Diferencias entre Glyphs, Briem y Tracy

Conserva estas diferencias: ninguna es verdad general. La construcción serifa frente a sans explica probablemente parte de ellas, pero ninguna fuente lo afirma [inferencia].

| Punto | Glyphs | Briem / Tracy | Por defecto y por qué |
|---|---|---|---|
| N | Iguala a H en ambos lados | 5 a 10 % más estrecha | Sans: empieza en H. Serifa: −5 %, el extremo prudente del rango. Prueba `HNH` |
| Izq. de h, k, l | Igual a n | 5 a 10 % más | Sans: n. Serifa: +5 % |
| g | Izq. con o | Ojo | Semilla con o; decide a ojo |
| a | Der. igual a n | Ojo | Ídem con n |
| n | Compensar el hombro desplazando el glifo | Izq. cerca de 14 % mayor | Compatibles en sentido. Parte de lados iguales y desplaza hasta igualar `noononno` |
| J | Sin regla | J der. = H, igual que RoboFont | Sigue a Briem y RoboFont |

Tracy no se leyó. Lo atribuido llega por Briem o por un extracto, de modo que no lo cites como suyo. **Atribución sin verificar**: `HHOHH` y `nnonn` suelen atribuirse a Tracy, pero un artículo las atribuye a Kaech, que empezó con cadenas de O e I ([JGED](https://jged.uns.ac.rs/index.php/jged/article/download/541/615/1285), extracto). Di «cadenas de control», sin autor.

**Valor general**: siembra con Glyphs, refina con Briem en diseños serifa o de texto y usa HT Letterspacer o Kern On como control de coherencia cuando estén disponibles. Razón: Glyphs da números de arranque, Briem aporta matices ópticos, y una herramienta por área detecta incoherencias, no decide.

**Enlaza laterales tarde.** Las claves métricas ahorran trabajo pero pueden ocultar esas diferencias de 5 a 10 % [inferencia]. Valores fijos sumados o restados funcionan mejor, según el autor de Glyphs. Un lateral numérico es frágil entre diseños: un tercio de contraforma vale para texto.

## 5. Cadenas de prueba

`proof.py --pagina control` incluye: `nnnnnnnn`, `nnonnonno`, `noononno`, `oooooooo`, `HHHHHHHH`, `HHOHHOHH`, `HOHOHOHO`, `OOOOOOOO`, las series `nanbnc...`, `oaoboc...`, `HAHBHC...`, `OAOBOC...` y `H0H1H2H3H4 n,n.n;n:n¿n¡n`.

| Cadena | Mira | Origen | Se comprueba con |
|---|---|---|---|
| `noononno` | Todos los huecos iguales | [Glyphs](https://glyphsapp.com/learn/spacing) | `--pagina control` |
| `nnonoo`, `HHOHOO` | Seudopalabras | [Glyphs Forum](https://forum.glyphsapp.com/t/do-you-have-any-quick-spacing-tips-for-my-font-design/20871), extracto | `--texto` |
| `onono`, `OHOH` | Ritmo recta-redonda | Briem | `--texto` |
| `minimum` | Ritmo equilibrado; ahorra horas de kerning | Paulo Goode ([foro](https://typedrawers.com/discussion/comment/48290), extracto) | `--pagina palabras` |
| `n?n`, `o?o`, con `?` = letra nueva | Glifo nuevo entre referencias | [Glyphs](https://glyphsapp.com/learn/spacing) | `--texto "nanoa nsnos"` |
| `0n0`, `H0H` | Cifras frente a letras | [inferencia] | `--texto` |
| `VAND`, con N-D de referencia | Kerning en contexto | [Glyphs](https://glyphsapp.com/learn/kerning) | `--texto` |
| `T.T` frente a `TT` | Sobrekerning | [Glyphs](https://glyphsapp.com/learn/kerning) | `--texto` |
| `Il1 O0 rn m cl d` | Desambiguación | [inferencia] | `--pt-control 12` |

Comprueba siempre a tamaños reales con `--pagina texto` (9, 10,5, 12, 16 y 24 pt) y `--pagina cascada`. Trabaja con palabras reales desde un conjunto reducido: adhesiontext devuelve palabras válidas con los caracteres ya dibujados ([fuente: Leonidas](https://leonidas.net/tag/transcript/), extracto). `--pagina oscuro`: el texto invertido muestra más el espaciado desigual, así que revisa ahí el kerning ([fuente: MyFonts](https://myfonts.com/pages/fontscom-learning-fontology-level-2-display-typography-reverse-display-type), extracto).

Para ojos frescos, desenfoca o voltea ([Glyphs](https://glyphsapp.com/learn/spacing)). No se halló plantilla autorizada de pruebas.

## 6. Autoespaciado

Úsalo como control, no como juez. Disponibilidad: Glyphs es solo macOS, de modo que HT Letterspacer y Kern On no corren de forma nativa en el flujo Windows/WSL con UFO [inferencia]; no se halló puerto en las fuentes leídas.

### HT Letterspacer

Espacia por área de blanco ([tutorial](https://letterspacer.htfonts.com/tutorial/en.html)). Hipótesis de partida para texto a 1000 UPM:

| Parámetro | Valor de partida | Función | Se calibra con |
|---|---|---|---|
| `paramArea` | 200–400 | Área de blanco, en milésimas de UPM | n |
| `paramDepth` | 10–25 % de x | Profundidad de medida | o, c, v |
| `paramOver` | Sin cifra | Extiende sobre y bajo la zona x; útil en i, l, j y a, d, q | i, j, l |

Flujo: n fija el área; o y c/v, la profundidad; i/j/l, el exceso. Copia a cada máster; ejecuta; afina coeficientes por categoría, porque las mayúsculas suelen verse apretadas; revisa kerning. No es herramienta de kerning ni sustituye al juicio. El tutorial cubre la v1; la v2 es un plugin con la misma lógica. Los archivos de configuración de Glyphs 2 no valen en Glyphs 3.

Parada: compara con tu espaciado manual; donde difieran, mira `noononno` y decide. No aceptes el resultado sin mirarlo.

### Kern On (autoespaciado)

Ajusta un lateral para que un lado del glifo dé kerning cero con sus compañeros, y su «special spacing» mantiene grupos intencionadamente más holgados o apretados ([manual](https://kern-on.com/manual)). Si un par se resiste, ajusta el espaciado en lugar de forzar modelos cero.

### FontLab

FontLab 9 incluye Auto Space y Auto Kern neuronales, además de Aidus ([fuente: FontLab](https://www.fontlab.com/font-editor/fontlab-9/)). Salió el 5 de noviembre de 2026, por lo que su estabilidad no puede juzgarse, y **no se halló en las fuentes un procedimiento paso a paso, ni parámetros, ni evidencia de calidad**. Tampoco se confirmó que conserve importación y exportación UFO.

Flujo prudente [inferencia]: trabaja sobre una copia; aplica Auto Space tras fijar a mano n, o, H, O; compara con tus valores por la tabla de §3; revisa con las mismas cadenas; aplica Auto Kern después, con los umbrales de §8. Trata el resultado como propuesta y regístralo en la procedencia, ya que un resultado de IA debe declararse.

## 7. Kerning por grupos

Empieza solo cuando los laterales dejen de mejorar: cambiar el espaciado obliga a rehacer el kerning ([fuente: Glyphs](https://glyphsapp.com/learn/spacing)). Fuente principal: [Glyphs, Kerning](https://glyphsapp.com/learn/kerning).

1. **Grupos.** Cada glifo tiene grupo izquierdo y derecho. El grupo derecho de uno se empareja con el izquierdo de otro. Agrupa por forma de borde; las capitales griegas, latinas y cirílicas parecidas deben ser glifos separados porque sus grupos difieren ([fuente: Glyphs](https://handbook.glyphsapp.com/en/single-page/)). El kerning por clases mantiene los datos mucho menores ([fuente: Google Fonts](https://fonts.google.com/knowledge/glossary/kerning_kerning_pairs), extracto).
2. **Categorías, con grupos cerrados**: minúscula-minúscula, mayúscula-minúscula, puntuación con letras y cifras.
3. **Excepciones**: grupo-glifo, glifo-grupo, glifo-glifo. Abre solo el lado necesario. Una mayúscula que choca con un diacrítico minúsculo suele pedir excepción grupo-glifo.
4. **Pasada de diacríticos**, separada de la base [inferencia].
5. **Limpieza**.

Mantén un par sin kerning como referencia (nn o HH), prueba en contexto y juzga a tamaño de texto, porque el zoom lleva a kernear de más. «Kern roughly, space precisely.»

**Español** [inferencia], a partir de la RAE: cuida `¿A`, `¡T`, `«A`, y prueba en caja alta con `.case`.

**Entre redonda y cursiva**: prueba pares en la frontera ([fuente: Briem](https://blog.fontlab.com/2024/04/08/briem-bold-italic-spacing/)).

**Tabulares**: sin kerning.

**Entre escrituras**: **no se halló procedimiento fiable**. No lo inventes; pide revisión.

**Variables**: si el kerning falla en una variable, comprueba pares ausentes en másteres, añade pares cero y revisa GPOS.

## 8. Umbrales

| Umbral | Hipótesis | Origen | Si se incumple |
|---|---|---|---|
| Tope por par | No más de cerca del 40 % de la anchura del glifo | [Glyphs](https://glyphsapp.com/learn/kerning) | `T.T` puede quedar más apretado que `TT`; revisa el par |
| Valor mínimo | Unas 10 u. a 1000 UPM | [inferencia], sobre el aviso de Glyphs | Muchos pares bajo 10: vuelve a laterales |
| Pares en latín | 500 a 1500 | Glyphs, sin base declarada de conjunto de glifos | Si sobran muchos, sospecha del espaciado |
| GPOS | 64 KB | Glyphs | Quita pares pequeños, reduce excepciones grandes o usa extensión |
| Modelos Kern On | 30 a 100 por máster | [Kern On](https://kern-on.com/manual) | Ver §9 |

Las cifras de 500–1500 y 30–100 no chocan: unas son pares de salida por clases y otras modelos [inferencia]. Para conjuntos de glifos grandes **no se hallaron cifras**.

Herramientas citadas por Glyphs para comprobar: Kern-A-Lytics, Kernkraft, GapFinder, KernCrasher, Auto Bumper, Exception Cleaner. Show Group Members superpone miembros para revelar colisiones, también con diacríticos.

## 9. Flujo con Kern On

Asistente para Glyphs, no automático; plantea el kerning como eliminación de incoherencias ([manual](https://kern-on.com/manual)).

1. **Compila antes las features**: las necesita para saber qué pares kernear.
2. **Fija 30 a 100 modelos por máster**. Los modelos de valor cero controlan igual de bien.
3. Los pares automáticos se calculan desde los modelos; cambiar uno lo convierte en modelo. Los independientes se conservan sin usarse como modelo.
4. Atiende avisos: los modelos contradictorios se mueven a independientes.
5. **Másteres**: los modelos van por máster; los interpolados pueden heredar; «Autokern from» permite que una cursiva use los modelos de la redonda. En variables, todos los másteres comparten el límite de 64 kB.
6. **Finaliza** regenerando grupos con límite de kB. Cierra Kern On antes de añadir o renombrar glifos.

Practicantes informan de que a veces la causa real de un cambio sugerido eran los laterales ([fuente: TypeDrawers](https://typedrawers.com/discussion/comment/53659), extracto).

**Desacuerdo.** Glyphs presenta el kerning como trabajo manual por grupos; Kern On trata los grupos como resultado generado. Ambos flujos están vigentes: una familia documentada se presenta con kerning manual ([fuente: Klim](https://klim.co.nz/fonts/soehne/), extracto). Por defecto en WSL/UFO: grupos manuales, porque Kern On requiere Glyphs.

## 10. Variaciones de estilo

| Estilo | Regla | Origen | Prueba |
|---|---|---|---|
| Negrita | Aprieta; reduce contraformas y laterales | [Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/4-2-bold/briem-4-22-limits/), [Glyphs](https://glyphsapp.com/learn/multiple-masters-part-1-setting-up-masters) | `--pagina pesos` |
| Cursiva | Rectángulo inclinado de anchura completa (Simonson) o línea inclinada con laterales estrechos (Lozos) en el pivote; se aceptan laterales negativos | [TypeDrawers](https://typedrawers.com/discussion/1378/italics-workflow), foro | `nonon` y pares con redonda |
| Oblicua | Larabie deja la derecha un poco más apretada y recalcula por peso | Ídem | Párrafo mixto |
| Versalitas | «Un poco más» de espaciado | [Glyphs](https://glyphsapp.com/learn/making-small-caps) | `--feat smcp` |
| Tamaños pequeños | Más espaciado; el espacio de palabra suele bajar con `opsz` [dato] ([Cozens](https://simoncozens.github.io/optical-size)) | Ver `02-dibujo-y-correcciones.md` | `--pagina cascada` |
| Másteres | Recalcula, no copies: Space Bar compara másteres y Letterspacer Interpolator interpola ajustes | [Glyphs](https://glyphsapp.com/learn/spacing) | `--var wght=...` |

## 11. Orden y criterios de parada

No se halló fuente que cuantifique rondas. Los criterios siguientes son [inferencia].

| Fase | Trabajo | Parar cuando | Volver atrás si |
|---|---|---|---|
| 1 | n, o con `noononno` a tamaño de uso | Todos los huecos se ven iguales | La n o la o cambian de forma |
| 2 | H, O, y v/V como referencia angulada | `HOHOHO`, `nvnvn` a tamaño de uso son iguales | Los laterales de n u o cambian |
| 3 | Propagación por §3 | Series `nanb...` y `HAHB...` sin saltos | Un grupo entero se ve mal: revisa la referencia |
| 4 | a, f, g, s, t, z, S a ojo | `adhesion`, `minimum`, párrafo gris | |
| 5 | Cifras, puntuación, espacio | `H0H1`, `n,n.n`, texto real | |
| 6 | Control con herramienta | Las diferencias restantes están decididas | |
| 7 | Grupos y kerning por categorías | Pares clave resueltos; sin colisiones en contexto | Muchos pares bajo 10 u.: vuelve a la fase 3 |
| 8 | Excepciones y diacríticos | `--pagina idiomas` y `oscuro` limpias | Un par supera el 40 % |
| 9 | Limpieza | Dentro de 64 KB; `build.py PROYECTO --rapido` correcto | GPOS desborda |

**Parada global**: el párrafo a tamaño de uso muestra gris uniforme desenfocado, no hay parejas que salten al leer, y una pasada adicional no mejora más de lo que estropea. Un consejo de foro resume el criterio: kernea solo cuando el espaciado deje de mejorar. Deja reposar y vuelve: si sigues satisfecho con ojos frescos, cierra.

El agente da aquí un borrador de nivel medio: el ritmo final y el kerning fino son juicio humano. Entrega pruebas y lista de dudas, y no declares terminado sin aprobación.
