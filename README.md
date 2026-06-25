# Menu Logoff

Menu de sessão personalizado para Zorin OS com estética inspirada no macOS. Interface elegante para desligar, reiniciar, fazer logout ou suspender o sistema.

![versão](https://img.shields.io/badge/versão-1.0.5-blue)
![python](https://img.shields.io/badge/python-3.10%2B-green)
![licença](https://img.shields.io/badge/licença-MIT-yellow)

## Funcionalidades

- **Desligar** — Encerra todos os apps e desliga o computador
- **Reiniciar** — Fecha tudo e reinicia o sistema
- **Sair** — Encerra a sessão e volta à tela de login
- **Suspender** — Salva o estado na memória e entra em modo de espera
- **Tema dinâmico** — Detecta automaticamente tema claro/escuro do GNOME
- **Navegação completa por teclado** — Setas, Tab, Enter e Escape
- **Bordas arredondadas** — Renderização Cairo com cantos suaves
- **Pacote DEB** — Instalação nativa em Debian/Ubuntu/Zorin

## Tecnologias

- **Python 3.10+**
- **GTK3** (PyGObject)
- **Cairo** (renderização gráfica)
- **PyInstaller** (build standalone)
- **systemd / GNOME Session** (integração com sistema)

## Instalação

### Pacote DEB

```bash
sudo dpkg -i releases/menu-logoff_1.0.5_amd64.deb
```

### Build manual

```bash
# Instalar dependências do sistema
make setup

# Build e instalação completa
make installbuild
```

## Uso

### Via terminal

```bash
menu-logoff
```

### Via atalho

Pressione `Super` e busque por "Menu Logoff" nos aplicativos.

### Atalhos de teclado

| Tecla | Ação |
|-------|------|
| `←` `→` `↑` `↓` `Tab` | Navegar entre botões |
| `Enter` `Espaço` | Confirmar ação |
| `Escape` | Fechar menu |

## Desenvolvimento

```bash
# Clonar repositório
git clone <repo-url>
cd projeto-menu-logoff

# Criar ambiente virtual
uv sync

# Executar em modo dev
make run

# Build rápido para testes
make dev

# Limpar builds
make clean
```

## Estrutura do projeto

```
.
├── app/
│   ├── assets/icons/     # Ícones PNG (48x48)
│   ├── main.py           # Código-fonte principal
│   └── version.txt       # Versão atual
├── scripts/
│   ├── build.sh          # Script mestre de build
│   └── main.spec         # Especificação PyInstaller
├── releases/             # Pacotes DEB gerados
├── Makefile              # Comandos de build
└── pyproject.toml        # Configuração do projeto
```

## Comandos Makefile

| Comando | Descrição |
|---------|-----------|
| `make dev` | Build rápido para testes |
| `make installbuild` | Configura, constrói e instala (tudo em um) |
| `make run` | Executa o app direto (modo dev) |
| `make clean` | Limpa builds e caches |

## Requisitos do sistema

- Zorin OS 16+ / Ubuntu 20.04+ / Debian 11+
- GNOME ou GNOME-based desktop
- systemd
- Compositor gráfico ativo (X11 com composição ou Wayland)

## Licença

MIT
