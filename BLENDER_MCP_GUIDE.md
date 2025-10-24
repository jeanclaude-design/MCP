# Guide d'utilisation de l'intégration Blender MCP

## 🎯 Présentation

Ce guide explique comment utiliser l'intégration Blender MCP dans votre projet FastAPI. L'agent Blender vous permet de contrôler Blender à distance via le Model Context Protocol.

## 📋 Prérequis

### 1. Installer Blender avec le plugin MCP

Vous devez d'abord installer le serveur MCP dans Blender :

```bash
# Cloner le repository Blender MCP
git clone https://github.com/ahujasid/blender-mcp.git

# Suivre les instructions d'installation du plugin dans Blender
# Voir : https://github.com/ahujasid/blender-mcp#installation
```

### 2. Lancer le serveur MCP dans Blender

Une fois le plugin installé dans Blender :
1. Ouvrez Blender
2. Activez le plugin MCP dans les préférences
3. Le serveur MCP démarre automatiquement sur `localhost:3000` (port par défaut)

### 3. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

## 🚀 Utilisation via l'API REST

Une fois votre serveur FastAPI lancé (`./launch.sh`), vous pouvez envoyer des commandes à Blender via l'endpoint `/mcp`.

### Configuration du serveur Blender

Si votre serveur Blender MCP utilise un port différent :

```bash
curl -X POST http://localhost:5005/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "command": "blender_configure_server",
    "host": "localhost",
    "port": 3000
  }'
```

## 📦 Exemples de commandes

### 1. Créer un objet 3D

#### Créer un cube
```bash
curl -X POST http://localhost:5005/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "command": "blender_create_object",
    "object_type": "CUBE",
    "name": "MonCube",
    "location": [0, 0, 0],
    "scale": [1, 1, 1]
  }'
```

#### Créer une sphère
```bash
curl -X POST http://localhost:5005/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "command": "blender_create_object",
    "object_type": "SPHERE",
    "name": "MaSphere",
    "location": [2, 0, 0],
    "scale": [0.5, 0.5, 0.5]
  }'
```

Types d'objets disponibles : `CUBE`, `SPHERE`, `CYLINDER`, `CONE`, `PLANE`, `TORUS`, etc.

### 2. Modifier un objet existant

```bash
curl -X POST http://localhost:5005/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "command": "blender_modify_object",
    "object_name": "MonCube",
    "location": [1, 2, 3],
    "rotation": [0, 0, 1.57],
    "scale": [2, 2, 2]
  }'
```

### 3. Appliquer un matériau

```bash
curl -X POST http://localhost:5005/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "command": "blender_apply_material",
    "object_name": "MaSphere",
    "material_name": "MateriauRouge",
    "color": [1.0, 0.0, 0.0, 1.0],
    "metallic": 0.8,
    "roughness": 0.2
  }'
```

**Notes :**
- `color` : valeurs RGBA entre 0.0 et 1.0
- `metallic` : 0.0 (non métallique) à 1.0 (totalement métallique)
- `roughness` : 0.0 (lisse) à 1.0 (rugueux)

### 4. Exécuter un script Python dans Blender

```bash
curl -X POST http://localhost:5005/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "command": "blender_run_script",
    "script": "import bpy\nbpy.ops.mesh.primitive_monkey_add(location=(0, 0, 2))\nprint(\"Suzanne ajoutée!\")"
  }'
```

### 5. Obtenir les informations de la scène

```bash
curl -X POST http://localhost:5005/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "command": "blender_get_scene_info"
  }'
```

Retourne la liste des objets, caméras, lumières, etc. présents dans la scène.

### 6. Contrôler la caméra

```bash
curl -X POST http://localhost:5005/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "command": "blender_control_camera",
    "location": [7, -7, 5],
    "rotation": [1.1, 0, 0.785],
    "lens": 50
  }'
```

**Notes :**
- `location` : position [x, y, z]
- `rotation` : rotation en radians [x, y, z]
- `lens` : focale en millimètres

### 7. Faire un rendu

```bash
curl -X POST http://localhost:5005/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "command": "blender_render",
    "output_path": "/tmp/mon_rendu.png",
    "resolution_x": 1920,
    "resolution_y": 1080,
    "samples": 256
  }'
```

**Notes :**
- `samples` : nombre d'échantillons (plus = meilleure qualité mais plus lent)
- Le rendu est sauvegardé dans `output_path`

### 8. Ajouter un asset Poly Haven

```bash
curl -X POST http://localhost:5005/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "command": "blender_add_polyhaven_asset",
    "asset_type": "hdri",
    "asset_name": "kloofendal_48d_partly_cloudy_puresky"
  }'
```

Types d'assets disponibles :
- `hdri` : environnements HDRI
- `texture` : textures PBR
- `model` : modèles 3D

## 🧪 Exemple complet : Créer une scène

Voici un script Python qui crée une scène complète :

```python
import requests
import json

BASE_URL = "http://localhost:5005/mcp"

def send_command(command, **kwargs):
    payload = {"command": command, **kwargs}
    response = requests.post(BASE_URL, json=payload)
    return response.json()

# 1. Créer un plan (sol)
print("Création du sol...")
send_command("blender_create_object",
    object_type="PLANE",
    name="Sol",
    scale=[10, 10, 1]
)

# 2. Créer un cube
print("Création du cube...")
send_command("blender_create_object",
    object_type="CUBE",
    name="Cube1",
    location=[0, 0, 1]
)

# 3. Appliquer un matériau bleu au cube
print("Application du matériau...")
send_command("blender_apply_material",
    object_name="Cube1",
    color=[0.1, 0.3, 0.8, 1.0],
    metallic=0.5,
    roughness=0.3
)

# 4. Positionner la caméra
print("Positionnement de la caméra...")
send_command("blender_control_camera",
    location=[7, -7, 5],
    rotation=[1.1, 0, 0.785],
    lens=50
)

# 5. Faire un rendu
print("Rendu de la scène...")
result = send_command("blender_render",
    output_path="/tmp/ma_scene.png",
    resolution_x=1920,
    resolution_y=1080,
    samples=128
)

print("Scène créée et rendue !")
print(result)
```

## 🐍 Utilisation directe de l'agent Python

Vous pouvez aussi utiliser directement l'agent dans votre code Python :

```python
from agents import blender_agent

# Créer un objet
result = blender_agent.create_object(
    object_type="SPHERE",
    name="MaSphere",
    location=[0, 0, 2]
)
print(result)

# Appliquer un matériau
result = blender_agent.apply_material(
    object_name="MaSphere",
    color=[1.0, 0.0, 0.0, 1.0],
    metallic=0.8,
    roughness=0.2
)
print(result)

# Obtenir les infos de la scène
scene_info = blender_agent.get_scene_info()
print(scene_info)
```

## 🔧 Dépannage

### Le serveur ne répond pas

Vérifiez que :
1. Blender est ouvert avec le plugin MCP activé
2. Le serveur MCP est bien lancé dans Blender
3. Le port est correct (par défaut 3000)
4. Aucun pare-feu ne bloque la connexion

### Erreur "aiohttp n'est pas installé"

```bash
pip install aiohttp
```

### Erreur de timeout

Le serveur Blender peut prendre du temps pour certaines opérations (rendu, etc.). Le timeout est fixé à 30 secondes par défaut.

## 📚 Ressources

- [Repository Blender MCP](https://github.com/ahujasid/blender-mcp)
- [Documentation Blender MCP](https://blender-mcp.com/)
- [Poly Haven Assets](https://polyhaven.com/)
- [Documentation Blender Python API](https://docs.blender.org/api/current/)

## 🎨 Cas d'usage avancés

### Automatiser la création de modèles

Vous pouvez créer des scripts qui génèrent automatiquement des modèles 3D basés sur des données :

```python
# Créer une grille de cubes avec différentes couleurs
for x in range(5):
    for y in range(5):
        send_command("blender_create_object",
            object_type="CUBE",
            name=f"Cube_{x}_{y}",
            location=[x * 2, y * 2, 0],
            scale=[0.8, 0.8, 0.8]
        )

        # Couleur basée sur la position
        r = x / 5
        g = y / 5
        b = 0.5

        send_command("blender_apply_material",
            object_name=f"Cube_{x}_{y}",
            color=[r, g, b, 1.0]
        )
```

### Intégration avec un agent vocal

Combinez l'agent Blender avec l'assistant vocal existant pour contrôler Blender à la voix !

---

**Auteur:** Jean-Claude Spinelli
**Dernière mise à jour:** 2025-10-24
