# 🎤 MCP FastAPI – Assistant vocal local multi-agents (PDF, Gmail, Web, Whisper)

Ce projet implémente un système **multi-agents** piloté par **FastAPI** et **FastMCP**, incluant :
- 🔍 un agent de recherche de fichiers PDF
- 📧 un agent d’envoi d’e-mail via Gmail API
- 🌐 un agent de veille Web (scraping mot-clé)
- 🗣️ un assistant vocal local basé sur [Whisper](https://github.com/openai/whisper) pour exécuter des commandes vocales
- 🖥️ une interface HTML/JavaScript
- 🐳 un déploiement Dockerisé prêt à l’emploi

---

## 🧱 Architecture

```text
[Interface Web HTML/JS]
         |
     [FastAPI REST (FastMCP)]
         |
 ┌────────────┬─────────────┬─────────────┐
 |            |             |             |
PDF Agent   Gmail Agent   Web Agent   Vocal Agent (Whisper)
```

---

## 🚀 Installation rapide

### 1. 📦 Pré-requis

- [Python 3.11+](https://www.python.org/)
- [Docker](https://docs.docker.com/get-docker/)
- [Git](https://git-scm.com/)
- Un **microphone actif** (sauf si tu n'utilises pas l’agent vocal)
- Optionnel : un environnement Linux natif (recommandé pour la voix)

---

### 2. 📥 Création du projet (script automatique)

```bash
mkdir mcp-fastapi-agents
cd mcp-fastapi-agents
python3 ../setup_mcp_project_full.py
```

---

### 3. 🛠 Lancement complet

```bash
chmod +x launch.sh
./launch.sh
```

Accès à l’interface Web :
➡️ [http://localhost:5005/client/index.html](http://localhost:5005/client/index.html)

---

## 🧪 Tester le microphone (facultatif)

```bash
python3 test_microphone.py
```

- ✅ Volume détecté = micro OK
- ⚠️ Silencieux = vérifier le micro / permissions
- ❌ PortAudio introuvable ? Installer avec :
  ```bash
  sudo apt install portaudio19-dev libportaudio2
  pip install sounddevice
  ```

---

## 🗣️ Lancer l'assistant vocal Whisper (local)

```bash
python3 agents/voice_assistant.py
```

> 🧠 Tu peux dire :
> - « Cherche un PDF »
> - « Envoie un mail »
> - « Fais une veille Web »
> - « Stop » (pour quitter)

---

## 🧠 Commandes API manuelles

Tu peux aussi interagir via `curl`, `httpie`, ou ton interface web.

```bash
# Recherche PDF
curl -X POST http://localhost:5005/mcp -H "Content-Type: application/json" -d '{"command":"search_pdf"}'

# Envoi mail
curl -X POST http://localhost:5005/mcp -H "Content-Type: application/json" -d '{"command":"send_email","to":"email@example.com","subject":"Test","body":"Hello"}'

# Veille Web
curl -X POST http://localhost:5005/mcp -H "Content-Type: application/json" -d '{"command":"web_watch","url":"https://news.ycombinator.com","keyword":"AI"}'
```

---

## 📧 Configuration Gmail

1. Va sur : [https://developers.google.com/gmail/api/quickstart/python](https://developers.google.com/gmail/api/quickstart/python)
2. Crée tes identifiants OAuth2
3. Place ton fichier `token.json` à la racine du projet
4. Configure `.env` :

```
EMAIL_TO=ton.email@gmail.com
GMAIL_TOKEN_PATH=token.json
```

---

## 🖥️ Créer un raccourci Linux `.desktop`

```bash
cp assistant_vocal.desktop ~/.local/share/applications/
chmod +x ~/.local/share/applications/assistant_vocal.desktop
```

Il apparaîtra dans ton menu comme : **"Assistant Vocal MCP"**  
Icône personnalisée disponible dans `assets/mic.svg`.

---

## 📂 Structure du projet

```
.
├── agents/               # Tous les agents (PDF, Gmail, Web, vocal)
├── background/           # Worker MCP
├── client/               # Interface web HTML/JS
├── server/               # API FastAPI
├── assets/               # Icône SVG pour interface
├── launch.sh             # Script de lancement
├── Dockerfile            # Build MCP + agents
├── docker-compose.yml    # MCP + Worker
├── test_microphone.py    # Test du micro
├── assistant_vocal.desktop
├── requirements.txt
└── README.md
```

---

## 🧩 Extensions possibles

- 🔁 Ajout d’un 5e agent : résumé de texte, OCR, assistant vocal avec LLM local
- 🧠 Intégration LangChain ou LlamaIndex
- 🔊 Synthèse vocale IA plus naturelle (TTS ou Bark)

---

## 👤 Auteur

Ce projet a été généré par [Jean-Claude Spinelli] avec l’assistance de ChatGPT.

---

## 📝 Licence

Projet open-source. Réutilisation autorisée avec attribution.
