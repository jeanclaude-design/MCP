#!/bin/bash
# install_blender_wsl.sh
# Script d'installation automatique de Blender avec MCP sur WSL

set -e  # Arrêter en cas d'erreur

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     🚀 Installation de Blender + MCP sur WSL              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifier que nous sommes sur WSL
if ! grep -qi microsoft /proc/version; then
    error "Ce script est conçu pour WSL. Vous n'êtes pas sur WSL."
    exit 1
fi

success "WSL détecté"

# Vérifier la version de WSL
info "Vérification de l'environnement..."
if [ -n "$DISPLAY" ]; then
    success "DISPLAY est configuré : $DISPLAY"
else
    warning "DISPLAY n'est pas configuré. WSLg pourrait ne pas être disponible."
    warning "Vous devrez peut-être installer VcXsrv (voir le guide complet)"
fi

# Mise à jour du système
info "Mise à jour du système..."
sudo apt update
sudo apt upgrade -y

# Installation des dépendances graphiques
info "Installation des dépendances graphiques..."
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
    libgl1-mesa-dri \
    git \
    curl \
    wget \
    python3-pip

success "Dépendances installées"

# Demander à l'utilisateur quelle méthode d'installation
echo ""
echo "Choisissez la méthode d'installation de Blender :"
echo "  1) Snap (Recommandé - dernière version)"
echo "  2) Téléchargement manuel (contrôle de la version)"
echo "  3) APT (version du dépôt - peut être ancienne)"
read -p "Votre choix (1-3) : " install_choice

case $install_choice in
    1)
        info "Installation de Blender via Snap..."
        sudo apt install snapd -y
        sudo snap install blender --classic

        # Créer un lien symbolique
        sudo ln -sf /snap/bin/blender /usr/local/bin/blender
        BLENDER_PYTHON_PATH="/snap/blender/current/4.3/python/bin/python3.11"
        ;;

    2)
        info "Installation de Blender par téléchargement manuel..."

        # Demander la version
        echo "Quelle version de Blender voulez-vous ?"
        echo "  Exemples : 4.3.0, 4.2.3, 4.1.1"
        read -p "Version (défaut: 4.3.0) : " blender_version
        blender_version=${blender_version:-4.3.0}

        # Extraire la version majeure.mineure
        blender_major=$(echo $blender_version | cut -d. -f1,2)

        # Créer le dossier Applications
        mkdir -p ~/Applications
        cd ~/Applications

        # URL de téléchargement
        DOWNLOAD_URL="https://mirrors.ocf.berkeley.edu/blender/release/Blender${blender_major}/blender-${blender_version}-linux-x64.tar.xz"

        info "Téléchargement depuis $DOWNLOAD_URL"
        wget $DOWNLOAD_URL -O blender.tar.xz

        info "Extraction..."
        tar -xf blender.tar.xz
        rm blender.tar.xz

        # Créer un lien symbolique
        sudo ln -sf ~/Applications/blender-${blender_version}-linux-x64/blender /usr/local/bin/blender

        BLENDER_PYTHON_PATH="~/Applications/blender-${blender_version}-linux-x64/${blender_major}/python/bin/python3.11"
        success "Blender téléchargé et installé"
        ;;

    3)
        info "Installation de Blender via APT..."
        sudo apt install blender -y

        # Trouver le chemin Python de Blender
        BLENDER_PYTHON_PATH=$(blender --background --python-expr "import sys; print(sys.executable)" 2>/dev/null | tail -1)
        success "Blender installé depuis le dépôt APT"
        ;;

    *)
        error "Choix invalide. Installation annulée."
        exit 1
        ;;
esac

# Vérifier l'installation de Blender
info "Vérification de l'installation de Blender..."
if command -v blender &> /dev/null; then
    BLENDER_VERSION=$(blender --version | head -n 1)
    success "Blender installé : $BLENDER_VERSION"
else
    error "Blender n'a pas été installé correctement"
    exit 1
fi

# Cloner le repository Blender MCP
info "Installation du plugin Blender MCP..."
cd ~

if [ -d "blender-mcp" ]; then
    warning "Le dossier blender-mcp existe déjà. Mise à jour..."
    cd blender-mcp
    git pull
else
    git clone https://github.com/ahujasid/blender-mcp.git
    cd blender-mcp
fi

success "Repository Blender MCP cloné"

# Installer les dépendances Python du plugin
info "Installation des dépendances Python du plugin MCP..."

# Essayer d'installer avec le Python de Blender
if [ -f "$BLENDER_PYTHON_PATH" ]; then
    $BLENDER_PYTHON_PATH -m pip install --upgrade pip 2>/dev/null || warning "Impossible de mettre à jour pip pour Blender Python"
    $BLENDER_PYTHON_PATH -m pip install -r requirements.txt 2>/dev/null || warning "Certaines dépendances n'ont pas pu être installées"
else
    warning "Python de Blender non trouvé. Vous devrez installer les dépendances manuellement."
fi

# Créer un script de lancement rapide
info "Création d'un script de lancement..."
cat > ~/launch_blender.sh << 'EOF'
#!/bin/bash
# Script de lancement de Blender avec vérification de l'affichage

if [ -z "$DISPLAY" ]; then
    echo "⚠️  DISPLAY n'est pas configuré"
    echo "Configuration automatique..."
    export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
    echo "DISPLAY défini sur : $DISPLAY"
fi

echo "🚀 Lancement de Blender..."
blender "$@"
EOF

chmod +x ~/launch_blender.sh
success "Script de lancement créé : ~/launch_blender.sh"

# Ajouter des alias utiles dans .bashrc si pas déjà présents
if ! grep -q "alias blender-mcp" ~/.bashrc; then
    info "Ajout d'alias utiles dans .bashrc..."
    cat >> ~/.bashrc << 'EOF'

# Alias Blender MCP
alias blender-mcp='~/launch_blender.sh'
alias blender-bg='blender --background'
EOF
    success "Alias ajoutés à .bashrc"
fi

# Résumé final
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              ✅ Installation terminée !                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
success "Blender est installé et prêt à l'emploi"
success "Plugin Blender MCP téléchargé dans ~/blender-mcp"
echo ""
echo "📝 Prochaines étapes :"
echo ""
echo "   1️⃣  Tester que Blender se lance :"
echo "      ${BLUE}blender${NC} ou ${BLUE}~/launch_blender.sh${NC}"
echo ""
echo "   2️⃣  Installer le plugin MCP dans Blender :"
echo "      - Ouvrez Blender"
echo "      - Allez dans Edit → Preferences → Add-ons"
echo "      - Cliquez sur 'Install...'"
echo "      - Sélectionnez le dossier : ~/blender-mcp/addon/"
echo "      - Activez le plugin 'Blender MCP'"
echo "      - Cliquez sur 'Start Server'"
echo ""
echo "   3️⃣  Tester l'intégration avec l'API FastAPI :"
echo "      ${BLUE}cd ~/MCP${NC}"
echo "      ${BLUE}python3 test_blender_mcp.py --simple${NC}"
echo ""
echo "📚 Pour plus d'informations, consultez :"
echo "   - BLENDER_WSL_INSTALL.md (guide détaillé)"
echo "   - BLENDER_MCP_GUIDE.md (utilisation de l'API)"
echo ""

# Test de l'affichage X11
echo "🧪 Test de l'affichage graphique..."
if command -v xclock &> /dev/null; then
    info "Vous pouvez tester l'affichage avec : xclock"
else
    info "Installation de x11-apps pour les tests..."
    sudo apt install x11-apps -y
    info "Testez l'affichage avec : xclock"
fi

echo ""
warning "Si Blender ne se lance pas :"
echo "   1. Vérifiez que WSLg est actif ou que VcXsrv est lancé"
echo "   2. Vérifiez DISPLAY : echo \$DISPLAY"
echo "   3. Consultez BLENDER_WSL_INSTALL.md section 'Dépannage'"
echo ""

success "Installation complète ! 🎉"
