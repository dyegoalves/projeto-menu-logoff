---
tags: [core, gtk, aplicacao]
relacionado: [[Interface de Sessão]]
status: ativo
tipo: modulo
versao: 1.0.0
---

# Aplicação GTK Principal

Classe base que gerencia o ciclo de vida da aplicação GTK, inicialização e controle da janela de sessão.

## Como funciona

A aplicação estende `Gtk.Application` para fornecer gerenciamento adequado do ciclo de vida:

1. **Inicialização**: Define `application_id` único (`com.dyego.menu-logoff`)
2. **Ativação**: Cria ou reapresenta a janela de sessão
3. **Gerenciamento de estado**: Mantém referência da janela para evitar múltiplas instâncias
4. **Encerramento**: Limpa referências e finaliza o processo GTK

O padrão singleton garante que apenas uma instância do menu exista por vez.

## Arquivos principais

- `app/main.py` — Implementação das classes `SessionApp` e ponto de entrada
- `app/session-menu.desktop` — Arquivo de entrada para integração com desktop

## Integrações

- [[Interface de Sessão]] — Cria e gerencia a janela principal
- [[Empacotamento Debian]] — Usa o desktop entry para integração no sistema

## Configuração

```python
application_id="com.dyego.menu-logoff"
```

**Dependências:**
- `gi.repository.Gtk` — Framework GTK 3.0
- `gi.repository.GLib` — Loop principal e utilitários
- `gi.repository.Gdk` — Recursos de tela e visual

## Observações importantes

- **Reapresentação de janela**: Se a janela já existe e está visível, `present()` traz para frente em vez de criar nova
- **Referência fraca**: A janela é armazenada em `self.window` e limpa no evento `destroy`
- **Exit status**: Retorna código de saída adequado via `app.run(sys.argv)`
- **PyInstaller**: O entrypoint aponta para `app/main.py` no build
