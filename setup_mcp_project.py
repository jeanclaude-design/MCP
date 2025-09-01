
import os
from pathlib import Path

project_structure = {
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
