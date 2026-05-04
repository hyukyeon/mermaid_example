#!/usr/bin/env bash
set -euo pipefail
if [ $# -eq 0 ]; then
  echo "Usage: $0 file1.svg [file2.svg ...]"
  exit 2
fi
python3 "$(dirname "$0")/svg_to_mermaid.py" "$@"
