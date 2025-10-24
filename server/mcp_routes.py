# server/mcp_routes.py
from fastapi import APIRouter
from agents.local_pdf_agent import search_pdf
from agents.gmail_agent import send_email
from agents.web_watch_agent import start_web_watch, get_web_watch_summary, list_web_watches
from agents.tavily_agent import search_web_tavily
from agents import blender_agent
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

    # ===== Commandes Blender MCP =====

    if cmd == "blender_create_object":
        object_type = req.get("object_type", "CUBE")
        name = req.get("name")
        location = req.get("location")
        scale = req.get("scale")
        return blender_agent.create_object(object_type, name, location, scale)

    if cmd == "blender_modify_object":
        object_name = req.get("object_name")
        if not object_name:
            return {"status": "error", "message": "Le nom de l'objet est requis."}
        location = req.get("location")
        rotation = req.get("rotation")
        scale = req.get("scale")
        return blender_agent.modify_object(object_name, location, rotation, scale)

    if cmd == "blender_apply_material":
        object_name = req.get("object_name")
        if not object_name:
            return {"status": "error", "message": "Le nom de l'objet est requis."}
        material_name = req.get("material_name", "Material")
        color = req.get("color")
        metallic = req.get("metallic", 0.0)
        roughness = req.get("roughness", 0.5)
        return blender_agent.apply_material(object_name, material_name, color, metallic, roughness)

    if cmd == "blender_run_script":
        script = req.get("script")
        if not script:
            return {"status": "error", "message": "Le script Python est requis."}
        return blender_agent.run_python_script(script)

    if cmd == "blender_get_scene_info":
        return blender_agent.get_scene_info()

    if cmd == "blender_control_camera":
        location = req.get("location")
        rotation = req.get("rotation")
        lens = req.get("lens")
        return blender_agent.control_camera(location, rotation, lens)

    if cmd == "blender_render":
        output_path = req.get("output_path", "/tmp/render.png")
        resolution_x = req.get("resolution_x", 1920)
        resolution_y = req.get("resolution_y", 1080)
        samples = req.get("samples", 128)
        return blender_agent.render_scene(output_path, resolution_x, resolution_y, samples)

    if cmd == "blender_add_polyhaven_asset":
        asset_type = req.get("asset_type")
        asset_name = req.get("asset_name")
        if not asset_type or not asset_name:
            return {"status": "error", "message": "Le type et le nom de l'asset Poly Haven sont requis."}
        return blender_agent.add_polyhaven_asset(asset_type, asset_name)

    if cmd == "blender_configure_server":
        host = req.get("host", "localhost")
        port = req.get("port", 3000)
        blender_agent.configure_blender_server(host, port)
        return {"status": "success", "message": f"Serveur Blender MCP configuré sur {host}:{port}"}

    return {"status": "error", "message": "Commande inconnue"}

