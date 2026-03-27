#!/bin/bash
# Script Mestre de Build e Gerenciamento - Menu Logoff
# Uso: ./build.sh [setup|dev|release|deb]

set -e

# Configurações
PKG_NAME="menu-logoff"
VERSION=$(grep -m 1 'version =' pyproject.toml | cut -d '"' -f 2)
echo "$VERSION" > app/version.txt
DEB_NAME="releases/${PKG_NAME}_${VERSION}_amd64.deb"
SPEC="scripts/main.spec"
DIST_DIR=".build/dist"
BUILD_DIR=".build/work"
DEB_BUILD_DIR=".build/deb-temp"

# --- Funções ---

setup_system() {
    echo "🛠️  Instalando dependências do sistema..."
    sudo apt update
    sudo apt install -y pkg-config libcairo2-dev libgirepository-2.0-dev gir1.2-gtk-3.0 libgtk-3-dev python3-dev python3-pip upx patchelf
    echo "✅ Sistema pronto!"
}

run_pyinstaller() {
    local MODE=$1
    echo "🚀 Build mode: $MODE"
    
    # Detectar ambiente Python
    if [ -d ".venv" ]; then
        PYTHON_CMD="uv run python"
    elif [ -d "venv" ]; then
        source venv/bin/activate
        PYTHON_CMD="python"
    else
        uv sync --quiet
        PYTHON_CMD="uv run python"
    fi

    if [ "$MODE" == "release" ]; then
        echo "🧹 Limpando builds anteriores..."
        rm -rf $DIST_DIR $BUILD_DIR
        echo "⚙️  Construindo release otimizada..."
        $PYTHON_CMD -m PyInstaller --clean $SPEC --distpath $DIST_DIR --workpath $BUILD_DIR --noconfirm 2>&1 | tail -10
    else
        echo "⚡ Construindo dev incremental..."
        $PYTHON_CMD -m PyInstaller $SPEC --distpath $DIST_DIR --workpath $BUILD_DIR --noconfirm 2>&1 | tail -10
    fi
}

create_deb() {
    echo "📦 Gerando pacote Debian..."
    if [ ! -f "$DIST_DIR/main" ]; then
        echo "❌ Erro: Executável não encontrado em $DIST_DIR/main. Rode o build primeiro."
        exit 1
    fi

    rm -rf $DEB_BUILD_DIR
    mkdir -p $DEB_BUILD_DIR/usr/local/bin $DEB_BUILD_DIR/usr/share/applications $DEB_BUILD_DIR/usr/share/pixmaps $DEB_BUILD_DIR/DEBIAN
    
    # Control
    cat <<EOF > $DEB_BUILD_DIR/DEBIAN/control
Package: $PKG_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Dyego Alves
Description: Custom power menu for Zorin OS with macOS-inspired aesthetics.
EOF

    # Desktop entry
    cat <<EOF > $DEB_BUILD_DIR/usr/share/applications/menu-logoff.desktop
[Desktop Entry]
Name=Menu Logoff
Comment=Custom logoff menu for Zorin
Exec=/usr/local/bin/menu-logoff
Icon=$PKG_NAME
Terminal=false
Type=Application
Categories=System;Utility;
Keywords=shutdown;reboot;logout;suspend;
StartupWMClass=com.dyego.menu-logoff
EOF

    # Copy files
    cp $DIST_DIR/main $DEB_BUILD_DIR/usr/local/bin/menu-logoff
    chmod +x $DEB_BUILD_DIR/usr/local/bin/menu-logoff
    cp app/assets/icons/icon-app.png $DEB_BUILD_DIR/usr/share/pixmaps/$PKG_NAME.png
    
    # Build package
    mkdir -p releases
    dpkg-deb --build $DEB_BUILD_DIR $DEB_NAME > /dev/null
    rm -rf $DEB_BUILD_DIR
    
    echo "✅ SUCESSO! Pacote criado: $DEB_NAME"
}

# --- Fluxo Principal ---

case "$1" in
    setup)
        setup_system
        ;;
    dev)
        run_pyinstaller "dev"
        ;;
    release)
        run_pyinstaller "release"
        create_deb
        ;;
    deb)
        create_deb
        ;;
    *)
        echo "Uso: $0 {setup|dev|release|deb}"
        exit 1
        ;;
esac
