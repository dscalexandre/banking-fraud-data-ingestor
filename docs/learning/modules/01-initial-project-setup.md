# 01 — Initial project setup

## Objetivo

Estabelecer um ambiente de desenvolvimento Python 3.12 reproduzível para o projeto, com dependências e ferramentas de qualidade gerenciadas pelo Poetry, convenções de edição compartilhadas, teste mínimo de compatibilidade e validação contínua no GitHub Actions. O módulo prepara a base local e de CI; não entrega um fluxo de ingestão nem provisiona infraestrutura.

## Visão geral da tecnologia

O Poetry centraliza metadados, restrição de Python, dependências de desenvolvimento e configurações de ferramentas em `pyproject.toml`, enquanto `poetry.lock` fixa as versões resolvidas para instalações reproduzíveis. Pytest executa o smoke test, Ruff realiza a análise estática e o GitHub Actions aplica as mesmas verificações em Python 3.12 nos pull requests e pushes para `main`. EditorConfig e a configuração do VS Code reduzem divergências de edição e fazem a IDE usar o ambiente local `.venv`.

## Implementação e aprendizagem

`pyproject.toml` restringe o projeto a Python `>=3.12,<3.13`, declara o grupo `dev` e concentra as opções de pytest e Ruff. O `poetry.lock` é versionado junto dessa declaração, e o README documenta o fluxo local: configurar o virtualenv dentro do projeto, instalar dependências, executar `poetry check`, Ruff e pytest.

O teste em `tests/test_smoke.py` lê a restrição declarada no `pyproject.toml` e compara-a à versão do interpretador em execução. Assim, a regra de compatibilidade tem uma única fonte de verdade e é validada tanto localmente quanto na CI. O workflow `.github/workflows/ci.yml` instala Poetry 2.3.3, cria o ambiente no projeto, executa `poetry check` e Ruff no job `Quality`, e pytest no job `Tests (3.12)`.

`.editorconfig` define codificação, fim de linha, indentação e tratamento de espaços por tipo de arquivo. `.vscode/settings.json` aponta o VS Code para `.venv/bin/python`, usa o Poetry como gerenciador de ambiente e pacote, e ativa formatação e limpeza de espaços ao salvar. `data/raw/.gitkeep` preserva no versionamento o diretório reservado aos dados brutos sem introduzir dados reais.

## Conceitos essenciais

Uma instalação reproduzível parte da especificação de dependências e de seu lockfile: `pyproject.toml` define as faixas aceitas e `poetry.lock` registra a resolução usada pela instalação. Manter ambos sincronizados é uma consequência explícita da ADR-001.

O ambiente virtual no projeto é o diretório `.venv` configurado pelo Poetry. A configuração do VS Code referencia esse mesmo interpretador, evitando que comandos na IDE usem uma instalação global diferente da usada por `poetry run` e pela CI.

Integração contínua aplica as verificações em um executor limpo. Neste módulo, isso confirma que os metadados são válidos, que o código atende às regras de lint e que o smoke test aceita o interpretador Python 3.12 configurado no workflow.

## Alternativas consideradas

Conda oferece suporte a ambientes científicos e dependências não Python, o que poderia acomodar esse tipo de carga. A ADR-001 o rejeita neste incremento porque introduziria um modelo mais amplo de ambiente e empacotamento do que o necessário para o projeto.

`pip` com `venv` utiliza ferramentas nativas do ecossistema Python e poderia criar o ambiente virtual. Não foi adotado porque exigiria mecanismos adicionais e mais controle manual para lockfile, grupos de dependências e execução padronizada.

Pipenv fornece gerenciamento de dependências e ambiente virtual. Foi preterido por estar menos alinhado à decisão de centralizar metadados, build e configuração de ferramentas no `pyproject.toml`.

## Evidências

### Arquivos inspecionados

`docs/architecture/solution-design.md` — reserva `docs/learning/modules/01-initial-project-setup.md` como documentação de aprendizagem e define que a árvore arquitetural é direcional, não uma afirmação de implementação.

`docs/adr/ADR-001-adotar-poetry.md` — registra a adoção do Poetry, suas consequências e as alternativas Conda, `pip` com `venv` e Pipenv.

`pyproject.toml` — comprova a restrição Python 3.12, as dependências de desenvolvimento e as configurações de pytest e Ruff.

`poetry.lock` — é o lockfile versionado das dependências declaradas.

`tests/test_smoke.py` — comprova a validação da versão do interpretador contra `project.requires-python`.

`.github/workflows/ci.yml` — comprova os jobs `Quality` e `Tests (3.12)`, ambos executados em Python 3.12 com Poetry.

`.editorconfig` e `.vscode/settings.json` — comprovam, respectivamente, as convenções de edição e o uso do ambiente local gerenciado pelo Poetry no VS Code.

`README.md` — documenta os pré-requisitos e os comandos de preparação e validação locais.

`data/raw/.gitkeep` — comprova a presença versionada do diretório reservado a dados brutos, sem dados inseridos.

### Evidências da entrega integrada

[PR #4 — `chore(dev): configurar ambiente de desenvolvimento`](https://github.com/dscalexandre/banking-fraud-data-ingestor/pull/4) está com estado `MERGED`, teve como base `main` e foi integrado pelo merge commit `a3109398827f658373606dd5261f0ada6d51452b` em 07/10/2026. Seus oito commits abrangem padrões de edição, VS Code, diretório de dados, ADR, dependências, smoke test, CI e README; os arquivos alterados correspondem a esse escopo.

A [Issue #3 — `Configurar o ambiente de desenvolvimento`](https://github.com/dscalexandre/banking-fraud-data-ingestor/issues/3) foi fechada pelo PR #4. Seus critérios de aceite marcam como concluídos a instalação pelo Poetry, a restrição a Python 3.12, Ruff e pytest configurados, smoke test, ADR, README, CI e ausência de segredos ou dados sensíveis versionados.

Os checks do PR #4 foram concluídos com sucesso: `Quality` e `Tests (3.12)`, ambos no workflow CI. Os seis commits anteriores à criação de `.github/workflows/ci.yml` não possuíam check configurado; o commit que introduziu a CI e o commit final do PR foram cobertos por esses dois checks aprovados. Não há comentários na Issue #3 que registrem falha ou pendência funcional conhecida.

## Documentação oficial

| Tecnologia ou componente | Aplicação no módulo | Fonte oficial |
|---|---|---|
| Poetry | Gerenciamento de dependências, lockfile e ambiente virtual do projeto. | [Managing environments](https://python-poetry.org/docs/managing-environments/) |
| Pytest | Execução do smoke test de compatibilidade do interpretador. | [pytest documentation](https://docs.pytest.org/en/stable/) |
| Ruff | Análise estática configurada no `pyproject.toml` e executada pela CI. | [Ruff documentation](https://docs.astral.sh/ruff/) |
| GitHub Actions | Execução automatizada de qualidade e testes em pull requests e `main`. | [GitHub Actions quickstart](https://docs.github.com/en/actions/get-started/quickstart) |
| Visual Studio Code | Seleção do interpretador e integração com o ambiente Python local. | [Python environments in VS Code](https://code.visualstudio.com/docs/python/environments) |
| EditorConfig | Convenções de formatação compartilhadas entre editores. | [EditorConfig](https://editorconfig.org/) |
