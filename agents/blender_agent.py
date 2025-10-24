# agents/blender_agent.py
"""
Agent pour communiquer avec le serveur MCP Blender.
Permet de créer et manipuler des modèles 3D dans Blender via le Model Context Protocol.
"""

import logging
import json
from typing import Dict, Any, Optional, List
import asyncio

log = logging.getLogger("blender_mcp")

# Configuration du serveur MCP Blender
# Le serveur MCP Blender doit être lancé séparément dans Blender
BLENDER_MCP_HOST = "localhost"
BLENDER_MCP_PORT = 3000  # Port par défaut du serveur Blender MCP

class BlenderMCPClient:
    """Client pour communiquer avec le serveur MCP Blender"""

    def __init__(self, host: str = BLENDER_MCP_HOST, port: int = BLENDER_MCP_PORT):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"

    async def send_command(self, tool: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Envoie une commande au serveur MCP Blender

        Args:
            tool: Nom de l'outil MCP à utiliser
            arguments: Arguments pour l'outil

        Returns:
            Résultat de l'exécution de la commande
        """
        try:
            import aiohttp

            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool,
                    "arguments": arguments
                }
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/mcp",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "status": "success",
                            "result": result.get("result", {}),
                            "message": "Commande exécutée avec succès"
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "status": "error",
                            "message": f"Erreur serveur Blender MCP: {error_text}"
                        }

        except ImportError:
            return {
                "status": "error",
                "message": "aiohttp n'est pas installé. Installez-le avec: pip install aiohttp"
            }
        except asyncio.TimeoutError:
            return {
                "status": "error",
                "message": f"Timeout lors de la connexion au serveur Blender MCP sur {self.base_url}"
            }
        except Exception as e:
            log.error(f"Erreur lors de la communication avec Blender MCP: {e}")
            return {
                "status": "error",
                "message": f"Erreur de connexion: {str(e)}. Assurez-vous que Blender avec le plugin MCP est lancé."
            }


# Instance globale du client
_blender_client = BlenderMCPClient()


def create_object(object_type: str = "CUBE", name: Optional[str] = None,
                  location: Optional[List[float]] = None,
                  scale: Optional[List[float]] = None) -> Dict[str, Any]:
    """
    Crée un objet 3D dans Blender

    Args:
        object_type: Type d'objet (CUBE, SPHERE, CYLINDER, CONE, PLANE, etc.)
        name: Nom de l'objet
        location: Position [x, y, z]
        scale: Échelle [x, y, z]

    Returns:
        Résultat de la création
    """
    try:
        arguments = {
            "type": object_type.upper()
        }

        if name:
            arguments["name"] = name
        if location:
            arguments["location"] = location
        if scale:
            arguments["scale"] = scale

        # Utiliser asyncio.run pour exécuter la coroutine
        result = asyncio.run(_blender_client.send_command("create_object", arguments))
        return result

    except Exception as e:
        log.error(f"Erreur create_object: {e}")
        return {
            "status": "error",
            "message": f"Erreur lors de la création de l'objet: {str(e)}"
        }


def modify_object(object_name: str, location: Optional[List[float]] = None,
                  rotation: Optional[List[float]] = None,
                  scale: Optional[List[float]] = None) -> Dict[str, Any]:
    """
    Modifie un objet existant dans Blender

    Args:
        object_name: Nom de l'objet à modifier
        location: Nouvelle position [x, y, z]
        rotation: Nouvelle rotation [x, y, z] en radians
        scale: Nouvelle échelle [x, y, z]

    Returns:
        Résultat de la modification
    """
    try:
        arguments = {
            "name": object_name
        }

        if location:
            arguments["location"] = location
        if rotation:
            arguments["rotation"] = rotation
        if scale:
            arguments["scale"] = scale

        result = asyncio.run(_blender_client.send_command("modify_object", arguments))
        return result

    except Exception as e:
        log.error(f"Erreur modify_object: {e}")
        return {
            "status": "error",
            "message": f"Erreur lors de la modification de l'objet: {str(e)}"
        }


def apply_material(object_name: str, material_name: str = "Material",
                   color: Optional[List[float]] = None,
                   metallic: float = 0.0, roughness: float = 0.5) -> Dict[str, Any]:
    """
    Applique un matériau à un objet

    Args:
        object_name: Nom de l'objet
        material_name: Nom du matériau
        color: Couleur RGBA [r, g, b, a] (0.0 à 1.0)
        metallic: Valeur métallique (0.0 à 1.0)
        roughness: Rugosité (0.0 à 1.0)

    Returns:
        Résultat de l'application du matériau
    """
    try:
        arguments = {
            "object_name": object_name,
            "material_name": material_name,
            "metallic": metallic,
            "roughness": roughness
        }

        if color:
            arguments["color"] = color

        result = asyncio.run(_blender_client.send_command("apply_material", arguments))
        return result

    except Exception as e:
        log.error(f"Erreur apply_material: {e}")
        return {
            "status": "error",
            "message": f"Erreur lors de l'application du matériau: {str(e)}"
        }


def run_python_script(script: str) -> Dict[str, Any]:
    """
    Exécute un script Python dans Blender

    Args:
        script: Code Python à exécuter

    Returns:
        Résultat de l'exécution
    """
    try:
        arguments = {
            "script": script
        }

        result = asyncio.run(_blender_client.send_command("run_python", arguments))
        return result

    except Exception as e:
        log.error(f"Erreur run_python_script: {e}")
        return {
            "status": "error",
            "message": f"Erreur lors de l'exécution du script: {str(e)}"
        }


def get_scene_info() -> Dict[str, Any]:
    """
    Récupère les informations sur la scène Blender actuelle

    Returns:
        Informations sur la scène (objets, caméras, lumières, etc.)
    """
    try:
        result = asyncio.run(_blender_client.send_command("get_scene_info", {}))
        return result

    except Exception as e:
        log.error(f"Erreur get_scene_info: {e}")
        return {
            "status": "error",
            "message": f"Erreur lors de la récupération des infos de scène: {str(e)}"
        }


def control_camera(location: Optional[List[float]] = None,
                   rotation: Optional[List[float]] = None,
                   lens: Optional[float] = None) -> Dict[str, Any]:
    """
    Contrôle la caméra de la scène

    Args:
        location: Position de la caméra [x, y, z]
        rotation: Rotation de la caméra [x, y, z] en radians
        lens: Focale de la caméra en mm

    Returns:
        Résultat du contrôle de la caméra
    """
    try:
        arguments = {}

        if location:
            arguments["location"] = location
        if rotation:
            arguments["rotation"] = rotation
        if lens:
            arguments["lens"] = lens

        result = asyncio.run(_blender_client.send_command("camera_control", arguments))
        return result

    except Exception as e:
        log.error(f"Erreur control_camera: {e}")
        return {
            "status": "error",
            "message": f"Erreur lors du contrôle de la caméra: {str(e)}"
        }


def render_scene(output_path: str = "/tmp/render.png",
                 resolution_x: int = 1920, resolution_y: int = 1080,
                 samples: int = 128) -> Dict[str, Any]:
    """
    Lance un rendu de la scène

    Args:
        output_path: Chemin de sortie du rendu
        resolution_x: Largeur en pixels
        resolution_y: Hauteur en pixels
        samples: Nombre d'échantillons pour le rendu

    Returns:
        Résultat du rendu
    """
    try:
        arguments = {
            "output_path": output_path,
            "resolution_x": resolution_x,
            "resolution_y": resolution_y,
            "samples": samples
        }

        result = asyncio.run(_blender_client.send_command("render_scene", arguments))
        return result

    except Exception as e:
        log.error(f"Erreur render_scene: {e}")
        return {
            "status": "error",
            "message": f"Erreur lors du rendu: {str(e)}"
        }


def add_polyhaven_asset(asset_type: str, asset_name: str) -> Dict[str, Any]:
    """
    Ajoute un asset de Poly Haven (HDRI, texture, modèle)

    Args:
        asset_type: Type d'asset (hdri, texture, model)
        asset_name: Nom de l'asset Poly Haven

    Returns:
        Résultat de l'ajout de l'asset
    """
    try:
        arguments = {
            "asset_type": asset_type.lower(),
            "asset_name": asset_name
        }

        result = asyncio.run(_blender_client.send_command("add_polyhaven_asset", arguments))
        return result

    except Exception as e:
        log.error(f"Erreur add_polyhaven_asset: {e}")
        return {
            "status": "error",
            "message": f"Erreur lors de l'ajout de l'asset Poly Haven: {str(e)}"
        }


def configure_blender_server(host: str = "localhost", port: int = 3000):
    """
    Configure l'adresse du serveur MCP Blender

    Args:
        host: Adresse du serveur
        port: Port du serveur
    """
    global _blender_client
    _blender_client = BlenderMCPClient(host, port)
    log.info(f"Serveur Blender MCP configuré sur {host}:{port}")
