#!/usr/bin/env bash
# Replay the D1.2 walk schedule: stand 0-3s, command[0]=0.15 for 3-6s, stand 6-8s.
set -euo pipefail

MINI_ROOT="${OPEN_DUCK_MINI:-$HOME/Open_Duck_Mini}"
PLAYGROUND_ROOT="${OPEN_DUCK_PLAYGROUND:-$HOME/Open_Duck_Playground}"
ONNX="${OPEN_DUCK_ONNX:-$MINI_ROOT/BEST_WALK_ONNX_2.onnx}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export OPEN_DUCK_MINI="$MINI_ROOT"
export OPEN_DUCK_PLAYGROUND="$PLAYGROUND_ROOT"
export OPEN_DUCK_ONNX="$ONNX"
export DISPLAY="${DISPLAY:-:0}"
export MUJOCO_GL="${MUJOCO_GL:-glfw}"

if [[ ! -d "$PLAYGROUND_ROOT" ]]; then
  echo "error: Playground not found: $PLAYGROUND_ROOT" >&2
  exit 1
fi

cd "$PLAYGROUND_ROOT"

if [[ -x "${HOME}/env_duck_playground/bin/python" ]]; then
  exec "${HOME}/env_duck_playground/bin/python" "$SCRIPT_DIR/run_openduck_eval.py"
fi

if command -v uv >/dev/null 2>&1; then
  exec uv run python "$SCRIPT_DIR/run_openduck_eval.py"
fi

echo "error: need ~/env_duck_playground or uv" >&2
exit 1
