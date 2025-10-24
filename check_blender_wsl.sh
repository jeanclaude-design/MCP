#!/bin/bash
# check_blender_wsl.sh
# Script de vérification de l'environnement Blender sur WSL

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     🔍 Vérification de l'environnement Blender WSL        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Fonction pour afficher le résultat
check_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
        return 0
    else
        echo -e "${RED}❌ $2${NC}"
        if [ -n "$3" ]; then
            echo -e "   ${YELLOW}→ $3${NC}"
        fi
        return 1
    fi
}

# Compteur de problèmes
ISSUES=0

echo "🐧 Vérification de l'environnement WSL..."
echo "─────────────────────────────────────────────────────────────"

# 1. Vérifier WSL
if grep -qi microsoft /proc/version; then
    check_status 0 "WSL détecté"
    WSL_VERSION=$(grep -i microsoft /proc/version | sed 's/.*microsoft/microsoft/')
    echo "   Version: $WSL_VERSION"
else
    check_status 1 "WSL non détecté" "Ce script est conçu pour WSL"
    ((ISSUES++))
fi

# 2. Vérifier DISPLAY
echo ""
echo "🖥️  Vérification de l'affichage graphique..."
echo "─────────────────────────────────────────────────────────────"

if [ -n "$DISPLAY" ]; then
    check_status 0 "DISPLAY est défini : $DISPLAY"
else
    check_status 1 "DISPLAY n'est pas défini" "Exportez DISPLAY ou utilisez WSLg"
    echo "   Pour corriger : export DISPLAY=\$(cat /etc/resolv.conf | grep nameserver | awk '{print \$2}'):0"
    ((ISSUES++))
fi

# 3. Vérifier les bibliothèques graphiques
echo ""
echo "📚 Vérification des bibliothèques graphiques..."
echo "─────────────────────────────────────────────────────────────"

REQUIRED_LIBS=(
    "libgl1-mesa-glx"
    "libglu1-mesa"
    "libxi6"
    "libxrender1"
)

for lib in "${REQUIRED_LIBS[@]}"; do
    if dpkg -l | grep -q "^ii.*$lib"; then
        check_status 0 "$lib installé"
    else
        check_status 1 "$lib non installé" "sudo apt install $lib"
        ((ISSUES++))
    fi
done

# 4. Vérifier Blender
echo ""
echo "🎨 Vérification de Blender..."
echo "─────────────────────────────────────────────────────────────"

if command -v blender &> /dev/null; then
    check_status 0 "Blender trouvé"
    BLENDER_VERSION=$(blender --version 2>/dev/null | head -n 1)
    echo "   ${BLUE}$BLENDER_VERSION${NC}"

    # Vérifier le chemin
    BLENDER_PATH=$(which blender)
    echo "   Chemin: $BLENDER_PATH"

    # Tester l'exécution en mode background
    if blender --background --python-expr "print('Test OK')" &>/dev/null; then
        check_status 0 "Blender s'exécute en mode background"
    else
        check_status 1 "Blender ne s'exécute pas correctement" "Vérifiez les dépendances"
        ((ISSUES++))
    fi
else
    check_status 1 "Blender non trouvé" "Installez Blender avec ./install_blender_wsl.sh"
    ((ISSUES++))
fi

# 5. Vérifier le plugin Blender MCP
echo ""
echo "🔌 Vérification du plugin Blender MCP..."
echo "─────────────────────────────────────────────────────────────"

if [ -d "$HOME/blender-mcp" ]; then
    check_status 0 "Repository Blender MCP trouvé"

    # Vérifier les fichiers importants
    if [ -d "$HOME/blender-mcp/addon" ]; then
        check_status 0 "Dossier addon présent"
    else
        check_status 1 "Dossier addon manquant" "Re-clonez le repository"
        ((ISSUES++))
    fi

    if [ -f "$HOME/blender-mcp/requirements.txt" ]; then
        check_status 0 "Fichier requirements.txt présent"
    else
        check_status 1 "Fichier requirements.txt manquant"
        ((ISSUES++))
    fi
else
    check_status 1 "Repository Blender MCP non trouvé" "Clonez avec : git clone https://github.com/ahujasid/blender-mcp.git"
    ((ISSUES++))
fi

# 6. Vérifier les outils de test
echo ""
echo "🧪 Vérification des outils de test..."
echo "─────────────────────────────────────────────────────────────"

if command -v xclock &> /dev/null; then
    check_status 0 "xclock installé (test X11)"
else
    check_status 1 "xclock non installé" "sudo apt install x11-apps"
fi

if command -v glxinfo &> /dev/null; then
    check_status 0 "glxinfo installé (test OpenGL)"

    # Tester OpenGL
    if glxinfo 2>/dev/null | grep -q "OpenGL version"; then
        GL_VERSION=$(glxinfo 2>/dev/null | grep "OpenGL version" | cut -d: -f2 | xargs)
        echo "   OpenGL: $GL_VERSION"
    fi
else
    check_status 1 "glxinfo non installé" "sudo apt install mesa-utils"
fi

# 7. Vérifier la connectivité réseau (pour MCP)
echo ""
echo "🌐 Vérification de la connectivité réseau..."
echo "─────────────────────────────────────────────────────────────"

if command -v curl &> /dev/null; then
    check_status 0 "curl installé"
else
    check_status 1 "curl non installé" "sudo apt install curl"
    ((ISSUES++))
fi

# Tester le port 3000 (serveur MCP)
if lsof -i :3000 &>/dev/null; then
    echo -e "${YELLOW}⚠️  Le port 3000 est déjà utilisé${NC}"
    echo "   Processus utilisant le port 3000 :"
    lsof -i :3000 | grep -v COMMAND
else
    check_status 0 "Port 3000 disponible"
fi

# 8. Vérifier Python et pip
echo ""
echo "🐍 Vérification de Python..."
echo "─────────────────────────────────────────────────────────────"

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    check_status 0 "Python installé : $PYTHON_VERSION"
else
    check_status 1 "Python non installé" "sudo apt install python3"
    ((ISSUES++))
fi

if command -v pip3 &> /dev/null; then
    check_status 0 "pip installé"
else
    check_status 1 "pip non installé" "sudo apt install python3-pip"
    ((ISSUES++))
fi

# 9. Vérifier le projet MCP FastAPI
echo ""
echo "📦 Vérification du projet MCP FastAPI..."
echo "─────────────────────────────────────────────────────────────"

if [ -f "$HOME/MCP/test_blender_mcp.py" ]; then
    check_status 0 "Script de test Blender MCP trouvé"
else
    check_status 1 "Script de test non trouvé" "Vérifiez le dossier ~/MCP"
fi

if [ -f "$HOME/MCP/agents/blender_agent.py" ]; then
    check_status 0 "Agent Blender trouvé"
else
    check_status 1 "Agent Blender non trouvé"
fi

# Résumé final
echo ""
echo "═══════════════════════════════════════════════════════════════"

if [ $ISSUES -eq 0 ]; then
    echo -e "${GREEN}✅ Aucun problème détecté ! Tout est prêt.${NC}"
    echo ""
    echo "🚀 Prochaines étapes :"
    echo "   1. Lancez Blender : blender"
    echo "   2. Installez le plugin MCP dans Blender"
    echo "   3. Démarrez le serveur MCP dans Blender"
    echo "   4. Testez : python3 ~/MCP/test_blender_mcp.py --simple"
else
    echo -e "${RED}⚠️  $ISSUES problème(s) détecté(s)${NC}"
    echo ""
    echo "📝 Actions recommandées :"
    echo "   1. Corrigez les problèmes listés ci-dessus"
    echo "   2. Relancez ce script pour vérifier"
    echo "   3. Consultez BLENDER_WSL_INSTALL.md pour plus d'aide"
fi

echo "═══════════════════════════════════════════════════════════════"
echo ""

# Test optionnel de l'affichage
echo -e "${BLUE}💡 Astuce : Testez l'affichage graphique avec :${NC}"
echo "   xclock"
echo "   (Si une horloge apparaît, X11 fonctionne !)"
echo ""

exit $ISSUES
