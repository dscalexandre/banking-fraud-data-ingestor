# 02 - Criação do agente de aprendizagem

## Objetivo

Disponibilizar o agente `learning-documenter` para criar ou atualizar, de modo
rastreável, a documentação de aprendizagem de módulos concluídos e integrados
à `main`. A entrega inclui o perfil do agente, uma skill que delimita o fluxo
de trabalho e o template canônico dos documentos gerados.

## Visão geral da tecnologia

O módulo configura o OpenAI Codex por meio de um perfil TOML versionado no
repositório e de uma skill local. O perfil seleciona a responsabilidade de
documentação de aprendizagem e exige o uso da skill. A skill concentra o
procedimento de localizar Pull Requests integrados, verificar a elegibilidade
do módulo e gerar um único documento Markdown a partir de um template. Essa
separação mantém o agente fora da implementação e da documentação técnica.

## Implementação e aprendizagem

`.codex/agents/learning-documenter.toml` declara o agente
`learning-documenter`, descreve seu escopo e instrui o Codex a usar a skill
homônima. `.agents/skills/learning-documenter/SKILL.md` recebe um módulo ou
Pull Requests, identifica todos os incrementos da entrega e exige que estejam
com estado `MERGED` e integrados à `main` antes de alterar documentação.

Para a operação `criar`, a skill confirma que o módulo está concluído, que seus
checks obrigatórios foram aprovados e que não há pendências funcionais
conhecidas. Ela cria exatamente um arquivo em `docs/learning/modules/`, com
até 300 linhas, usando
`.agents/skills/learning-documenter/assets/module-learning.md` como contrato
estrutural. Para `atualizar`, preserva o conteúdo não afetado e só altera o
documento quando houver mudança integrada material comprovada.

O template separa objetivo, tecnologia, implementação, conceitos, evidências e
documentação oficial. As evidências distinguem os arquivos inspecionados das
validações realmente executadas e registram PRs, Issues, merge commits e checks
que compõem o módulo documentado. A primeira validação da capacidade gerou
`docs/learning/modules/01-initial-project-setup.md` para o módulo de ambiente
de desenvolvimento, sem alterar sua implementação.

## Conceitos essenciais

Uma skill é o procedimento reutilizável que Codex descobre pelo metadado e
carrega quando selecionado. Neste módulo, ela torna verificável o limite entre
documentar uma entrega já integrada e produzir conteúdo para trabalho ainda em
construção.

Elegibilidade é o gate anterior à escrita: o agente precisa comprovar o
conjunto completo de Pull Requests do módulo, seus merges na `main`, a Issue
concluída quando existir e os checks aprovados. Assim, a documentação descreve
somente o comportamento entregue, e não planejamento ou incrementos isolados.

O template é um contrato estrutural. Ele mantém as seções e a ordem do
documento, limita o conteúdo ao módulo e exige links para fontes oficiais das
tecnologias efetivamente implementadas.

## Evidências

### Arquivos inspecionados

`.codex/agents/learning-documenter.toml` — perfil do Codex, descrição do papel,
modo de sandbox e instrução para usar a skill.

`.agents/skills/learning-documenter/SKILL.md` — entrada, critérios de
elegibilidade, procedimento, restrições e resultado permitido ao agente.

`.agents/skills/learning-documenter/assets/module-learning.md` — estrutura
canônica do documento de aprendizagem e tabela de documentação oficial.

`docs/learning/modules/01-initial-project-setup.md` — documento produzido na
validação inicial da capacidade para o módulo já integrado de ambiente de
desenvolvimento.

`docs/architecture/solution-design.md` — papel do `learning-documenter` e seu
acionamento após a integração de um módulo à `main`.

### Validações executadas

`gh pr list --state merged --limit 100 --json number,title,url,state,mergedAt,baseRefName,headRefName,body,mergeCommit,closedAt,statusCheckRollup,assignees` — PR #6 localizado como integrado à `main`; os checks `Quality`, `Tests (3.12)`, `Analyze (actions)` e `Analyze (python)` concluíram com sucesso; o check agregado `CodeQL` concluiu como neutro.

`gh issue list --state closed --limit 100 --json number,title,url,state,closedAt,body` — Issue #5 localizada como fechada, com os critérios de aceite do agente de aprendizagem concluídos.

`git merge-base --is-ancestor 83fad4091bd111309322c7667698bb0e332cb9c7 main` — confirmou que o merge commit do PR #6 é ancestral de `main`.

### Evidências da entrega integrada

[PR #6 — chore(codex): configurar e validar agente de aprendizagem](https://github.com/dscalexandre/banking-fraud-data-ingestor/pull/6) foi integrado à `main` em 12/09/2026 pelo merge commit `83fad4091bd111309322c7667698bb0e332cb9c7`. Ele adicionou o perfil, a skill, o template e o documento de validação do agente.

A [Issue #5 — Configurar e validar o agente de aprendizagem do OpenAI Codex](https://github.com/dscalexandre/banking-fraud-data-ingestor/issues/5) foi fechada pelo PR #6. Seus critérios de aceite registram a descoberta da skill e do perfil, a criação por descrição de módulo, a atualização por Pull Requests integrados, a estrutura canônica, os links oficiais e o isolamento dos arquivos produzidos.

Os checks obrigatórios do PR #6 concluíram com sucesso: `Quality`,
`Tests (3.12)`, `Analyze (actions)` e `Analyze (python)`. O check agregado
`CodeQL` foi concluído com resultado neutro.

## Documentação oficial

| Tecnologia ou componente | Aplicação no módulo | Fonte oficial |
|---|---|---|
| OpenAI Codex | Perfil especializado, skill reutilizável e orientação de projeto para documentar módulos integrados. | [Personalização do Codex](https://learn.chatgpt.com/docs/customization/overview) |
