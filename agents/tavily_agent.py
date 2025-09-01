import os
from tavily import TavilyClient
import logging

log = logging.getLogger("mcp")

def search_web_tavily(query: str):
    """
    Effectue une recherche web en utilisant l'API Tavily.
    Nécessite la variable d'environnement TAVILY_API_KEY.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        log.error("TAVILY_API_KEY n'est pas définie dans les variables d'environnement.")
        return {"status": "error", "message": "TAVILY_API_KEY non configurée."}

    try:
        tavily = TavilyClient(api_key=api_key)
        results = tavily.search(query=query, search_depth="basic")
        
        # Tavily retourne un dictionnaire avec une clé 'results' contenant une liste de dictionnaires
        # Chaque dictionnaire de résultat contient 'title', 'url', 'content'
        formatted_results = []
        for r in results.get('results', []):
            formatted_results.append({
                "title": r.get("title"),
                "url": r.get("url"),
                "content": r.get("content")
            })
        
        return {"status": "ok", "results": formatted_results}
    except Exception as e:
        log.error(f"Erreur lors de la recherche Tavily : {e}")
        return {"status": "error", "message": f"Erreur lors de la recherche Tavily : {str(e)}"}

if __name__ == "__main__":
    # Exemple d'utilisation (pour les tests locaux)
    # Assurez-vous que TAVILY_API_KEY est définie dans votre environnement
    os.environ["TAVILY_API_KEY"] = "YOUR_TAVILY_API_KEY_HERE" # Remplacez par une vraie clé pour tester
    
    print("Test de recherche Tavily pour 'actualités IA'")
    res = search_web_tavily("actualités IA")
    print(res)