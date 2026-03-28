---
tags: [moc, indice, mapa]
relacionado: [[Menu Logoff]]
status: ativo
tipo: moc
versao: 1.0.0
---

# Menu Logoff - Map of Content

Índice principal de toda a documentação do sistema **Menu Logoff**.

## Visão Geral

Menu Logoff é um menu de sessão personalizado para Zorin OS com estética inspirada no macOS, permitindo gerenciamento de energia e sessão do usuário.

## Módulos do Sistema

### Núcleo da Aplicação
- [[Aplicação GTK Principal]] — Estrutura base da aplicação GTK e ciclo de vida
- [[Interface de Sessão]] — Janela principal e componentes visuais do menu
- [[Gerenciador de Tema]] — Detecção e adaptação a temas claro/escuro do sistema

### Funcionalidades
- [[Ações de Sessão]] — Comandos de desligar, reiniciar, logout e suspender
- [[Sistema de Ícones]] — Gerenciamento e carregamento de ícones das ações
- [[Descrições Contextuais]] — Textos explicativos das ações por contexto

### Infraestrutura
- [[Build System]] — Scripts e configuração de compilação PyInstaller
- [[Empacotamento Debian]] — Geração de pacotes .deb para instalação
- [[Configuração do Projeto]] — Metadados e dependências do projeto

### Recursos Visuais
- [[Estilização CSS]] — CSS dinâmico para aparência personalizada
- [[Renderização Cairo]] — Desenho da janela arredondada com transparência
- [[Ativos Gráficos]] — Ícones e recursos visuais do sistema

## Conexões entre Módulos

```
Aplicação GTK Principal
├── Interface de Sessão
│   ├── Gerenciador de Tema
│   ├── Estilização CSS
│   └── Renderização Cairo
├── Ações de Sessão
│   └── Sistema de Ícones
└── Descrições Contextuais

Build System
└── Empacotamento Debian

Configuração do Projeto
└── Ativos Gráficos
```

## Navegação Rápida

| Categoria | Módulo | Status |
|-----------|--------|--------|
| Core | [[Aplicação GTK Principal]] | ✅ Ativo |
| UI | [[Interface de Sessão]] | ✅ Ativo |
| UI | [[Gerenciador de Tema]] | ✅ Ativo |
| Feature | [[Ações de Sessão]] | ✅ Ativo |
| Feature | [[Sistema de Ícones]] | ✅ Ativo |
| Feature | [[Descrições Contextuais]] | ✅ Ativo |
| Infra | [[Build System]] | ✅ Ativo |
| Infra | [[Empacotamento Debian]] | ✅ Ativo |
| Infra | [[Configuração do Projeto]] | ✅ Ativo |
| UI | [[Estilização CSS]] | ✅ Ativo |
| UI | [[Renderização Cairo]] | ✅ Ativo |
| Assets | [[Ativos Gráficos]] | ✅ Ativo |
