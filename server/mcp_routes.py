# server/mcp_routes.py
from fastapi import APIRouter
from agents.local_pdf_agent import search_pdf
from agents.gmail_agent import send_email
from agents.web_watch_agent import start_web_watch, get_web_watch_summary, list_web_watches
from agents.tavily_agent import search_web_tavily
import logging

router = APIRouter()
log = logging.getLogger("mcp")

@router.post("/")
async def handle_command(req: dict):
    log.warning("MCP REQ: %s", req)  # debug UI
    cmd = req.get("command")

    if cmd == "search_pdf":
        source = (req.get("source") or "local").lower()

        # dirs: peut être None, "", "a;b", ["a","b"]
        raw_dirs = req.get("dirs")
        dirs = None
        if source == "local":
            if raw_dirs is None:
                dirs = ["/host/home"]
            elif isinstance(raw_dirs, str):
                parts = [p.strip() for p in raw_dirs.split(";") if p.strip()]
                dirs = parts or ["/host/home"]
            elif isinstance(raw_dirs, list):
                dirs = [str(p).strip() for p in raw_dirs if str(p).strip()] or ["/host/home"]
            else:
                dirs = ["/host/home"]

        return search_pdf(
            query=req.get("query"),
            source=source,
            search_dirs=dirs,
            search_in_contents=bool(req.get("in_contents", False)),
        )

    if cmd == "send_email":
        return send_email(req.get("to"), req.get("subject"), req.get("body"))

    if cmd == "start_web_watch":
        url = req.get("url")
        keyword = req.get("keyword")
        if not url or not keyword:
            return {"status": "error", "message": "URL et mot-clé sont requis pour démarrer la veille."}
        return start_web_watch(url, keyword)

    if cmd == "get_web_watch_summary":
        watch_id = req.get("watch_id")
        if not watch_id:
            return {"status": "error", "message": "ID de veille est requis pour obtenir la synthèse."}
        return get_web_watch_summary(watch_id)

    if cmd == "list_web_watches":
        return list_web_watches()

    if cmd == "search_web_tavily":
        query = req.get("query")
        if not query:
            return {"status": "error", "message": "La requête est requise pour la recherche web Tavily."}
        return search_web_tavily(query)

    return {"status": "error", "message": "Commande inconnue"}

