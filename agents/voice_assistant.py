import whisper, sounddevice as sd, numpy as np, requests, tempfile, scipy.io.wavfile as wav
try:
    import pyttsx3                                  # TTS local
    engine = pyttsx3.init()
    # Sélection d'une voix française si dispo
    for v in engine.getProperty("voices"):
        if "fr" in v.id.lower():
            engine.setProperty("voice", v.id)
            break
except Exception as e:                              # pas de TTS ? -> mode silencieux
    print("⚠️  TTS désactivé :", e)
    engine = None

model = whisper.load_model("base")                  # STT Whisper local

def speak(text):
    if engine:
        engine.say(text)
        engine.runAndWait()
    else:
        print("[TTSOFF]", text)

def record_audio(duration=5, sr=16000):
    sd.default.samplerate, sd.default.channels = sr, 1
    print("🎤 Parlez…")
    audio = sd.rec(int(duration * sr), dtype="int16")
    sd.wait()
    return audio.squeeze(), sr

def transcribe(buf, sr):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav.write(tmp.name, sr, buf)
        return model.transcribe(tmp.name, language="fr")["text"].lower()

def main():
    banner = (
        "Assistant vocal Whisper lancé.\n"
        "Commandes : « Cherche un PDF » | « Envoie un mail » | « Fais une veille Web » | « Stop »"
    )
    print(banner)
    speak(banner)
    while True:
        audio, sr = record_audio()
        try:
            cmd = transcribe(audio, sr)
            print("🧠 Vous avez dit :", cmd)
            if "pdf" in cmd:
                requests.post("http://localhost:5005/mcp",
                              json={"command": "search_pdf"})
                speak("Recherche de fichiers PDF effectuée.")
            elif "mail" in cmd or "email" in cmd:
                requests.post("http://localhost:5005/mcp", json={
                    "command": "send_email",
                    "to": "votre.email@gmail.com",
                    "subject": "Fichier détecté",
                    "body": "Un document a été trouvé."
                })
                speak("E-mail envoyé.")
            elif "veille" in cmd or "web" in cmd:
                requests.post("http://localhost:5005/mcp", json={
                    "command": "web_watch",
                    "url": "https://news.ycombinator.com/",
                    "keyword": "AI"
                })
                speak("Analyse Web effectuée.")
            elif "stop" in cmd or "quitte" in cmd:
                speak("Arrêt de l’assistant.")
                break
            else:
                speak("Commande non reconnue.")
        except Exception as e:
            print("Erreur STT/TTS :", e)
            speak("Je n’ai pas compris.")

if __name__ == "__main__":
    main()

