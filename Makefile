.PHONY: help dev installbuild run clean

help:
	@echo "🛠️  Menu-Logoff (Limpeza Total)"
	@echo ""
	@echo "  make dev          # Build rápido para testes"
	@echo "  make installbuild # CONFIGURA, CONSTROI E INSTALA (Tudo em um!)"
	@echo "  make run          # Roda o app direto (modo dev)"
	@echo "  make clean        # Limpa tudo"
	@echo ""

dev:
	@echo "⚡ Build rápido..."
	@bash scripts/build.sh dev

installbuild:
	@echo "🛠️  Preparando ambiente e dependências..."
	@bash scripts/build.sh setup
	@echo "🚀 Gerando o binário..."
	@bash scripts/build.sh release
	@echo "📦 Instalando no sistema..."
	@sudo dpkg -i releases/menu-logoff_$(shell grep -m 1 'version =' pyproject.toml | cut -d '"' -f 2)_amd64.deb
	@echo "🎉 Tudo pronto e atualizado!"

run:
	@echo "▶️  Executando app..."
	@uv run python app/main.py

clean:
	@echo "🧹 Limpando tudo..."
	@rm -rf .build/ *.spec *.pyc __pycache__ .venv venv releases/* app/version.txt
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
