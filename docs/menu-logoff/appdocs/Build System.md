---
tags: [infra, build, pyinstaller, compilacao]
relacionado: [[Empacotamento Debian]]
status: ativo
tipo: infra
versao: 1.0.0
---

# Build System

Scripts e configuração para compilar aplicação Python em executável standalone via PyInstaller.

## Como funciona

### Script `build.sh`

Suporta 4 modos via argumento:

| Comando | Descrição |
|---------|-----------|
| `setup` | Instala dependências do sistema (apt) |
| `dev` | Build rápido incremental |
| `release` | Build limpo + otimizado + gera .deb |
| `deb` | Apenas gera pacote Debian (sem recompilar) |

### Fluxo Release

```
1. Limpa builds anteriores (.build/dist, .build/work)
2. Roda PyInstaller com --clean
3. Gera executável em .build/dist/main
4. Cria estrutura do pacote Debian
5. Copia executável + desktop entry + ícone
6. Build do .deb via dpkg-deb
```

### Especificação `main.spec`

Configuração do PyInstaller:

```python
datas = [
    ('../app/assets/icons', 'assets/icons'),
    ('../app/version.txt', '.')
]
hiddenimports = collect_all('gi')  # GTK e dependências
console = False  # Sem terminal
upx = False  # Desabilitado para builds rápidos
```

## Arquivos principais

- `scripts/build.sh` — Script bash mestre de build
- `scripts/main.spec` — Configuração PyInstaller
- `Makefile` — Comandos make (dev, installbuild, run, clean)

## Integrações

- [[Empacotamento Debian]] — Gera pacote .deb no modo release
- [[Ativos Gráficos]] — Inclui ícones e versão no build
- [[Configuração do Projeto]] — Lê versão do `pyproject.toml`

## Configuração

**Dependências do sistema (setup):**
```bash
pkg-config libcairo2-dev libgirepository-2.0-dev 
gir1.2-gtk-3.0 libgtk-3-dev python3-dev python3-pip 
upx patchelf
```

**Makefile commands:**
```bash
make dev          # Build rápido
make installbuild # Setup + build + install
make run          # Roda sem build (dev)
make clean        # Limpa tudo
```

## Observações importantes

- **UV**: Usa `uv run python` se `.venv` existe
- **Incremental**: Modo `dev` não limpa build anterior (mais rápido)
- **UPX**: Desabilitado por padrão (`upx=False`), pode habilitar no spec
- **Hidden imports**: `collect_all('gi')` captura GTK + dependências C
- **Paths relativos**: Spec file usa `../app/` pois roda de `scripts/`
- **Output**: Executável em `.build/dist/main`
- **Clean agressivo**: `make clean` remove `.build/`, `.venv/`, `releases/*`
