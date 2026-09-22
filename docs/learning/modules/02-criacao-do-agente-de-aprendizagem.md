# 02 - Criação do agente de aprendizagem

## Objetivo

Disponibilizar o agente `learning-documenter` para criar ou atualizar
documentação de aprendizagem de módulos já concluídos e integrados à `main`,
com um fluxo verificável, um perfil local do Codex e um template canônico para
os documentos produzidos.

## Visão geral da tecnologia

O módulo usa skills do Codex para associar uma capacidade a instruções e recursos
versionados no repositório. A skill define quando a documentação pode ser
produzida, quais evidências devem ser verificadas e o formato do resultado. O
perfil do agente seleciona essa skill e limita sua responsabilidade à
documentação de aprendizagem. Markdown é o formato do artefato resultante, o
que permite versionar o conteúdo junto às evidências que ele descreve.

## Implementação e aprendizagem

`.codex/agents/learning-documenter.toml` registra o perfil
`learning-documenter` e determina o uso obrigatório da skill homônima. A skill
em `.agents/skills/learning-documenter/SKILL.md` recebe um módulo ou Pull
Requests, identifica os incrementos relacionados e exige que todos estejam
integrados por Pull Request com estado `MERGED` antes de alterar um documento.

Para a operação `criar`, o agente confirma que o módulo está completo, que os
checks obrigatórios foram aprovados e, quando houver Issue vinculada, que ela
está concluída. Para `atualizar`, ele preserva o conteúdo não afetado e só usa
mudanças posteriores que também tenham sido integradas e validadas. Assim, a
documentação é uma consequência da entrega integrada, e não um artefato que
autoriza sua implementação ou merge.

`assets/module-learning.md` fornece a estrutura fixa do documento: objetivo,
tecnologia, implementação, conceitos, evidências e documentação oficial. A
skill exige exatamente um arquivo Markdown em `docs/learning/modules/`, com no
máximo 300 linhas, e permite omitir somente a seção de alternativas quando não
houver evidência de alternativas consideradas. O PR #6 validou o caminho de
criação com a documentação do ambiente inicial e o caminho de atualização a
partir de Pull Requests integrados.

## Conceitos essenciais

Uma skill é um diretório com `SKILL.md` e recursos opcionais; neste módulo, ela
transforma regras de elegibilidade, pesquisa de evidências e estrutura de saída
em um fluxo repetível para o Codex.

Evidência integrada é o conjunto de Pull Requests que compõe o módulo, seus
merge commits, checks concluídos e a Issue associada. A exigência de evidência
impede que o agente documente trabalho em construção ou confunda um incremento
isolado com um módulo completo.

O template canônico funciona como contrato estrutural: preserva os mesmos nomes,
níveis e ordem de seções para que documentos de módulos diferentes tenham
rastreabilidade e leitura consistentes.

## Evidências

### Arquivos inspecionados

`.codex/agents/learning-documenter.toml` — perfil registrado do Codex, descrição
da capacidade e instrução para usar obrigatoriamente a skill.

`.agents/skills/learning-documenter/SKILL.md` — entradas, elegibilidade,
operações `criar` e `atualizar`, limites de alteração e critérios de conclusão.

`.agents/skills/learning-documenter/assets/module-learning.md` — estrutura
canônica exigida para cada documento de aprendizagem.

`docs/learning/modules/01-initial-project-setup.md` — resultado da validação de
criação do agente para o módulo de ambiente de desenvolvimento.

`.github/workflows/ci.yml` — jobs `Quality` e `Tests (3.12)` que validaram o PR
integrado.

`docs/architecture/solution-design.md` — árvore arquitetural que posiciona o
perfil e a skill de aprendizagem em `.codex/agents/` e `.agents/skills/`.

### Validações executadas

`gh pr view 6 --json number,title,url,state,mergedAt,mergeCommit,statusCheckRollup,closingIssuesReferences,body,commits,files` — PR #6 confirmado como `MERGED`; checks `Quality`, `Tests (3.12)`, `Analyze (actions)` e `Analyze (python)` concluíram com `SUCCESS`.

`gh issue view 5 --json number,title,url,state,closedAt,body,labels,comments` — Issue #5 confirmada como `CLOSED`, com todos os critérios de aceite marcados como concluídos.

### Evidências da entrega integrada

[PR #6 — chore(codex): configurar e validar agente de aprendizagem](https://github.com/dscalexandre/banking-fraud-data-ingestor/pull/6) foi integrado à `main` em 12/09/2026 pelo merge commit `83fad4091bd111309322c7667698bb0e332cb9c7`. Ele criou a skill, seu template, o perfil do agente e o documento de validação do ambiente inicial; os checks `Quality`, `Tests (3.12)`, `Analyze (actions)` e `Analyze (python)` foram concluídos com sucesso.

A [Issue #5 — Configurar e validar o agente de aprendizagem do OpenAI Codex](https://github.com/dscalexandre/banking-fraud-data-ingestor/issues/5) foi encerrada pelo PR #6. Seus critérios confirmam a descoberta da skill, o uso do perfil, os fluxos `criar` e `atualizar`, a estrutura canônica e o isolamento dos arquivos gerados.

## Documentação oficial

| Tecnologia ou componente | Aplicação no módulo | Fonte oficial |
|---|---|---|
| Codex skills | Define o fluxo reutilizável e reúne instruções, template e recursos do agente. | [Criar skills](https://developers.openai.com/docs/build-skills) |
| Personalização do Codex | Fundamenta o uso de instruções e skills específicas do repositório. | [Personalização](https://developers.openai.com/docs/customization/overview) |
