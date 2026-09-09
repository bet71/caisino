#!/usr/bin/env bash
set -euo pipefail
docker compose exec api python -m scripts.seed
echo "seed ok"
