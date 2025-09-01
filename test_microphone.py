
import sounddevice as sd
import numpy as np

def test_microphone(duration=3, samplerate=16000):
    print("🎤 Test du micro en cours...")
    try:
        audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()
        volume = np.linalg.norm(audio) / len(audio)
        if volume > 0.01:
            print("✅ Le micro fonctionne. Volume moyen détecté :", volume)
        else:
            print("⚠️ Le micro semble silencieux. Vérifiez la configuration.")
    except Exception as e:
        print("❌ Erreur avec le micro :", str(e))

if __name__ == "__main__":
    test_microphone()
