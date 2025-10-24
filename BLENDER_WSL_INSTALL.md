# 🐧 Guide d'installation de Blender sur WSL (Windows Subsystem for Linux)

Ce guide explique comment installer et configurer Blender sur WSL pour l'utiliser avec le serveur MCP.

## 📋 Table des matières

1. [Prérequis](#prérequis)
2. [Méthode 1 : WSL2 avec WSLg (Recommandé)](#méthode-1--wsl2-avec-wslg-recommandé)
3. [Méthode 2 : WSL2 avec X11 Server](#méthode-2--wsl2-avec-x11-server)
4. [Installation de Blender](#installation-de-blender)
5. [Installation du plugin MCP Blender](#installation-du-plugin-mcp-blender)
6. [Vérification et test](#vérification-et-test)
7. [Dépannage](#dépannage)

---

## 📋 Prérequis

### Vérifier votre version de WSL

```bash
wsl --version
```

**Important :** Vous devez utiliser WSL2 (pas WSL1).

Si vous avez WSL1, mettez à jour :

```powershell
# Dans PowerShell (Windows) en tant qu'administrateur
wsl --set-default-version 2
wsl --update
```

### Vérifier votre distribution

```bash
cat /etc/os-release
```

Ce guide couvre Ubuntu, Debian et autres distributions basées sur Debian.

---

## 🎯 Méthode 1 : WSL2 avec WSLg (Recommandé)

**WSLg** (Windows Subsystem for Linux GUI) est intégré dans WSL2 depuis 2021. C'est la méthode la plus simple.

### Étape 1 : Vérifier si WSLg est disponible

```bash
echo $DISPLAY
```

Si vous voyez quelque chose comme `:0` ou `:1`, WSLg est activé. ✅

### Étape 2 : Mettre à jour WSL (Windows)

```powershell
# Dans PowerShell (Windows) en tant qu'administrateur
wsl --update
wsl --shutdown
```

Puis redémarrez votre distribution WSL.

### Étape 3 : Installer les dépendances graphiques

```bash
sudo apt update
sudo apt install -y \
    libgl1-mesa-glx \
    libglu1-mesa \
    libxi6 \
    libxrender1 \
    libxrandr2 \
    libxfixes3 \
    libxcursor1 \
    libxinerama1 \
    libxxf86vm1 \
    libgomp1 \
    libsm6
```

### Étape 4 : Passer à [Installation de Blender](#installation-de-blender)

---

## 🖥️ Méthode 2 : WSL2 avec X11 Server

Si WSLg ne fonctionne pas, utilisez un serveur X11 externe.

### Étape 1 : Installer VcXsrv (Windows)

1. Téléchargez VcXsrv : https://sourceforge.net/projects/vcxsrv/
2. Installez-le sur Windows
3. Lancez XLaunch avec ces paramètres :
   - Display number : `0`
   - Start no client : ✅
   - Disable access control : ✅
   - **Important :** Cochez "Disable access control"

### Étape 2 : Configurer DISPLAY dans WSL

```bash
# Ajouter à votre ~/.bashrc
echo 'export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '\''{print $2}'\''):0' >> ~/.bashrc
echo 'export LIBGL_ALWAYS_INDIRECT=1' >> ~/.bashrc

# Recharger la configuration
source ~/.bashrc

# Vérifier
echo $DISPLAY
```

### Étape 3 : Installer les dépendances

```bash
sudo apt update
sudo apt install -y \
    x11-apps \
    libgl1-mesa-glx \
    libglu1-mesa \
    libxi6 \
    libxrender1 \
    libxrandr2 \
    libxfixes3 \
    libxcursor1 \
    libxinerama1 \
    libxxf86vm1 \
    libgomp1 \
    libsm6
```

### Étape 4 : Tester X11

```bash
# Tester avec xclock
xclock
```

Si une fenêtre d'horloge apparaît, X11 fonctionne ! ✅

### Étape 5 : Configurer le pare-feu Windows

VcXsrv doit être autorisé dans le pare-feu Windows :
1. Ouvrez "Pare-feu Windows Defender"
2. Autoriser une application
3. Ajoutez VcXsrv (vcxsrv.exe)
4. Cochez "Privé" et "Public"

---

## 📦 Installation de Blender

### Option A : Installation via Snap (Recommandé)

```bash
# Installer snapd si nécessaire
sudo apt update
sudo apt install snapd -y

# Installer Blender
sudo snap install blender --classic

# Créer un lien symbolique pour un accès facile
sudo ln -s /snap/bin/blender /usr/local/bin/blender
```

### Option B : Installation via le site officiel

```bash
# Créer un dossier pour Blender
mkdir -p ~/Applications
cd ~/Applications

# Télécharger Blender (version 4.3 LTS - ajustez selon la dernière version)
wget https://mirrors.ocf.berkeley.edu/blender/release/Blender4.3/blender-4.3.0-linux-x64.tar.xz

# Extraire
tar -xf blender-4.3.0-linux-x64.tar.xz

# Créer un lien symbolique
sudo ln -s ~/Applications/blender-4.3.0-linux-x64/blender /usr/local/bin/blender

# Nettoyer
rm blender-4.3.0-linux-x64.tar.xz
```

### Option C : Installation via apt (version plus ancienne)

```bash
sudo apt update
sudo apt install blender -y
```

⚠️ **Note :** Cette méthode installe souvent une version plus ancienne de Blender.

### Vérifier l'installation

```bash
blender --version
```

### Lancer Blender

```bash
# Lancer Blender en mode graphique
blender

# Ou en mode headless (sans interface graphique)
blender --background
```

---

## 🔌 Installation du plugin MCP Blender

### Étape 1 : Cloner le repository Blender MCP

```bash
cd ~
git clone https://github.com/ahujasid/blender-mcp.git
cd blender-mcp
```

### Étape 2 : Installer les dépendances Python

```bash
# Si vous utilisez Blender via snap
/snap/blender/current/4.3/python/bin/python3.11 -m pip install --upgrade pip
/snap/blender/current/4.3/python/bin/python3.11 -m pip install -r requirements.txt

# Si vous avez installé Blender manuellement
~/Applications/blender-4.3.0-linux-x64/4.3/python/bin/python3.11 -m pip install --upgrade pip
~/Applications/blender-4.3.0-linux-x64/4.3/python/bin/python3.11 -m pip install -r requirements.txt
```

### Étape 3 : Installer le plugin dans Blender

#### Méthode automatique (script)

```bash
# Créer un script d'installation
cat > install_mcp_addon.py << 'EOF'
import bpy
import os
import shutil
from pathlib import Path

# Chemin du plugin
addon_src = Path.home() / "blender-mcp" / "addon"
addon_dest = Path(bpy.utils.user_resource('SCRIPTS')) / "addons" / "blender_mcp"

# Copier le plugin
if addon_dest.exists():
    shutil.rmtree(addon_dest)
shutil.copytree(addon_src, addon_dest)

# Activer le plugin
bpy.ops.preferences.addon_enable(module="blender_mcp")

# Sauvegarder les préférences
bpy.ops.wm.save_userpref()

print("✅ Plugin MCP Blender installé avec succès!")
EOF

# Exécuter le script dans Blender
blender --background --python install_mcp_addon.py
```

#### Méthode manuelle (via l'interface Blender)

1. Lancez Blender :
   ```bash
   blender
   ```

2. Allez dans : **Edit → Preferences → Add-ons**

3. Cliquez sur **Install...**

4. Naviguez vers : `~/blender-mcp/addon/`

5. Sélectionnez le dossier ou le fichier `.zip` du plugin

6. Activez le plugin en cochant la case à côté de **"Blender MCP"**

7. Configurez le port si nécessaire (par défaut : `3000`)

8. Cliquez sur **Start Server** pour lancer le serveur MCP

### Étape 4 : Configurer le serveur MCP

Une fois le plugin installé et activé :

1. Dans les préférences du plugin, vous verrez :
   - **Host :** `localhost`
   - **Port :** `3000` (par défaut)
   - **Bouton "Start Server"**

2. Cliquez sur **"Start Server"**

3. Vous devriez voir : `✅ MCP Server running on localhost:3000`

---

## ✅ Vérification et test

### Test 1 : Vérifier que Blender fonctionne

```bash
# Lancer Blender
blender
```

Si l'interface graphique s'ouvre, c'est bon ! ✅

### Test 2 : Vérifier que le serveur MCP est lancé

```bash
# Dans un nouveau terminal WSL
curl http://localhost:3000/health
```

Si vous obtenez une réponse, le serveur MCP fonctionne ! ✅

### Test 3 : Tester l'intégration avec votre API

```bash
# Lancer votre serveur FastAPI (dans le projet MCP)
cd ~/MCP
./launch.sh

# Dans un autre terminal, tester
python3 test_blender_mcp.py --simple
```

Si un cube est créé dans Blender, tout fonctionne ! 🎉

---

## 🔧 Dépannage

### Problème : Blender ne se lance pas (erreur X11)

**Symptôme :**
```
Error: Unable to open a display
```

**Solutions :**

1. **Vérifier DISPLAY :**
   ```bash
   echo $DISPLAY
   ```
   Doit afficher quelque chose comme `:0` ou `:1`

2. **Vérifier que VcXsrv est lancé (si vous utilisez X11 Server)**

3. **Tester avec une app simple :**
   ```bash
   sudo apt install x11-apps
   xclock
   ```

4. **Réexporter DISPLAY :**
   ```bash
   export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
   ```

### Problème : Blender se lance mais crash immédiatement

**Solutions :**

1. **Installer les drivers Mesa :**
   ```bash
   sudo apt install mesa-utils libgl1-mesa-dri
   ```

2. **Utiliser le rendu logiciel :**
   ```bash
   LIBGL_ALWAYS_SOFTWARE=1 blender
   ```

3. **Vérifier OpenGL :**
   ```bash
   glxinfo | grep "OpenGL version"
   ```

### Problème : Le serveur MCP ne démarre pas

**Solutions :**

1. **Vérifier que le port 3000 est libre :**
   ```bash
   sudo lsof -i :3000
   ```

2. **Vérifier les logs dans Blender :**
   - Allez dans : **Window → Toggle System Console**

3. **Réinstaller les dépendances Python du plugin**

### Problème : "Permission denied" lors de l'installation

**Solution :**
```bash
sudo chown -R $USER:$USER ~/blender-mcp
```

### Problème : Performance graphique lente

**Solutions :**

1. **Utiliser WSLg plutôt que VcXsrv** (plus performant)

2. **Réduire la qualité graphique dans Blender :**
   - Edit → Preferences → System → Cycles Render Devices

3. **Utiliser le mode CPU uniquement :**
   ```bash
   blender --background  # Mode sans interface pour les rendus
   ```

---

## 🚀 Script d'installation automatique complet

Voici un script qui fait tout automatiquement :

```bash
#!/bin/bash
# install_blender_wsl.sh

echo "🚀 Installation de Blender sur WSL avec MCP"
echo "=========================================="

# Mise à jour du système
echo "📦 Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

# Installation des dépendances
echo "📦 Installation des dépendances graphiques..."
sudo apt install -y \
    libgl1-mesa-glx \
    libglu1-mesa \
    libxi6 \
    libxrender1 \
    libxrandr2 \
    libxfixes3 \
    libxcursor1 \
    libxinerama1 \
    libxxf86vm1 \
    libgomp1 \
    libsm6 \
    mesa-utils \
    git \
    curl \
    wget

# Installation de Blender via Snap
echo "📦 Installation de Blender..."
sudo apt install snapd -y
sudo snap install blender --classic

# Créer un lien symbolique
sudo ln -sf /snap/bin/blender /usr/local/bin/blender

# Vérifier l'installation
echo "✅ Blender installé :"
blender --version

# Cloner Blender MCP
echo "📦 Installation du plugin Blender MCP..."
cd ~
if [ -d "blender-mcp" ]; then
    echo "⚠️  Le dossier blender-mcp existe déjà. Mise à jour..."
    cd blender-mcp
    git pull
else
    git clone https://github.com/ahujasid/blender-mcp.git
    cd blender-mcp
fi

# Installer les dépendances Python du plugin
echo "📦 Installation des dépendances Python du plugin..."
# Note: Cela nécessite que Blender soit lancé au moins une fois
/snap/blender/current/4.3/python/bin/python3.11 -m pip install --upgrade pip || true
/snap/blender/current/4.3/python/bin/python3.11 -m pip install -r requirements.txt || true

echo ""
echo "✅ Installation terminée !"
echo ""
echo "📝 Prochaines étapes :"
echo "   1. Lancez Blender : blender"
echo "   2. Allez dans Edit → Preferences → Add-ons"
echo "   3. Cliquez sur Install et sélectionnez ~/blender-mcp/addon/"
echo "   4. Activez le plugin 'Blender MCP'"
echo "   5. Cliquez sur 'Start Server'"
echo ""
echo "🧪 Puis testez avec :"
echo "   cd ~/MCP"
echo "   python3 test_blender_mcp.py --simple"
```

Sauvegardez ce script et exécutez-le :

```bash
chmod +x install_blender_wsl.sh
./install_blender_wsl.sh
```

---

## 📚 Ressources supplémentaires

- [Documentation officielle WSL](https://docs.microsoft.com/en-us/windows/wsl/)
- [Documentation WSLg](https://github.com/microsoft/wslg)
- [Blender sur Linux](https://www.blender.org/download/linux/)
- [Repository Blender MCP](https://github.com/ahujasid/blender-mcp)
- [VcXsrv](https://sourceforge.net/projects/vcxsrv/)

---

## 🎓 Conseils avancés

### Créer un alias pour lancer Blender avec MCP

```bash
# Ajouter à ~/.bashrc
echo 'alias blender-mcp="blender"' >> ~/.bashrc
source ~/.bashrc
```

### Lancer Blender en arrière-plan avec le serveur MCP

```bash
# Créer un script de lancement
cat > ~/start_blender_mcp.sh << 'EOF'
#!/bin/bash
blender --background --python ~/blender-mcp/start_server.py
EOF

chmod +x ~/start_blender_mcp.sh
```

### Créer un service systemd (optionnel)

Pour lancer automatiquement le serveur MCP au démarrage :

```bash
# Créer le fichier de service
sudo nano /etc/systemd/system/blender-mcp.service
```

Contenu :
```ini
[Unit]
Description=Blender MCP Server
After=network.target

[Service]
Type=simple
User=votreuser
WorkingDirectory=/home/votreuser
ExecStart=/usr/local/bin/blender --background --python /home/votreuser/blender-mcp/start_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Activer :
```bash
sudo systemctl daemon-reload
sudo systemctl enable blender-mcp
sudo systemctl start blender-mcp
```

---

**Auteur :** Jean-Claude Spinelli
**Dernière mise à jour :** 2025-10-24
