#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/lattice_model_node_demo.py"
python3 "$SCRIPT_DIR/engines/nest1_formal_engine.py"
