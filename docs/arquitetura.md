Percorra o projeto inteiro e documente cada módulo e funcionalidade de forma separada, 
criando um arquivo .md individual para cada um no vault do Obsidian.

Siga obrigatoriamente estas regras: 

1. Nome dos arquivos em PascalCase com espaços (ex: "Sistema de Pagamentos.md")
2. Cada arquivo deve seguir esta estrutura:
3. Cada arquivo deve começar com o frontmatter:

---
tags: [categoria1, categoria2]
relacionado: [[Outro Módulo]]
status: ativo
tipo: feature
versao: 1.0.0
---


# Nome do Módulo

Descrição clara e direta do que o módulo faz e por que ele existe no sistema.

## Como funciona

Explique o funcionamento geral, fluxo de dados, regras principais e comportamento esperado.

## Arquivos principais

- `caminho/arquivo1.ext` — descrição breve
- `caminho/arquivo2.ext` — descrição breve

## Integrações

- [[Outro Módulo]]
- [[Serviço Externo]]

Descreva como este módulo se comunica com outros.

## Configuração

Variáveis, parâmetros, flags ou dependências necessárias.

## Observações importantes

Pontos críticos, limitações, decisões relevantes ou cuidados ao modificar.


4. Use [[wiki-links]] para conectar arquivos relacionados entre si

5. Documente o estado atual — sem histórico de mudanças

6. Crie também um arquivo MOC (Map of Content) principal com o nome do projeto, 
   listando todos os módulos e suas conexões

O vault está localizado em: /home/dyegoalves/projetos/menu-logoff/docs/menu-logoff/appdocs