---
tags: [feature, acao, sistema, energia]
relacionado: [[Interface de Sessão]]
status: ativo
tipo: feature
versao: 1.0.0
---

# Ações de Sessão

Gerencia os comandos de energia e sessão: desligar, reiniciar, logout e suspender.

## Como funciona

Cada ação é mapeada para um comando do sistema:

| Ação | Ícone | Label | Comando |
|------|-------|-------|---------|
| `shutdown` | `shutdown.png` | Desligar | `systemctl poweroff` |
| `restart` | `restart.png` | Reiniciar | `systemctl reboot` |
| `logout` | `logout.png` | Sair | `gnome-session-quit --logout --no-prompt` |
| `suspend` | `suspend.png` | Suspenso | `systemctl suspend -i` |

### Fluxo de execução

1. Usuário clica no botão ou pressiona Enter/Space
2. `on_button_clicked()` é chamado com o comando
3. Janela é ocultada imediatamente (`self.hide()`)
4. Timeout de 150ms agenda `_execute_and_quit()`
5. Comando é executado via `subprocess.Popen()`
6. Aplicação encerra (`close_menu()`)

### Delay intencional

O `GLib.timeout_add(150, ...)` garante que a UI desapareça antes do comando executar, evitando flicker.

## Arquivos principais

- `app/main.py` — Métodos `on_button_clicked()`, `_execute_and_quit()` (linhas 280-300)
- `app/main.py` — Definição `DESCRIPTIONS` e lista `actions` (linhas 56-60, 135-141)

## Integrações

- [[Interface de Sessão]] — Botões acionam as ações
- [[Descrições Contextuais]] — Usa mesma chave CSS para descrições
- [[Sistema de Ícones]] — Cada ação tem ícone associado

## Configuração

**Comandos hardcoded** — podem ser customizados na lista `actions`:

```python
actions = [
    ("shutdown.png", "Desligar",  "shutdown", "systemctl poweroff"),
    ("restart.png",  "Reiniciar", "restart",  "systemctl reboot"),
    ("logout.png",   "Sair",      "logout",   "gnome-session-quit --logout --no-prompt"),
    ("suspend.png",  "Suspenso",  "suspend",  "systemctl suspend -i"),
]
```

## Observações importantes

- **systemctl**: Requer systemd (padrão no Zorin OS/Ubuntu)
- **gnome-session-quit**: Específico para GNOME/Zorin
- **Flag `-i`**: Em `suspend -i` ignora inibidores (ex: apps prevenindo suspensão)
- **Tratamento de erro**: `try/except` em `_execute_and_quit()` silencia falhas
- **Polkit**: Comandos podem solicitar autenticação via PolicyKit dependendo da configuração
- **Logout sem prompt**: `--no-prompt` força logout imediato sem confirmação
