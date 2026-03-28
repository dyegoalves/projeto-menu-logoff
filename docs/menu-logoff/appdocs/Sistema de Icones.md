---
tags: [ui, icones, recursos, visual]
relacionado: [[Acoes de Sessao]]
status: ativo
tipo: feature
versao: 1.0.0
---

# Sistema de Ícones

Carrega e exibe ícones PNG para cada botão de ação na interface.

## Como funciona

### Estrutura de diretórios

```
app/
└── assets/
    └── icons/
        ├── icon-app.png      # Ícone do aplicativo (janela)
        ├── shutdown.png      # Desligar
        ├── restart.png       # Reiniciar
        ├── logout.png        # Sair/Logout
        └── suspend.png       # Suspender
```

### Carregamento

A função `_load_icon()`:

1. Constrói path completo: `ICONS_DIR + filename`
2. Usa `GdkPixbuf.Pixbuf.new_from_file_at_scale()` para carregar com resize
3. Cria `Gtk.Image` a partir do pixbuf
4. Fallback: retorna `Gtk.Label(label="?")` se falhar

### Tamanho

Ícones são carregados em **48x48px** (parâmetro `size=48`).

## Arquivos principais

- `app/main.py` — Método `_load_icon()` (linhas 265-272)
- `app/main.py` — Variável `ICONS_DIR` (linha 21)
- `app/assets/icons/` — Diretório com 5 arquivos PNG

## Integrações

- [[Ações de Sessão]] — Cada ação referencia um arquivo de ícone
- [[Interface de Sessão]] — Botões contêm ícones carregados por este sistema
- [[Aplicação GTK Principal]] — Define ícone da janela via `icon-app.png`
- [[Empacotamento Debian]] — Copia ícones para `/usr/share/pixmaps/`

## Configuração

**Path resolution:**
```python
ICONS_DIR = resource_path("assets/icons")
```

A função `resource_path()` funciona tanto em modo dev quanto PyInstaller:
- Dev: Usa `__file__` do script
- PyInstaller: Usa `sys._MEIPASS`

## Observações importantes

- **Escala**: `new_from_file_at_scale()` mantém aspect ratio (último parâmetro `True`)
- **Fallback**: Label "?" previne crash se ícone faltar
- **PyInstaller**: Ícones devem ser incluídos via `datas` no spec file
- **Formato**: PNG com alpha channel para transparência
- **Consistência**: Todos ícones de ação devem ter estilo visual coerente
