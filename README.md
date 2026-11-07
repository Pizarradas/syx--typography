# diseno-tipografias

Skill para [Claude Code](https://code.claude.com/docs/en/skills) que diseña y produce tipografías originales de principio a fin: del brief al WOFF2, con comprobaciones en cada fase y registro de la procedencia de cada glifo.

Trabaja con UFO + designspace y compila con fontmake. Puede dibujar por código o actuar como ingeniería y control de calidad de una persona que dibuja en Fontra, FontLab o Glyphs.

## Qué puedes pedirle

```text
Quiero crear una tipografía geométrica para titulares, variable en peso y lista para mi web.
Revisa el espaciado y las métricas de la fuente de esta carpeta.
Mi fuente sale con falsa negrita en Word y los acentos no se colocan bien. Arréglalo.
Prepara esta fuente para la web sin perder las features.
¿Qué programa me recomiendas para diseñar tipos en Windows?
```

La skill se activa sola con este tipo de peticiones. No sirve para elegir fuentes existentes ni para maquetar con ellas, y no ayuda a clonar o renombrar fuentes ajenas: propone alternativas legítimas.

## Instalación

Sustituye `USUARIO/REPOSITORIO` por este repositorio. Usa solo una de las dos vías, o la skill aparecerá dos veces.

### Como plugin

```bash
claude plugin marketplace add USUARIO/REPOSITORIO
claude plugin install diseno-tipografias@diseno-tipografias
```

También acepta la URL completa del repositorio. Se invoca como `/diseno-tipografias:diseno-tipografias`.

Para actualizarla, ejecuta `claude plugin update diseno-tipografias@diseno-tipografias` y reinicia Claude Code. Para quitarla, usa `claude plugin uninstall diseno-tipografias`.

### Como skill personal

```bash
git clone https://github.com/USUARIO/REPOSITORIO.git ~/.claude/skills/diseno-tipografias
```

Se invoca como `/diseno-tipografias`. Para actualizarla, ejecuta `git pull` en esa carpeta.

## Requisitos

- Linux, macOS o Windows con WSL2. Las herramientas solo se han probado en Linux bajo WSL2.
- [uv](https://docs.astral.sh/uv/getting-started/installation/) y git.

La primera vez, la skill ejecuta `scripts/setup_env.sh`, que crea un entorno aislado en `~/.local/share/type-design/venv` con fontTools, fontmake, gftools, Font Bakery y otras herramientas de PyPI. Nada se instala en el sistema. Cambia la ubicación con la variable `TYPE_DESIGN_VENV`.

En Windows, guarda los proyectos en el sistema de archivos de WSL, no en `/mnt/c`.

`fontspector` es opcional: si está instalado, el control de calidad lo usa en lugar de Font Bakery.

## Cómo trabaja

Cada fase termina en una puerta: no se avanza hasta superarla.

| Fase | Trabajo | Puerta |
|---|---|---|
| 0. Concepto | Brief, usos, idiomas, hipótesis de parámetros | Razón de ser escrita y primer sello de procedencia |
| 1. Prueba de concepto | n, o, H, O; luego a, d, e, h, s | La idea se percibe en palabras y la persona la aprueba |
| 2. Primer borrador | Minúsculas, mayúsculas, cifras, puntuación | Color uniforme en texto corrido |
| 3. Familia | Pesos, anchuras, cursiva, versalitas | Másteres compatibles, sin saltos ni quiebros |
| 4. Cobertura | Diacríticos, conjunto de glifos, idiomas | Texto real correcto en los idiomas del brief |
| 5. Ingeniería | Kerning, features, métricas, nombres, hinting | Compilación de un comando y pruebas de conformación |
| 6. Calidad | Control automático y revisión en entornos reales | Revisión humana |
| 7. Publicación | WOFF2, CSS, licencia, auditoría final | Sin caracteres ni features perdidos, y procedencia completa |

Es una síntesis propia de la investigación de esta skill, no un estándar publicado.

## Programas recomendados

| Situación | Programa |
|---|---|
| Por código, con Claude | UFO + designspace y fontmake |
| Windows, gratis | Fontra Pak |
| Windows, profesional | FontLab 9 |
| macOS, profesional | Glyphs 4 |

Los detalles y sus límites están en [`references/04-programas-y-toolchain.md`](references/04-programas-y-toolchain.md).

## Qué incluye

**Herramientas (`scripts/`)**

| Script | Función |
|---|---|
| `setup_env.sh` | Instala la cadena en un entorno aislado |
| `new_project.py` | Crea UFO, designspace, brief y registro |
| `trazos.py`, `motor.py` | Dibujo por código con másteres compatibles por construcción |
| `check_sources.py` | Compatibilidad, contornos, nodos, anclas y enlaces de estilo |
| `build.py` | Compila y verifica con OTS, coherencia, conformación y control de calidad |
| `proof.py` | Pruebas PNG: control, palabras, texto, cascada, glifos, pesos, idiomas, oscuro |
| `shape_tests.py` | Pruebas de conformación con HarfBuzz, también frente a un WOFF2 |
| `coverage.py` | Cobertura de letras, signos y marcas por idioma |
| `web_export.py` | WOFF2 y CSS, comprobando que no se pierden caracteres ni features |
| `registro.py` | Procedencia por glifo y sellos con hash |
| `copy_check.py` | Alarma de calco entre dos fuentes |

**Referencias (`references/`)**

| Archivo | Tema |
|---|---|
| `01-brief-y-parametros.md` | Brief, vocabulario, parámetros y evidencia de legibilidad |
| `02-dibujo-y-correcciones.md` | Correcciones ópticas, Bézier, pesos, cursivas y cifras |
| `03-espaciado-y-kerning.md` | Espaciado y kerning |
| `04-programas-y-toolchain.md` | Programas, cadena de herramientas y trampas conocidas |
| `05-ingenieria-opentype.md` | Métricas, nombres, features, variables, hinting y control de calidad |
| `06-idiomas-y-cobertura.md` | Conjuntos de glifos, español, diacríticos y otras escrituras |
| `07-web.md` | Exportación, carga y rendimiento web |
| `08-originalidad-licencias-ia.md` | Originalidad, derecho por territorios, licencias e IA |
| `09-generos.md` | Restricciones por género tipográfico |

Las plantillas y ejemplos están en `assets/`.

## Qué esperar

- **Fiable en lo verificable:** compatibilidad entre másteres, métricas, nombres, features, cobertura y compilación.
- **Por código** rinde mejor en geométricas, modulares, monoespaciadas y de píxel. Una serifa de texto expresiva necesita a una persona que dibuje.
- **No sustituye al ojo:** que todas las comprobaciones pasen demuestra conformidad, no calidad de diseño. Hay que revisar las pruebas y probar en navegadores, Windows, macOS, Word e impresión.
- **No certifica la originalidad:** ninguna herramienta puede hacerlo. La skill aporta un método y deja constancia del proceso.
- **Autoría con IA:** la protección jurídica de los contornos generados por IA es incierta y varía por país. La skill los registra por glifo para declararlos con honestidad.
- **Datos fechados:** precios, versiones y soporte de navegadores corresponden a noviembre de 2026 y caducan. Revísalos antes de confiar en ellos.
- **Base de conocimiento desigual:** varias obras canónicas se citan a través de fuentes secundarias, y muchas cifras son convenciones de oficio. Las referencias marcan el origen de cada dato y los desacuerdos entre fuentes.

La parte legal es orientativa y no constituye asesoramiento jurídico.

## Licencia

[MIT](LICENSE). Esta licencia cubre la skill, no las tipografías que crees con ella: su licencia la decides tú.
