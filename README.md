# Projet MCP FastAPI avec assistant vocal

Ce projet contient un serveur MCP en FastAPI avec plusieurs agents :
- 🔍 Recherche PDF locale
- 📧 Envoi Gmail
- 🌐 Veille Web
- 🗣️ Assistant vocal (Whisper)
- **🎨 Blender MCP - Contrôle de Blender 3D via AI** *(nouveau!)*

## Lancement rapide

```bash
chmod +x launch.sh
./launch.sh
```

## 🎨 Nouveau : Intégration Blender MCP

Contrôlez Blender 3D directement depuis l'API ! Créez, modifiez et rendez des modèles 3D via des commandes simples.

**Voir le guide complet:** `BLENDER_MCP_GUIDE.md`

**Test rapide:**
```bash
# Assurez-vous que Blender avec MCP est lancé
python3 test_blender_mcp.py --simple
```

### Exemple d'utilisation

```bash
# Créer un cube
curl -X POST http://localhost:5005/mcp \
  -H "Content-Type: application/json" \
  -d '{"command":"blender_create_object","object_type":"CUBE","name":"MonCube"}'
```

Pour plus d'exemples, consultez `BLENDER_MCP_GUIDE.md`.

---

Utilisez `agents/voice_assistant.py` pour interagir avec le projet à la voix.# mcp-fastapi-agent
# mcp-fastapi-agent
