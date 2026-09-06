![Banking Fraud Data Ingestor](docs/assets/banking-fraud-data-ingestor.png)

# Banking Fraud Data Ingestor

## Objetivo

O projeto implementa o primeiro módulo de uma plataforma real de detecção de fraudes, responsável pela ingestão batch, captura de alterações (CDC) e eventos em streaming até sua entrega oficial no Amazon S3 ou no Apache Kafka gerenciado pela Confluent Cloud.

A arquitetura foi concebida para separar claramente as responsabilidades entre configuração da aplicação, infraestrutura, código da aplicação, infraestrutura como código (IaC), contratos de dados, observabilidade, segurança e automação por meio de pipelines de CI/CD, favorecendo a evolução, a manutenção e a operação independente de cada fluxo de ingestão.

## Estado do projeto

Projeto em estruturação inicial para o primeiro incremento funcional de produção, começando pelo fluxo `countries`; os componentes produtivos ainda não estão implementados nesta etapa de governança.

## Contribuição

Este projeto não está aceitando contribuições externas no momento. As diretrizes serão publicadas quando o projeto estiver preparado para colaboração.
