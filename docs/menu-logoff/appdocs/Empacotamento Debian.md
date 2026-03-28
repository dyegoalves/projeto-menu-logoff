---
tags: [infra, debian, pacote, instalacao]
relacionado: [[Build System]]
status: ativo
tipo: infra
versao: 1.0.0
---

# Empacotamento Debian

Gera pacote `.deb` para instalação no Zorin OS/Ubuntu.

## Como funciona

### Estrutura do pacote

```
menu-logoff_1.0.1_amd64.deb
├── DEBIAN/
│   └── control          # Metadados do pacote
├── usr/
│   ├── local/bin/
│   │   └── menu-logoff  # Executável
│   ├── share/
│   │   ├── applications/
│   │   │   └── menu-logoff.desktop  # Entrada no menu
│   │   └── pixmaps/
│   │       └── menu-logoff.png      # Ícone do app
```

### Arquivo `control`

```
Package: menu-logoff
Version: 1.0.1
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Dyego Alves
Description: Custom power menu for Zorin OS with macOS-inspired aesthetics.
```

### Desktop Entry

```ini
[Desktop Entry]
Name=Menu Logoff
Comment=Custom logoff menu for Zorin
Exec=/usr/local/bin/menu-logoff
Icon=menu-logoff
Terminal=false
Type=Application
Categories=System;Utility;
Keywords=shutdown;reboot;logout;suspend;
StartupWMClass=com.dyego.menu-logoff
```

### Processo de build

Função `create_deb()` no `build.sh`:

1. Limpa diretório temporário `.build/deb-temp`
2. Cria estrutura de diretórios
3. Gera arquivo `control` dinamicamente
4. Gera `desktop entry` dinamicamente
5. Copia executável de `.build/dist/main`
6. Copia ícone de `app/assets/icons/icon-app.png`
7. Build via `dpkg-deb --build`
8. Limpa diretório temporário

## Arquivos principais

- `scripts/build.sh` — Função `create_deb()` (linhas 55-85)
- `app/session-menu.desktop` — Template de desktop entry (não usado diretamente)

## Integrações

- [[Build System]] — Chamado no modo `release` após PyInstaller
- [[Ativos Gráficos]] — Usa ícone `icon-app.png` no pacote
- [[Aplicação GTK Principal]] — Desktop entry referencia `application_id`

## Configuração

**Nome do pacote:**
```bash
PKG_NAME="menu-logoff"
DEB_NAME="releases/${PKG_NAME}_${VERSION}_amd64.deb"
```

**Instalação:**
```bash
sudo dpkg -i releases/menu-logoff_1.0.1_amd64.deb
```

**Remoção:**
```bash
sudo apt remove menu-logoff
```

## Observações importantes

- **Prefixo**: Instalado em `/usr/local/bin` (não `/usr/bin`)
- **Ícone**: Copiado para `/usr/share/pixmaps/` (legado, mas funcional)
- **StartupWMClass**: Crucial para ícone correto no dock/launcher
- **Keywords**: Melhora busca no menu de aplicativos
- **Seção `utils`**: Categoria padrão para utilitários
- **Arch amd64**: Apenas x86_64 (não suporta ARM/32-bit)
- **Makefile**: `make installbuild` automatiza build + install
