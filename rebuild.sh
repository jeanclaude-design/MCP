#!/usr/bin/env bash
set -euo pipefail

echo "🧹 Down..."
docker compose down || true

echo "🧱 Build (no cache)..."
docker compose build --no-cache --progress=plain

echo "🚀 Up..."
docker compose up -d

echo "📜 Logs (mcp-server)..."
docker compose logs -f mcp-server

