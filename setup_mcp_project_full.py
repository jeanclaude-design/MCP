
import os
from pathlib import Path

project_structure = {
    "background/worker.py": """import time
from agents.local_pdf_agent import search_pdf

if __name__ == "__main__":
    while True:
        result = search_pdf()
        print("Tâche de fond : fichiers PDF trouvés :", result.get("files_found", []))
        time.sleep(60)
""",
    "client/index.html": """<!DOCTYPE html>
<html>
<head>
  <title>MCP Agents</title>
</head>
<body>
  <h2>Contrôle des Agents</h2>
  <button onclick="search()">🔍 Chercher PDF</button>
  <button onclick="sendMail()">📧 Envoyer Email</button>
  <button onclick="watchWeb()">🌐 Veille Web</button>
  <pre id="output"></pre>
  <script>
    async function search() {
      const res = await fetch("/mcp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command: "search_pdf", filename_pattern: "*.pdf" })
      });
      const data = await res.json();
      document.getElementById("output").innerText = JSON.stringify(data, null, 2);
    }

    async function sendMail() {
      const res = await fetch("/mcp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          command: "send_email",
          to: "votre.email@gmail.com",
          subject: "PDF détecté",
          body: "Un document a été trouvé."
        })
      });
      const data = await res.json();
      document.getElementById("output").innerText = JSON.stringify(data, null, 2);
    }

    async function watchWeb() {
      const res = await fetch("/mcp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          command: "web_watch",
          url: "https://news.ycombinator.com/",
          keyword: "AI"
        })
      });
      const data = await res.json();
      document.getElementById("output").innerText = JSON.stringify(data, null, 2);
    }
  </script>
</body>
</html>
""",
    "server/main.py": """from fastapi import FastAPI
from server.mcp_routes import router

app = FastAPI(title="MCP Server")

app.include_router(router, prefix="/mcp")
""",
    "server/mcp_routes.py": """from fastapi import APIRouter
from agents.local_pdf_agent import search_pdf
from agents.gmail_agent import send_email
from agents.web_watch_agent import check_web_update

router = APIRouter()

@router.post("/")
async def handle_command(req: dict):
    cmd = req.get("command")
    if cmd == "search_pdf":
        return search_pdf(req.get("filename_pattern", "*.pdf"))
    elif cmd == "send_email":
        return send_email(req.get("to"), req.get("subject"), req.get("body"))
    elif cmd == "web_watch":
        return check_web_update(req.get("url", "https://news.ycombinator.com/"), req.get("keyword", "AI"))
    return {"error": "Commande inconnue"}
""",
    "requirements.txt": """fastapi
uvicorn
google-api-python-client
google-auth
google-auth-oauthlib
watchdog
requests
beautifulsoup4
openai-whisper
pyttsx3
sounddevice
scipy
""",
    "Dockerfile": """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y libasound2-dev portaudio19-dev ffmpeg  && pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "5005"]
""",
    "docker-compose.yml": """version: '3'
services:
  mcp-server:
    build: .
    ports:
      - "5005:5005"
    volumes:
      - .:/app
    restart: unless-stopped

  background-worker:
    build: .
    command: python background/worker.py
    depends_on:
      - mcp-server
    restart: unless-stopped
""",
    "launch.sh": """#!/bin/bash
echo "🚀 Lancement du projet MCP vocal..."
docker-compose up --build -d
echo "📢 Serveur en ligne sur http://localhost:5005/client/index.html"
""",
    "README.md": """# Projet MCP FastAPI avec assistant vocal

Ce projet contient un serveur MCP en FastAPI, des agents de recherche PDF, d'envoi Gmail, de veille Web et un assistant vocal local basé sur Whisper.

Lancement :
```bash
chmod +x launch.sh
./launch.sh
```

Utilisez `agents/voice_assistant.py` pour interagir avec le projet à la voix.""",

    "agents/gmail_agent.py": """from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText

def send_email(to, subject, body):
    try:
        creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/gmail.send"])
        service = build('gmail', 'v1', credentials=creds)

        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        sent = service.users().messages().send(userId="me", body={'raw': raw}).execute()
        return {"status": "sent", "message_id": sent['id']}
    except Exception as e:
        return {"status": "error", "message": str(e)}""",

    "agents/local_pdf_agent.py": """import glob
import os

def search_pdf(filename_pattern="*.pdf", search_dir="~/Documents"):
    search_dir = os.path.expanduser(search_dir)
    pattern = os.path.join(search_dir, "**", filename_pattern)
    found = glob.glob(pattern, recursive=True)
    return {"status": "ok", "files_found": found}""",

    "agents/web_watch_agent.py": """import requests
from bs4 import BeautifulSoup

def check_web_update(url="https://news.ycombinator.com/", keyword="AI"):
    try:
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")
        matches = [a.text for a in soup.find_all("a") if keyword.lower() in a.text.lower()]
        return {"status": "ok", "matches": matches, "url": url}
    except Exception as e:
        return {"status": "error", "message": str(e)}""",

    "agents/voice_assistant.py": """import whisper
import sounddevice as sd
import numpy as np
import requests
import pyttsx3
import tempfile
import scipy.io.wavfile as wav

model = whisper.load_model("base")

def record_audio(duration=5, samplerate=16000):
    print("🎤 Parlez maintenant...")
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    return audio.squeeze(), samplerate

def transcribe(audio_array, samplerate):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        wav.write(tmpfile.name, samplerate, audio_array)
        result = model.transcribe(tmpfile.name, language='fr')
    return result["text"]

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def voice_command_loop():
    speak("Assistant vocal Whisper lancé. Parlez après le bip.")
    while True:
        audio, rate = record_audio()
        try:
            command = transcribe(audio, rate).lower()
            print(f"🧠 Commande : {command}")
            speak(f"Vous avez dit : {command}")

            if "pdf" in command:
                res = requests.post("http://localhost:5005/mcp", json={"command": "search_pdf"})
                speak("Recherche de fichiers PDF effectuée.")
            elif "mail" in command:
                res = requests.post("http://localhost:5005/mcp", json={
                    "command": "send_email",
                    "to": "votre.email@gmail.com",
                    "subject": "Fichier détecté",
                    "body": "Un document a été trouvé."
                })
                speak("Email envoyé.")
            elif "web" in command:
                res = requests.post("http://localhost:5005/mcp", json={
                    "command": "web_watch",
                    "url": "https://news.ycombinator.com/",
                    "keyword": "AI"
                })
                speak("Analyse Web effectuée.")
            elif "stop" in command:
                speak("Assistant arrêté.")
                break
            else:
                speak("Commande non reconnue.")
        except Exception as e:
            print("Erreur :", e)
            speak("Je n'ai pas compris.")

if __name__ == "__main__":
    voice_command_loop()""",
}

def create_project():
    for path, content in project_structure.items():
        filepath = Path(path)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            f.write(content)
    print("✅ Projet MCP vocal généré localement.")

if __name__ == "__main__":
    create_project()
