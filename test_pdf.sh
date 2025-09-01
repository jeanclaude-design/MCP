#!/usr/bin/env bash
set -euo pipefail

QUERY="${1:-Relativité générale}"

echo "🔎 Test LOCAL sur /host/home (contenu inclus) — requête : $QUERY"
docker compose exec -T mcp-server python - <<PY
from agents.local_pdf_agent import search_pdf
print(search_pdf("$QUERY", source="local",
                 search_dirs=["/host/home"], search_in_contents=True)["files_found"][:10])
PY

echo -e "\n🌐 Test WEB — requête : $QUERY"
docker compose exec -T mcp-server python - <<PY
from agents.local_pdf_agent import search_pdf
print(search_pdf("$QUERY", source="web")["files_found"][:10])
PY

