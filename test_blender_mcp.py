#!/usr/bin/env python3
"""
Script de test pour l'intégration Blender MCP
Teste les différentes fonctionnalités de l'agent Blender
"""

import requests
import json
import time

BASE_URL = "http://localhost:5005/mcp"

def send_command(command, **kwargs):
    """Envoie une commande à l'API MCP"""
    payload = {"command": command, **kwargs}
    print(f"\n📤 Envoi de la commande: {command}")
    print(f"   Paramètres: {json.dumps(kwargs, indent=2)}")

    try:
        response = requests.post(BASE_URL, json=payload, timeout=10)
        result = response.json()

        if result.get("status") == "success":
            print(f"✅ Succès: {result.get('message', 'OK')}")
        else:
            print(f"❌ Erreur: {result.get('message', 'Erreur inconnue')}")

        return result
    except requests.exceptions.ConnectionError:
        print(f"❌ Erreur: Impossible de se connecter au serveur FastAPI sur {BASE_URL}")
        print(f"   Assurez-vous que le serveur est lancé avec ./launch.sh")
        return {"status": "error", "message": "Connexion refusée"}
    except requests.exceptions.Timeout:
        print(f"⏱️  Timeout: La requête a pris trop de temps")
        return {"status": "error", "message": "Timeout"}
    except Exception as e:
        print(f"❌ Erreur inattendue: {str(e)}")
        return {"status": "error", "message": str(e)}


def test_blender_connection():
    """Teste la connexion au serveur Blender MCP"""
    print("\n" + "="*60)
    print("🔌 Test de connexion au serveur Blender MCP")
    print("="*60)

    result = send_command("blender_get_scene_info")
    return result.get("status") == "success"


def test_create_objects():
    """Teste la création d'objets 3D"""
    print("\n" + "="*60)
    print("📦 Test de création d'objets 3D")
    print("="*60)

    # Créer un cube
    send_command("blender_create_object",
        object_type="CUBE",
        name="TestCube",
        location=[0, 0, 1],
        scale=[1, 1, 1]
    )

    time.sleep(0.5)

    # Créer une sphère
    send_command("blender_create_object",
        object_type="SPHERE",
        name="TestSphere",
        location=[3, 0, 1],
        scale=[0.8, 0.8, 0.8]
    )

    time.sleep(0.5)

    # Créer un cylindre
    send_command("blender_create_object",
        object_type="CYLINDER",
        name="TestCylinder",
        location=[-3, 0, 1]
    )


def test_modify_object():
    """Teste la modification d'objets"""
    print("\n" + "="*60)
    print("✏️  Test de modification d'objets")
    print("="*60)

    send_command("blender_modify_object",
        object_name="TestCube",
        location=[0, 0, 2],
        rotation=[0, 0, 0.785],  # 45 degrés en radians
        scale=[1.5, 1.5, 1.5]
    )


def test_apply_materials():
    """Teste l'application de matériaux"""
    print("\n" + "="*60)
    print("🎨 Test d'application de matériaux")
    print("="*60)

    # Matériau rouge pour le cube
    send_command("blender_apply_material",
        object_name="TestCube",
        material_name="MateriauRouge",
        color=[1.0, 0.0, 0.0, 1.0],
        metallic=0.8,
        roughness=0.2
    )

    time.sleep(0.5)

    # Matériau bleu pour la sphère
    send_command("blender_apply_material",
        object_name="TestSphere",
        material_name="MateriauBleu",
        color=[0.0, 0.3, 1.0, 1.0],
        metallic=0.5,
        roughness=0.5
    )


def test_camera_control():
    """Teste le contrôle de la caméra"""
    print("\n" + "="*60)
    print("📷 Test de contrôle de la caméra")
    print("="*60)

    send_command("blender_control_camera",
        location=[7, -7, 5],
        rotation=[1.1, 0, 0.785],
        lens=50
    )


def test_python_script():
    """Teste l'exécution de scripts Python"""
    print("\n" + "="*60)
    print("🐍 Test d'exécution de script Python")
    print("="*60)

    script = """
import bpy
print("Script Python exécuté dans Blender!")
print(f"Nombre d'objets dans la scène: {len(bpy.data.objects)}")
"""

    send_command("blender_run_script", script=script)


def test_scene_info():
    """Teste la récupération des informations de scène"""
    print("\n" + "="*60)
    print("ℹ️  Test de récupération des informations de scène")
    print("="*60)

    result = send_command("blender_get_scene_info")

    if result.get("status") == "success" and result.get("result"):
        print("\n📊 Informations de la scène:")
        print(json.dumps(result.get("result"), indent=2))


def run_all_tests():
    """Lance tous les tests"""
    print("\n" + "="*60)
    print("🚀 LANCEMENT DES TESTS BLENDER MCP")
    print("="*60)

    print("\n⚠️  PRÉREQUIS:")
    print("   1. Le serveur FastAPI doit être lancé (./launch.sh)")
    print("   2. Blender doit être ouvert avec le plugin MCP activé")
    print("   3. Le serveur MCP Blender doit tourner (par défaut sur localhost:3000)")

    input("\n▶️  Appuyez sur Entrée pour continuer...")

    # Test de connexion
    if not test_blender_connection():
        print("\n❌ Échec de connexion au serveur Blender MCP")
        print("\n💡 Vérifiez que:")
        print("   - Blender est ouvert")
        print("   - Le plugin MCP est installé et activé")
        print("   - Le serveur MCP tourne dans Blender")
        print("   - Le port est correct (défaut: 3000)")
        return

    # Tests de fonctionnalités
    test_create_objects()
    test_modify_object()
    test_apply_materials()
    test_camera_control()
    test_python_script()
    test_scene_info()

    print("\n" + "="*60)
    print("✅ TESTS TERMINÉS")
    print("="*60)
    print("\n💡 Vérifiez Blender pour voir les objets créés!")


def test_simple_cube():
    """Test simple rapide - créer un seul cube"""
    print("\n" + "="*60)
    print("🎲 Test simple: Création d'un cube")
    print("="*60)

    result = send_command("blender_create_object",
        object_type="CUBE",
        name="SimpleTestCube",
        location=[0, 0, 0]
    )

    if result.get("status") == "success":
        print("\n✅ Le cube a été créé avec succès!")
        print("   Vérifiez Blender pour le voir.")
    else:
        print("\n❌ Échec de création du cube")
        print(f"   Raison: {result.get('message')}")


if __name__ == "__main__":
    import sys

    print("""
╔════════════════════════════════════════════════════════════╗
║          TEST BLENDER MCP - FastAPI Integration           ║
╚════════════════════════════════════════════════════════════╝
    """)

    if len(sys.argv) > 1 and sys.argv[1] == "--simple":
        test_simple_cube()
    else:
        run_all_tests()

    print("\n✨ Script de test terminé\n")
