---
tags: [ui, texto, contexto, descricao]
relacionado: [[Acoes de Sessao]]
status: ativo
tipo: feature
versao: 1.0.0
---

# Descrições Contextuais

Exibe texto explicativo dinâmico baseado na ação focada ou em hover.

## Como funciona

### Mapeamento de descrições

Dicionário `DESCRIPTIONS` associa cada classe CSS à sua descrição:

```python
DESCRIPTIONS = {
    "shutdown": "Encerra todos os apps e desliga o computador.",
    "restart":  "Fecha tudo e reinicia o sistema do zero.",
    "logout":   "Encerra sua sessão e volta à tela de login.",
    "suspend":  "Salva o estado na memória e entra em modo de espera.",
}
```

### Atualização

Método `_update_desc(idx)`:

1. Recebe índice do botão (0-3)
2. Busca classe CSS correspondente (`self.css_classes[idx]`)
3. Obtém descrição do dicionário
4. Atualiza `self.desc_label.set_text(text)`

### Gatilhos de atualização

| Evento | Método | Comportamento |
|--------|--------|---------------|
| Foco no botão | `on_btn_focus()` | Atualiza descrição |
| Mouse enter | `on_btn_enter()` | Atualiza descrição + grab focus |
| Mouse leave (botão) | `on_btn_leave()` | Limpa descrição |
| Mouse leave (hbox) | `on_hbox_leave()` | Limpa descrição |

## Arquivos principais

- `app/main.py` — Dicionário `DESCRIPTIONS` (linhas 63-68)
- `app/main.py` — Métodos de atualização (linhas 245-263)

## Integrações

- [[Ações de Sessão]] — Usa mesmas chaves CSS (`shutdown`, `restart`, etc.)
- [[Interface de Sessão]] — `desc_label` é atualizado dinamicamente

## Configuração

**Sem configuração** — textos hardcoded em `DESCRIPTIONS`.

**Estilo do label:**
```css
#DescLabel {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
    padding-top: 10px;
    margin: 16px 0 6px 0;
}
```

## Observações importantes

- **Clear on leave**: Descrição é limpa quando mouse sai dos botões
- **Foco vs Hover**: Ambos atualizam descrição, mas hover também grab focus
- **Default state**: Botão "Desligar" (índice 0) já vem focado com descrição visível
- **Line wrap**: Label tem `set_line_wrap(True)` para textos longos
- **Centralizado**: `set_justify(Gtk.Justification.CENTER)` mantém texto centralizado
- **Acessibilidade**: Descrições fornecem contexto adicional para usuários
