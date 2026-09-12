# 01 - Configuração inicial do ambiente de desenvolvimento

## Objetivo

Entregar uma base de desenvolvimento reproduzível para o módulo de ingestão de
fraudes, com versão de Python definida, dependências bloqueadas, ambiente local
padronizado, validação automatizada e instruções de preparação. Esta entrega não
implementa fluxos de ingestão nem provisiona infraestrutura.

## Visão geral da tecnologia

O projeto usa Python 3.12 como única versão suportada e Poetry para concentrar
metadados, grupos de dependências, ambiente virtual e lock de dependências. Ruff
e pytest formam a verificação local de qualidade. O GitHub Actions reproduz essa
validação em pull requests e pushes para `main`; VS Code e EditorConfig reduzem
diferenças de ambiente e formatação entre colaboradores.

## Implementação e aprendizagem

`pyproject.toml` estabelece `>=3.12,<3.13`, declara o projeto em modo não
empacotável e centraliza as dependências de desenvolvimento, as opções de pytest
e as regras do Ruff. `poetry.lock` registra a resolução dessas dependências. A
ADR-001 formaliza a escolha do Poetry e determina que ambos os arquivos permaneçam
sincronizados.

O ambiente virtual é configurado no diretório do projeto. `.vscode/settings.json`
aponta o VS Code para `.venv/bin/python` e para o gerenciador do Poetry, enquanto
`.editorconfig` padroniza codificação, finais de linha, indentação e espaços finais.
O diretório `data/raw/` é reservado por meio de `.gitkeep`, sem introduzir dados
brutos no controle de versão.

`tests/test_smoke.py` lê a restrição de versão diretamente de `pyproject.toml` e
verifica se o interpretador em execução a atende. Na CI, os jobs `Quality` e
`Tests (3.12)` instalam Poetry 2.3.3, usam Python 3.12, instalam o lock e executam,
respectivamente, `poetry check` mais Ruff, e pytest. O README expõe a mesma sequência
para o uso local.

## Conceitos essenciais

Reprodutibilidade significa que desenvolvimento local e CI resolvem o mesmo conjunto
de dependências a partir de `pyproject.toml` e `poetry.lock`. O lock evita que uma
nova versão compatível seja escolhida silenciosamente em cada instalação.

A restrição de versão do Python é uma política executável: o teste smoke a consulta
na fonte de configuração, evitando duplicar o intervalo esperado no teste. A CI usa
a mesma versão para detectar incompatibilidades antes da integração.

Separar ferramentas de desenvolvimento no grupo `dev` mantém o projeto sem
dependências de produção neste incremento e deixa explícito que Ruff, pytest,
`packaging` e `tomli` existem para validar e testar o ambiente.

## Alternativas consideradas

Conda gerencia ambientes e dependências não Python e seria apropriado para cenários
científicos. A amplitude desse modelo adicionaria complexidade desnecessária ao
ambiente Python inicial, por isso a ADR-001 registrou Poetry como alternativa mais
adequada aos grupos de dependências e à execução local e de CI.

`pip` com `venv` usa ferramentas nativas e tem menor camada adicional, mas exigiria
controle manual complementar para lock, grupos de dependências e uma execução
padronizada. Foi descartado porque a entrega exige centralizar esses elementos.

Pipenv também combina dependências e ambiente virtual, porém foi considerado menos
alinhado à estratégia de reunir metadados, build e configurações de ferramentas no
`pyproject.toml`. A adoção do Poetry preserva essa centralização.

## Evidências

### Arquivos inspecionados

`pyproject.toml` — versão suportada do Python, modo não empacotável, dependências de desenvolvimento e configurações de pytest e Ruff.

`poetry.lock` — resolução versionada das dependências declaradas pelo projeto.

`docs/adr/ADR-001-adotar-poetry.md` — decisão aceita, motivação, consequências e alternativas para o Poetry.

`.editorconfig` — padrões compartilhados de edição e formatação.

`.vscode/settings.json` — interpretador e gerenciador de ambiente configurados para Poetry no workspace.

`data/raw/.gitkeep` — reserva do diretório de dados brutos sem versionar conteúdo.

`tests/test_smoke.py` — teste que compara o interpretador ativo com a restrição em `pyproject.toml`.

`.github/workflows/ci.yml` — jobs de qualidade e testes no Python 3.12, executados em pull requests e pushes para `main`.

`README.md` — pré-requisitos e comandos documentados para preparar e validar o ambiente.

### Validações executadas

`awk '/[[:blank:]]+$/ { print NR; failed=1 } END { exit failed }' docs/learning/modules/01-initial-project-setup.md` — nenhuma linha com espaço em branco ao final foi reportada.

`wc -l docs/learning/modules/01-initial-project-setup.md` — documento com menos de 300 linhas.

### Evidências da entrega integrada

[PR #4 — chore(dev): configurar ambiente de desenvolvimento](https://github.com/dscalexandre/banking-fraud-data-ingestor/pull/4) foi integrado à `main` em 11/09/2026 pelo merge commit `46fecc9c239bd4d7ff024f459cc19f9475ca4eaa`. Ele reúne os oito commits do módulo e os arquivos de configuração, teste, CI, ADR e README inspecionados.

A [Issue #3 — Configurar o ambiente inicial de desenvolvimento](https://github.com/dscalexandre/banking-fraud-data-ingestor/issues/3) foi fechada pelo PR #4; seus critérios de aceite estão concluídos e correspondem ao escopo entregue. Os checks obrigatórios do workflow `CI` concluíram com sucesso: `Quality` e `Tests (3.12)`.

## Documentação oficial

| Tecnologia ou componente | Aplicação no módulo | Fonte oficial |
|---|---|---|
| Python 3.12 | Versão única aceita pelo projeto e pela CI. | [Documentação do Python 3.12](https://docs.python.org/3.12/) |
| Poetry | Dependências, ambiente virtual, lock e execução dos comandos. | [Uso básico do Poetry](https://python-poetry.org/docs/basic-usage/) |
| Ruff | Análise estática no job de qualidade e no comando local. | [Documentação do Ruff](https://docs.astral.sh/ruff/) |
| pytest | Execução do teste smoke localmente e na CI. | [Documentação do pytest](https://docs.pytest.org/en/stable/) |
| GitHub Actions | Automação de qualidade e testes para pull requests e `main`. | [Build e testes Python no GitHub Actions](https://docs.github.com/en/actions/tutorials/build-and-test-code/python) |
