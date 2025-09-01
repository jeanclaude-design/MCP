import requests
from bs4 import BeautifulSoup
import json
import os
import time
from typing import Dict, Any, List

WATCHES_FILE = "web_watches.json"

def _load_watches():
    if not os.path.exists(WATCHES_FILE):
        return {}
    with open(WATCHES_FILE, "r") as f:
        return json.load(f)

def _save_watches(watches):
    with open(WATCHES_FILE, "w") as f:
        json.dump(watches, f, indent=2)

def _perform_web_watch(url: str, keyword: str) -> List[str]:
    """Performs a single web scrape and returns matching links."""
    try:
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")
        matches = [a.text for a in soup.find_all("a") if keyword.lower() in a.text.lower()]
        return matches
    except Exception as e:
        print(f"Error performing web watch for {url} with keyword {keyword}: {e}")
        return []

def start_web_watch(url: str, keyword: str) -> Dict[str, Any]:
    """Starts a new web watch (simulated deferred execution)."""
    watches = _load_watches()
    watch_id = str(int(time.time())) # Simple unique ID
    
    watches[watch_id] = {
        "url": url,
        "keyword": keyword,
        "status": "started",
        "last_run": None,
        "results": [],
        "summary": "Synthèse non disponible."
    }
    _save_watches(watches)

    # Simulate immediate first run for demonstration
    matches = _perform_web_watch(url, keyword)
    watches[watch_id]["results"].append({"timestamp": time.time(), "matches": matches})
    watches[watch_id]["last_run"] = time.time()
    
    # Simulate synthesis (simple concatenation for now)
    if matches:
        watches[watch_id]["summary"] = f"Veille sur '{keyword}' à l'URL '{url}' a trouvé {len(matches)} correspondances. Exemples: {', '.join(matches[:3])}..."
    else:
        watches[watch_id]["summary"] = f"Veille sur '{keyword}' à l'URL '{url}' n'a trouvé aucune correspondance."

    _save_watches(watches)
    
    return {"status": "ok", "watch_id": watch_id, "message": "Veille web démarrée et première exécution simulée."}

def get_web_watch_summary(watch_id: str) -> Dict[str, Any]:
    """Retrieves the summary of a specific web watch."""
    watches = _load_watches()
    watch = watches.get(watch_id)
    if not watch:
        return {"status": "error", "message": "ID de veille non trouvé."}
    
    return {"status": "ok", "watch_id": watch_id, "summary": watch["summary"], "results": watch["results"]}

def list_web_watches() -> Dict[str, Any]:
    """Lists all active web watches."""
    watches = _load_watches()
    return {"status": "ok", "watches": watches}