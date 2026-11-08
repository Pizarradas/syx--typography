#!/usr/bin/env bash
# Instala la cadena de herramientas de Python en un entorno aislado. Es idempotente.
# Por defecto instala el núcleo (dibujo, compilación, pruebas, web). `--qa` añade
# las herramientas de auditoría (Font Bakery, diffenator2), pesadas y solo
# necesarias en las fases 5 y 6.
# Requiere uv (https://docs.astral.sh/uv/). Nada se instala en el sistema.
#
# fontspector NO se instala aquí: es un binario externo y su instalación la decide
# la persona (ver references/04-programas-y-toolchain.md). Sin él se usa Font Bakery.
set -euo pipefail
VENV="${TYPE_DESIGN_VENV:-$HOME/.local/share/type-design/venv}"
case "$PWD" in /mnt/*) echo "AVISO: estás bajo /mnt/ (disco de Windows). Un UFO son cientos de archivos pequeños y ahí el I/O es varias veces más lento: crea los proyectos dentro del sistema de archivos de WSL (p. ej. ~/fuentes)." >&2 ;; esac
UV="$(command -v uv || true)"
[ -n "$UV" ] || [ ! -x "$HOME/.local/bin/uv" ] || UV="$HOME/.local/bin/uv"
if [ -z "$UV" ]; then
  echo "Falta uv. Instálalo y vuelve a ejecutar: https://docs.astral.sh/uv/getting-started/installation/" >&2
  exit 1
fi
mkdir -p "$(dirname "$VENV")"
[ -x "$VENV/bin/python" ] || "$UV" venv --python 3.13 "$VENV"
"$UV" pip install --quiet --python "$VENV/bin/python" \
  "fonttools[ufo,woff,unicode,lxml]" ufoLib2 fontmake gftools fontc \
  skia-pathops uharfbuzz pillow booleanOperations brotli hyperglot ufostroker \
  opentype-sanitizer ttfautohint-py
if [ "${1:-}" = "--qa" ]; then
  "$UV" pip install --quiet --python "$VENV/bin/python" fontbakery diffenator2
fi
echo "Entorno listo: $VENV"
"$VENV/bin/python" -c "import fontTools; print('fontTools', fontTools.version)"
"$VENV/bin/fontmake" --version | sed 's/^/fontmake /'
"$VENV/bin/fontc" --version
[ -x "$VENV/bin/fontbakery" ] && "$VENV/bin/fontbakery" --version || echo "fontbakery: no instalado (setup_env.sh --qa lo añade)"
command -v fontspector >/dev/null && fontspector --version || echo "fontspector: no instalado (opcional)"
