#!/bin/bash
# Setup das dependências do sistema para desenvolvimento
# Execute com sudo ou como root

set -e

echo "🛠️  Instalando dependências do sistema para compilar pycairo e pygobject..."

sudo apt update
sudo apt install -y \
    pkg-config \
    libcairo2-dev \
    libgirepository-2.0-dev \
    gir1.2-gtk-3.0 \
    libgtk-3-dev \
    python3-dev \
    python3-pip \
    upx \
    patchelf

echo ""
echo "✅ Dependências do sistema instaladas!"
echo ""
echo "📦 Agora instale as dependências Python com uv:"
echo "   $ uv sync"
echo ""
echo "🚀 E faça o build:"
echo "   $ ./build.sh dev      # Build rápido (desenvolvimento)"
echo "   $ ./build.sh release  # Build otimizado + DEB"
