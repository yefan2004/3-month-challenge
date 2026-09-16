#!/usr/bin/env bash
# Start official Open Duck Playground ONNX playback.
# Does not patch upstream repositories.
set -euo pipefail

MINI_ROOT="${OPEN_DUCK_MINI:-$HOME/Open_Duck_Mini}"
PLAYGROUND_ROOT="${OPEN_DUCK_PLAYGROUND:-$HOME/Open_Duck_Playground}"
ONNX="${OPEN_DUCK_ONNX:-$MINI_ROOT/BEST_WALK_ONNX_2.onnx}"
XML="$PLAYGROUND_ROOT/playground/open_duck_mini_v2/xmls/scene_flat_terrain.xml"

usage() {
  cat <<'EOF'
Usage: scripts/run_infer.sh [--help]

Environment:
  OPEN_DUCK_MINI         default: ~/Open_Duck_Mini
  OPEN_DUCK_PLAYGROUND   default: ~/Open_Duck_Playground
  OPEN_DUCK_ONNX         default: $OPEN_DUCK_MINI/BEST_WALK_ONNX_2.onnx
  DISPLAY                required for the MuJoCo viewer (WSLg: usually :0)

Runs:
  uv run playground/open_duck_mini_v2/mujoco_infer.py -o <onnx>
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ ! -d "$PLAYGROUND_ROOT" ]]; then
  echo "error: Playground not found: $PLAYGROUND_ROOT" >&2
  echo "clone https://github.com/apirrone/Open_Duck_Playground" >&2
  exit 1
fi

if [[ ! -f "$ONNX" ]]; then
  echo "error: ONNX not found: $ONNX" >&2
  echo "place BEST_WALK_ONNX_2.onnx per Open_Duck_Mini README" >&2
  exit 1
fi

if [[ ! -f "$XML" ]]; then
  echo "error: MJCF not found: $XML" >&2
  exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "error: uv not on PATH. Install: curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
  exit 1
fi

echo "playground: $PLAYGROUND_ROOT"
echo "onnx:       $ONNX"
echo "mjcf:       $XML"
echo "python:     $(uv run --directory "$PLAYGROUND_ROOT" python -c 'import sys; print(sys.version.split()[0])')"

cd "$PLAYGROUND_ROOT"
exec uv run playground/open_duck_mini_v2/mujoco_infer.py -o "$ONNX"
