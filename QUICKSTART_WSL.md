# ⚡ Guide de démarrage rapide - Blender MCP sur WSL

Guide ultra-rapide pour installer et utiliser Blender avec MCP sur WSL.

## 🚀 Installation en 3 étapes

### 1️⃣ Installer Blender + MCP (automatique)

```bash
cd ~/MCP
./install_blender_wsl.sh
```

Le script va :
- ✅ Installer toutes les dépendances
- ✅ Installer Blender (vous choisissez la méthode)
- ✅ Télécharger le plugin Blender MCP
- ✅ Configurer l'environnement

**Durée : 5-10 minutes**

### 2️⃣ Vérifier l'installation

```bash
./check_blender_wsl.sh
```

Ce script vérifie que tout est prêt à fonctionner.

### 3️⃣ Configurer le plugin dans Blender

```bash
# Lancer Blender
blender
```

Puis dans Blender :
1. **Edit → Preferences → Add-ons**
2. Cliquez sur **"Install..."**
3. Sélectionnez : `~/blender-mcp/addon/`
4. Activez le plugin **"Blender MCP"**
5. Cliquez sur **"Start Server"**

Vous devriez voir : `✅ MCP Server running on localhost:3000`

---

## 🧪 Test rapide

### Tester Blender seul

```bash
# Test d'affichage graphique
xclock

# Si l'horloge apparaît, X11 fonctionne ! ✅
```

### Tester l'intégration complète

```bash
# 1. Lancer votre API FastAPI
cd ~/MCP
./launch.sh

# 2. Dans un autre terminal, tester l'API Blender
python3 test_blender_mcp.py --simple
```

Si un cube apparaît dans Blender, c'est gagné ! 🎉

---

## 🐛 Problèmes courants

### Blender ne se lance pas (erreur DISPLAY)

```bash
# Vérifier DISPLAY
echo $DISPLAY
# Doit afficher quelque chose comme :0 ou :1

# Si vide, exporter manuellement
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0

# Relancer
blender
```

### Pas d'affichage graphique

**Vous avez 2 options :**

#### Option A : WSLg (intégré, recommandé)

```powershell
# Dans PowerShell Windows (administrateur)
wsl --update
wsl --shutdown
# Redémarrez WSL
```

#### Option B : VcXsrv (serveur X11 externe)

1. Téléchargez VcXsrv : https://sourceforge.net/projects/vcxsrv/
2. Lancez XLaunch avec :
   - Display number : `0`
   - Disable access control : ✅ (coché)
3. Dans WSL :
   ```bash
   export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
   ```

### Le serveur MCP ne démarre pas

```bash
# Vérifier que le port 3000 est libre
sudo lsof -i :3000

# Si occupé, tuer le processus
sudo kill -9 <PID>

# Relancer Blender et réessayer
```

### Test de l'API échoue

```bash
# 1. Vérifier que Blender est lancé
ps aux | grep blender

# 2. Vérifier que le serveur MCP est actif
curl http://localhost:3000/health

# 3. Vérifier que l'API FastAPI tourne
curl http://localhost:5005/

# 4. Relancer le test avec plus de détails
python3 test_blender_mcp.py
```

---

## 📖 Commandes utiles

```bash
# Lancer Blender
blender

# Lancer Blender en arrière-plan (sans interface)
blender --background

# Vérifier la version de Blender
blender --version

# Vérifier l'environnement WSL
./check_blender_wsl.sh

# Créer un cube via l'API
curl -X POST http://localhost:5005/mcp \
  -H "Content-Type: application/json" \
  -d '{"command":"blender_create_object","object_type":"CUBE"}'

# Obtenir les infos de la scène
curl -X POST http://localhost:5005/mcp \
  -H "Content-Type: application/json" \
  -d '{"command":"blender_get_scene_info"}'
```

---

## 📚 Documentation complète

- **Installation détaillée :** `BLENDER_WSL_INSTALL.md`
- **Utilisation de l'API :** `BLENDER_MCP_GUIDE.md`
- **Dépannage avancé :** `BLENDER_WSL_INSTALL.md` (section Dépannage)

---

## 🎯 Workflow typique

```bash
# Terminal 1 : Blender avec MCP
blender
# → Dans Blender : Activer le plugin MCP et Start Server

# Terminal 2 : API FastAPI
cd ~/MCP
./launch.sh

# Terminal 3 : Tests ou commandes
python3 test_blender_mcp.py --simple
# ou
curl -X POST http://localhost:5005/mcp -H "Content-Type: application/json" -d '{"command":"blender_create_object","object_type":"SPHERE"}'
```

---

## ⚡ Résumé des fichiers importants

| Fichier | Description |
|---------|-------------|
| `install_blender_wsl.sh` | Installation automatique de Blender + MCP |
| `check_blender_wsl.sh` | Vérification de l'environnement |
| `test_blender_mcp.py` | Script de test de l'intégration |
| `BLENDER_WSL_INSTALL.md` | Guide d'installation détaillé |
| `BLENDER_MCP_GUIDE.md` | Guide d'utilisation de l'API |
| `QUICKSTART_WSL.md` | Ce fichier (guide rapide) |

---

**Besoin d'aide ?** Consultez `BLENDER_WSL_INSTALL.md` section "Dépannage" 🛠️

**Auteur :** Jean-Claude Spinelli
