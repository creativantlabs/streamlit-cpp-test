#!/usr/bin/env bash
# Start the C++ quiz locally. Creates .venv and installs requirements on first run.
# Usage: ./run.sh [port]      (default port 8501)
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"
PORT="${1:-8501}"

if [ ! -x .venv/bin/python ]; then
    echo "Creating virtual environment in .venv ..."
    python3 -m venv .venv
fi

# Reinstall only when requirements.txt changed since the last install.
if [ ! -f .venv/.installed ] || [ requirements.txt -nt .venv/.installed ]; then
    echo "Installing requirements ..."
    .venv/bin/pip install -q -r requirements.txt
    touch .venv/.installed
fi

exec .venv/bin/streamlit run app.py --server.port "$PORT"
