# 02 - Configuração do agente de aprendizagem

## Objetivo

Disponibilizar o agente OpenAI Codex `learning-documenter` para criar ou
atualizar documentação de aprendizagem de módulos já concluídos e integrados à
`main`, com conteúdo rastreável às evidências da entrega. O módulo adiciona a
skill, o template canônico e o perfil do agente; não implementa fluxos de
ingestão nem altera dados ou infraestrutura do projeto.

## Visão geral da tecnologia

O OpenAI Codex permite especializar o trabalho do agente com um perfil e uma
skill versionados no repositório. Neste módulo, o perfil TOML identifica a
responsabilidade do agente e exige a skill; a skill em Markdown concentra o
procedimento de documentação. O template Markdown padroniza a estrutura do
resultado e o registro de evidências e fontes oficiais.

## Implementação e aprendizagem

`.codex/agents/learning-documenter.toml` define o perfil
`learning-documenter`, sua descrição, o modo de sandbox `workspace-write` e a
instrução para usar obrigatoriamente a skill homônima. As instruções também
restringem a responsabilidade à documentação de aprendizagem, sem assumir
implementação ou documentação técnica.

`.agents/skills/learning-documenter/SKILL.md` aceita a identificação de um
módulo ou de seus Pull Requests. Antes de produzir conteúdo, ela exige a
localização de todos os Pull Requests relevantes, o estado `MERGED`, a
integração à `main`, os checks aprovados e a ausência de pendências funcionais
conhecidas. A operação `criar` produz exatamente um Markdown em
`docs/learning/modules/`; a operação `atualizar` preserva o conteúdo não
afetado e depende de mudança integrada material comprovada.

`.agents/skills/learning-documenter/assets/module-learning.md` é o contrato
estrutural desse Markdown. Ele organiza objetivo, tecnologia, implementação,
conceitos, evidências e documentação oficial, e torna a seção de alternativas
condicional à existência de evidência. Como validação da capacidade, o PR
integrado também entregou a documentação do módulo de ambiente de
desenvolvimento, sem alterar sua implementação.

## Conceitos essenciais

Evidência de entrega integrada é o vínculo entre o documento e o conjunto
completo de Pull Requests que compõe um módulo. A exigência de merge, checks e
Issue concluída evita que o documento descreva um incremento isolado ou um
trabalho ainda planejado.

O template canônico é uma estrutura versionada que mantém as mesmas seções, a
ordem delas e a tabela de fontes oficiais em cada documento. A skill exige essa
estrutura e separa, nas evidências, arquivos que foram inspecionados de
validações que foram realmente executadas.

A separação de responsabilidades deixa a implementação, documentação técnica e
operações remotas fora do perfil. Assim, o agente atua depois da integração do
módulo e altera somente a documentação de aprendizagem autorizada.

## Evidências

### Arquivos inspecionados

`.codex/agents/learning-documenter.toml` — perfil do Codex, modo de sandbox e
instruções que tornam obrigatório o uso da skill.

`.agents/skills/learning-documenter/SKILL.md` — entradas aceitas, critérios de
elegibilidade, procedimento, formato do resultado e restrições do agente.

`.agents/skills/learning-documenter/assets/module-learning.md` — estrutura
canônica exigida para a documentação de módulos.

`docs/architecture/solution-design.md` — posição das skills, dos perfis Codex e
da documentação de aprendizagem na estrutura do repositório.

`docs/learning/modules/01-initial-project-setup.md` — documento produzido na
validação de criação da capacidade para um módulo já integrado.

### Validações executadas

`awk '/[[:blank:]]+$/ { print NR; failed=1 } END { exit failed }' docs/learning/modules/02-configuracao-do-agente-de-aprendizagem.md` — nenhuma linha com espaço em branco ao final foi reportada.

`wc -l docs/learning/modules/02-configuracao-do-agente-de-aprendizagem.md` — documento com menos de 300 linhas.

### Evidências da entrega integrada

[PR #6 — chore(codex): configurar e validar agente de aprendizagem](https://github.com/dscalexandre/banking-fraud-data-ingestor/pull/6) foi integrado à `main` em 12/09/2026 pelo merge commit `83fad4091bd111309322c7667698bb0e332cb9c7`. Ele é o único Pull Request que compõe este módulo e adicionou o perfil, a skill, o template e o documento usado para validar a criação.

A [Issue #5 — Configurar e validar o agente de aprendizagem do OpenAI Codex](https://github.com/dscalexandre/banking-fraud-data-ingestor/issues/5) foi fechada pelo PR #6. Seus critérios de aceite concluídos cobrem a descoberta da skill e do perfil, as operações `criar` e `atualizar`, a estrutura canônica, os links oficiais e o isolamento dos arquivos produzidos.

Os checks obrigatórios do PR #6 concluíram com sucesso: `Quality` e `Tests (3.12)`. As análises `CodeQL` de Python e GitHub Actions também concluíram com sucesso; o check agregado `CodeQL` foi concluído como neutro.

## Documentação oficial

| Tecnologia ou componente | Aplicação no módulo | Fonte oficial |
|---|---|---|
| OpenAI Codex Skills | Procedimento reutilizável que orienta a documentação de módulos integrados. | [Build skills](https://developers.openai.com/codex/skills/) |
