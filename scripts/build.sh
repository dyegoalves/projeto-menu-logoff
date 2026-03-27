#!/bin/bash

# Build script inteligente: usa venv existente ou uv
# Uso: ./build.sh [dev|release]

set -e

MODE="${1:-dev}"
SPEC="scripts/main.spec"
DIST_DIR=".build/dist"
BUILD_DIR=".build/work"

echo "🚀 Build mode: $MODE"
echo ""

# Detectar se existe venv ou uv
if [ -d "venv" ]; then
    echo "🔧 Usando venv existente..."
    source venv/bin/activate
    PYTHON_CMD="python"
elif command -v uv &> /dev/null; then
    echo "🔧 Usando uv (criando .venv)..."
    uv sync --quiet
    PYTHON_CMD="uv run python"
else
    echo "❌ Nenhum venv ou uv encontrado. Execute:"
    echo "   python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    echo "   OU instale o uv: https://docs.astral.sh/uv/"
    exit 1
fi

# Limpar apenas se for release
if [ "$MODE" = "release" ]; then
    echo "🧹 Limpando builds anteriores..."
    rm -rf $DIST_DIR $BUILD_DIR
    echo ""

    # Build com compressão UPX (se disponível)
    echo "⚙️  Construindo release..."
    if command -v upx &> /dev/null; then
        $PYTHON_CMD -m PyInstaller --clean $SPEC --distpath $DIST_DIR --workpath $BUILD_DIR --upx-dir=/usr/bin 2>&1 | tail -20
    else
        $PYTHON_CMD -m PyInstaller --clean $SPEC --distpath $DIST_DIR --workpath $BUILD_DIR 2>&1 | tail -20
    fi
else
    # Build incremental (SEM --clean) - MUITO mais rápido!
    echo "⚡ Construindo dev (incremental)..."
    if [ ! -f "$DIST_DIR/main" ]; then
        $PYTHON_CMD -m PyInstaller --clean $SPEC --distpath $DIST_DIR --workpath $BUILD_DIR 2>&1 | tail -20
    else
        $PYTHON_CMD -m PyInstaller $SPEC --distpath $DIST_DIR --workpath $BUILD_DIR 2>&1 | tail -20
    fi
fi

echo ""
echo "✅ Build concluído!"
if [ -f "$DIST_DIR/main" ]; then
    echo "📦 Executável: $DIST_DIR/main ($(du -h $DIST_DIR/main | cut -f1))"
else
    echo "❌ Executável não encontrado em $DIST_DIR/main"
    exit 1
fi

# Gerar DEB automaticamente se for release
if [ "$MODE" = "release" ]; then
    echo ""
    echo "📦 Gerando pacote DEB..."
    bash scripts/build-deb.sh
    echo ""
    echo "🎉 Pacote DEB pronto!"
fi
