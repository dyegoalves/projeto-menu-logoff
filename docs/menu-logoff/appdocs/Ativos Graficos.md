---
tags: [assets, recursos, icones, imagens]
relacionado: [[Sistema de Icones]]
status: ativo
tipo: recurso
versao: 1.0.0
---

# Ativos Gráficos

Recursos visuais estáticos (ícones PNG e versão) usados pela aplicação.

## Como funciona

### Ícones

Localizados em `app/assets/icons/`:

| Arquivo | Uso | Tamanho sugerido |
|---------|-----|------------------|
| `icon-app.png` | Ícone da janela e do app | 512x512 (escalável) |
| `shutdown.png` | Botão Desligar | 48x48 |
| `restart.png` | Botão Reiniciar | 48x48 |
| `logout.png` | Botão Sair | 48x48 |
| `suspend.png` | Botão Suspenso | 48x48 |

### Versão

Arquivo `app/version.txt` contém string de versão (ex: `1.0.1`).

Lido na inicialização:
```python
with open(resource_path("version.txt"), "r") as f:
    version = f.read().strip()
```

## Arquivos principais

- `app/assets/icons/icon-app.png`
- `app/assets/icons/shutdown.png`
- `app/assets/icons/restart.png`
- `app/assets/icons/logout.png`
- `app/assets/icons/suspend.png`
- `app/version.txt`

## Integrações

- [[Sistema de Ícones]] — Carrega ícones do diretório
- [[Interface de Sessão]] — Exibe versão no footer
- [[Aplicação GTK Principal]] — Usa `icon-app.png` como ícone da janela
- [[Build System]] — Inclui assets no PyInstaller via `datas`
- [[Empacotamento Debian]] — Copia `icon-app.png` para `/usr/share/pixmaps/`

## Configuração

**PyInstaller spec:**
```python
datas = [
    ('../app/assets/icons', 'assets/icons'),
    ('../app/version.txt', '.')
]
```

**Makefile:**
```bash
# Limpa versão no clean
rm -rf app/version.txt
```

## Observações importantes

- **Formato PNG**: Alpha channel necessário para transparência
- **Consistência visual**: Ícones devem seguir mesmo estilo (preenchimento, bordas, cores)
- **Resource path**: `resource_path()` resolve paths para dev e PyInstaller
- **Versão hardcoded no fallback**: Se `version.txt` falhar, usa `"1.0.1"`
- **Build limpo**: `make clean` remove `version.txt` — regenerado no build
- **Debian**: Ícone do app é instalado em `/usr/share/pixmaps/menu-logoff.png`
