---
tags: [ui, gtk, janela, interface]
relacionado: [[Aplicação GTK Principal]]
status: ativo
tipo: modulo
versao: 1.0.0
---

# Interface de Sessão

Janela principal do menu de sessão com layout, botões de ação e elementos visuais.

## Como funciona

A classe `SessionMenu` estende `Gtk.Window` e implementa:

### Estrutura do Layout

```
┌─────────────────────────────────┐
│  [ESPAÇO]  USUÁRIO  [✕ FECHAR]  │ ← Header
├─────────────────────────────────┤
│                                 │
│   [⚡]    [🔄]    [🚪]    [💤]   │ ← Botões de ação
│ Desligar Reiniciar Sair  Suspenso
│                                 │
├─────────────────────────────────┤
│  Descrição contextual da ação   │ ← Footer
│  v1.0.1                         │ ← Versão
└─────────────────────────────────┘
```

### Componentes

1. **Header**: Nome do usuário (centralizado) + botão fechar (direita)
2. **Corpo**: 4 botões horizontais com ícone + label
3. **Footer**: Separador + descrição + versão

### Comportamentos

- **Foco**: Navegação por teclado (setas, Tab, Enter, Escape)
- **Mouse**: Hover atualiza descrição e foco
- **Transparência**: Janela arredondada com alpha channel via Cairo

## Arquivos principais

- `app/main.py` — Classe `SessionMenu` (linhas 56-350)
- `app/assets/icons/` — Ícones dos botões de ação

## Integrações

- [[Aplicação GTK Principal]] — Instanciada e gerenciada por `SessionApp`
- [[Gerenciador de Tema]] — Detecta tema escuro/claro na inicialização
- [[Estilização CSS]] — Aplica estilos customizados via `GtkCssProvider`
- [[Renderização Cairo]] — Desenha fundo arredondado no evento `draw`
- [[Ações de Sessão]] — Executa comandos ao clicar nos botões
- [[Sistema de Ícones]] — Carrega ícones para cada botão
- [[Descrições Contextuais]] — Atualiza label de descrição por foco/hover

## Configuração

**Propriedades da janela:**
```python
set_decorated(False)        # Sem bordas da janela
set_resizable(False)         # Tamanho fixo
set_keep_above(True)         # Sempre no topo
set_modal(True)              # Modal
set_position(CENTER)         # Centralizada
```

**Margens do layout:**
- Topo: 14px
- Base: 18px
- Laterais: 16px

## Observações importantes

- **Compositing**: Requer tela com compositor ativo para transparência (`screen.is_composited()`)
- **Visual RGBA**: Usa `get_rgba_visual()` para alpha blending correto
- **App paintable**: `set_app_paintable(True)` permite desenho customizado no `draw`
- **Focus tracking**: Descrições atualizam via eventos `focus-in-event`, `enter-notify-event`, `leave-notify-event`
- **Teclado**: 
  - `Escape` → fecha menu
  - `Enter/Space` → ativa botão focado
  - `Setas/Tab` → navega entre botões
