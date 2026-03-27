.PHONY: help setup build dev release clean install install-deb test

help:
	@echo "🛠️  Menu-Logoff Build System (uv + PyInstaller)"
	@echo ""
	@echo "Setup (primeira vez apenas):"
	@echo "  make setup       # Instalar dependências do sistema (requer sudo)"
	@echo "  make deps        # Instalar dependências Python com uv"
	@echo ""
	@echo "Build:"
	@echo "  make dev         # Build rápido incremental (~15s)"
	@echo "  make release     # Build otimizado + DEB (~30-60s)"
	@echo "  make clean       # Limpar arquivos de build"
	@echo ""
	@echo "Instalação:"
	@echo "  make install-deb # Instalar pacote DEB no sistema"
	@echo ""
	@echo "Executar:"
	@echo "  make run         # Executar app diretamente (modo dev)"
	@echo ""

setup:
	@echo "🔧 Instalando dependências do sistema..."
	@bash scripts/setup-system.sh

deps:
	@echo "📦 Instalando dependências Python com uv..."
	uv sync

dev:
	@echo "⚡ Build rápido (dev)..."
	@bash scripts/build.sh dev

release:
	@echo "📦 Build release + DEB..."
	@bash scripts/build.sh release

clean:
	@echo "🧹 Limpando arquivos de build..."
	rm -rf .build/ *.spec *.pyc __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

clean-all: clean
	@echo "🔥 Limpando tudo (VENV e RELEASES)..."
	rm -rf .venv venv releases/*

install-deb:
	@echo "📦 Instalando pacote DEB..."
	sudo dpkg -i releases/menu-logoff_1.0.0_amd64.deb

run:
	@echo "▶️  Executando app (modo dev)..."
	uv run python main.py

test:
	@echo "🧪 Testando app..."
	uv run python main.py &
	sleep 2
	pkill -f "main.py" || true
	@echo "✅ Teste concluído!"
