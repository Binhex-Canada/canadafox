#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

export MOZCONFIG="$(pwd)/mozconfig"
cd firefox
python3 ./mach run
