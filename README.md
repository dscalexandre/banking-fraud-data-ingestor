![Banking Fraud Data Ingestor](docs/assets/banking-fraud-data-ingestor.png)

# Banking Fraud Data Ingestor

## Objetivo

O projeto implementa o primeiro módulo de uma plataforma real de detecção de fraudes, responsável pela ingestão batch, captura de alterações (CDC) e eventos em streaming até sua entrega oficial no Amazon S3 ou no Apache Kafka gerenciado pela Confluent Cloud.

A arquitetura foi concebida para separar claramente as responsabilidades entre configuração da aplicação, infraestrutura, código da aplicação, infraestrutura como código (IaC), contratos de dados, observabilidade, segurança e automação por meio de pipelines de CI/CD, favorecendo a evolução, a manutenção e a operação independente de cada fluxo de ingestão.

## Arquitetura

Consultar o [desenho da solução](docs/architecture/solution-design.md), que
constitui a referência arquitetural para o desenvolvimento do projeto.

## Tecnologias

- Python
- Poetry
- PostgreSQL
- Debezium
- Apache Kafka
- Kafka Connect
- Confluent Cloud
- AWS Lambda
- Amazon S3
- Docker
- Terraform
- GitHub Actions

## Pré-requisitos

- Python `>=3.12,<3.13`
- Poetry 2.x
- Git

## Preparação do ambiente

Configurar o ambiente virtual dentro do projeto:

```bash
poetry config virtualenvs.in-project true
```

Instale as dependências:

```bash
poetry install
```

Validar a configuração:

```bash
poetry check
```

Executar o lint:

```bash
poetry run ruff check .
```

Executar os testes:

```bash
poetry run pytest
```

## Status

Projeto preparado para iniciar o primeiro incremento funcional de produção pelo fluxo
`countries`, com governança, referência arquitetural, CI e ambiente local estabelecidos;
a infraestrutura produtiva ainda não foi provisionada nesta etapa.

## Contribuição

Este projeto não está aceitando contribuições externas no momento. As diretrizes serão publicadas quando o projeto estiver preparado para colaboração.

## Licença

Este projeto está licenciado sob a licença MIT. Consultar [LICENSE](LICENSE).
