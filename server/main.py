# server/main.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from server.mcp_routes import router
import os

app = FastAPI(title="MCP Server - FastAPI")

# Sert le frontend (http://localhost:5005/client/ → index.html)
app.mount("/client", StaticFiles(directory="client", html=True), name="client")

# API MCP (POST /mcp)
app.include_router(router, prefix="/mcp")

# Route pour servir les fichiers PDF
@app.get("/files")
async def serve_file(path: str):
    # Sécurité: s'assurer que le chemin est dans le répertoire autorisé
    # Ici, on suppose que tous les fichiers sont sous /host/home
    # et que /host/home est monté en lecture seule dans le Dockerfile
    if not path.startswith("/host/home"):
        raise HTTPException(status_code=403, detail="Accès non autorisé au chemin spécifié")
    
    # Vérifier si le fichier existe
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    # Retourner le fichier
    return FileResponse(path)

# Sanity check (GET /)
@app.get("/")
async def root():
    return {"message": "MCP Server is running"}

