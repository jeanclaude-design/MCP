# ---------- Dockerfile (API MCP + FastAPI + static /client) ----------
FROM python:3.11-slim

# utilitaires (healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code de l'appli
COPY . .

EXPOSE 5005

# IMPORTANT : cible FastAPI = server.main:app
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "5005"]



