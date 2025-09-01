docker compose down
docker compose build --no-cache --progress=plain
docker compose up -d
docker compose logs -f mcp-server
