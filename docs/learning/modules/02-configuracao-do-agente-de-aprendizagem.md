# 02 - Configuração do agente de aprendizagem

## Objetivo

Disponibilizar o agente OpenAI Codex `learning-documenter` para criar ou
atualizar documentação de aprendizagem de módulos já concluídos e integrados à
`main`, com conteúdo rastreável às evidências da entrega. O módulo adiciona a
skill, seu template canônico e o perfil que exige seu uso; não implementa
fluxos de ingestão nem altera o comportamento dos dados do projeto.

## Visão geral da tecnologia

O OpenAI Codex permite especializar o comportamento do agente por instruções e
skills. Neste módulo, uma skill em Markdown concentra o procedimento de
documentação, enquanto um perfil TOML identifica o agente e lhe atribui esse
procedimento. Um template Markdown torna a estrutura do resultado consistente
e permite registrar arquivos inspecionados, validações, evidências da entrega
integrada e referências oficiais.

## Implementação e aprendizagem

`.codex/agents/learning-documenter.toml` define o perfil
`learning-documenter`, sua descrição e o modo de sandbox `workspace-write`. As
instruções do perfil determinam o uso obrigatório da skill e limitam sua
responsabilidade à documentação de aprendizagem, sem implementação ou
documentação técnica.

`.agents/skills/learning-documenter/SKILL.md` define as entradas de módulo,
operação e Pull Requests. Antes de criar um documento, o procedimento localiza
todos os Pull Requests do módulo e exige que estejam integrados à `main`, com
checks aprovados e sem pendências funcionais conhecidas. A skill também limita
a alteração a exatamente um Markdown em `docs/learning/modules/`, requer o
template canônico, impede ações remotas e separa a documentação da entrega de
implementação.

O template em `.agents/skills/learning-documenter/assets/module-learning.md`
organiza o aprendizado em objetivo, tecnologia, implementação, conceitos,
evidências e documentação oficial. A seção de alternativas é condicional às
evidências. Como validação do próprio agente, o PR integrado produziu o
documento do módulo de ambiente de desenvolvimento sem modificar arquivos fora
dos caminhos previstos.

## Conceitos essenciais

Evidência de entrega integrada é o vínculo entre o documento e o conjunto
completo de Pull Requests que implementou o módulo. Esse vínculo impede que
uma documentação criada a partir de um incremento isolado descreva um estado
incompleto.

Template canônico é uma estrutura versionada que define as seções e a tabela de
fontes oficiais do documento. A skill exige preservar essa estrutura, para que
as documentações dos módulos apresentem os mesmos tipos de evidência.

Separação de responsabilidades limita este agente à documentação posterior à
integração. A implementação, a documentação técnica e operações remotas ficam
fora de seu escopo, como determinado pelo perfil e pela skill.

## Evidências

### Arquivos inspecionados

`.agents/skills/learning-documenter/SKILL.md` — entradas aceitas, critérios de
elegibilidade, procedimento, formato do resultado e restrições do agente.

`.agents/skills/learning-documenter/assets/module-learning.md` — estrutura
canônica exigida para a documentação de módulos.

`.codex/agents/learning-documenter.toml` — identificação do perfil, sandbox e
instruções que tornam o uso da skill obrigatório.

`docs/architecture/solution-design.md` — posição arquitetural das skills, dos
perfis Codex e da documentação de aprendizagem na estrutura do repositório.

`docs/learning/modules/01-initial-project-setup.md` — resultado da validação de
criação produzido pelo módulo integrado.

### Validações executadas

`awk '/[[:blank:]]+$/ { print NR; failed=1 } END { exit failed }' docs/learning/modules/02-configuracao-do-agente-de-aprendizagem.md` — nenhuma linha com espaço em branco ao final foi reportada.

`wc -l docs/learning/modules/02-configuracao-do-agente-de-aprendizagem.md` — documento com menos de 300 linhas.

### Evidências da entrega integrada

[PR #6 — configurar e validar agente de aprendizagem](https://github.com/dscalexandre/banking-fraud-data-ingestor/pull/6) foi integrado à `main` em 12/09/2026 pelo merge commit `83fad4091bd111309322c7667698bb0e332cb9c7`. Ele é o único Pull Request que compõe este módulo e adicionou a skill, o template, o perfil e a documentação usada na validação de criação.

A [Issue #5 — Configurar e validar o agente de aprendizagem do OpenAI Codex](https://github.com/dscalexandre/banking-fraud-data-ingestor/issues/5) foi fechada pelo PR #6; todos os seus critérios de aceite estão concluídos e cobrem a descoberta da skill, o perfil, as operações `criar` e `atualizar`, a estrutura do documento e o isolamento dos arquivos gerados.

Os checks obrigatórios do PR #6 concluíram com sucesso: `Quality` e `Tests (3.12)`. O PR também registrou sucesso para as análises `CodeQL` de Python e GitHub Actions.

## Documentação oficial

| Tecnologia ou componente | Aplicação no módulo | Fonte oficial |
|---|---|---|
| OpenAI Codex Skills | Estrutura de instruções reutilizáveis aplicada ao procedimento de documentação. | [Build skills](https://developers.openai.com/codex/skills/) |
