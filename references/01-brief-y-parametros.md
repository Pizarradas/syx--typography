**Cuándo leer este archivo:** al empezar un proyecto o al cambiar de concepto, antes de dibujar el primer contorno, y siempre que debas justificar una decisión de proporción, modelo de trazo o legibilidad.

# Brief, parámetros y lógica de forma

## Contenido

1. [Cómo leer las cifras](#1-cómo-leer-las-cifras)
2. [Vocabulario de una sola definición](#2-vocabulario-de-una-sola-definición)
3. [Del brief a parámetros medibles](#3-del-brief-a-parámetros-medibles)
4. [Tablas por uso](#4-tablas-por-uso)
5. [Hoja de arranque](#5-hoja-de-arranque)
6. [Modelos de trazo](#6-modelos-de-trazo)
7. [Esqueletos](#7-esqueletos)
8. [Lógica de terminales](#8-lógica-de-terminales)
9. [Orden de trabajo](#9-orden-de-trabajo)
10. [Evidencia de legibilidad](#10-evidencia-de-legibilidad)

## 1. Cómo leer las cifras

Trata toda cifra como hipótesis de partida. Una cifra sin su prueba no sirve para decidir, porque los números publicados son pocos, se contradicen y dependen del diseño. Registra en el brief (`assets/plantilla_brief.md`) el valor inicial, el motivo y la prueba que lo confirmará.

| Etiqueta | Significa | Cuánto pesa |
|---|---|---|
| [dato] | Estudio o medición con datos | Describe lo medido; no prescribe tu diseño |
| [fuente: X] | Tutorial, autor o foro identificable | Práctica de alguien concreto |
| [convención] | Costumbre del oficio sin medición detrás | Punto de partida, nada más |
| [inferencia] | Deducción de esta investigación | Razonada, no publicada por nadie |

`(extracto)` indica que solo se vio un extracto de búsqueda, y `(foro)` que es opinión de practicante. Las tipografías comerciales se citan solo como datos medidos, nunca como objetivo: no copies sus proporciones, y menos aún sus contornos o tablas de métricas.

Varios libros canónicos no se leyeron (*The Stroke*, *Designing Type*, *Letters of Credit*, *Counterpunch*, la obra de Unger y el manual de Ahrens y Mugikura). Lo que aquí roce esas obras llega por extractos, reseñas o tutoriales: no lo cites como palabras de sus autores.

## 2. Vocabulario de una sola definición

Usa estos términos siempre en este sentido. Las fuentes no coinciden: Google Fonts separa contraste y ángulo de eje ([fuente: Google Fonts](https://fonts.google.com/knowledge/glossary/contrast)), mientras que Wikipedia los trata casi como sinónimos ([fuente: Wikipedia](https://en.wikipedia.org/wiki/Typeface_anatomy)). Aquí se separan porque son decisiones independientes: dos diseños pueden tener igual relación grueso-fino con eje distinto.

| Término | Definición única | Cómo se registra |
|---|---|---|
| **Contraste** | Relación entre las partes gruesas y finas del trazo | `grueso:fino`, p. ej. 1:1 o 3:1 [inferencia] |
| **Eje** (*stress*) | Ángulo de las partes más finas | Grados respecto a la vertical, medidos en la o [inferencia] |
| **Tipo de contraste** | Cómo nace el contraste: traslación, expansión o rotación | Una palabra, o híbrido declarado |

Regla de uso: nunca digas «contraste alto» para hablar del tipo, ni «eje» para hablar de cantidad. *Stress* es sinónimo de eje en este proyecto. Un diseño monolineal tiene contraste bajo; su eje puede quedar sin definir.

Definiciones de apoyo:

- **Altura x**: de la línea de base a la altura de la minúscula, sin ascendentes ni rebasamiento. Considera también las demás minúsculas sin asta ([fuente: Google Fonts](https://fonts.google.com/knowledge/glossary/x_height), extracto). La x sirve de referencia porque suele tener arriba y abajo planos ([fuente: Frere-Jones](https://stockholmstypografiskagille.se/typonyheter/typeface-mechanics-001/)).
- **Fracción de altura x**: altura x / cuerpo. A 1000 UPM, una altura x de 500 da 0,50.
- **Apertura**: abertura de una contraforma parcialmente cerrada (c, e, a, s). Es definición de trabajo sin fuente verificada; ninguna fuente leída la define.
- **Asta, panza, contraforma, terminal, hombro, brazo, pierna, barra, oreja, bucle, ápice y vértice**: según la anatomía estándar ([fuente: Wikipedia](https://en.wikipedia.org/wiki/Typeface_anatomy)). Contraforma cerrada en a, b, o; abierta en c, n, u. *Spur* es una pequeña proyección en un ángulo, no en un terminal. Contraste invertido significa que se intercambia qué trazos son gruesos.

**Vocabulario paramétrico.** Prefiérelo para hablar de cambios, porque nombra lo que un diseñador modifica: `XOPQ` trazo grueso, `YOPQ` trazo fino, `XTRA` anchura de contraforma, `YTLC` altura de minúscula ([fuente: Google Fonts](https://fonts.google.com/knowledge/using_type/introducing_parametric_axes)).

**Clasificación.** Vox-ATypI sigue siendo vocabulario compartido, pero la junta de ATypI lo retiró el 18 de marzo de 2021 ([fuente: ATypI](https://atypi.org/?p=1488)). El anuncio se fecha el 27 de abril según ATypI y el 21 según [Blaze Type](https://blazetype.eu/blog/voxatyp-i); da por buena la fecha de ATypI, que es la parte implicada. No se halló sustituto consensuado. Usa la clasificación para describir el resultado, nunca como dato de entrada: un rótulo como «grotesca» no te dice qué cambiar.

## 3. Del brief a parámetros medibles

### Procedimiento

1. **Responde por escrito por qué debe existir** y qué mejora frente a lo parecido; es una pregunta estándar de la crítica ([fuente: LettError](https://letterror.com/archive/badtype)). El fallo caro suele ser conceptual: un proyecto documentado duró unos 10 años sobre todo por una visión mal definida ([fuente: Clarke](https://jamieclarketype.com/blog/nave-font-story/), extracto).
2. **Fija el uso real**: medio, cuerpos, distancia de lectura, idiomas, estilos previstos y licencia. El idioma es un parámetro de diseño, porque cambia combinaciones de letras y detalles de glifo ([fuente: LettError](https://letterror.com/archive/badtype)).
3. **Convierte la exigencia en dirección** con la tabla de §4.
4. **Convierte la dirección en cantidad** con §5 y deja cada cantidad como hipótesis.
5. **Elige modelo de trazo, esqueleto y terminales** (§6 a §8). Son la lógica interna que hace original al diseño.
6. **Evalúa contra tres ejes**: funcionalidad (color uniforme, ajuste al fin, legibilidad, conjunto de caracteres), convención (familiaridad, actualidad) y calidad estética (originalidad, creatividad) ([fuente: Amado](https://typedesign.fba.up.pt/?p=571)).

### Las seis palancas

Solo la primera tiene datos masivos. Para las demás, calibra midiendo tipografías de referencia del mismo género con licencia adecuada. Mide para entender el género, no para copiar sus valores.

| Palanca | Qué se mide | Datos disponibles |
|---|---|---|
| Fracción de altura x | altura x / cuerpo | [dato] 1049 romanas: 0,28 a 0,58, media 0,46. 51 serifas de texto: 0,36 a 0,55, media 0,45 ([Legge y Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264)) |
| Asta / altura x | `XOPQ` de n / altura x | [dato] Sans regulares 13,5 a 19,8 %; sans negritas 18,9 a 40 %; mejora para baja visión con 22 a 33 % ([von Ompteda](https://researchonline.rca.ac.uk/5084/1/PhD%20von%20Ompteda%20-%20RCA%20Repository.pdf), extracto) |
| Contraste | grueso:fino | **No se halló conjunto primario por género** |
| Anchura | Anchura media / altura x | [dato] Razón media 1,03 en minúscula (Legge y Bigelow). Es media de alfabeto: ancla muy aproximada para n |
| Apertura | Hueco entre terminales de c, e, a, s [inferencia] | **No se halló conjunto primario por género** |
| Espaciado | Lado de n y o | Ver `03-espaciado-y-kerning.md` |

Las asociaciones entre personalidad y forma («seria», «amable») son [convención]. No se halló ninguna cifra autorizada, así que no las presentes como hechos. Tradúcelas a una hipótesis y compruébala con lectores o con el usuario.

### Condiciones de lectura

[dato] Según [Legge y Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264), la lectura fluida va de 0,2° a 2° de altura x, unas diez veces de rango. A 40 cm son 1,4 mm a 14 mm de altura x (4 a 40 pt). El tamaño crítico de consenso es 0,2° (estimaciones de 0,15° a 0,3°), y libros y prensa rondan 0,23° a 0,24°: el texto corriente vive cerca del límite.

Atención: esos 4 a 40 pt miden **la altura x, no el cuerpo**. La comprobación geométrica lo confirma: 1 pt son 0,353 mm, que a 40 cm subtienden unos 0,05°. La regla «grados ≈ puntos / 20» se aplica por tanto a la altura x en puntos [inferencia].

Fórmula de trabajo a 40 cm [inferencia]: `grados ≈ cuerpo × fracción / 20`. Para otra distancia, multiplica por `40 / distancia en cm`.

Ejemplo: pie de foto impreso a 8 pt. Con fracción 0,46 da 0,184°, por debajo del consenso de 0,2°. Con 0,52 da 0,208°. A 7 pt y 0,52 da 0,182°: necesita fracción mayor, más cuerpo o aceptar que queda en el borde de las estimaciones. Es un argumento para subir la altura x, no una prueba de que funcione: verifica en papel a tamaño real.

### Reparto vertical

[dato] Cerca del 87 % del negro de un alfabeto minúsculo está en la zona x, 10 % en ascendentes y 3 % en descendentes ([Legge y Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264)). Dedica el tiempo de dibujo en esa proporción: el color del texto se decide en la zona x. Esto no autoriza a recortar astas sin más, como explica §10.

## 4. Tablas por uso

### Medias medidas

Son descriptivas: dicen qué se ha hecho, no qué funciona mejor. Úsalas para situar tu hipótesis.

| Uso | Fracción media [dato] | Hipótesis derivada | Prueba |
|---|---|---|---|
| Libro de tapa dura | 0,42 | 0,42 a 0,45 para lectura larga | `proof.py --pagina texto` a 9–12 pt e impresión en papel |
| Bolsillo | 0,43 | Ídem, algo mayor si baja el cuerpo | Ídem |
| Prensa | 0,48 | Subir si el cuerpo baja | Papel de calidad real o simulada a 8–9 pt |
| Impresión adaptada a pantalla | 0,49 | Referencia intermedia | Pantalla real a tamaño real |
| Diseñada para pantalla | 0,52 | Cerca de 0,52 en interfaz | Pantalla de baja densidad y `--pagina cascada` |

Fuente de la tabla: [Legge y Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264). Los cuerpos menores usan fracciones mayores (correlación inversa de 0,71 en el censo de prensa) [dato].

### Dirección de cambio

Marca dirección, no cantidad; las cantidades salen de probar. Es [inferencia] a partir de los datos anteriores y de los ajustes para cuerpos pequeños descritos en [Just Another Foundry](https://justanotherfoundry.com/size-specific-adjustments-to-type-designs).

| Exigencia del brief | Altura x | Contraste | Anchura | Apertura | Espaciado |
|---|---|---|---|---|---|
| Cuerpo pequeño o mala reproducción | sube | baja | sube | abierta | sube |
| Lectura larga en libro impreso | 0,42 a 0,45 | moderado | moderada | moderada | moderado |
| Interfaz de pantalla | cerca de 0,52 | bajo | moderada a ancha | abierta | moderado o mayor |
| Titular | libre, a menudo menor | libre, puede ser alto | libre | libre | baja |
| Baja visión | alta | bajo | ancha | abierta | sube; asta de 22 a 33 % de x |

**Por qué estas direcciones** [inferencia]. Al reducirse la letra, los finos y los huecos son lo primero que se pierde, y la ganancia de tinta los cierra. El caso clásico de brief dictado por el medio es un diseño para guías telefónicas pensado contra la ganancia de tinta en papel prensa ([fuente: Wikipedia](https://Www.Wikipedia.org/wiki/Bell_Centennial)). Para un caso nuevo, pregunta qué se degrada primero en ese medio y qué parámetro lo protege.

## 5. Hoja de arranque

Punto de partida para una **sans de texto** a 1000 UPM. Es [inferencia] derivada de las cifras anteriores, no especificación publicada. El UPM suele ser 1000 o 2048 ([fuente: Glyphs](https://glyphsapp.com/learn/vertical-metrics)); no se halló fuente primaria para elegir.

| Parámetro | Hipótesis | Razón | Prueba que la confirma o la tumba |
|---|---|---|---|
| Altura x | 500 a 520 | Fracción 0,50 a 0,52, rango de pantalla | `noononno` y «adhesion» a tamaño real; comparar 500 y 520 lado a lado |
| Asta minúscula | 90 a 100 | 17 a 20 % de x, arriba del rango de sans regular, que acaba en 19,8 % | `--pagina texto`: gris uniforme y sin mancha a 9–12 pt |
| Asta más ligera | 75 a 90 | Sans de texto más ligera | Ídem; vigilar que no se debilite a 9 pt |
| Anchura de negro de n | unos 500 | Razón 1,03, ancla muy aproximada | `adhesion`, `minimum`: la n no debe parecer ni estrecha ni pesada |
| Rebasamiento | 10 a 15 | 2 a 3 % ([fuente: Glyphs](https://glyphsapp.com/learn/sketching)) | `HOHOHOHO` y `noononno` en `--pagina control`: alturas iguales a la vista |

Aviso de coherencia: 1,03 × 500 da 515, no 500, y las notas no precisan si esa anchura es de negro o de avance. Trátala como orden de magnitud. El extremo superior del asta sobre x de 500 (20 %) sobrepasa ligeramente el 19,8 % medido, de modo que empieza más cerca de 90 si no tienes un motivo.

Variantes [inferencia]:

| Variante | Fracción | Otros cambios | Prueba |
|---|---|---|---|
| Pie de foto | 0,52 a 0,55 | Más anchura, menos contraste, más espaciado | Papel a 7–8 pt; comparar con la regular reducida |
| Titular | 0,42 a 0,46 | Más contraste, menos espaciado | `--pagina cascada` de 36 a 96 pt |

Fija pronto, antes de los diacríticos: altura x, altura de mayúscula, ascendente, descendente, zonas de rebasamiento y el presupuesto de altura para marcas apiladas [inferencia]. Los valores de métricas verticales se calculan al final, pero un diseño muy alto o profundo debe probarse enseguida con la mayúscula acentuada más alta ([fuente: Glyphs](https://glyphsapp.com/learn/vertical-metrics)). Para calibrar: mide referencias del género, anota sus valores y decide en qué te apartas y por qué.

## 6. Modelos de trazo

El modelo decide dónde cae lo grueso y lo fino en cada glifo, y por eso da lógica interna. Noordzij evalúa las formas como trazos construidos con tres operaciones, visualizadas en su cubo ([fuente: Paldia y Čarnoký 2023](https://easychair.org/publications/preprint/WpBX)). LettError lo describe como el primer espacio de diseño conceptual, antecedente de la interpolación ([fuente: LettError](https://letterror.com/research/noordzij-cube)).

*The Stroke* no se leyó. Estas definiciones vienen de extractos y reseñas, y las fuentes no coinciden en cómo se presentó el marco: extractos de 1985 mencionan traslación y expansión como subdivisiones, y la formulación de tres contrastes aparece en textos posteriores ([extracto débil](https://www.scribd.com/document/321693104/1459761952432)). Usa el marco como herramienta, sin citarlo como texto suyo.

| Modelo | Útil | Qué predice | Dónde comprobarlo |
|---|---|---|---|
| **Traslación** | Plumilla ancha, ángulo constante | Eje inclinado; diagonales con peso distinto según dirección [inferencia] | o, e: el eje cae igual; v, x: cada diagonal pesa distinto |
| **Expansión** | Plumilla flexible, contraste por presión | Eje vertical y uniones finas [inferencia] | n, h: el hombro adelgaza al unirse; o: eje vertical |
| **Rotación** | Cambia el ángulo del útil | En la mayor parte de la escritura es efecto secundario, a menudo confundido con expansión ([fuente: Noordzij, RIDT 1991](https://typemedia.org/assets/download/The%20Shape%20of%20the%20Stroke,%20RIDT%201991,%20pp%2034-42_low.pdf), extracto) | s, a: si el ángulo gira, declara dónde y por qué |

Definiciones de útil según [reseña en Amphora](https://journals.lib.sfu.ca/index.php/amphora/article/download/2215/1625/7253) (extracto; el PDF no pudo leerse).

La secuencia histórica ayuda a situar una decisión: eje oblicuo, casi vertical y vertical ([fuente: Wikipedia](https://en.wikipedia.org/wiki/Vox-ATypI_classification)). Eso no impone el camino. Un diseño original puede inventar su útil si aplica la regla con coherencia, porque la crítica pregunta si problemas parecidos se resolvieron igual ([LettError](https://letterror.com/archive/badtype)) [inferencia].

### Plantilla de decisión [inferencia]

Decide en este orden y comprueba cada decisión en n, o, e, a, s antes de seguir:

1. **Tipo de contraste**: traslación, expansión o híbrido declarado.
2. **Ángulo**: en traslación, el ángulo de la plumilla fija el eje; más o menos inclinado desplaza el oscuro alrededor de la panza.
3. **Esqueleto**: §7.
4. **Lógica de terminales**: §8, derivada del útil.

Escribe una frase con la regla, por ejemplo: «útil de punta cortada con ángulo constante, sin rotación, terminales perpendiculares al recorrido». Si no cabe en una frase, el concepto aún no está cerrado. La frase es la prueba del sistema: cuando un glifo nuevo plantee una duda, responde aplicando la regla en lugar de buscar un modelo ajeno.

Para explorar esqueletos paramétricos, Paldia y Čarnoký proponen un parámetro llamado Contrast Tilt, pero la página resumen no lo define; no lo uses como si estuviera especificado ([preprint](https://easychair.org/publications/preprint/WpBX)).

## 7. Esqueletos

La terna humanista, racional y geométrico es una simplificación de trabajo [inferencia] construida sobre las descripciones de [Vox-ATypI](https://en.wikipedia.org/wiki/Vox-ATypI_classification). No se halló fuente citable que use «racional» exactamente en este sentido.

| Esqueleto | Rasgos | Se lleva bien con | Prueba |
|---|---|---|---|
| **Humanista** | Anchuras variables, formas abiertas; procede de capitales romanas y minúscula carolingia | Traslación | e, a, s abiertas; anchuras visiblemente distintas entre n, o, s |
| **Racional** | Anchuras regularizadas, terminales cerrados | Expansión o contraste bajo | c, e, s no se confunden entre sí a 9 pt |
| **Geométrico** | Módulos de círculo y cuadrado, formas repetidas | Monolineal o útil inventado | Corrige la geometría a ojo: `oo`, `nn`, `ee` no deben parecer de otro peso |
| **Propio** | Declarado en el brief | El que decida el concepto | Se aplica en n, o, e, a, s sin excepciones sin explicar |

La columna «se lleva bien con» es [inferencia]. Formas superelípticas: la matemática procede de Lamé y la popularizó Piet Hein ([fuente: The Brand Identity](https://the-brandidentity.com/interview/designing-in-squares-erkin-karamemet-takes-us-on-the-historical-journey-behind-his-modena-typeface)). El valor n = 2,5 viene de una fuente débil ([espejo de Wikipedia](https://wiki.riteme.site/wiki/Hypoellipse)): si lo usas, pruébalo y ajusta. Conforme un diseño se cuadra, el rebasamiento disminuye y la tensión sube (ver `02-dibujo-y-correcciones.md`).

Dave Crossland advierte contra apoyarse en *The Origin of the Serif* de Catich y sugiere lettermodel.org para entender proporciones ([fuente: TypeDrawers](https://typedrawers.com/discussion/comment/59302), foro, juicio personal). Ese recurso no se consultó.

## 8. Lógica de terminales

No se halló tratado específico sobre terminales. Lo siguiente es [inferencia], salvo donde se indica.

- **Deriva el terminal del útil**, no de un catálogo. Con traslación, el corte sigue el ángulo de la plumilla; con expansión, puede acabar en gota o bulbo. Los tipos nombrados en anatomía son cuña, bulbo, gota y losa ([fuente: Wikipedia](https://en.wikipedia.org/wiki/Typeface_anatomy)).
- **Trátalo como carga de información**. Las terminaciones de línea fueron el rasgo más importante para identificar letras en Fiset et al. 2008 [dato] (vía secundaria, [Typography.Guru](https://typography.guru/journal/what-makes-letters-legible-r37/)). Diferéncialas en lugar de uniformarlas hasta perder distinción.
- **Decide una regla por tipo de problema**: arranque de asta, fin de curva abierta (c, e, s, a), fin de diagonal, punta de t, f y r. Problemas parecidos, misma solución.
- **Ten en cuenta su efecto en la apertura**. Un terminal horizontal cierra c y e; uno perpendicular al trazo las abre. Comprueba `c e a s` a 9 pt con `--pagina texto`.
- **Reutiliza con variación controlada**: los componentes de esquina sirven para serifas y terminales (ver `02-dibujo-y-correcciones.md`).

Prueba del sistema: tapa todo salvo los terminales de `adhesion`; deberían pertenecer al mismo útil. Para originalidad, declara la lógica inventada, compruébala a nivel de sistema y compara con otras tipografías solo al final, porque imitar es un error de principiante citado ([fuente: TypeDrawers](https://typedrawers.com/discussion/comment/59302), foro).

## 9. Orden de trabajo

Síntesis de esta investigación [inferencia], no estándar publicado. Ninguna fundición consultada publica un calendario por fases, y no hay fuente sobre número de rondas de prueba.

| Fase | Trabajo | Salida comprobable | Puerta para avanzar |
|---|---|---|---|
| 0. Concepto | Brief, usos, idiomas, licencia, por qué existe | Brief fechado, referencias y su función | Respuesta escrita a «qué mejora» y primer registro de procedencia |
| 1. Prueba de concepto | n, o, H, O; luego a, d, e, h, s | `noononno`, «adhesion», prueba a tamaño real | La idea se transmite en palabras; primera auditoría de similitud |
| 2. Primer borrador | Minúscula, caja alta, cifras, puntuación | Un máster completo y espaciado grueso | Color uniforme en texto corrido; segunda auditoría |
| 3. Familia | Extremos de peso y anchura, cursiva, versalitas | Másteres compatibles, designspace | Interpolación sin quiebros en esquinas y puntos medios |
| 4. Cobertura | Diacríticos, conjunto de glifos, idiomas | Informe de cobertura, pruebas con texto real | Pruebas lingüísticas; revisor nativo si no lees la escritura |
| 5. Ingeniería | Kerning, features, métricas, nombres, hinting | Compilación reproducible en un comando | Sin fallos críticos; pruebas de conformación superadas |
| 6. Calidad | Pruebas en sistemas, papel, ofimática, navegador | Pruebas y comparaciones archivadas | Revisión humana firmada y crítica externa |
| 7. Publicación | Formatos, licencia, muestrario | Paquete versionado | Última auditoría de similitud y búsqueda de marca |

En cada iteración de las fases 1 a 3, compila con `build.py PROYECTO --rapido`, que ejecuta antes `check_sources.py` y se detiene si hay errores, y mira `proof.py fuente.ttf -o proofs/ --pagina control palabras texto`. Mirar las pruebas es obligatorio: un control automático superado demuestra conformidad, no calidad.

### Primeras decisiones

- **Papel o editor.** Desacuerdo real: Phinney recuerda una encuesta en la que aproximadamente la mitad bocetaba primero. Blokland y Adams defienden el papel; Adams porque empezar en digital suele desequilibrar las letras. Hudson y Kutilek trabajan casi siempre en el editor y juzgan a tamaño real ([fuente: TypeDrawers](https://typedrawers.com/discussion/comment/28006), foro). Por defecto [inferencia]: papel o pincel si la idea depende de la lógica de un útil; directo si el concepto es estructural o geométrico. En ambos casos, llega pronto a palabras. Razón: el agente no bosqueja, de modo que un concepto caligráfico necesita dibujos humanos de partida.
- **Palabras.** Distingue palabras de diseño como «adhesion» de palabras de prueba como «hamburgefons» ([fuente: Leonidas](https://leonidas.net/tag/transcript/), extracto). Progresión sugerida [inferencia]: n o → a d e h s → hamburgefonstiv → minúscula completa → H O → cifras.
- **Peso inicial.** Es una decisión, no un valor por defecto. Un proyecto documentado empezó por la seminegra ([fuente: Klim](https://klim.co.nz/blog/soehne-design-information/), extracto). Por defecto [inferencia]: empieza por el peso del uso principal, salvo que el concepto se lea mejor en otro.
- **Reparto con el agente.** La generación programática es fuerte en coherencia, construcción modular y compatibilidad; débil en curvas, corrección óptica y texto expresivo. El usuario aprueba n, o, H, O, a, e, g. No existe estudio controlado que compare agente y mano: es juicio razonado de esta investigación.

### Planificación

Mide el proyecto en **glifos por másteres**, no en «fuentes». Referencias autoinformadas, sin valor de tarifa: Crossland da una media de 1 a 6 meses a tiempo completo, hasta 18 de calendario; Simonson, 1 o 2 años por lanzamiento; Papazian, unas 8 horas por glifo incluido el espaciado ([fuente: TypeDrawers](https://typedrawers.com/discussion/comment/53069), foro). Esas 8 horas aplicadas a 600 glifos darían 4800 horas: es un techo que componentes e interpolación reducen mucho [inferencia]. Programa pausas: dejar reposar un boceto meses es práctica profesional ([fuente: Klim](https://klim.co.nz/blog/man-of-letters/), extracto).

## 10. Evidencia de legibilidad

Razón para leer esto: evita justificar decisiones con mitos y escribir afirmaciones falsas en un muestrario. Las cifras de esta sección son resultados de estudios, no objetivos de diseño; su última columna dice qué hacer con ellos.

### Cómo se lee

Los lectores identifican letras en paralelo y luego palabras. El reconocimiento paralelo de letras es el modelo aceptado; la forma de palabra «is no longer a viable model» y la legibilidad no debe evaluarse por la *bouma* que produzca [dato] ([Larson 2004](https://learn.microsoft.com/en-us/typography/develop/word-recognition), revisión). La superioridad de palabra aparece también con pseudopalabras, y la ventaja de 5 a 10 % de la minúscula es un efecto de práctica.

Matiz que debes conservar: en el estudio de frontera de Rayner, la combinación de forma similar y letras compartidas sí ayudó, y el propio Larson dice que eso no elimina el papel de la forma allí. No se recuperó la defensa de la visión contraria por parte de Unger.

Consecuencia: **diseña para diferenciar letras, no para producir siluetas**. El ritmo y el color uniforme siguen siendo objetivos legítimos del oficio, pero justifícalos por uniformidad y espaciado.

Datos útiles [dato] (Larson): fijaciones de 200 a 250 ms, sacádicos de 7 a 9 letras, unas 15 letras de alcance a la derecha, y los espacios entre palabras guían los sacádicos. Por eso el espacio es un glifo de diseño, no un residuo.

### Resultados y su uso

| Tema | Resultado | Límite | Qué hacer |
|---|---|---|---|
| Altura x | Mayor x mejoró todas las letras [dato] ([Cooreman y Beier 2024](https://readabilitymatters.org/?p=57664)) | Póster, muestras de 26, 12 y 12; no es lectura de pasajes | Sube x protegiendo astas |
| Altura x, desacuerdo | Ampliarla ayudó a letras de altura neutra y perjudicó a ascendentes y descendentes [dato] ([Larson y Carter 2015](https://www.microsoft.com/en-us/research/uploads/prod/2021/06/Larson-Carter-2015-Sitka.pdf), extracto) | Contradice «todas las letras» | Por defecto, sigue este resultado más cauto: comprueba h/n y b/p tras subir x |
| Anchura | Más anchas: mejor reconocimiento [dato] ([Oderkerk y Beier 2022](https://readabilitymatters.org/articles/fonts-of-wider-letter-shapes-improve-letter-recognition)) | Trigramas a 2° y 9° | Evita letras muy estrechas, sobre todo f, i, j, l, t |
| Anchura, desacuerdo | Arditi 1996 favorecía letras altas y estrechas [dato] (vía Legge y Bigelow) | Rango, tarea y posición retiniana cambian el resultado | No generalices; prueba en tu uso |
| Letras problemáticas | Las estrechas ganan al ensancharse; variantes para e, c, a, s, n, u, i, j, l, t, f ([Beier y Larson 2010](https://adk.elsevierpure.com/en/publications/design-improvements-for-frequently-misrecognized-letters), resumen) | Tamaños de efecto por letra sin verificar | Revisa esas letras primero |
| a de dos pisos | Mucho mejor que la de un piso; abrir más de lo normal la apertura podría anular la ventaja ([fuente: Bohm](https://typography.guru/journal/letters-symbols-misrecognition/), secundaria) | Secundaria | En texto, conserva dos pisos con apertura no exagerada |
| Serifas | Sin efecto en velocidad ni legibilidad a 0, 5 y 10 % de altura de mayúscula [dato] ([Arditi y Cho 2005](https://lists.w3.org/Archives/Public/w3c-wai-gl/2007JulSep/0173.html)) | Cualquier ganancia mínima viene del espaciado añadido | Decide las serifas por concepto, no por legibilidad |
| Diferencias individuales | 352 personas: 35 % de diferencia de velocidad entre su fuente más rápida y más lenta, sin efecto en comprensión; la preferencia no predijo velocidad [dato] ([Wallace et al. 2022](https://research.adobe.com/publication/towards-individuated-reading-experiences-different-fonts-increase-reading-speed-for-different-individuals)) | Fuentes corrientes, no diseños nuevos | No uses «me gusta» como prueba de legibilidad |
| Comparación por cuerpo | Comparar a igual cuerpo confunde tamaño real ([fuente: Herrmann](https://typography.guru/journal/what-makes-letters-legible-r37/)); en Sheedy et al. 2005 la mejor en pantalla tenía fracción 0,55 y la peor 0,45 [dato] (vía Legge y Bigelow) | x y otros rasgos varían a la vez | Compara a igual altura x |
| Amontonamiento | El espaciado centro a centro limita el tramo visual; un espaciado extra ancho no aumentó la velocidad [dato] (vía Legge y Bigelow) | Un estudio citado | Generoso en cuerpo pequeño, sin exceso |
| Condensado | Comprimir mucho debilita rasgos distintivos (Waller 2010, vía [Herrmann](https://typography.guru/journal/what-makes-letters-legible-r37/), secundaria) | Secundaria | Prueba en texto a tamaño real |

La revisión de Beier et al. 2025 apunta a diseños simples, contraformas abiertas, letras más anchas, x mayor y astas largas para diferenciar ([PubMed 40817624](https://pubmed.ncbi.nlm.nih.gov/40817624), solo resumen de búsqueda).

### Desambiguación

Confusiones reportadas: l/I/1/i, 1/7, B/8, D/0/O/o, i/j, cl/d, rn/m, vv/w; también S/5, Z/2, 6/9, sin estudio citado ([fuente: Bohm](https://typography.guru/journal/letters-symbols-misrecognition/), secundaria con opiniones del autor).

Recomendaciones probadas según esa fuente: serifas arriba y abajo en I, cola en l, brazo en 1, más hueco entre punto y asta en i, cola ancha en j, cero barrado o con punto. Chaparro et al. 2011: un remate inferior elevó la identificación del 1 de 43 a 97 %. No se halló estudio sobre rn/m a nivel de diseño de glifo.

Prueba: `proof.py fuente.ttf --pagina control --texto "Il1 O0 rn m cl d" --pt-control 12`. En cursiva, vigila a/o, k/R, J/f y r/v/Y (misma fuente).

### Qué se puede y qué no se puede afirmar

Tabla de esta investigación [inferencia] a partir de la evidencia anterior.

| Se puede decir | No se puede decir |
|---|---|
| «Diseñada para diferenciar caracteres, probada con X lectores» (si es cierto) | «Cura o ayuda a la dislexia» |
| «Espaciado generoso y caracteres inequívocos; elige lo que mejor te funcione» | «Más legible que X», sin un estudio propio comparable |
| «Altura x y aperturas pensadas para cuerpos pequeños» | «Las sans son más legibles que las serifas», o al revés |
| «Con buen color uniforme en las pruebas a 9–12 pt» | «Mejor forma de palabra» o «mejor *bouma*» como argumento de legibilidad |
| «Diseñada de forma independiente, con proceso documentado» | «Garantizada como única» o «científicamente probada» sin datos |

### Dislexia

Ninguna afirmación sobre dislexia debe aparecer en un muestrario.

- [dato] Kuster et al.: Dyslexie no mejoró velocidad ni precisión frente a Arial en 170 niños ([Annals of Dyslexia](https://link.springer.com/article/10.1007%2Fs11881-017-0154-6)).
- [dato] Marinus et al. 2016: 39 lectores leyeron 7 % más palabras por minuto, y el efecto desapareció al igualar el espaciado de Arial ([Dyslexia 22(3)](https://pubmed.ncbi.nlm.nih.gov/27194598/)). La eficacia vino del espaciado, no de las formas.
- [dato] Wery y Diliberto: sin beneficio de OpenDyslexic en 12 estudiantes ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5629233)). Las notas fechan este trabajo en 2016 y 2017; no se resolvió.
- No es del todo unánime: una tesis de UCL halló mayor precisión y ritmo en lectores jóvenes ([Broadbent](https://discovery.ucl.ac.uk/10173561/2/L.Broadbent%20EdD%20thesis.pdf)), y una revisión califica el conjunto de contradictorio ([AME](https://aes.amegroups.com/article/view/5209/html)).

Por defecto: oferta honesta de espaciado generoso, caracteres inequívocos y elección del lector. Motivo: es lo único que el peso de la evidencia sostiene.

Para baja visión, una tipografía conocida aplica distinción sobre uniformidad, pero no se halló estudio revisado por pares de su rendimiento ([repositorio](https://github.com/googlefonts/atkinson-hyperlegible)). Prueba siempre con personas del grupo destinatario antes de afirmar nada.
