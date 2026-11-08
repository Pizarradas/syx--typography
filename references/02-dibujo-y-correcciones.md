**Cuándo leer este archivo:** mientras dibujas o corriges glifos, antes de pasar de un grupo de letras al siguiente, al añadir pesos, cursivas, versalitas o tamaños ópticos, y al hacer una crítica.

# Dibujo y correcciones ópticas

## Contenido

1. [Regla de trabajo](#1-regla-de-trabajo)
2. [Correcciones ópticas](#2-correcciones-ópticas)
3. [Reglas Bézier](#3-reglas-bézier)
4. [Orden de propagación](#4-orden-de-propagación)
5. [Proporciones por grupo](#5-proporciones-por-grupo)
6. [Pesos](#6-pesos)
7. [Interpolación y másteres](#7-interpolación-y-másteres)
8. [Anchuras](#8-anchuras)
9. [Cursivas](#9-cursivas)
10. [Versalitas](#10-versalitas)
11. [Tamaños ópticos](#11-tamaños-ópticos)
12. [Cifras](#12-cifras)
13. [Puntuación](#13-puntuación)
14. [Errores típicos](#14-errores-típicos)
15. [Guion de crítica](#15-guion-de-crítica)

## 1. Regla de trabajo

Mide y luego deja que gane el ojo: «the eye should win every time» ([fuente: Frere-Jones](https://stockholmstypografiskagille.se/typonyheter/typeface-mechanics-001/)). Las cifras de este archivo son puntos de partida: aplica la cifra, genera la prueba indicada, míralo y corrige. Un número medido en una tipografía comercial describe ese diseño; no es un objetivo.

Etiquetas: [dato] medición o estudio, [fuente: X] tutorial o autor, [convención], [inferencia]. `(extracto)` significa visto solo en un resumen de búsqueda y `(foro)`, opinión de practicante.

Pruebas base tras cada tanda: `check_sources.py X.designspace`, `build.py PROYECTO --rapido` y `proof.py fuente.ttf -o proofs/ --pagina control palabras`. `proof.py` dibuja 1 pt como 2 px, es decir, tamaño real ampliado 2×. Para probar un conjunto propio, añade `--texto "HOHOHO nonono"`.

## 2. Correcciones ópticas

Razón de fondo: el ojo no lee áreas ni medidas iguales como iguales. Lo redondo y lo puntiagudo parecen menores, las curvas y verticales parecen más finas, y los centros geométricos parecen bajos. Comprende el efecto y podrás estimar el caso que no aparece en la tabla.

### Rebasamiento

| Caso | Hipótesis de partida | Origen | Prueba |
|---|---|---|---|
| Redondas | 2 a 3 % de x o mayúscula; 10 a 15 u. sobre x de 500 | [fuente: Wikipedia, citando a Karow](https://en.wikipedia.org/wiki/Overshoot_(typography)), 1 a 3 %; [fuente: Glyphs](https://glyphsapp.com/learn/sketching) | `nonono`, `HOHOHO`: la o no debe parecer ni menor ni saltar |
| Titular | Unas 10 u.; más en cuerpos pequeños | [fuente: Glyphs](https://glyphsapp.com/learn/sketching) | `--pagina cascada`: el rebasamiento fijo no vale igual a 8 y a 96 pt |
| Vértices en punta | Unos 5 % (A) | Karow, solo visto por Wikipedia | `HAH`, `HVH`: la punta llega a la línea |
| Vértices anchos | Sobre la línea | [fuente: Microsoft](https://learn.microsoft.com/en-us/typography/develop/character-design-standards/uppercase) | Ídem; una negrita puede embotar la V y reducir el rebasamiento ([Frere-Jones](https://stockholmstypografiskagille.se/typonyheter/typeface-mechanics-001/)) |
| Redondas cuadradas o superelípticas | 0 a 1 % | [inferencia], sobre Frere-Jones: cuanto más cuadrada, menos rebasamiento | `oxo` a tamaño real |
| Redondas ascendentes y descendentes (f, g, j) | A menudo sin rebasamiento | [fuente: Microsoft](https://learn.microsoft.com/en-us/typography/develop/character-design-standards/lowercase) | `fhl`, `gpy` en línea |
| Con serifas de losa | Quizá menos | [fuente: TypeDrawers](https://typedrawers.com/discussion/comment/13023), foro, extracto | Solo si la losa hace el trabajo a la vista |

**Desacuerdo.** Briem mide o 4 % sobre x en Times Roman y 7 % en Courier y Helvetica ([fuente: Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/2-0-basics/briem-2-06-illusion/)), muy por encima del 1 a 3 %. Puede deberse a otra forma de medir; no se resolvió. Por defecto: 2 a 3 %, porque dos fuentes independientes coinciden y un rebasamiento pequeño se detecta y corrige con facilidad. Reserva valores superiores para cuando la prueba lo pida.

Iguala el rebasamiento arriba y abajo en la mayoría de fuentes de texto, pero lo importante es la igualdad visual, no la matemática ([fuente: Microsoft](https://learn.microsoft.com/en-us/typography/develop/character-design-standards/lowercase)). Un cuadrado reducido cerca de 1 % parece más cuadrado (Hoefler y Frere-Jones, vía [Wikipedia](https://en.wikipedia.org/wiki/Overshoot_(typography))).

### Grosores

| Relación | Hipótesis | Origen | Prueba |
|---|---|---|---|
| Curva frente a asta | Curva de 11,5 a 20 % más gruesa | [fuente: Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/2-0-basics/briem-2-05-verticals/): 11,5 % en una D de Baskerville, 20 % en Times; ejemplos, no norma | `noon`, `HOOH`: curva y asta deben pesar igual a la vista |
| Vertical frente a horizontal | Horizontal más fina; asta de E 20 % más ancha en un ejemplo negro | [fuente: Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/2-0-basics/briem-2-06-illusion/). No hay norma para sans monolineal; la cifra de «una décima» no se confirmó | `EHT`, `eHe`: H y E parecen monolineales |
| Mayúscula frente a minúscula | Probar H sobre n en +0, +13, +26 y +39 % | [fuente: Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/6-0-elbow-grease/briem-6-05-density/); una Baskerville Monotype llega a 36 %. +13 % funciona en un diseño y no garantiza nada en otro | Genera cuatro versiones de H y compara `Hamburg`, `HnHnHn` |
| Cuerpo y peso aparente | Letra pequeña parece más negra | [fuente: Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/6-0-elbow-grease/briem-6-05-density/): la H pequeña de su serie es 16 % más ligera | `--pagina cascada` |
| Formas reducidas (fracciones, superiores) | Más peso que la escala, sin llegar a todo el asta | [fuente: Microsoft](https://learn.microsoft.com/en-us/typography/develop/character-design-standards/figures) | `1/2 11/17` y `x2` junto a texto |

Razón de la diferencia mayúscula-minúscula: las astas de la minúscula están más juntas, así que la minúscula es más densa ([fuente: Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/6-0-elbow-grease/briem-6-05-density/)).

Las correcciones escalan con el contraste. Un monolineal necesita adelgazar horizontales de forma explícita; un diseño de contraste alto ya lo incorpora [inferencia]. Conserva rectángulos de referencia de asta y curva minúscula, asta y curva mayúscula y asta fina, y pégalos para comprobar ([fuente: Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/2-0-basics/briem-2-05-verticals/)).

### Centros y barras

- **8**: panza inferior algo mayor; mitades iguales se ven mal ([fuente: Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/2-0-basics/briem-2-06-illusion/)).
- **Barras centradas** (Eth, T con trazo) y panza de Thorn: el centro visual queda algo por encima del matemático ([fuente: Microsoft](https://learn.microsoft.com/en-us/typography/develop/character-design-standards/uppercase)).
- **Cintura**: es decisión de diseño; las contraformas superior e inferior no tienen por qué equilibrarse. Mezcla variantes alta y baja y elige ([fuente: Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/6-0-elbow-grease/briem-6-06-proportions/)).
- **Porcentajes de altura de barras en H, A, e, t: no se halló ninguno.** *Designing Type* cubre esto letra a letra y no fue accesible, y la idea extendida de que la barra de A va más baja que la de H queda sin verificar. Procede así: prueba tres alturas en `HAHeHt`, juzga en palabras y anota la elegida. La barra de A no tiene por qué coincidir con la de E en AE (Microsoft).

### Uniones, diagonales y cruces

Correcciones cualitativas de [Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/2-0-basics/briem-2-06-illusion/):

- Adelgaza la curva de r donde encuentra el asta para evitar un área negra.
- Alarga la contraforma de v para que su mitad inferior no oscurezca; las letras pequeñas necesitan contraformas más largas que las grandes.
- Suaviza la unión de semicírculo y recta para evitar el «efecto hueso», en el que el borde recto parece cóncavo.
- Si un fino cruza un grueso en ángulo puede parecer roto: desplaza los extremos del fino.

Una asta inclinada solo por sesgo queda más fina que una vertical, y una asta rotada puede parecer más pesada ([fuente: Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/4-3-italic/briem-4-33-stems/)).

**Trampas de tinta.** Son espacios negativos deliberados en las uniones para que la tinta no se acumule; hoy a menudo son estilo y en algunos cuerpos pequeños siguen siendo útiles ([fuente: Google Fonts](https://fonts.google.com/knowledge/glossary/ink_trap), extracto). **No se halló fuente de fundición con dimensiones.** No inventes una cifra: si el medio lo exige, prueba impreso en el soporte real y escanea ampliado.

### Letras con apertura

S y C suelen ser algo menores que O porque sus aberturas las hacen parecer mayores. Carter: «I judge them purely by eye» ([fuente: Microsoft](https://learn.microsoft.com/en-us/typography/develop/character-design-standards/uppercase)). Prueba: `OSOCO`.

## 3. Reglas Bézier

Reglas de [Glyphs, Drawing good paths](https://glyphsapp.com/learn/drawing-good-paths), salvo indicación. Razón general: un contorno sencillo y regular interpola mejor, admite hinting y es más fácil de corregir.

1. **Nodos en extremos**, donde la tangente es horizontal o vertical. Excepción: omítelos si crean curvas muy planas, como en el remate de una a.
2. **Triángulo mágico**: cada segmento cabe en el triángulo de sus dos nodos y el cruce de las prolongaciones de sus manejadores. Los manejadores no se cruzan.
3. **Dos manejadores por segmento curvo**. Evita manejadores nulos.
4. **Evita inflexiones**, porque pueden causar quiebros al interpolar. Excepción declarada: serifas cóncavas construidas sin inflexión.
5. **Economía de puntos**: añade extremos y borra intermedios uno a uno.
6. **Continuidad**: nodos suaves donde la curva sigue; elimina bultos moviendo el nodo medio hacia el lado más plano ([fuente: Glyphs](https://glyphsapp.com/learn/sketching)).
7. **Contornos cerrados**: los abiertos se ignoran al exportar.
8. **Solapamientos**: consérvalos en la fuente y elimínalos al exportar; revisa restos y huecos.
9. **Estructura idéntica entre másteres**: mismos puntos, mismo orden e inicio.
10. **Dirección**: exterior antihorario y contraforma horario en la convención de Glyphs. Ninguna fuente aquí confirma la dirección inversa en TrueType; las herramientas de compilación suelen encargarse.

`check_sources.py` bloquea por incompatibilidad, contornos abiertos, unicodes duplicados y componentes rotos. Avisa de extremos sin nodo, manejadores nulos, curvas fuera del triángulo, quiebros (uniones casi colineales, de 1,5 a 20°) e inflexiones dentro de un segmento (regla 4): esos avisos requieren criterio, porque hay excepciones legítimas.

### Tensión de curva

**Desacuerdo.** Dos tutoriales de Glyphs difieren: [uno](https://glyphsapp.com/learn/drawing-good-paths) sitúa la mayoría entre algo menos de 60 % y más de 70 %; [otro](https://glyphsapp.com/learn/sketching) usa 58 % y 76 % como límites y dice que casi todas acaban justo por debajo de 80 %. El segundo es incoherente consigo mismo en esos dos números. Coinciden en el círculo, 55–56 %, que suele ser demasiado bajo para tipografía, y en que los diseños geométricos usan al menos 57–58 %.

Por defecto: empieza en 60 a 70 %, zona común a ambos, y sal de ella solo con un motivo visible. Reglas:

- Interior más tenso que el exterior opuesto, sobre todo en negrita. Un fino puede usar un valor para ambos.
- Cuanto más cuadrada la forma, más tensión; la tensión es variable de estilo [inferencia].
- Mantén la distribución de manejadores entre másteres para limitar el descuelgue al interpolar.

Prueba: `--pagina cascada --texto "oe nh"`. Mira a 96 pt los bultos y a 12 pt el peso desigual.

### Cúbicas y componentes

Dibuja en cúbicas y convierte al compilar. cu2qu convierte juntas las curvas de todos los másteres para mantener la compatibilidad ([fuente: fontTools](https://fonttools.readthedocs.io/en/latest/cu2qu/index.html), extracto). Reutiliza con control: los componentes de esquina sirven para serifas, esquinas y trampas ([fuente: Glyphs](https://glyphsapp.com/learn/reusing-shapes-corner-components)); los inteligentes, para partes ajustables como el hombro de n en m y h ([fuente: Glyphs](https://glyphsapp.com/learn/smart-components)). Son funciones de Glyphs. En un flujo UFO, obtén el mismo efecto derivando desde un esqueleto paramétrico común [inferencia].

No se halló ensayo de diseñadores que compare reutilización con excepciones. Regla de trabajo: reutiliza la estructura y corrige el resultado donde la vista lo pida.

### Comprobación matemática

Una prueba PNG no enseña un rebasamiento de 31 u donde el brief dice 14, un corte a 26° de la vertical donde la regla dice 26° del trazo, ni un lateral de −15 u. Todo eso apareció en un proyecto real que pasaba `check_sources.py` y se veía bien en palabras [dato: auditoría de este proyecto, noviembre de 2026]. `verificar.py` lo mide con tolerancias explícitas; `--meta` comprueba que el propio verificador detecta cada defecto inyectado.

Errores que conviene evitar desde el generador [inferencia, a partir de esa auditoría]:

| Error | Por qué ocurre | Regla |
|---|---|---|
| Rebasamiento doble | El eje de una curva horizontal se coloca con el fino nominal, pero con eje inclinado el trazo horizontal es más grueso | `reglas.eje_en_zona(zona, grosor_real)` |
| Laterales desplazados | El avance se calcula desde la caja del dibujo y la tinta no empieza en x = 0 | `reglas.cerrar_desde_tinta` |
| Regla de terminal incoherente | Astas cortadas respecto al trazo y curvas respecto a la vertical | Una sola definición: ángulo respecto a la perpendicular al trazo, con el eje como bisectriz de los dos bordes reales; mídela con `verificar.json` → `cincel` |
| Restos de corte | Un corte booleano demasiado corto deja astillas; uno demasiado largo muerde otra parte de la letra | Corta el trazo aislado y con la raíz exacta de la cúbica (`trazo(..., ini=, fin=)` de `motor.py`) |
| Espolones en uniones | La panza entra en el asta a la altura de un vértice del asta | Que el remate de la panza quede dentro del asta; `verificar.py` marca rectas < 15 u entre dos esquinas |
| Quiebros por redondeo | Tiradores cortos redondeados a enteros | `reglas.alinear_tiradores` |

Al escribir comprobaciones propias, pruébalas con defectos inyectados antes de confiar en ellas: en esa misma auditoría, dos signos invertidos dejaron el test del triángulo y un límite de tensión sin efecto, y el informe decía «sin errores».

## 4. Orden de propagación

Secuencia sintetizada [inferencia]; ninguna fuente la da completa. Empezar por n es lo común, porque sus formas se repiten ([fuente: Glyphs](https://glyphsapp.com/learn/sketching)): primero estructura, luego esqueleto recto, igualar astas, fijar rebasamiento y al final las curvas.

1. **n, o**; prueba `noononno`.
2. **h, m, u, r, i, l** desde n; **c, e, b, d, p, q** desde o.
3. **a, s, g**, las letras difíciles que cargan personalidad; luego **f, t, j**.
4. **v, w, y, x, k, z**, diagonales.
5. **H, O**; luego **E, F, L, I, T, D**; **C, G, Q, S**; y diagonales **A, V, W, M, N, K, X, Y, Z**.
6. **Cero**, cifras, puntuación, y por último diacríticos y extras.
7. **Vuelve a n** tras la negrita: las concesiones de la negrita alimentan la regular; dibújalas en paralelo ([fuente: Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/4-2-bold/briem-4-22-limits/)).

Entrega por grupos, no glifo a glifo: no pases de grupo sin mirar `proof.py --pagina control palabras`. Cuando cambies n u o de forma notable, repropaga y repite.

**Mantén constante**: zonas de alineación, familias de astas, lógica de terminales, regla de contraste, ritmo entre astas y contraformas.
**Deja variar**: rebasamiento por forma, adelgazamiento de uniones, grosor de curva por letra, anchuras [inferencia].

Razón: «letters must be alike enough to form rhythm, and distinct enough to be told apart» es la idea de [LettError](https://letterror.com/archive/badtype). Copiar geometría exacta no da coherencia; aplicar la misma regla sí.

## 5. Proporciones por grupo

**No se hallaron proporciones numéricas por letra ni para mayúsculas.** La relación letra a letra de a, e, s, g está en *Designing Type*, que no fue accesible. Lo siguiente son relaciones cualitativas; obtén las cantidades en la prueba.

| Grupo | Letras | Reglas | Prueba |
|---|---|---|---|
| **Rectas minúsculas** | n h m u r i l | n como módulo; h de n y l; m de n, normalmente con contraformas más estrechas ([fuente: Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/4-2-bold/briem-4-24-curves/)); hombro de n reutilizable en m (más estrecho) y h (cruce más bajo) ([Glyphs](https://glyphsapp.com/learn/smart-components)). Diferenciar u de n no ayudó a la u ([Bohm](https://typography.guru/journal/letters-symbols-misrecognition/), secundaria): no lo hagas solo por legibilidad | `nmnhnunrn`, `minimum` |
| **Redondas minúsculas** | o c e b d p q | Panzas de b, d, p, q engordan como o y luego se ajusta la unión (Briem). c y e: abertura ligada a la apertura del brief | `obodopoqo`, `ocoeo` |
| **Personalidad** | a s g f t j | Sin regla numérica. Ensanchar t y l ayudó ([Bohm](https://typography.guru/journal/letters-symbols-misrecognition/), secundaria). s: mueve el centro al condensar (Briem) | `adhesion`, `hamburgefonstiv` |
| **Diagonales minúsculas** | v w y x k z | Contraforma de v alargada; en ultranegra, la pierna de k no puede igualar el asta y se afina, y un afinado leve puede pasar a la regular ([Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/4-2-bold/briem-4-22-limits/)) | `nvnwnynxn`, `kayak` |
| **Rectas mayúsculas** | H I E F L T D | H como módulo; revisar peso sobre n (§2) | `HEHFHLHTH` |
| **Redondas mayúsculas** | O C G Q S | S y C menores que O; Q comparte espaciado con O | `OCOGOQOSO` |
| **Diagonales mayúsculas** | A V W M N K X Y Z | Punta rebasa más; las de útil de traslación pesan distinto por dirección [inferencia] | `HAHVHWH`, `AVA` |

La anchura media de minúscula se acerca a la altura x [dato] ([Legge y Bigelow 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264)). Las proporciones humanistas derivan de capitales romanas y carolingia; las geométricas, de círculos y rectángulos ([fuente: Wikipedia](https://en.wikipedia.org/wiki/Vox-ATypI_classification)). Los mismos tres grupos organizan el espaciado (`03-espaciado-y-kerning.md`).

## 6. Pesos

### Curva de progresión

De Groot propuso en 1987 que los intermedios ópticamente correctos caen por debajo de la media lineal: entre 40 y 70, la seminegra queda algo por debajo de 55 ([fuente: De Groot](https://www.lucasfonts.com/learn/interpolation-theory)). La media geométrica da 52,9; esa equivalencia es lectura propia [inferencia], porque su fórmula solo aparece en imágenes.

**Desacuerdo.** Ben Blom sitúa las progresiones típicas sobre o bajo la recta; Linus Romer replica que por encima no son raras ([fuente: TypeDrawers](https://typedrawers.com/discussion/comment/34832), foro). Existen además curvas de compromiso, como las de Impallari y Schneider ([fuente: TypeDrawers](https://typedrawers.com/discussion/comment/68430), foro), cuyos resultados son punto de partida. Por defecto [inferencia]: usa la geométrica en rangos pequeños y una de compromiso en rangos amplios, porque en estos la geométrica se queda muy fina en el centro, como muestra el ejemplo.

Ejemplo con astas de 20 a 220 en nueve pasos [inferencia]:

| Paso | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| Geométrica (razón ≈ 1,35) | 20 | 27 | 36 | 49 | 66 | 90 | 121 | 163 | 220 |
| Lineal | 20 | 45 | 70 | 95 | 120 | 145 | 170 | 195 | 220 |

Ejemplo de familia corta con Regular 90 y Bold 140 [inferencia], razón ≈ 1,25 por paso: Light 72, Regular 90, Medium 112, Bold 140. La lineal daría Medium 115: en rangos pequeños la diferencia es de pocas unidades. Prueba: `--pagina pesos`, un párrafo con palabras en cada peso; los saltos deben parecer iguales. Imprime y ajusta durante días ([fuente: Puckett, TypeDrawers](https://typedrawers.com/discussion/comment/18466), foro).

Usa el asta de H o n como coordenada de interpolación. Muchos diseñadores ponen el valor del eje cerca de la anchura del asta; Glyphs usa Regular 100 y Bold 250 como ejemplo, no objetivo ([fuente: Glyphs](https://glyphsapp.com/learn/multiple-masters-part-1-setting-up-masters)).

### Objetivo de negrita

Negrita de dos quintos a dos tercios más pesada que la regular ([fuente: Briem](https://blog.fontlab.com/2024/04/08/briem-bold-italic-spacing/)). Una regular de 90 da 126 a 150 [inferencia], o 25 a 30 % de una x de 500, dentro del rango medido en sans negritas de 18,9 a 40 % [dato] ([von Ompteda](https://researchonline.rca.ac.uk/5084/1/PhD%20von%20Ompteda%20-%20RCA%20Repository.pdf), extracto). Los ejemplos 40→70 (+75 %) y 100→250 (+150 %) van más lejos: ilustran método, y el segundo puede ser un máster más pesado.

Prueba: pon palabras negritas en un párrafo regular y comprueba que destacan sin agujerear. Evita una negrita cuya asta se acerque al hueco de la contraforma (Nick Shinn, [TypeDrawers](https://typedrawers.com/discussion/comment/18466), foro).

### No es un solo número

Los trazos horizontales crecen más despacio que los verticales. Una familia de 1:1 a 3:1 vertical:horizontal no debería usar 2:1 en el punto medio, porque funciona mejor un contraste algo menor ([fuente: De Groot](https://www.lucasfonts.com/learn/interpolation-theory)). Cada topología necesita su curva: L tiene un solo trazo horizontal y mucho sitio; F y C reparten altura entre dos; el euro tiene cuatro y es de los casos difíciles. Llega un punto en que las horizontales no pueden engordar sin que la letra desaparezca; las verticales tienen más margen. Prueba: `LFCE€` en todos los pesos con `--pagina pesos`.

### Reparto del peso

Hipótesis para o, u, a: **3/4 hacia dentro, 1/4 hacia fuera** ([fuente: Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/4-2-bold/briem-4-23-where/)). Todo por fuera solo conviene a letras extendidas y todo por dentro a condensadas.

Ejemplo [inferencia]: de asta 90 a 140, añade 50 por trazo: unas 37 hacia la contraforma y 13 hacia fuera. La n crece poco de anchura y su contraforma se reduce, razón por la que la negrita necesita apretar el espaciado.

- Los finos de o, c, e se mantienen casi constantes; la curva inferior de c y e necesita un extra; la curva derecha de e puede ser más ligera que la izquierda (Briem).
- Un fino de negrita puede ser tan fino como el de la regular; uno más pesado solo conviene a unos 8 pt o menos ([fuente: Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/4-2-bold/briem-4-24-curves/)).
- Construye por partes: n desde u invertida, h de n y l, m de n; panzas como o. En b: asta negrita, contraforma reducida en horizontal hasta la de o, en vertical hasta que los finos igualen u, y curva exterior hasta el grosor de o (Briem).
- Astas más pesadas no bastan para un texto denso: aprieta el espaciado; acortar serifas ayuda ([fuente: Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/4-2-bold/briem-4-22-limits/)).

### Altura x en negritas

**Sin consenso.** Una encuesta rápida halló mitad y mitad ([fuente: TypeDrawers](https://typedrawers.com/discussion/1060/taller-x-heights-for-bolder-weights), foro); Kent Lew habla de 10 a 20 unidades ([fuente: TypeDrawers](https://typedrawers.com/discussion/comment/69785), foro); las alturas iguales se han hecho más comunes, en gran parte por el texto en pantalla (Puckett). Por defecto [inferencia]: en interfaz, mantenla igual, porque Puckett liga esa práctica al texto en pantalla; en impresión, prueba +10 a +20 con negritas mezcladas en un párrafo ligero, la prueba que propone Rushton.

## 7. Interpolación y másteres

- **Coloca másteres en los extremos** y añade intermedios solo donde falle. Hace falta uno en cada extremo de eje, no en cada esquina (Hudson, [TypeDrawers](https://typedrawers.com/discussion/3612/what-is-best-practise-in-variable-font-development), extracto). Mínimo: ejes + 1, probado primero sin más ([fuente: Scheichelbauer](https://forum.glyphsapp.com/t/how-to-set-up-the-values-for-three-axis-variable-font-how-many-masters/12066), extracto).
- **Dibuja el extremo muy pesado**: interpolar es seguro y extrapolar no ([fuente: Briem](https://blog.fontlab.com/2024/04/08/briem-bold-italic-spacing/)). Elige extremos según el uso más extremo previsto, de forma que sobrevivan las contraformas [inferencia].
- **Desacuerdo**: un diseñador trabaja desde los extremos y otro afirma que desde el centro la calidad es mejor; un máster extra da algo más de control a costa de archivos y trabajo mucho mayores ([fuente: TypeDrawers](https://typedrawers.com/discussion/2185/multiple-master-designspace-design-workflow), extracto). Por defecto: extremos, porque garantiza que el espacio no requiere extrapolación; valida en el punto medio enseguida.
- **Extrapolación**: ninguna fuente respalda publicar resultados extrapolados. Para pasar de un máster, convierte esa posición en extremo del eje.
- **Corrección local**: capas intermedias o másteres de glifo antes que promover un máster completo ([fuente: FontLab](https://help.fontlab.com/fontlab/7/manual/Working-with-Font-Variations/), extracto, documentación antigua, a comprobar). No se halló tutorial sobre límites de calidad de la extrapolación.
- **Origen**: Regular para escritorio; un extremo para web, por tamaño ([fuente: Glyphs](https://glyphsapp.com/learn/creating-a-variable-font)). El origen Regular es el más compatible, y es el valor por defecto de esta skill.
- **Compatibilidad por construcción**: deriva todos los másteres de un esqueleto paramétrico común [inferencia]. Si editas a mano, usa el mismo orden de contornos.

Prueba: `check_sources.py`, `build.py PROYECTO --rapido`, `proof.py --pagina pesos` y varios `--var wght=...` en esquinas y puntos medios. Busca quiebros, contraformas cerradas y saltos de peso.

## 8. Anchuras

No se halló planificación numérica de familias de anchura. Comprimir por escala es un error clásico: distorsiona contraformas y curvas ([fuente: Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/4-0-modules/briem-4-10-squeeze/)). El procedimiento de Briem parte de escalar a 50 %, restaura alturas, sube la minúscula, reconstruye 21 letras, mueve el centro de s, corrige k y revisa z. Condensar mucho debilita la legibilidad (Waller 2010, vía [Herrmann](https://typography.guru/journal/what-makes-letters-legible-r37/), secundaria).

## 9. Cursivas

**Decide primero: cursiva verdadera u oblicua.** La verdadera es otra construcción y conviene empezarla de cero (Hudson, [TypeDrawers](https://typedrawers.com/discussion/2861/how-do-i-start-working-on-italics), extracto). Inclinar y corregir se aplica sobre todo a oblicuas (Typogopher, [Glyphs Forum](https://forum.glyphsapp.com/t/best-practices-for-obliques-in-the-same-glyphs-file/25163), foro).

Flujo [inferencia]: concepto → inclinación y pivote → n, a, e, o como formas cursivas → mayúsculas inclinando y corrigiendo → espaciado con control inclinado → kerning de la redonda solo como semilla.

**Ángulo.** No se confirmó ningún rango estándar. Datos sueltos: una familia subió a 12° para separarse de su redonda ([fuente: Klim](https://klim.co.nz/blog/tiempos-design-information/), extracto); unos 20° se llaman «bastante inclinada» y dan problemas de contraste en los pesos más finos ([fuente: TypeDrawers](https://typedrawers.com/discussion/comment/59096), foro). La convención de 8 a 12° no se confirmó. Prueba: palabras en cursiva dentro de un párrafo redondo.

**Pivote.** Desacuerdo: Simonson prefiere la mitad de la altura x, porque un anclaje en la línea de base desplaza las mayúsculas a la derecha frente a la redonda; Seifert sostiene que basta con que sea coherente ([fuente: TypeDrawers](https://typedrawers.com/discussion/1378/italics-workflow), foro). Por defecto: mitad de x, un solo pivote para todos los glifos. Cumple ambas condiciones.

**Peso.** Un sesgo adelgaza la perpendicular solo 1 % a 8° y 6 % a 20° [inferencia] (geometría: coseno del ángulo). Sin embargo, las cursivas de Galliard y Stempel Garamond tienen astas 15 % más ligeras que su redonda ([fuente: Briem](https://help.fontlab.com/fontlab/8/tutorials/briem/4-3-italic/briem-4-33-stems/)). La mayor parte del aligeramiento responde a densidad y curvas, porque las cursivas son más estrechas y sus astas quedan más juntas. Prueba: párrafo mixto; debe compartir gris con la redonda.

**Oblicuas.** Mezcla sesgo y rotación: Carewe usa entre 50/50 y 60/40, con menos rotación a más ángulo y anchura ([fuente: Glyphs Forum](https://forum.glyphsapp.com/t/best-practices-for-obliques-in-the-same-glyphs-file/25163), foro). Larabie estrecha los glifos antes de inclinar (foro). Inclinar sin más no suele dar un gris igual a la redonda ([fuente: TypeDrawers](https://typedrawers.com/discussion/comment/2105/), extracto). Las mediciones de Briem en dos sans no mostraron compensación por inclinación en sus oblicuas.

**Encaje.** La cursiva debe funcionar con la redonda porque comparten palabras: prueba pares y ajusta laterales en la frontera ([fuente: Briem](https://blog.fontlab.com/2024/04/08/briem-bold-italic-spacing/)). El negro suele quedar a la derecha del centro matemático ([fuente: Microsoft](https://learn.microsoft.com/en-us/typography/develop/character-design-standards/lowercase)). Simonson acepta laterales negativos en cursiva ([fuente: TypeDrawers](https://typedrawers.com/discussion/1378/italics-workflow), foro).

## 10. Versalitas

Conserva el grosor de asta: no las obtengas por escalado. Sintetizadas quedan demasiado ligeras, apretadas y a menudo estrechas ([fuente: Monotype](https://www.myfonts.com/pages/fontscom-learning-fontology-level-1-type-anatomy-small-caps)).

| Parámetro | Hipótesis | Origen | Prueba |
|---|---|---|---|
| Altura | Algo sobre x: 530 sobre x de 480, unos +10 % | [fuente: Glyphs](https://glyphsapp.com/learn/making-small-caps) | Palabras en versalita dentro de un párrafo |
| Altura, alternativa | 10 a 15 % sobre x | [fuente: CreativePro](https://creativepro.com/good-things-small-packages/), extracto | Ídem |
| Altura, relativa | 65 a 80 % de la mayúscula | [fuente: Microsoft](https://learn.microsoft.com/en-us/typography/develop/character-design-standards/uppercase) | Ídem |
| Espaciado | «Un poco más» | Glyphs | `--feat smcp --texto "nonon hamburgefons"` |

**Desacuerdo de grado.** Monotype dice «muy ligeramente» más altas, frente al 10–15 %. Con x / mayúscula de 0,7, ese rango equivale a 77–80 % de la mayúscula, compatible con Microsoft [inferencia]. Por defecto: +10 % en texto, y sube si parecen raquíticas. La dirección horizontal/vertical de la página de Microsoft es contradictoria (sus ejemplos dicen lo contrario a su frase): no te apoyes en ella. Modula la ganancia de anchura entre pesos, porque los pesados ya parecen más cuadrados ([fuente: TypeDrawers](https://typedrawers.com/discussion/comment/61480), foro, extracto).

Da a las versalitas sus zonas de rebasamiento. En español, prepara `exclamdown.c2sc` y `questiondown.c2sc` ([fuente: Glyphs](https://glyphsapp.com/learn/making-small-caps)). Las cifras no casan con versalitas: añade `.sc` ([fuente: Glyphs](https://glyphsapp.com/learn/small-cap-figures), extracto). Prueba: `proof.py --feat smcp --pagina texto`.

## 11. Tamaños ópticos

**Desacuerdo.** Se espera en cuerpos pequeños más peso, menos contraste, más anchura, a menudo más x, astas más cortas, aperturas mayores, formas más simples y más espaciado (Ahrens y Mugikura, vía [Cozens](https://simoncozens.github.io/optical-size); los valores medidos del manual no estuvieron disponibles). Las mediciones de Cozens sobre el catálogo de Google discrepan [dato]: la altura de ascendentes apenas cambia, la altura x es mixta y no surge fórmula clara; el espacio entre palabras suele bajar con `opsz` y la anchura suele estrecharse con el tamaño. Él mismo advierte que su medida puede limitar el resultado de contraste y desconfía de su modelo de R² 0,90.

Por defecto: reduce contraste primero, porque se describe como el ajuste más importante, y añade espaciado; decide el resto probando. Prueba: `--pagina cascada` y papel. Los diseños grandes se optimizan para elegancia más que para legibilidad ([Larson y Carter 2015](https://www.microsoft.com/en-us/research/uploads/prod/2021/06/Larson-Carter-2015-Sitka.pdf), extracto).

## 12. Cifras

- **Modelo**: cero como base de espaciado y forma ([fuente: Microsoft](https://learn.microsoft.com/en-us/typography/develop/character-design-standards/figures)).
- **Alineadas**: alturas planas de mayúscula en la mayoría de tipografías.
- **Proporcionales**: a menudo comparten el ancho del cero, con el 1 más estrecho. Dólar, libra, euro y similares van al ancho de cifra.
- **Elzevirianas**: 0, 1, 2 en altura x; 3, 4, 5, 7, 9 bajan; 6, 8 suben.
- **Superiores**: escala horizontal 63 %, vertical 60 % y rebasamiento cerca de 60 % del de cifra; refuerza trazos, porque la escala adelgaza.
- **Sufijos**: `.tf`, `.tosf`, `.lf`, `.osf`; Glyphs detecta elzevirianas si el cero es más de 17 % más corto que el ocho ([fuente: Glyphs](https://glyphsapp.com/learn/figure-sets)).
- **8**: panza inferior mayor (§2).
- **Euro**: no copies el logotipo de la Comisión; redibújalo por fuente ([fuente: Microsoft](https://learn.microsoft.com/en-us/typography/develop/euro)).
- **Tabulares**: glifos nuevos, sin kerning. Google exige proporcionales por defecto y la especificación señala que las tabulares suelen serlo; sigue a Google si le envías la fuente.

Son documentos heredados editados entre 2018 y 2023: sus reglas de diseño valen, sus notas de software no. **No se halló fuente sobre elección de anchura tabular ni construcción de moneda.**

Prueba: `H0H1H2H3H4` en `--pagina control`, `--feat tnum --texto "1111 0000 7171"`, y `--feat frac --texto "1/2 11/17 2 1/4"`.

## 13. Puntuación

Sin procedimiento autorizado de diseño de puntuación. Valores de [Microsoft](https://learn.microsoft.com/en-us/typography/develop/character-design-standards/punctuation) como hipótesis:

| Elemento | Hipótesis | Prueba |
|---|---|---|
| Punto, coma, dos puntos, punto y coma | Mismo avance, centrados a la vista entre n y o | `n,n.n;n:n` |
| Punto centrado | Tamaño del punto | `l·l` |
| Paréntesis | Arriba según alturas de mayúscula; abajo, 1/2 a 3/4 del descendente | `(Hp)` |
| Comillas angulares | Alineadas con la altura x | `«nHn»` |
| Guiones | Centrados en la altura x | `n-n n–n n—n` |
| Interrogación | Altura redonda de mayúscula | `n?nH?H` |
| Subrayado | 5 a 10 % del em bajo la línea de base | Texto subrayado con `p g y` |

**Español** [inferencia], a partir de la RAE, que considera obligatorios los signos de apertura y prefiere las comillas angulares en impresos: ¿ ¡ no deben ser una simple rotación; necesitan formas `.case` para caja alta; cuida `¿A ¡T «A`; armoniza ª º con `ordn` para 1.º y 2.ª. No se recuperó el texto de la RAE sobre letra voladita. Prueba: `proof.py --pagina idiomas`, con líneas de catalán `COL·LEGI` y `paral·lel`.

**Ligaduras y ampersand.** Dibuja las ligaduras de serifa una a una, con transición suave; en sans suelen ser versiones apretadas de los glifos base. El peso de & se relaciona a menudo con la minúscula ([fuente: Microsoft](https://learn.microsoft.com/en-us/typography/develop/character-design-standards/lowercase)).

## 14. Errores típicos

Procede mayoritariamente de foros: refleja consenso de práctica, no prueba ([fuente: TypeDrawers](https://typedrawers.com/discussion/comment/59302), foro).

| Error | Síntoma | Corrección |
|---|---|---|
| Espaciar mal, y espacio demasiado ancho | Texto a rachas o huecos entre palabras | Espacia a tamaño de lectura; ver `03-espaciado-y-kerning.md` |
| Imitar sin propósito | Nada propio que declarar | Vuelve a la regla del útil y al brief |
| Kerning prematuro | Muchos pares pequeños | Primero laterales |
| No revisar todos los glifos | Primeras letras mejores o distintas | Repasa desde n |
| Curvas con bultos o proporciones dispares | «Los delatores obvios» ([TypeDrawers](https://typedrawers.com/discussion/comment/13283/), foro) | Curvas, `check_sources.py` y reglas de §3 |
| Condensar por escala | Curvas planas, contraformas mal | §8 |
| Trabajar con mucho zoom | Espaciado apretado | Prueba a tamaño real ([Glyphs](https://glyphsapp.com/learn/spacing)) |
| Dar por terminada la fuente pronto | «when you think you're [*sic*] typeface is done, it probably isn't» (FettleFoundry) | Pausa y vuelve con ojos frescos |

## 15. Guion de crítica

Orden sugerido [inferencia]; no se halló guía de crítica publicada por fundiciones. Usa `proof.py`:

1. **Palabras y párrafo a tamaño de uso** (`texto`, `palabras`). Lee, no inspecciones.
2. **Desenfoca o entorna los ojos** para ver el color: localiza manchas oscuras y claras. Voltear o desenfocar da ojos frescos ([Glyphs](https://glyphsapp.com/learn/spacing)).
3. **Cadenas**: `noononno`, `HOHOHO`, `minimum`, `0n0`, caja mixta y todo mayúsculas (`control`).
4. **Glifos atípicos** (`glifos`).
5. **Desambiguación**: `Il1 O0 rn m cl d`.
6. **Contornos**: bultos (`check_sources.py`).
7. **Pares**: redonda con cursiva, regular con negrita (`pesos`).

Preguntas de [LettError](https://letterror.com/archive/badtype), que se declara «wholly subjective and unscientific»: ¿es coherente?, ¿se parecen y se distinguen lo justo?, ¿formas fluidas?, ¿progresión de peso y anchura sensata?, ¿caracteres notablemente buenos o malos?, ¿conjunto completo y diacríticos?, ¿funciona en columna?, ¿tiene razón de existir?, ¿sirve al idioma?, ¿es familiar al lector?

Para texto, añade de [Amado](https://typedesign.fba.up.pt/?p=571): color a 8–12 pt, métricas, eje, arcos, ritmo, laterales, cierre de aperturas, uniones y compensaciones ópticas. El color y la textura uniformes son probablemente la cualidad más importante de una buena tipografía de texto ([fuente: Monotype](https://www.myfonts.com/pages/fontscom-learning-fyti-typographic-tips-good-text-face-part-one)).

Busca crítica humana en el mismo género con pruebas a tamaño real antes de publicar. Solo importa el resultado: si la cifra y el ojo discrepan, gana el ojo, y anota por qué.
