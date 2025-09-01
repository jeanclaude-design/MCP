import time
from agents.local_pdf_agent import search_pdf

if __name__ == "__main__":
    while True:
        result = search_pdf()
        print("Tâche de fond : fichiers PDF trouvés :", result.get("files_found", []))
        time.sleep(60)
