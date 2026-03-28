---
tags: [ui, css, estilo, visual]
relacionado: [[Interface de Sessão]]
status: ativo
tipo: feature
versao: 1.0.0
---

# Estilização CSS

CSS dinâmico que define aparência dos componentes da interface.

## Como funciona

A função `_build_css()` gera CSS como bytes para carregar via `GtkCssProvider`.

### Estrutura do CSS

```css
/* Reset e fonte do sistema */
* { font-family: "{gtk-font-name}", sans-serif; }

/* Janela principal */
#SessionWindow { background-color: transparent; }

/* Label do usuário */
#UserLabel { 
    font-size: 11px; 
    font-weight: 800; 
    color: rgba(255, 255, 255, 0.5); 
    letter-spacing: 1.2px; 
}

/* Botão fechar (X) */
#CloseButton { 
    background: rgba(255, 255, 255, 0.08);
    border-radius: 50%;
    /* ... hover state com vermelho #e0443e */
}

/* Separadores */
#HeaderSeparator, #FooterSeparator { 
    background-color: rgba(255, 255, 255, 0.08);
    min-height: 1px;
}

/* Botões de sessão */
.session-button { 
    background: transparent;
    border-radius: 20px;
    transition: all 200ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.session-button:hover { 
    background-color: rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Labels de texto */
.btn-label { /* texto dos botões */ }
#DescLabel { /* descrição contextual */ }
#VersionLabel { /* versão no footer */ }
```

### Cores e Estilo

- **Fundo**: `rgba(25, 25, 25, 0.85)` — vidro escuro premium
- **Borda**: `rgba(255, 255, 255, 0.12)` — borda sutil branca
- **Hover**: `rgba(255, 255, 255, 0.1)` — brilho ao passar mouse
- **Fechamento**: `#e0443e` — vermelho macOS no hover
- **Texto**: Vários alphas de branco (0.15 a 0.95)

## Arquivos principais

- `app/main.py` — Função `_build_css()` (linhas 42-106)

## Integrações

- [[Interface de Sessão]] — Aplica CSS via `GtkCssProvider`
- [[Gerenciador de Tema]] — Poderia variar CSS por tema (atualmente fixo)
- [[Renderização Cairo]] — Complementa desenho do fundo arredondado

## Configuração

**Sem configuração externa** — CSS é gerado dinamicamente mas com valores fixos.

**Fontes do sistema:**
```python
font_name = _get_font_name()  # Usa gtk-font-name
```

## Observações importantes

- **IDs vs Classes**: Usa ambos (`#UserLabel` vs `.session-button`)
- **Transições**: `cubic-bezier` para animação suave de hover
- **RGBA**: Alpha blending requer compositor ativo
- **Bytes**: CSS retornado como `.encode()` para `load_from_data()`
- **Provider priority**: `STYLE_PROVIDER_PRIORITY_APPLICATION` sobrescreve tema do sistema
- **Limitação**: Não responde a mudanças de tema em runtime (apenas na inicialização)
