---
tags: [ui, tema, gnome, sistema]
relacionado: [[Interface de Sessão]]
status: ativo
tipo: feature
versao: 1.0.0
---

# Gerenciador de Tema

Detecta automaticamente se o sistema está usando tema claro ou escuro e adapta a interface.

## Como funciona

A detecção ocorre em cascata, verificando múltiplas fontes:

### 1. GNOME Color Scheme (Moderno)
```bash
gsettings get org.gnome.desktop.interface color-scheme
```
Se retornar conter `"dark"`, tema é escuro.

### 2. GTK Application Preference
```python
settings.get_property("gtk-application-prefer-dark-theme")
```
Verifica se app prefere tema escuro explicitamente.

### 3. GTK Theme Name
```python
theme = settings.get_property("gtk-theme-name")
```
Se o nome do tema contém `"dark"` (case-insensitive), é tema escuro.

### Aplicação

O resultado (`self._dark`) é armazenado mas atualmente **não é usado ativamente** — o CSS é fixo em modo escuro premium.

## Arquivos principais

- `app/main.py` — Função `_is_dark_theme()` (linhas 24-40)

## Integrações

- [[Interface de Sessão]] — Chama `_is_dark_theme()` no `__init__`
- [[Estilização CSS]] — Poderia usar `_dark` para alternar temas (atualmente fixo)

## Configuração

**Sem configuração necessária** — detecção automática via `gsettings` e GTK.

**Dependências:**
- `subprocess` — Executa `gsettings`
- `Gtk.Settings` — Acessa configurações GTK

## Observações importantes

- **Fallback seguro**: Se `gsettings` falhar (exceção), continua para checks GTK
- **Zorin OS**: Baseado em GNOME, usa `gsettings` como fonte primária
- **Limitação atual**: A detecção existe mas o CSS não é dinâmico — sempre usa tema escuro
- **Melhoria futura**: Poderia gerar CSS diferente baseado em `self._dark`
- **Performance**: Executado apenas uma vez na inicialização
