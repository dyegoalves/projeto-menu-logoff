Percorra o projeto inteiro e documente cada módulo e funcionalidade de forma separada, 
criando um arquivo .md individual para cada um no vault do Obsidian.

Siga obrigatoriamente estas regras:

1. Cada arquivo deve começar com o frontmatter:
---
tags: [categorias relevantes]
relacionado: [[Arquivos conectados]]
status: ativo
tipo: feature | arquitetura | decisão | endpoint | componente
versao: 1.0.0
---

2. Nome dos arquivos em separado por hifen e sem espaços (ex: "sistema-de-pagamentos.md")

3. Cada arquivo deve seguir esta estrutura:
# Nome do Módulo
Descrição do que faz e por que existe.
## Como funciona
## Arquivos principais
## Integrações
## Configuração
## Observações importantes

4. Use [[wiki-links]] para conectar arquivos relacionados entre si
5. Documente o estado atual — sem histórico de mudanças
6. Crie também um arquivo MOC (Map of Content) principal com o nome do projeto, 
   listando todos os módulos e suas conexões

O vault está localizado em: /home/dyegoalves/obsidian-cofres/menu-logoff