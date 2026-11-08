# Originalidad, licencias e IA

Léelo cuando pidan copiar o parecerse a una fuente, cuando dibujes contornos por código, en cada auditoría de similitud y antes de elegir licencia, publicar o hacer una afirmación pública.

**Esto no es asesoramiento jurídico.** El derecho es territorial y cambia. Datos jurídicos revisados hasta el 7-11-2026, en parte por fuentes secundarias, con enlace junto a cada dato y su fecha cuando la fuente la da. Antes de una decisión comercial, un abogado del país debe confirmarlo. Tú orientas y documentas: nunca dictamines que algo «es legal», «no infringe» o «está protegido».

Etiquetas: `[dato legal: fuente]` norma o resolución según esa fuente; `[fuente: X]` otro dato; `[propuesta de esta skill]` regla de trabajo, sin valor de estándar; `[inferencia]` razonamiento propio.

## Contenido
[Peticiones que reorientar](#peticiones-que-debes-reorientar) · [Revivals](#revivals-legítimos) · [Procedencia](#protocolo-de-procedencia) · [Auditoría](#auditoría-de-similitud) · [Mapa jurídico](#mapa-jurídico-por-territorio) · [Calendario UE y España](#calendario-de-la-ue-y-orden-en-españa) · [Licencias](#licencias) · [Venta](#venta-y-canales) · [IA: estado](#ia-estado-del-terreno) · [IA: este agente](#ia-el-trabajo-de-este-agente) · [Comunicación pública](#comunicación-pública) · [Sin verificar](#estados-sin-verificar)

## Peticiones que debes reorientar
La línea legal y la ética no coinciden, y el oficio sostiene la más estricta. El antiguo Code Morale de ATypI consideraba contrario a la ética reproducir la tipografía de otro miembro «identical or slightly modified»; se retiró en 2004 sin sustituto y se conoce por un foro que cita documentos [fuente: TypeDrawers, secundaria](https://typedrawers.com/discussion/comment/45141). Google Fonts exige que el diseño sea original o un revival legítimo de dominio público [fuente: GF Guide](https://googlefonts.github.io/gf-guide/onboarding). Trabaja con la regla estricta aunque en un país concreto la copia pudiera no ser ilícita, porque esta skill promete originalidad [propuesta de esta skill].

Responde en tres pasos: di qué no harás, da el motivo en una frase y ofrece enseguida un camino original. Sin sermón: quien pide «algo como X» casi siempre quiere una cualidad de X, no sus puntos.

| Petición | Qué haces | Por qué | Alternativa |
|---|---|---|---|
| Clonar una fuente | Rechaza | Reproducir el diseño, aunque cambie un poco, es lo que el oficio rechaza | Extrae función y cualidades, y escribe un brief propio |
| Calcar, autotrazar o vectorizar un espécimen de obra con derechos | Rechaza | Copia la forma con independencia de la herramienta | Dibujar desde el esqueleto y la lógica de trazo del brief |
| Partir de un `.ttf`, `.otf` o `.ufo` ajeno | Rechaza, tenga o no licencia de uso | Una licencia de uso no autoriza derivar. En *Adobe*, extraer puntos copió expresión literal [dato legal: Wikipedia](https://en.wikipedia.org/wiki/Adobe_Systems,_Inc._v._Southern_Software,_Inc.) | Proyecto desde cero. Si es OFL, ver el derivado honesto más abajo |
| Interpolar o escalar contornos de terceros | Rechaza | En *Adobe*, un escalado del 101 % vertical fue cambio mecánico [dato legal: Wikipedia](https://en.wikipedia.org/wiki/Adobe_Systems,_Inc._v._Southern_Software,_Inc.) | Másteres propios interpolando entre sí |
| Copiar tablas de métricas o kerning | Rechaza | Es parte de la prohibición del protocolo; además, alguna EULA limita expresamente el uso del kerning [fuente: MyFonts](https://www.myfonts.com/pages/license-agreement?id=eula_2275&eula_lang=eula_en) | Espaciado y kerning propios con `03-espaciado-y-kerning.md` |
| Imitar a una persona o marca | Rechaza la imitación por nombre | La transferencia de estilo de una fuente o persona es rojo (ver [niveles](#niveles-aplicados-a-este-agente)); la marca añade riesgo de nombre y confusión [inferencia] | Describir la voz de marca con palabras y traducirla a parámetros propios |
| Subir fuentes ajenas a una IA | No las aceptes ni las abras | Las EULA lo prohíben o limitan [fuente: MyFonts](https://www.myfonts.com/pages/license-agreement?id=eula_2275&eula_lang=eula_en) [fuente: Lineto](https://lineto.com/information/legal/legal/lineto-eula); la FAQ de OFL trata lo resultante como derivado [dato legal: OFL FAQ 1.25](https://openfontlicense.org/ofl-faq/) | Pide capturas de **tu** dibujo y una descripción verbal de lo que le gusta de la otra |
| «Hazme X pero con otro nombre» | Rechaza | Cambiar el nombre no cambia los contornos; la marca solo cubre el nombre | Preguntar qué problema resuelve X y qué le falta |
| «Es de un sitio gratis» | Comprueba antes | Gratis no significa libre | Leer su licencia; si no consta, tratarla como ajena |

### Inspiración por género no es copia
No rechaces lo que es género. «Una grotesca neutra», «una serifa de texto con contraste de traslación» o «una mono para código» piden convenciones compartidas. Hazlo con estas reglas [propuesta de esta skill]:
- Las referencias informan del género, nunca de los contornos. Anota cada una en la tabla del brief y usa rangos de varias fuentes, no los valores de una sola.
- Mira las referencias sin abrir sus binarios, y nunca escribas de memoria coordenadas de una fuente conocida.
- Añade un rasgo con motivo propio por cada convención que heredes. Ver [decisión](#decidir-entre-convención-y-rasgo-distintivo).

### Respuestas modelo
- **Clon:** «No voy a reproducir Helvetica, ni con cambios menores: sería copiar el diseño de otra persona y no podríamos llamarla original. Sí puedo hacer una grotesca neutra propia. Dime para qué la usarás y qué te gusta de esa fuente, por ejemplo la calma o la altura x, y lo convierto en un brief.»
- **Binario:** «Prefiero no abrir ese archivo: tener licencia para usar una fuente no permite partir de ella, y subirla a una IA suele estar prohibido. Enséñame dónde te funciona y describimos qué hace bien; dibujo desde cero con esos objetivos.»
- **Otro nombre:** «El nombre no cambia los contornos, así que seguiría siendo una copia. ¿Qué necesitas que X no te da, precio, licencia, algún rasgo? Si el problema es la licencia, quizá baste una fuente libre existente; si quieres algo propio, empezamos por el brief.»

### Salidas legítimas que no son «original»
- **Derivado OFL.** Partir de una fuente OFL es lícito bajo sus condiciones: sigue en OFL, respeta las RFN y no se vende sola [dato legal: OFL 1.1](https://openfontlicense.org/open-font-license-official-text/). Es un derivado y debe llamarse así: esta skill no lo presenta como original.
- **Fuente existente o encargo al titular.** Si basta con una fuente libre, dilo; una variante de una fuente ajena se pide a quien tiene sus derechos.
- **Sustituto compatible en métricas.** Arimo y Liberation Sans comparten anchos con Arial, con otro nombre y otros contornos [fuente: Wikipedia](https://en.wikipedia.org/wiki/Liberation_fonts). Existe en la práctica, pero choca con la regla de no copiar métricas: no lo hagas por defecto y deja la decisión a la persona con un abogado [propuesta de esta skill].

## Revivals legítimos
Un revival es apropiación que exige notas éticas [fuente: Dat Journal, solo resumen](https://datjournal.anhembi.br/dat/article/view/116), y en TypeDrawers dónde poner el límite se trata como ética, no como ley [fuente: TypeDrawers](https://typedrawers.com/discussion/comment/47036). No se hallaron códigos de revival publicados por fundiciones: estos pasos son [propuesta de esta skill], basada en la investigación.

Todos los pasos son necesarios:
1. **Identifica la fuente** en `BRIEF.md`: fundidor, fecha y por qué revivirla ahora.
2. **Comprueba los derechos en cada mercado** y que la persona anote la verificación. No se puede decidir en general si un diseño histórico está libre. Alemania y Francia admiten copyright sobre tipografías, y en España dura vida + 70 años [dato legal: TRLPI art. 26](https://www.boe.es/buscar/act.php?id=BOE-A-1996-8930). Si no se puede comprobar, detente.
3. **Parte de impresos, nunca de una digitalización ajena**: una fuente digital previa puede tener software y puntos protegidos. Una reinterpretación de Gill Sans separó el diseño libre del software protegido [fuente: OSP](https://ospublish.constantvzw.org/blog/news/sans-guilt-it-looks-like-the-story-continues). Adobe usó muestrarios de bibliotecas, fundiciones y colecciones [fuente: Adobe Type Library](https://www.oreilly.com/library/view/adobe-type-library/9780132964371/ch01sec1lev10.html), y se cita Letterform Archive [fuente: TypeDrawers](https://typedrawers.com/discussion/comment/63136). Guarda procedencia y permiso de las imágenes.
4. **Dibuja de nuevo**, sin autotrazar, y registra el origen por glifo y el material consultado.
5. **Elige un nombre nuevo** y busca marcas: el histórico puede estar vigente, y no se comprobó ninguno.
6. **Decláralo revival**, con crédito al autor original aunque la ley no lo exija y lista pública de cambios. Prefiere una reinterpretación con punto de vista a un facsímil: es más segura y mejor [inferencia].

## Protocolo de procedencia
**El protocolo es propuesta de esta skill, no un estándar.** No se encontró metodología reconocida de limpieza de originalidad ni métrica aceptada por tribunales o por el sector [fuente: investigación, 7-11-2026]. Su valor es práctico: el mismo registro sirve para probar la primera divulgación, sostener la autoría y ser honesto sobre la IA.

| Momento | Acción | Comando o archivo |
|---|---|---|
| Inicio | Brief fechado con referencias y reparto con IA; búsqueda de nombre guardada; primer commit **antes** del primer sello | `BRIEF.md`, `git commit` |
| Primer contorno y después | Registra cada glifo al crearlo o cambiar de origen | `registro.py glifo` |
| Cada puerta aprobada | Commit, sello y commit del sello | `registro.py sello` |
| Tras control, minúscula, antes de publicar | Auditoría de similitud | `registro/auditorias/` |
| Antes de publicar | Ningún glifo sin registrar; hash de los binarios; sello de tercero | `registro.py resumen`, `sha256sum` |
| Primera divulgación | Fecha, lugar y prueba | `registro/primera_divulgacion.md` |
| Colaboradores | Cesión y garantía de originalidad por escrito; `copy_check.py` antes de aceptar sus archivos | carpeta de contratos, fuera de git si es confidencial |

### Comandos
```bash
PY="${TYPE_DESIGN_VENV:-$HOME/.local/share/type-design/venv}/bin/python"
$PY scripts/registro.py glifo PROYECTO n,o,H,O codigo-regla-humana "regla: BRIEF §Concepto; generador commit abc123"
$PY scripts/registro.py glifo PROYECTO a humano "redibujado por Ana en FontLab en capa vacía"
git -C PROYECTO add -A && git -C PROYECTO commit -m "aprobado control n o H O"
$PY scripts/registro.py sello PROYECTO "aprobado control n o H O por Ana"
git -C PROYECTO add registro && git -C PROYECTO commit -m "sello: control n o H O"
$PY scripts/registro.py resumen PROYECTO
sha256sum PROYECTO/fonts/* > PROYECTO/registro/hash_binarios_v1.0.txt
```

### Qué hace `registro.py`, y qué no
- `glifo` añade filas a `registro/procedencia_glifos.csv`. El último origen manda en el resumen y el historial se conserva. No comprueba que el glifo exista; `resumen` sí detecta los glifos sin registrar.
- `sello` añade a `registro/sellos.tsv` la hora del sistema, un SHA-256 de **solo** `sources/`, el commit y la nota. No cubre `BRIEF.md`, `registro/` ni los binarios. Si `sources/` tiene cambios sin confirmar avisa y marca el commit con `+sucio`, y antes del primer commit escribe `sin-commit`: confirma antes de sellar.
- `resumen` compara con todos los másteres y muestra hasta 40 glifos sin registrar.
- `fonts/` y `proofs/` están en `.gitignore`: guarda el hash de cada versión y copia los especímenes fechados a `registro/`.
- Orígenes válidos, con su [criterio](#clasificar-el-origen-de-un-glifo): `humano`, `codigo-regla-humana`, `ia-modificado-humano`, `ia-generado`, y `heredado-desconocido` para fuentes recibidas.

### Fechar con un tercero y probar la primera divulgación
Un hash en tu propio repositorio solo convence a quien confíe en él. Para valor probatorio, un tercero independiente debe fijar la fecha de los hashes de fuentes y binarios de cada versión [propuesta de esta skill]. La investigación no evaluó ningún servicio: explica la necesidad, deja elegir a la persona y anota el recibo. Un sello prueba que un contenido existía en una fecha, no quién lo creó ni que sea original.

Quien alega diseño no registrado debe probar fecha y lugar de la primera divulgación [dato legal: EUIPO](https://www.euipo.europa.eu/en/help-centre/design/faq-unregistered-community-designs). Guarda en `registro/primera_divulgacion.md` fecha y hora, lugar (URL, evento, país), qué se mostró, captura y hash. Trata una beta, un espécimen o una publicación con letras reconocibles como posible inicio del reloj [inferencia].

## Auditoría de similitud
**Ninguna herramienta certifica la originalidad**: ni los identificadores, ni la superposición, ni `copy_check.py`, ni esta skill. Tampoco existe umbral porcentual aceptado por tribunales o por el sector: no presentes nunca un porcentaje como prueba legal. En la UE y España cuenta la impresión general del usuario informado, ponderando la libertad del autor [dato legal: Ley 20/2003 arts. 5–7](https://www.boe.es/buscar/act.php?id=BOE-A-2003-13615).

Audita en tres momentos [propuesta de esta skill]: **tras los caracteres de control**, cuando cambiar de rumbo es barato; **con la minúscula completa**, con ritmo y texto real; y **antes de publicar**, con el juego definitivo. Guarda cada ronda en `registro/auditorias/AAAA-MM-DD-momento/`.

| Método | Qué hace | Límite | Quién |
|---|---|---|---|
| Identificadores por imagen (WhatTheFont, Matcherator) | Devuelven vecinos de su base [fuente: Creative Bloq](https://www.creativebloq.com/typography/best-font-identifiers) | Solo ven su base; se discute la precisión de Matcherator. Sin resultados no significa nada | Persona |
| Identifont | Cuestionario de rasgos [fuente: Creative Bloq](https://www.creativebloq.com/typography/best-font-identifiers) | También limitado a su base | Persona o agente con sus respuestas |
| Revisión manual del género | Compara con los más vendidos y catálogos libres del género | Depende de quien mira; no exhaustiva | Persona |
| Superposición normalizada | Superpone tu dibujo y cada vecina a igual altura x y asta | Requiere imagen o archivo ajeno; no compares con binarios sin derecho | Persona, en su equipo |
| Tabla de rasgos | Compara rasgos concretos y su combinación | Juicio, no medición | Agente propone, persona decide |
| Firma de avances y kerning | Compara anchos y pares como firma estadística | Solo si la licencia lo permite: una EULA puede prohibirlo | Persona |
| `copy_check.py` | Busca puntos compartidos entre dos binarios | Detecta calco casi literal, no parecido | Agente sobre archivos con derecho |

### Identificadores
1. Exporta palabras reales a tamaño de texto y de titular, no el alfabeto completo. Revisa antes las condiciones de la herramienta: no se investigó si conservan imágenes ni si eso afecta a la novedad [inferencia].
2. Guarda los primeros resultados de cada herramienta con fecha y captura.
3. Lleva las vecinas plausibles a la tabla de rasgos. Una coincidencia es una vecina que revisar, no una acusación.

### `copy_check.py`: qué mide de verdad
```bash
$PY scripts/copy_check.py fonts/Mia.ttf otra.ttf
```

Lee binarios compilados, no UFO. Empareja letras y cifras por punto de código y omite los glifos de menos de 8 puntos. Lleva cada glifo a su propia caja, lo que anula escala, anchura y desplazamiento, prueba inclinaciones de -14° a 14° en ambos sentidos y calcula qué parte de los puntos coincide a menos de unas 6 milésimas de la caja. Da la mediana, los 15 glifos más coincidentes y `ALARMA` (salida 1) si más de `max(3, 10 %)` de los glifos llegan al 70 %. Esos umbrales son arbitrarios.

Sigue el razonamiento de *Adobe*: dos diseñadores independientes rara vez comparten puntos de control [dato legal: Wikipedia](https://en.wikipedia.org/wiki/Adobe_Systems,_Inc._v._Southern_Software,_Inc.). Lo sensato es usarlo como alarma de calco, sobre todo en archivos de colaboradores.

[fuente: prueba propia, 7-11-2026] Con versiones transformadas sintéticamente de una fuente de 1000 glifos aproximadamente:

| Comparación con el original | Glifos ≥ 70 % | Alarma |
|---|---|---|
| Escala uniforme 105 % | 890 | Sí |
| Anchura 90 % | 776 | Sí |
| +10 unidades en vertical | 1013 | Sí |
| Ruido de ±3 por punto | 944 | Sí |
| Inclinada 7° | 785 | Sí |
| Ubuntu frente a DejaVu Sans, diseños independientes | 4 de 1020 | No |
| DejaVu Sans frente a DejaVu Serif | 4 de 1944 | No |
| Ubuntu Sans frente a Ubuntu Sans Mono (misma autoría) | 18 de 1011 | No |

Conclusiones que debes respetar:
- **Un calco redibujado pasa sin alarma.** Cambiar la estructura de puntos o el trazo basta para evitarla. «Sin alarma» no significa «no copiado», y mucho menos «original». La conversión a cúbicas no se ha medido con esta versión.
- **El parecido visual no se mide.** Dos diseños casi iguales dibujados por separado no comparten puntos.
- **Una alarma no prueba copia.** Formas geométricas simples (T, H, П) coinciden entre diseños independientes. Mira qué glifos salen: si son letras con curvas, detente y revisa el origen.
- En variables lee solo el máster por defecto: compara instancias de los extremos. Los glifos sin Unicode no se comparan. La prueba, con pocos pares sintéticos, describe; no valida.
- Úsalo solo con fuentes que tengas derecho a abrir, y revisa su EULA. Que al modelo solo lleguen porcentajes, no contornos [propuesta de esta skill].

### Tabla de rasgos
Rellena una por ronda con las 2–5 vecinas más cercanas, con palabras concretas, sin «parecido» ni «elegante» [propuesta de esta skill]. Columnas: `Rasgo | Mi fuente | Vecina A | Vecina B | ¿Convención o distintivo? | Decisión`. Filas: `a` (panza, remate, cuello), `g` (pisos, oreja, enlace), `e` (ángulo, apertura), `R` (pata, unión), `k` (unión de diagonales), `y` (cola), terminales, uniones, modelo de contraste y proporciones.

### Decidir entre convención y rasgo distintivo
Los tribunales comparan detalles y combinaciones: en el caso Spectral se buscó la combinación de características originales de Le Monde y se atendió a detalles como el grosor de las serifas [dato legal: Kluwer](https://legalblogs.wolterskluwer.com/copyright-blog/france-le-mondes-font-is-original-but-has-not-been-copied-by-google/). Por eso importa más la combinación que un rasgo aislado. Aplica estas preguntas, que son juicio de diseño y no prueba legal [propuesta de esta skill]:
1. **¿Lo comparten muchas fuentes independientes del género?** Si sí, apunta a convención. En una grotesca neutra hay poca libertad y es esperable cierta cercanía.
2. **¿Lo exige la función?** Una forma impuesta por legibilidad o técnica es más convención que autoría.
3. **¿Tiene un motivo propio escrito en el brief?** Si solo existe porque la vecina lo hace, es señal de alarma.
4. **¿Coincide una combinación de varios rasgos no obligados con la misma vecina?** Es lo que más pesa: **redibuja**.

Redibuja desde tu lógica de forma, no ajustando milímetros la vecina: alejarse poco de ella sigue partiendo de ella. Anota la decisión y por qué, confirma con la persona y repite la ronda si hubo cambios. Si queda duda y la fuente se va a comercializar, deriva a un abogado. El juicio final es humano.

## Mapa jurídico por territorio
Estado a 7-11-2026. La protección es doble: diseño de letras y software. La marca cubre solo el nombre [fuente: OFL FAQ](https://openfontlicense.org/ofl-faq/). La tabla de Monotype procede de parte interesada.

| Territorio | Diseño | Software | Nota |
|---|---|---|---|
| EE. UU. | No: «Typeface as typeface» [dato legal: 37 CFR 202.1](https://www.law.cornell.edu/cfr/text/37/202.1) | Disputado | *Laatz* debilitó la vía del registro |
| UE | Sí: «typographic typefaces»; registrado, 5 años renovables hasta 25; no registrado, solo contra copia [dato legal: Reg. 2024/2822](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402822) | Excluido del diseño | Rige desde el 1-5-2025, parte desde el 1-7-2026 [fuente: Curell](https://curell.com/en/eu-directive-and-regulation-update-enhancing-design-protection/); diseño y copyright pueden acumularse [fuente: Monotype](https://www.monotype.com/resources/update-application-copyright-law-typeface-design-and-font-software) |
| España | Sí: «caracteres tipográficos»; 5 años renovables hasta 25 [dato legal: Ley 20/2003](https://www.boe.es/buscar/act.php?id=BOE-A-2003-13615) | Programas en TRLPI 10.1.i [dato legal: TRLPI](https://www.boe.es/buscar/act.php?id=BOE-A-1996-8930) | Copyright vida + 70; derechos morales irrenunciables; autor persona natural [fuente: Cuatrecasas](https://www.cuatrecasas.com/es/spain/articulo/internacional-inteligencia-artificial-y-derechos-de-autor). Sin caso español encontrado |
| Reino Unido | Sí: uso normal no infringe; 25 años tras el fin del año de primera comercialización se puede copiar para producir tipos [dato legal: CDPA s.54–55](https://www.legislation.gov.uk/ukpga/1988/48/part/I/chapter/III/crossheading/typefaces); registrable [dato legal: RDA s.1(3)](https://www.legislation.gov.uk/ukpga/Geo6/12-13-14/88/section/1) | Desconocido [fuente: Monotype](https://www.monotype.com/resources/update-application-copyright-law-typeface-design-and-font-software) | Sin fuente británica sobre software |
| Alemania | Sí, por jurisprudencia: Candida (BGH 1958), Futura (LG Frankfurt 1979) [fuente: Monotype](https://www.monotype.com/resources/update-application-copyright-law-typeface-design-and-font-software) | Sí: LG Köln 2000 [fuente: Monotype](https://www.monotype.com/resources/update-application-copyright-law-typeface-design-and-font-software) | Schriftzeichengesetz 1981, no verificada contra la ley [fuente: Wikipedia](https://en.wikipedia.org/wiki/Intellectual_property_protection_of_typefaces) |
| Francia | Sí en 2023: Le Monde original, sin infracción por Spectral [dato legal: Kluwer](https://legalblogs.wolterskluwer.com/copyright-blog/france-le-mondes-font-is-original-but-has-not-been-copied-by-google/) | Sí [fuente: Monotype](https://www.monotype.com/resources/update-application-copyright-law-typeface-design-and-font-software) | **Desacuerdo:** Wikipedia lo limita a diseño industrial [fuente: Wikipedia](https://en.wikipedia.org/wiki/Intellectual_property_protection_of_typefaces) |
| Japón | **Disputado:** «no cubierto» [fuente: Wikipedia](https://en.wikipedia.org/wiki/Intellectual_property_protection_of_typefaces); «sí, estándar alto», citando también *Gona U* en contra [fuente: Monotype](https://www.monotype.com/resources/update-application-copyright-law-typeface-design-and-font-software) | Sí, según Monotype | Verifica antes de contar con él |

### EE. UU.: el desacuerdo vivo
- *Adobe v. Southern Software* (N.D. Cal. 1998): extraer los puntos de Utopia y escalarlos 101 % fue cambio mecánico; la elección de puntos fue autoría original [dato legal: Wikipedia](https://en.wikipedia.org/wiki/Adobe_Systems,_Inc._v._Southern_Software,_Inc.). La sentencia no se leyó completa.
- *Laatz v. Zazzle* (N.D. Cal.): en marzo de 2024 se distinguió *Adobe* porque Laatz no creó el software; en agosto de 2025 se desestimó por defectos de sus registros, **sin decidir** la copyrightabilidad general [dato legal: Butterick, 21-12-2025](https://matthewbutterick.com/chron/the-copyrightability-of-fonts-revisited.html). Apelación interlocutoria denegada en octubre de 2025 [dato legal: MLex](https://www.mlex.com/mlex/articles/2402719/font-designer-denied-interlocutory-appeal-in-us-copyright-fight-with-zazzle). Seguía abierto en enero de 2026 [fuente: Monotype](https://www.monotype.com/resources/update-application-copyright-law-typeface-design-and-font-software).
- **Monotype frente a Butterick.** El consejero general de Monotype sostiene que el software está protegido, con dificultades de registro [fuente: Monotype, 30-1-2026](https://www.monotype.com/resources/update-application-copyright-law-typeface-design-and-font-software). Butterick sostiene que probablemente no lo esté y que los registros son vulnerables [fuente: Butterick](https://matthewbutterick.com/chron/the-copyrightability-of-fonts-revisited.html). Ambos tienen posición: no los presentes como doctrina cerrada.

## Calendario de la UE y orden en España
El orden de las acciones puede decidir la protección. El reloj empieza con la primera divulgación, y una beta lo pone en marcha [inferencia].

| Momento | Qué ocurre |
|---|---|
| Antes de divulgar | Situación más limpia para solicitar diseño registrado [inferencia]. Registrado: 5 años desde la solicitud, renovables hasta 25 [dato legal: Reg. 2024/2822](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402822) [dato legal: Ley 20/2003 art. 43](https://www.boe.es/buscar/act.php?id=BOE-A-2003-13615) |
| Día 0, primera divulgación pública en la UE | Empieza el diseño no registrado y el periodo de gracia. Prueba fecha y lugar [dato legal: EUIPO](https://www.euipo.europa.eu/en/help-centre/design/faq-unregistered-community-designs) |
| Hasta el mes 12 | Aún se puede solicitar el registrado [dato legal: EUIPO](https://www.euipo.europa.eu/en/help-centre/design/faq-unregistered-community-designs) [dato legal: Ley 20/2003 art. 10](https://www.boe.es/buscar/act.php?id=BOE-A-2003-13615). Desde el 1-7-2026 la gracia cubre también un diseño que no dé impresión general distinta [dato legal: EUIPO, reforma](https://euipo.europa.eu/tunnel-web/secure/webdav/guest/document_library/contentPdfs/law_and_practice/EUDR-legislative-changes/DLR-Summary-narrative-phases-I-and-II_en.pdf) |
| Después del mes 12 | La vía registrada se cierra para ese diseño: no agotes los 3 años para registrar luego, porque se pierde novedad [dato legal: EUIPO](https://www.euipo.europa.eu/en/help-centre/design/faq-unregistered-community-designs) |
| Año 3 | Termina el diseño no registrado [dato legal: EUIPO](https://www.euipo.europa.eu/en/help-centre/design/faq-unregistered-community-designs) |

Datos de solicitud: Locarno 18-03 [dato legal: WIPO](https://locpub.wipo.int/enfr/pdf-download.pdf?lang=en&tab=&viewMode=loc&dateInForce=20270101&classNumber=18). EUIPO pide cadena de mayúsculas y minúsculas, cifras árabes y cinco líneas de texto; **esa página figura como obsoleta**, comprueba la edición vigente [dato legal: EUIPO, directrices 5.3.9](https://guidelines.euipo.europa.eu/2213908/2064948/designs-guidelines/5-3-9-typographic-typefaces). El diseño cubre la apariencia, no el archivo: trata ambos como activos separados [inferencia].

**Orden práctico para alguien en España** [inferencia]:
1. Diseño registrado de la UE o español para la familia insignia, dentro del plazo.
2. Diseño no registrado de la UE con prueba de primera divulgación.
3. Contrato: EULA y cesiones.
4. Marca sobre el nombre.
5. Copyright como capa posible, no como base. *Mio & Konektra* pudo rebajar el umbral para arte aplicado [fuente: Monotype](https://www.monotype.com/resources/update-application-copyright-law-typeface-design-and-font-software), pero aplicarlo a tipografías es lectura propia, no doctrina.

Una estrategia basada solo en registrar en EE. UU. es débil [inferencia]. Si la primera divulgación se hará fuera de la UE, o el mercado es otro, pide consejo antes: los periodos de gracia de otros países no se estudiaron.

## Licencias
**OFL 1.1 para alcance, EULA modular para vender.** No mezcles sin cuidado: lo publicado bajo OFL y sus derivados no se pueden relicenciar [inferencia]. Apache 2.0 aporta concesión de patentes [dato legal: Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0), pero no hay evidencia de que se siga eligiendo para fuentes nuevas.

| | OFL 1.1 | EULA propia |
|---|---|---|
| Venta | No sola; sí incluida con software [dato legal: OFL 1.1](https://openfontlicense.org/open-font-license-official-text/) | Sí |
| Derivados | Siguen en OFL; los documentos no se ven afectados [dato legal: OFL 1.1](https://openfontlicense.org/open-font-license-official-text/) | Los que permitas |
| Subsetting | Es modificación; cambio de formato normalmente también, salvo WOFF y Functional Equivalence [dato legal: OFL FAQ 2.2, 2.6, 2.7](https://openfontlicense.org/ofl-faq/) | Debes regularlo |
| Marca | OFL no concede derechos de marca [dato legal: OFL FAQ](https://openfontlicense.org/ofl-faq/) | Regúlalo aparte |
| Riesgo | Sin control de uso | Requiere redacción: no se encontró EULA modelo de abogados ni análisis para derecho español |

### Reserved Font Names: desacuerdo SIL/Google
- SIL: las RFN son opcionales y anima a usarlas; nada queda reservado por defecto [fuente: OFL FAQ 5.6–5.7](https://openfontlicense.org/ofl-faq/).
- Google: «The Open Font License should not have any Reserved Font Names» [fuente: GF Guide](https://googlefonts.github.io/gf-guide/onboarding), y Fontbakery falla si aparece esa cadena en la tabla `name` [fuente: Fontbakery](https://fontbakery.readthedocs.io/en/latest/fontbakery/profiles/googlefonts.html).

Decide así [inferencia]: si aspiras a Google Fonts, sin RFN. Si publicas fuera y quieres proteger el nombre, RFN o, mejor, una marca real. Una RFN obliga a renombrar a quien recorte la fuente para la web, y `07-web.md` depende del subsetting. No reserves nombres ligados a marcas ajenas [fuente: OFL FAQ](https://openfontlicense.org/ofl-faq/).

### Campos del archivo
Deben coincidir con la licencia real: la FAQ de OFL pide vigilar conflictos entre `fsType` y `name` [fuente: OFL FAQ 4.2.2](https://openfontlicense.org/ofl-faq/).

| Campo | OFL (formato GF) | EULA |
|---|---|---|
| ID 0, copyright | `Copyright {año} The {familia} Project Authors ({url git})` [fuente: GF requisitos](https://googlefonts.github.io/gf-guide/requirements.html) | Aviso del titular real |
| ID 7, marca | Solo si existe, con `TRADEMARKS.md` [fuente: GF requisitos](https://googlefonts.github.io/gf-guide/requirements.html) | Solo si existe; con consejo legal [fuente: OpenType](https://learn.microsoft.com/en-us/typography/opentype/spec/name) |
| ID 8, 9, 11, 12 | Fabricante, diseñador y URLs | Igual |
| ID 13, licencia | `This Font Software is licensed under the SIL Open Font License, Version 1.1.` | Resumen o texto; un resumen puede crear conflictos de interpretación [inferencia] |
| ID 14, URL | `https://openfontlicense.org` | URL estable de tu licencia |
| `OS/2.fsType` | `0`, instalable [fuente: OpenType OS/2](https://learn.microsoft.com/en-us/typography/opentype/spec/os2) | Según lo vendido; revisa la especificación |
| Paquete | `OFL.txt` con la primera línea igual que ID 0; una URL sola no se recomienda [fuente: OFL FAQ 4.2.2](https://openfontlicense.org/ofl-faq/) [fuente: GF licencia](https://googlefonts.github.io/gf-guide/license-file.html) | Texto completo y resumen legible |

Trampas del esqueleto de esta skill [fuente: prueba propia, 7-11-2026]:
- `new_project.py` deja licencia y autoría vacías por defecto (`--licencia pendiente`) y `check_sources.py` lo avisa: las decide la persona. `--licencia ofl` escribe texto y URL de OFL, `--autoria` fija copyright y diseñador, y `fsType` queda en 0. Con EULA, rellena los IDs 13 y 14 a mano.
- El aviso por defecto no lleva URL git ni rellena diseñador: complétalos.
- Sin `openTypeOS2Type`, una compilación mínima con ufo2ft dio `fsType 4` (previsualizar e imprimir), más restrictivo de lo que concede una OFL. Con `openTypeOS2Type = []` dio 0. Comprueba el valor en la fuente compilada.

GF habla de «bit 0» para la incrustación instalable; la especificación usa el valor 0 y reserva el bit 0 [fuente: OpenType OS/2](https://learn.microsoft.com/en-us/typography/opentype/spec/os2). Sigue la especificación. Al revisar fuentes ajenas, mira su repositorio: los listados se contradicen [fuente: Greptile](https://www.greptile.com/grepository/jetbrainsmono).

### Cláusulas de una EULA
Sugiere a la persona que un abogado revise o redacte; tú solo preparas el borrador. No se halló sentencia sobre estas cláusulas. Una EULA de 2026 debería cubrir [inferencia]: usos y límites (escritorio, web, app, puestos, páginas vistas, usuarios activos); logotipo, de forma expresa; difusión, ePub y PDF incrustado; modificación, añadidos y subsetting; agencias y transferencia al cliente; auditoría, jurisdicción y terminación; e IA, prohibiendo entrenar y permitiendo software normal con IA, según el modelo de Typodermic [fuente: Typodermic](https://typodermicfonts.com/license/), para no vetar programas corrientes.

Referencias de mercado, no plantillas: Fontspring separa escritorio, web y app, y limita app por usuarios activos mensuales [fuente: Fontspring](https://www.fontspring.com/license/fontspring/desktop); Creative Market veta `@font-face` con licencia de escritorio [fuente: Creative Market](https://creativemarket.com/licenses/terms/fonts); MyFonts veta glifos, contornos y kerning en desarrollo de IA, salvo metadatos no renderizados [fuente: MyFonts](https://www.myfonts.com/pages/license-agreement?id=eula_2275&eula_lang=eula_en); Lineto veta crear fuentes por IA [fuente: Lineto](https://lineto.com/information/legal/legal/lineto-eula).

**Encargos.** Dalton Maag declara que el cliente posee toda la propiedad intelectual tras la entrega [fuente: Dalton Maag](https://daltonmaag.com/services/custom-font-design.html). En España los derechos morales son inalienables: trátalos aparte [dato legal: TRLPI art. 14](https://www.boe.es/buscar/act.php?id=BOE-A-1996-8930). Entrega el dosier de procedencia con las fuentes, y si hay glifos de origen IA, dilo **antes** de firmar cualquier cesión o garantía [propuesta de esta skill].

## Venta y canales
Los datos publicados son escasos. **No hay datos fiables de precio por estilo, por paquete ni de ingresos: no des cifras** y no las estimes.

| Canal | Dato disponible | Calidad |
|---|---|---|
| Monotype | 50 % en MyFonts; 25 % en el resto, incluida la aplicación de licencias [fuente: Monotype](https://foundrysupport.monotype.com/hc/en-us/articles/360048861171-Monotype-Distribution-Agreement) | Contrato publicado |
| Monotype Fonts | Regalías por indicadores indirectos desde 2023 [fuente: Monotype](https://foundrysupport.monotype.com/hc/en-us/articles/15723177145236-Monotype-Fonts-Royalty-Model) | Documento propio |
| Fontspring, Creative Market / Font Bros | 70 % / 65 % | Foros, fechas variables [fuente: TypeDrawers](https://typedrawers.com/discussion/comment/35931) [fuente: TypeDrawers](https://typedrawers.com/discussion/comment/63399) |
| Adobe Fonts | Suscripción fija y porcentaje; ingresos variables según quién cuenta | Anécdota [fuente: TypeDrawers](https://typedrawers.com/discussion/comment/35941) |
| Google Fonts | OFL, repositorio público, TTF, Fontbakery, GF Latin Core; curaduría del equipo de Google [fuente: GF Guide](https://googlefonts.github.io/gf-guide/onboarding) | Primaria. Modelo de pago de encargos no hallado |
| Future Fonts, I Love Typography, Fontstand, Fontdue | Sin datos | No afirmes nada |

Monotype dijo que en 2022 la mitad de 433 fundiciones independientes recibía de ella al menos el 50 % de sus ingresos [fuente: Monotype, nota de prensa](https://www.prnewswire.com/news-releases/monotype-launches-a-new-foundry-program-designed-to-empower-and-scale-the-type-community-301904499.html): la dependencia de un canal es un riesgo reconocido. Una fuente secundaria habla de unas 30 fundiciones que rompieron con Monotype en 2024 [fuente: Typeberry](https://typeberry.co/blog/30-foundries-quit-monotype). Mezcla razonable para un independiente: web propia, uno o dos minoristas sin exclusiva y suscripción opcional; evita exclusivas al principio. Proyecta aparte los ingresos del 50 y del 25 %. Una fuente libre con extensiones o encargos de pago es otro modelo posible. Todo esto es [inferencia]. La fiscalidad no se investigó.

## IA: estado del terreno
Datos a noviembre de 2026; este campo caduca rápido.

Cozens, que entrenó su propio modelo, opina el 22-6-2026 que CJK ya sería apta para producción, pero el latín es pobre por espaciado, kerning, métricas, anchuras, ligaduras y features; avisa de que falta revisión de diseñadores y de que las demos pueden ser selectivas [fuente: Cozens](https://simoncozens.github.io/state-of-ai-font-generation/). En editores es asistencia con revisión, como Auto Space y Auto Kern en FontLab [fuente: FontLab](https://www.fontlab.com/font-editor/fontlab-9/). TypeDrawers es mayoritariamente escéptico, y Larabie avisa de que los defectos actuales no son salvaguarda duradera [fuente: TypeDrawers](https://typedrawers.com/discussion/5626/can-you-tell-the-difference-between-ai-generated-vs-human-made-fonts). Sobre Gothic Gumdrop, un participante rechazó publicarla y Cozens, a título personal, antepuso la calidad a la herramienta [fuente: TypeDrawers](https://typedrawers.com/discussion/5609/critique-request-for-gothic-gumdrop-100-ai-generated-submission-to-google-fonts). No se halló postura oficial de ATypI ni datos de uso profesional.

**Autoría de lo generado:**
- *Thaler v. Perlmutter*: se mantuvo la autoría humana; el Supremo denegó revisión el 2-3-2026 sin entrar en el fondo [dato legal: SCOTUSblog](https://www.scotusblog.com/cases/thaler-v-perlmutter/). Lo asistido por IA sigue abierto.
- Oficina de Copyright de EE. UU., parte 2 (29-1-2025): los prompts solos no dan control humano suficiente; usar IA como herramienta no limita la protección; un dibujo humano como entrada protege solo la expresión humana perceptible; caso por caso [dato legal: IPWatchdog](https://ipwatchdog.com/2025/01/29/part-two-copyright-office-ai-report-says-creative-prompting-doesnt-constitute-authorship/). Hay quien lee que el prompting podría bastar en el futuro [dato legal: Mondaq](https://www.mondaq.com/unitedstates/copyright/1588226/part-2-ai-copyrightability). El texto oficial no se leyó.
- España: el autor es persona natural y decide el grado de participación humana [dato legal: Cuatrecasas](https://www.cuatrecasas.com/es/spain/articulo/internacional-inteligencia-artificial-y-derechos-de-autor). El Registro niega inscribir obra de IA, según prensa [fuente: Genbeta](https://www.genbeta.com/actualidad/registro-propiedad-intelectual-espanol-tambien-le-niega-copyright-a-obras-creadas-ias-asi-argumenta/amp).
- **Entrenamiento:** ninguna decisión trata de fuentes, y las que hay difieren. *Bartz* (23-6-2025) vio uso legítimo con libros adquiridos lícitamente, no con copias piratas [dato legal: Akin](https://www.akingump.com/en/insights/ai-law-and-regulation-tracker/district-court-rules-ai-training-can-be-fair-use-in-bartz-v-anthropic). *Kadrey* (25-6-2025) también, en ese expediente, con la dilución de mercado como posible giro [dato legal: Copyright Alliance](https://copyrightalliance.org/kadrey-v-meta-decision/); ambos jueces discrepan sobre ella [dato legal: FisherBroyles](https://fisherbroyles.com/news/client-alert-summary-and-strategic-analysis-of-judge-chhabrias-fair-use-ruling-in-kadrey-v-meta). *Getty v. Stability* [2025] EWHC 2863 (Ch): el modelo no es copia infractora, con permiso para apelar el 17-12-2025 [dato legal: CMS](https://cms.law/en/swe/publication/artificial-intelligence-and-copyright-case-tracker/united-kingdom-getty-images-us-inc-ors-v-stability-ai-ltd2). *GEMA v. OpenAI* (LG München I, 11-11-2025) halló infracción en letras de canciones; razonamiento no leído [dato legal: CMS](https://cms.law/en/swe/publication/artificial-intelligence-and-copyright-case-tracker/united-kingdom-getty-images-us-inc-ors-v-stability-ai-ltd2).
- **Licencias:** la FAQ de OFL 1.25 considera derivada de OFL toda fuente producida por un sistema cuyos datos incluyan fuentes de un proyecto. La 1.26 admite herramientas de IA si el resultado no pretende ser una fuente [dato legal: OFL FAQ](https://openfontlicense.org/ofl-faq/). Es interpretación de SIL, no sentencia. En el mismo foro se discute que la derivación de estilo sea obra derivada legal [fuente: TypeDrawers](https://typedrawers.com/discussion/5609/critique-request-for-gothic-gumdrop-100-ai-generated-submission-to-google-fonts).

## IA: el trabajo de este agente
Esta skill hace algo que los niveles no resuelven solos: **un agente de IA escribe código que coloca los puntos**, a partir de reglas humanas. No es un generador de imágenes ni un dibujo a mano. Trátalo como ámbar, solo si cada condición se cumple y se documenta. La clasificación es [propuesta de esta skill], no un estándar. Ninguna sentencia hallada trata este caso.

### Niveles aplicados a este agente
| Nivel | Qué hace el agente | Condición |
|---|---|---|
| Verde | Investigar, datos lingüísticos, features, compilar, control de calidad, auditar espaciado de archivos propios, pruebas, documentación, borradores de licencia para abogado, crítica de dibujos propios | Revisión humana normal |
| Ámbar | Código que escribe geometría según reglas humanas; sugerencias paramétricas; limpieza de dibujos humanos; imágenes de ambiente que nunca se calcan | Declarar y registrar por glifo; la persona controla cada decisión expresiva |
| Rojo para decir «original» | Contornos en los que la IA decidió la forma, publicados tal cual; transferencia de estilo; recibir fuentes ajenas; entrenar sin licencia; prometer exclusividad o copyright sobre glifos generados | No lo hagas. Si la persona quiere publicar lo primero, puede hacerlo declarándolo y sin llamarlo original: es lectura propia del nivel [inferencia] |

### Clasificar el origen de un glifo
Clasifica por quién decidió la forma, no por quién pulsó el botón [propuesta de esta skill]:

| Origen | Úsalo cuando | Detalle |
|---|---|---|
| `humano` | Una persona colocó los puntos en un editor, desde cero o en capa vacía, sin calcar salida generada | Quién y con qué programa |
| `codigo-regla-humana` | Una persona fijó por escrito la regla concreta (parámetro, proporción, lógica de terminal) y el código la ejecuta | Sección del brief, commit del generador, quién aprobó |
| `ia-modificado-humano` | Partió de salida del agente o de un modelo y una persona cambió su forma | Qué cambió y quién |
| `ia-generado` | El agente eligió la forma o la regla, y la persona solo aprobó | Qué pidió la persona |

- **Aprobar no es dibujar.** Un «me gusta» no convierte un glifo en `codigo-regla-humana`. Elegir entre alternativas del agente es zona gris: anótalo como `ia-generado` y descríbelo en el detalle.
- Una regla abstracta («que sea cálida») no es una regla humana suficiente. Tú estarías decidiendo la forma.
- Los compuestos heredan el origen de sus piezas. Los valores propuestos por el agente y aceptados sin cambios deben constar como tales.
- Ante la duda, usa el origen menos favorable a la autoría humana: sobredeclarar IA es corregible; una afirmación falsa, no.

### Cómo declararlo
Nunca reclames autoría para ti ni escribas «100 % a mano» si no es literalmente cierto. Di la verdad a clientes, distribuidores y registros. Ante la Oficina de Copyright de EE. UU., la expresión no humana se excluye de la solicitud [inferencia]. Revisa también las condiciones de cada distribuidor antes de enviar.

Plantilla de declaración, con los recuentos reales de `registro.py resumen`:

> {Familia} se diseñó con {persona} como responsable del concepto y de las decisiones de forma. Los contornos de {N} glifos los generó código escrito por un agente de IA ({modelo}) a partir de reglas fijadas por {persona}. {M} glifos fueron redibujados o corregidos a mano por {persona}. {P} glifos conservan forma decidida por la IA. La procedencia por glifo consta en el registro del proyecto, y el proceso incluyó auditorías de similitud, que no garantizan la unicidad.

No incluyas cifras que no salgan del registro. Pon a la persona como diseñadora en ID 9 solo si de verdad dirigió el diseño, y mantén accesible esta declaración [propuesta de esta skill].

### Consecuencias jurídicas plausibles
Todo este bloque es [inferencia] sobre las fuentes citadas: ninguna resolución trata contornos generados por código escrito por una IA.

| Capa | Efecto plausible | Estado |
|---|---|---|
| Copyright UE y España | Hace falta autor humano y aportación creativa. Una regla humana precisa ayuda; la ejecución del agente, no. Protección dudosa y, a lo sumo, parcial | Abierto; depende del grado de intervención |
| Selección de puntos, EE. UU. | El único asidero del software es la selección de puntos de un autor (*Adobe*). Puntos colocados por algoritmo no son esa selección, y la IA la erosiona | Asidero muy débil, aún más tras *Laatz* |
| Código generador | La Oficina ha registrado programas originales aunque su salida no sea protegible [dato legal: 57 FR 6201](https://archives.federalregister.gov/issue_slice/1992/2/21/6201-6203.pdf#page=2). Si el código lo escribió la IA, la exigencia de autoría humana le alcanza también | Débil; Compendium §723 no leído |
| Diseño registrado UE/España | Se apoya en novedad y carácter singular más que en la autoría; podría seguir disponible | **Pregunta abierta, sin autoridad hallada.** No lo prometas |
| Diseño no registrado UE | Misma incógnita; además, solo actúa frente a copia | Pregunta abierta |
| Marca y contrato | No dependen de quién dibujó: la marca cubre el nombre y la EULA obliga a quien la acepta | Los más estables; no impiden que un tercero sin contrato imite |
| OFL FAQ 1.25 | No conoces tu corpus de entrenamiento: no afirmes que no contiene fuentes. Si la lógica de la FAQ alcanza a tu salida, chocaría con una EULA propietaria. Un modelo de procedencia desconocida no se puede limpiar | Sin resolver. Publicar en OFL reduce el conflicto, no lo prueba. Avisa si el destino es EULA o encargo exclusivo |
| Parecido involuntario | Un modelo puede reproducir patrones vistos sin que nadie lo pretenda | Por eso se audita siempre, también lo generado por reglas |

Dilo a la persona desde la primera sesión, en lenguaje llano: «Con contornos generados por mí, tu protección puede ser menor y no sabemos cuánto. Puedo ayudarte a reforzarla, no a garantizarla.»

### Qué debe hacer la persona para reforzar su autoría
Cada acción deja rastro. Ninguna garantiza nada: no se conoce el umbral suficiente [propuesta de esta skill].

1. **Decidir antes.** Escribe y firma con fecha el concepto, la lógica de forma, los parámetros y las excepciones. Cuanto más concreta sea la decisión y antes de ver la salida, mejor.
2. **Corregir.** Da correcciones concretas de forma, no valoraciones. Guárdalas como notas por versión.
3. **Redibujar.** Es lo que más aporta: coloca tú los puntos de los glifos clave en un editor (`n o a e g` y los que dan carácter), con su commit. Eso devuelve a manos humanas la selección de puntos. Añádelos a la lista de glifos congelados para que el generador no los pise, y regístralos con su nuevo origen.
4. **Aprobar.** Deja constancia con nombre y fecha en cada puerta (`registro.py sello`). Aprobar sostiene el control, pero por sí solo no crea autoría.
5. **Registrar.** Sella con un tercero, guarda la primera divulgación, valora diseño registrado dentro de plazo y marca sobre el nombre. Pregunta a un abogado cómo declarar la IA en cada solicitud.

Si la fuente va a una EULA o a un encargo con garantía de originalidad, recomienda redibujar más glifos que en un proyecto libre. Una serifa de texto expresiva sigue siendo trabajo de mano humana; una geometría fuerte es el reparto más realista.

## Comunicación pública
Una frase pública es una afirmación verificable: debe poder sostenerse con el registro. Si no se sostiene, propón la versión verdadera en la misma respuesta [propuesta de esta skill].

| Aceptable (si es cierto y consta en el registro) | No aceptable | Por qué |
|---|---|---|
| «Diseñada de forma independiente, con proceso documentado» | «Garantizada como única» | Nadie puede garantizarlo |
| «Auditada con identificadores y revisión manual el {fecha}» | «Certificada como original», «libre de plagio» | No existe certificación |
| «Sin coincidencias relevantes en las herramientas usadas el {fecha}» | «0 % de similitud», «98 % original» | Ningún porcentaje vale como prueba |
| «Contornos generados por código a partir de reglas de {persona} y revisados por {persona}» | «100 % a mano», «artesanal», si hubo código o IA | Sería falso |
| «Se usó IA en {tareas}; detalle por glifo disponible» | «Hecha sin IA», si la hubo en contornos | Sería falso; el agente ya es IA |
| «{N} de {T} glifos redibujados a mano por {persona}» | «Diseñada por [nombre del modelo o del agente]», «autoría de la IA» | El agente no reclama autoría |
| «Revival de {fuente}, por {autor}; cambios: {lista}» | «Inspirada en» para ocultar un revival | Oculta el origen |
| «Licencia OFL 1.1» o «Licencia en {URL}» | «Protegida en todo el mundo», «con copyright garantizado» | La protección es territorial e incierta |
| «Sigue el género grotesco» | «Como {fuente}, pero gratis», «alternativa a {fuente}» sin revisar | Riesgo de marca y confesión de copia [inferencia] |

## Estados sin verificar
No conviertas estos puntos en hechos:
- **Convención de Viena:** Alemania la ratificó, pero parece no estar en vigor; la lista de WIPO, sin fecha, dice «Treaty not yet in force» [fuente: WIPO, vía búsqueda](https://wipo.int/export/sites/www/treaties/en/docs/other_treaties/vtf-parties.pdf). Trátala como no operativa.
- **EE. UU.:** Compendium §§723 y 906.4; informe parte 3, final o no [fuente: copyright.gov](https://www.copyright.gov/ai/); *Allen v. Perlmutter*; *Laatz* tras enero de 2026; acuerdo en *Bartz*; apelaciones de uso legítimo de 2026.
- **Reino Unido, Francia, España:** apelación en *Getty*; si se recurrió el caso de Le Monde, cuyas partes varían según la prensa; arts. 96 y 102 TRLPI, no leídos, y ninguna doctrina española sobre fuentes.
- **UE:** directrices de EUIPO marcadas como obsoletas; Ley de IA y exclusión de minería de datos para fuentes, no investigadas; detalles del Arreglo de La Haya.
- **Marcas:** no se comprobó ningún registro concreto, como Helvetica o Times New Roman.
