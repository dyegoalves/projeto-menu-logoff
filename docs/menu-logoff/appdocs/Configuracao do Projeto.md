---
tags: [config, metadata, projeto, dependencias]
relacionado: [[Build System]]
status: ativo
tipo: config
versao: 1.0.0
---

# Configuração do Projeto

Metadados, dependências e configurações gerais do projeto.

## Como funciona

### `pyproject.toml`

Arquivo principal de configuração do projeto Python moderno (PEP 621).

**Metadados:**
```toml
name = "menu-logoff"
version = "1.0.1"
description = "Custom power menu for Zorin OS with macOS-inspired aesthetics"
requires-python = ">=3.10"
license = "MIT"
authors = [{name = "Dyego Alves", email = "dyegoalves@example.com"}]
```

**Classificadores:**
- Development Status :: 4 - Beta
- Environment :: X11 Applications :: GTK
- Operating System :: POSIX :: Linux
- Programming Language :: Python :: 3

**Dependências:**
```toml
dependencies = [
    "pygobject>=3.46.0",    # GTK bindings
    "pyinstaller>=6.0.0",   # Build tool
]
```

**Configuração PyInstaller:**
```toml
[tool.pyinstaller]
entrypoint = "app/main.py"
name = "menu-logoff"
onefile = true
console = false
datas = ["app/assets/icons/*.png:assets/icons"]
hiddenimports = ["gi", "gi.repository.Gtk", ...]
```

### `.gitignore`

Ignora arquivos de build e ambiente:
```
dist
build
venv
__pycache__
.build
*.pyc
```

### `Makefile`

Comandos disponíveis:
- `make dev` — Build rápido
- `make installbuild` — Setup + build + install
- `make run` — Executa em modo dev
- `make clean` — Limpa tudo

## Arquivos principais

- `pyproject.toml` — Configuração principal
- `Makefile` — Automação de comandos
- `.gitignore` — Padrões de exclusão Git
- `ABBBCLAUDE.md` — Documentação adicional (se existir)

## Integrações

- [[Build System]] — Lê versão e config PyInstaller do `pyproject.toml`
- [[Empacotamento Debian]] — Usa versão e metadados do `pyproject.toml`
- [[Ativos Gráficos]] — Versão lida de `app/version.txt` (gerada no build)

## Configuração

**Python mínimo:** 3.10

**Keywords:**
```
gtk, menu, power-management, zorin-os
```

**Build system:**
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel", "pyinstaller>=6.0"]
build-backend = "setuptools.build_meta"
```

## Observações importantes

- **UV**: Projeto usa `uv` como package manager (`.venv/`, `uv.lock`)
- **Package = false**: `[tool.uv]` indica que não é pacote publicável
- **Versão única**: `pyproject.toml` é fonte da verdade, `version.txt` é derivado
- **Hidden imports**: Lista completa de módulos GTK no PyInstaller
- **Console = false**: Aplicação GUI sem terminal
- **Onefile**: Empacota tudo em único executável
- **Licença MIT**: Código aberto, uso livre
