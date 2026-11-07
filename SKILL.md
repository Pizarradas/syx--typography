---
name: diseno-tipografias
description: "Diseña tipografías y fuentes originales de principio a fin: brief, dibujo de glifos, espaciado, kerning, OpenType, fuentes variables, cobertura de idiomas, control de calidad, optimización web (WOFF2), licencias y originalidad. Úsala siempre que alguien quiera crear, dibujar o producir una tipografía, typeface, font o familia tipográfica, generar un .ttf/.otf/.woff2 propio, diseñar una fuente de marca, monoespaciada, de texto o display, revisar o mejorar una fuente propia (espaciado, kerning, métricas, features, variable), o trabajar con UFO, designspace, Glyphs, FontLab, Fontra, fontmake o fontTools, aunque no diga «skill». También sirve para decidir qué programa usar, para preparar una fuente propia para la web y para responder a «hazme una fuente igual que X». No es para elegir fuentes existentes para un diseño ni para maquetar con ellas."
license: MIT
compatibility: "Requiere Linux, macOS o WSL2, Python gestionado con uv y git. Algunas herramientas se instalan en un entorno aislado."
---

# Diseño de tipografías originales

Una tipografía no se dibuja letra a letra: se construye como un sistema. Un concepto escrito se traduce en parámetros, se prueba en palabras reales, se corrige a ojo y se convierte en un archivo verificado. Esta skill organiza ese trabajo como lo haría un equipo: dirección de tipo, dibujo, espaciado, ingeniería, idiomas, web y procedencia.

## Principios

1. **Cada cifra es una hipótesis.** Los números de esta skill son puntos de partida con su prueba. Si la prueba visual contradice al número, gana el ojo.
2. **Se mira, siempre.** Tras cada cambio de forma genera una prueba PNG y ábrela con Read. Sin ver el resultado no hay decisión de diseño; un script que pasa no significa nada estético.
3. **Se trabaja en palabras.** Nunca juzgues un glifo aislado. La letra existe en `noononno`, «adhesion» y un párrafo a tamaño real.
4. **Se dice la verdad sobre el alcance.** El agente garantiza lo verificable (compatibilidad, nombres, métricas, features, cobertura, compilación). No puede garantizar belleza, ritmo final, soporte de escrituras sin revisor nativo ni originalidad absoluta.
5. **Original de verdad.** Nunca se parte de contornos, métricas ni kerning ajenos. Las referencias informan del género, no de las formas. Si piden clonar una fuente, lee `references/08-originalidad-licencias-ia.md` y propón una alternativa original.

## Arranque

Las rutas `scripts/`, `references/` y `assets/` de la skill y de sus referencias son relativas a `${CLAUDE_SKILL_DIR}`, y `$PY scripts/x.py` en una referencia significa `$PY ${CLAUDE_SKILL_DIR}/scripts/x.py`. Los proyectos de fuentes se crean fuera de esa carpeta.

Prepara el entorno una vez y úsalo para todos los scripts. Si falta `uv`, `setup_env.sh` se detiene e indica cómo instalarlo: pídeselo a la persona, no lo instales por tu cuenta.

```bash
PY=~/.local/share/type-design/venv/bin/python
[ -x "$PY" ] || bash ${CLAUDE_SKILL_DIR}/scripts/setup_env.sh
```

Después fija cuatro cosas. Pregunta solo lo que no se pueda deducir del pedido. Si el encargo es «hazlo todo tú» o no se puede preguntar, decide con los valores por defecto, marca cada decisión como *pendiente de aprobación* en `BRIEF.md` y en el informe, y registra los glifos como `ia-generado`: el nombre, la licencia y la autoría siguen siendo de la persona.

- **Uso:** medio, cuerpos, idiomas, licencia.
- **Modo de trabajo:**
  - *Agente por código*: esqueleto paramétrico, ideal para geométricas, modulares, monoespaciadas, píxel y stencil.
  - *Persona con editor*: el agente hace ingeniería, QA y web. Mejor para texto serifa, cursivas y caligrafía.
  - *Híbrido*: el agente hace el borrador y la persona corrige n, o, H, O, a, e, g.
- **Programa:** por defecto, UFO + designspace en WSL. Fontra Pak (gratis) o FontLab 9 en Windows, Glyphs 4 en macOS. Detalles en `references/04-programas-y-toolchain.md`.
- **Alcance realista:** el coste es glifos × másteres. Un primer proyecto sano es una Regular (o variable en peso) con letras básicas del español. Una familia profesional lleva meses: dilo antes de empezar. Si piden una serifa expresiva solo por código, avisa de que el resultado será un borrador.

## Fases y puertas

No avances sin superar la puerta. Las puertas evitan el fallo más caro, un concepto mal definido que se descubre al final. Este flujo es una síntesis propia de esta investigación, no un estándar publicado.

### 0. Concepto
Crea el proyecto y rellena el brief:
```bash
$PY ${CLAUDE_SKILL_DIR}/scripts/new_project.py RUTA --family "Nombre" --wght 300:400:700 --x-height 510 --cap 700
```
Lee `references/01-brief-y-parametros.md`. Escribe por qué debe existir, usos, modelo de trazo e hipótesis de parámetros. Haz la búsqueda de nombre y el primer registro.
**Puerta:** `BRIEF.md` responde a «qué mejora» y hay un primer `registro.py sello`.

### 1. Prueba de concepto
Dibuja n, o, H, O; luego a, d, e, h, s. Lee `references/02-dibujo-y-correcciones.md`. Si dibujas por código, usa `scripts/trazos.py` y el patrón de `assets/ejemplo_generador.py`.
```bash
$PY ${CLAUDE_SKILL_DIR}/scripts/check_sources.py sources/Familia.designspace
$PY ${CLAUDE_SKILL_DIR}/scripts/build.py PROYECTO --rapido
$PY ${CLAUDE_SKILL_DIR}/scripts/proof.py fonts/variable/*.ttf -o proofs --pagina control palabras --texto "..."
```
**Puerta:** la idea se percibe en palabras y lo aprueba la persona. Muéstrale las pruebas y pregunta. Primera auditoría de similitud.

### 2. Primer borrador
Completa minúscula, mayúsculas, cifras y puntuación con espaciado grueso. Lee `references/03-espaciado-y-kerning.md`.
**Puerta:** color uniforme en texto corrido (`proof.py --pagina texto cascada oscuro`). Segunda auditoría.

### 3. Familia
Extremos de peso y anchura, cursiva, versalitas. Los másteres van en los extremos; añade intermedios solo si falla la interpolación. Nunca publiques extrapolaciones.
```bash
~/.local/share/type-design/venv/bin/fonttools varLib.interpolatable sources/Familia.designspace
```
Detecta puntos iniciales girados y contornos invertidos, que `check_sources.py` no ve.
**Puerta:** `check_sources.py` sin errores, `interpolatable` limpio y `proof.py --pagina pesos` sin saltos ni quiebros.

### 4. Cobertura
Diacríticos, conjunto de glifos e idiomas. Lee `references/06-idiomas-y-cobertura.md`. El español exige ¿ ¡ ñ ª º « » € bien dibujados, no rotados ni heredados.
```bash
$PY ${CLAUDE_SKILL_DIR}/scripts/coverage.py FUENTE.ttf --langs spa,cat,glg,eus,ast,por
```
**Puerta:** cobertura limpia en los idiomas del brief, con texto real en `proof.py --pagina idiomas`. Escrituras que no lees: revisor nativo o se declaran sin revisar.

### 5. Ingeniería
Kerning, features, métricas, nombres, hinting. Lee `references/05-ingenieria-opentype.md`. Escribe pruebas en `tests/shaping.json`: si una regla no tiene prueba, no está terminada.
```bash
$PY ${CLAUDE_SKILL_DIR}/scripts/build.py PROYECTO --con-fontc
```
**Puerta:** compilación de un comando, OTS limpio, coherencia y pruebas de conformación superadas.

### 6. Calidad
```bash
$PY ${CLAUDE_SKILL_DIR}/scripts/build.py PROYECTO --qa        # informes en qa/; --solo-qa no recompila
```
Resuelve o justifica cada FAIL. Una compilación con QA vacío es un error, no un aprobado. Prueba en lo que el agente no puede ver: navegadores reales (Playwright y Chromium pueden no estar disponibles), Windows a baja densidad, macOS, Word, impresión. Pide esa revisión a la persona, con una lista concreta.
**Puerta:** revisión humana firmada y crítica externa si es para publicar.

### 7. Publicación
Exporta y verifica. Lee `references/07-web.md` y `references/08-originalidad-licencias-ia.md`.
```bash
$PY ${CLAUDE_SKILL_DIR}/scripts/web_export.py fonts/variable/*.ttf -o web --slug nombre
$PY ${CLAUDE_SKILL_DIR}/scripts/shape_tests.py fonts/variable/*.ttf tests/shaping.json --comparar web/nombre-v1.woff2
```
**Puerta:** última auditoría de similitud, búsqueda de marca, licencia en los campos del archivo, WOFF2 sin caracteres ni features perdidos, conformación igual a la del TTF y `registro.py resumen` sin glifos sin registrar.

## Registro de procedencia

Es lo que convierte el proceso en prueba de autoría y honestidad. Mantenlo desde el primer contorno:

```bash
# La persona dictó una regla de forma concreta y el código la ejecuta:
$PY ${CLAUDE_SKILL_DIR}/scripts/registro.py glifo PROYECTO n,o,H,O codigo-regla-humana "regla del brief: terminal a 17°, decidida por la persona"
# El agente decidió la forma (p. ej., «hazlo todo tú»), aunque la persona apruebe después:
$PY ${CLAUDE_SKILL_DIR}/scripts/registro.py glifo PROYECTO a,e,g ia-generado "forma decidida por el agente"
$PY ${CLAUDE_SKILL_DIR}/scripts/registro.py sello PROYECTO "aprobada la prueba de concepto"
```

Elige el origen con rigor: una petición abstracta no es una regla humana, y aprobar no es dibujar. Criterios en `references/08-originalidad-licencias-ia.md`. Una fuente recibida usa `heredado-desconocido`. Confirma en git antes de cada sello; en un proyecto recibido sin repositorio, pide permiso para crearlo y, si no, el sello queda como `sin-commit`. Nunca escribas «100 % a mano» si no es cierto.

## Dibujar por código con calidad

- Cada glifo es una función de parámetros que emite siempre la misma secuencia de puntos. La compatibilidad entre másteres queda garantizada por construcción.
- Usa `scripts/motor.py` para trazos con grosor variable, cortes de terminal y anillos, y `scripts/trazos.py` para contornos directos. Un corte debe actuar siempre sobre el mismo segmento: si cambia de segmento según el máster, cambia el número de puntos.
- Recoge los fallos por glifo y guarda los másteres solo al final. Un fallo a medio máster deja archivos desiguales y `check_sources.py` da decenas de errores que esconden la causa.
- Pon los parámetros en un solo lugar y deriva de ellos asta, fino, rebasamiento y espaciado. No dupliques números por glifo.
- Evita la geometría pura. Compensa curvas frente a rectas, horizontales frente a verticales, uniones y mayúsculas frente a minúsculas. Un círculo perfecto se ve mal.
- Reutiliza partes (hombro, panza, remate), pero corrige ópticamente cada glifo. El sistema da coherencia; la excepción da vida.
- Protege lo que la persona retoque: lista de glifos congelados que el generador no sobrescribe.

## Herramientas

| Script | Para qué |
|---|---|
| `scripts/setup_env.sh` | Instala la cadena en un entorno aislado |
| `scripts/new_project.py` | Crea UFO, designspace, brief y registro |
| `scripts/trazos.py` | Contornos directos: rectas, óvalos, componentes, anclas |
| `scripts/motor.py` | Motor de trazos: esqueleto a contorno, con cortes de terminal y anillos |
| `scripts/check_sources.py` | Compatibilidad, contornos abiertos, nodos en extremos, tensiones |
| `scripts/build.py` | Compila y ejecuta OTS, coherencia, conformación, fontc y QA |
| `scripts/proof.py` | Pruebas PNG: control, palabras, texto, cascada, glifos, pesos, idiomas, oscuro |
| `scripts/shape_tests.py` | Pruebas de conformación con HarfBuzz; `--comparar` frente a un WOFF2 |
| `scripts/coverage.py` | Cobertura de letras, signos y marcas por idioma con Hyperglot |
| `scripts/web_export.py` | WOFF2, CSS, verificación de caracteres y features, presupuestos |
| `scripts/registro.py` | Procedencia por glifo y sellos con hash |
| `scripts/copy_check.py` | Alarma de calco entre dos fuentes; no certifica originalidad |

## Referencias

| Archivo | Cuándo leerlo |
|---|---|
| `references/01-brief-y-parametros.md` | Fase 0, vocabulario, evidencia de legibilidad |
| `references/02-dibujo-y-correcciones.md` | Al dibujar: óptica, Bézier, pesos, cursivas, cifras |
| `references/03-espaciado-y-kerning.md` | Al espaciar y hacer kerning |
| `references/04-programas-y-toolchain.md` | Al elegir programa o si falla la compilación |
| `references/05-ingenieria-opentype.md` | Métricas, nombres, features, variables, hinting, QA |
| `references/06-idiomas-y-cobertura.md` | Conjuntos de glifos, español, diacríticos, escrituras |
| `references/07-web.md` | Exportación y carga web |
| `references/08-originalidad-licencias-ia.md` | Peticiones de copia, auditoría, licencias, derecho, IA |
| `references/09-generos.md` | Restricciones por género |

## Cómo informar

Al terminar una fase, muestra la prueba y da un informe breve: qué se hizo, qué pasó las puertas (con cifras), qué no se ha podido verificar y qué decisión corresponde a la persona. No describas una fuente como terminada, profesional u original si las puertas no lo sustentan.
