# Desenho da Solução de Ingestão de Dados Bancários

## Conteúdo de referência arquitetural permanente

As seções desta parte definem o escopo e o desenho de alto nível do sistema.
Elas devem permanecer em `docs/architecture/solution-design.md`, mesmo que outros detalhes
sejam especializados em contratos, runbooks ou documentação operacional.

## 1. Contexto, objetivo e fronteiras

**Local recomendado:** `docs/architecture/solution-design.md`.

O projeto `banking-fraud-data-ingestor` implementa o primeiro módulo de uma plataforma real de detecção de fraudes. Sua responsabilidade termina na entrega oficial e verificável dos dados no Amazon S3 ou no Apache Kafka gerenciado no Confluent Cloud. Os destinos no Databricks aparecem apenas como referência downstream e não fazem parte do escopo operacional deste repositório.

Sob a perspectiva da Engenharia de Dados moderna, o projeto incorpora os principais pilares adotados em plataformas corporativas, incluindo ingestão batch e streaming, contratos de dados, qualidade, observabilidade, recuperação, segurança, testes, documentação e arquitetura orientada a eventos.

A arquitetura foi concebida com uma clara separação de responsabilidades entre **configuração da aplicação**, **infraestrutura**, **código da aplicação**, **infraestrutura como código (IaC)**, **workflows e pipelines de CI/CD**, **captura de mudanças (CDC)** e **orquestração dos fluxos de ingestão**, favorecendo a manutenção, a evolução, os testes e a operação independente de cada fluxo de ingestão.

O desenvolvimento pode utilizar ferramentas de assistência baseadas em inteligência artificial para apoiar revisão, refatoração, documentação e automação, sempre com validação técnica e aderência às práticas de engenharia do projeto.

A solução prevê a validação e entrega dos arquivos batch, a carga de clientes no Amazon RDS for PostgreSQL, a captura de alterações por meio do Confluent Cloud PostgreSQL CDC Source Connector gerenciado e baseado em Debezium, e a publicação das transações por meio da AWS Lambda, consolidando os principais fluxos operacionais previstos para o módulo.

### 1.1 Estratégia de implantação inicial

O primeiro incremento será um **vertical slice mínimo de produção**, começando pelo fluxo de `countries`. O escopo
funcional deve nascer com controles reais de segurança,
idempotência, observabilidade, recuperação, testes, infraestrutura como código e
implantação protegida.

Somente o ambiente `prod` será provisionado inicialmente. A infraestrutura deve ser
composta por módulos Terraform reutilizáveis e por um root module exclusivo de produção,
permitindo adicionar futuramente `dev` e `staging` sem reorganizar o repositório nem
alterar a identidade dos recursos produtivos.

Produção não poderá depender de estados, outputs ou recursos de ambientes futuros. A
relação entre ambientes, quando existirem, ocorrerá pela promoção do mesmo commit e do
mesmo artefato versionado no pipeline, mantendo contas, credenciais, dados e estados
Terraform isolados.

Os diretórios de ambientes ainda inexistentes não devem ser criados apenas como
placeholders. O suporte futuro será preservado pela separação entre `modules/` e
`environments/prod/` e pela parametrização explícita de `environment`.

## 2. Arquitetura dos fluxos de ingestão

Após o bootstrap seguro da conta e do repositório, os fluxos devem ser implementados e
colocados em produção na ordem apresentada nesta seção. Cada fluxo só avança quando seus
critérios de operação, reconciliação e recuperação estiverem atendidos. A sequência começa
por `countries`, reutiliza sua fundação em `fraud_report`, avança para o CDC de clientes e
termina com o fluxo de transações em streaming.

### 2.1 Países

```text
countries.csv
      │
      ▼
S3 Incoming Zone
(upload concluído e identificado)
      │
      ▼ evento S3 filtrado pelo prefixo incoming/countries/
AWS Lambda Countries Ingestor
      │
      ▼
Validação batch
(contrato, contagem, unicidade, checksum e idempotência)
      │
      ├── inválido ──► S3: quarantine/countries/
      │               + relatório de validação
      │
      ▼
S3 Landing Zone
(publicação oficial do arquivo original + manifesto de ingestão)
      │
      ▼
Databricks
(country_coordinates)
```

O fluxo será considerado apto para produção somente quando possuir contrato executável,
identificação idempotente, publicação sem exposição de arquivos parciais, manifesto,
quarentena, reconciliação, logs estruturados, métricas, alarmes, smoke test e runbooks de
falha e replay. Uma sugestão de identidade de ingestão é a composição de dataset, checksum
do conteúdo e versão do contrato.

A execução inicial será orientada a evento: a criação concluída de um objeto em
`incoming/countries/` acionará uma AWS Lambda empacotada como artefato imutável. O filtro
do evento deve impedir acionamentos pelos prefixos de saída. O controle durável de
idempotência deve registrar o estado da ingestão antes da entrega oficial, evitando que
reentregas do evento S3 publiquem o mesmo conteúdo novamente. Limites de tamanho e tempo
da Lambda devem ser documentados; sua substituição futura por outro executor não poderá
alterar o contrato nem o layout da landing zone.

### 2.2 Ocorrências de fraude

```text
fraud_report/*.csv
      │
      ▼
Validação de CSV, esquema, contagem, IDs e checksum
      │
      ├── inválido ──► Amazon S3 (prefixo: quarantine/fraud_report/)
      │                + relatório de validação
      │
      ▼
Amazon S3 Landing Zone
(arquivos originais + manifesto de ingestão)
      │
      ▼
Databricks
(fraud_reports)
```

### 2.3 Clientes

```text
customers.csv
└── Validação de esquema, unicidade e chave primária
    │
    └── Amazon RDS for PostgreSQL
        │
        ├── Tabela customers
        │
        ├── Chave primária
        │   └── customers.id
        │
        ├── Replicação lógica habilitada
        │
        └── PostgreSQL WAL
            │
            └── Confluent Cloud PostgreSQL CDC Source Connector
                └── Conector gerenciado baseado em Debezium
                    │
                    ├── Captura dos eventos
                    │   │
                    │   ├── Snapshot inicial
                    │   │   └── Eventos READ do estado inicial
                    │   │
                    │   └── CDC contínuo
                    │       ├── INSERT
                    │       ├── UPDATE
                    │       └── DELETE
                    │
                    └── Tratamento e publicação
                        │
                        ├── Chave Kafka
                        │   └── customers.id
                        │
                        ├── Falha transitória
                        │   └── Retry automático
                        │
                        ├── Falha permanente
                        │   ├── Logs e métricas
                        │   ├── Alerta operacional
                        │   └── Conector interrompido
                        │
                        └── Publicação bem-sucedida
                            └── Confluent Cloud
                                └── Cluster Kafka gerenciado
                                    └── fraud.customers.cdc.v1
                                        │
                                        ├── Amazon S3 Sink Connector
                                        │   └── archive/customers/cdc/
                                        │
                                        └── Databricks Structured Streaming
                                            └── banking_customers
```

O fluxo de clientes depende da replicação lógica do Amazon RDS for PostgreSQL e da conectividade segura entre o banco e o conector gerenciado da Confluent Cloud. Credenciais devem ser mantidas em serviço de segredos e nunca versionadas no repositório.

### 2.4 Transações

```text
transactions/*.json
      │
      ▼
AWS Lambda Producer
      │
      ▼
Apache Kafka gerenciado pela Confluent Cloud
(Tópico: fraud.transactions.v1)
      │
      ├── erro permanente ──► Tópico DLQ: fraud.transactions.dlq.v1
      ├──► Databricks Structured Streaming ──► bronze_transactions
      └──► Amazon S3 (prefixo: archive/transactions/events/)
```

## 3. Organização e estrutura-alvo do repositório

```text
banking-fraud-data-ingestor/
├── .agents/                        # skills reutilizáveis dos agentes Codex
│   └── skills/
│       ├── learning-documenter/
│       │   ├── SKILL.md            # fluxo de documentação de aprendizagem
│       │   └── assets/             # recurso/template estático empacotado da skill
│       │       └── module-learning.md
│       ├── technical-documenter/
│       │   └── SKILL.md            # documentação técnica afetada por cada módulo
│       ├── module-builder/
│       │   └── SKILL.md            # construção completa de um módulo por vez
│       ├── module-reviewer/
│       │   └── SKILL.md            # revisão independente do módulo construído
│       ├── batch-ingestor/
│       │   └── SKILL.md            # fluxo batch, quarentena, manifestos e relatórios
│       ├── customers-cdc-ingestor/
│       │   └── SKILL.md            # carga de clientes, RDS e CDC gerenciado
│       └── transactions-dlq-replayer/
│           └── SKILL.md            # publicação, retry, replay e DLQ de transações
│
├── .codex/
│   └── agents/                      # perfis dos agentes no OpenAI Codex
│       ├── learning-documenter.toml
│       ├── technical-documenter.toml
│       ├── module-builder.toml
│       ├── module-reviewer.toml
│       ├── batch-ingestor.toml
│       ├── customers-cdc-ingestor.toml
│       └── transactions-dlq-replayer.toml
│
├── .github/
│   ├── CODEOWNERS                  # aprovação das áreas críticas e de produção
│   └── workflows/
│       ├── ci.yml                  # qualidade, contratos, testes e build do artefato
│       ├── security.yml            # segredos, dependências, código e IaC
│       ├── terraform-plan.yml      # plan obrigatório e publicável para revisão
│       ├── deploy-production.yml   # apply/deploy aprovado no GitHub Environment production
│       └── ingest-countries.yml    # execução/replay manual protegido do primeiro fluxo
│
├── .vscode/
│   └── settings.json
│
├── config/
│   ├── application/
│   │   ├── base.yaml               # comportamento comum, sem segredos
│   │   └── prod.yaml               # parâmetros não sensíveis de produção
│   ├── confluent/
│   │   └── customers-postgresql-cdc-source.json # parâmetros não sensíveis do conector gerenciado
│   ├── observability/
│   │   ├── alarms.yaml
│   │   └── slos.yaml
│   └── logging.yaml
│
├── contracts/                      # contratos executáveis e versionados
│   ├── batch/
│   │   ├── countries.schema.json
│   │   ├── customers.schema.json
│   │   └── fraud-report.schema.json
│   ├── kafka/
│   │   ├── customers-cdc.schema.json
│   │   ├── transactions.schema.json
│   │   └── dlq-envelope.schema.json
│   └── manifests/
│       ├── ingestion-manifest.schema.json
│       └── validation-report.schema.json
│
├── data/
│   └── raw/
│       └── .gitkeep
│
├── docs/
│   ├── architecture/
│   │   └── solution-design.md
│   ├── assets/
│   │   └── banking-fraud-data-ingestor.png
│   ├── adr/
│   │   └── ADR-001-adotar-poetry.md
│   ├── learning/
│   │   └── modules/                # destino final documentado pela skill
│   │       └── 01-initial-project-setup.md
│   ├── runbooks/
│   │   ├── connector-failure.md
│   │   ├── transactions-dlq-reprocessing.md
│   │   └── replay-recovery.md
│   ├── contracts.md
│   ├── landing-zone.md
│   └── operations.md
│
├── infrastructure/
│   └── terraform/
│       ├── bootstrap/
│       │   ├── backend/             # estado remoto, locking, criptografia e versionamento
│       │   └── github-oidc/         # autenticação temporária do pipeline na AWS
│       ├── modules/
│       │   ├── s3-landing-zone/     # incoming, landing, quarentena, manifestos e relatórios
│       │   ├── security/            # KMS e IAM de privilégio mínimo
│       │   ├── observability/       # logs, métricas, dashboards e alarmes
│       │   ├── budgets/             # orçamento e alertas básicos de custo
│       │   ├── countries-ingestor/  # Lambda, evento S3 e permissões do primeiro fluxo
│       │   ├── ingestion-control/   # estado durável de idempotência e execução
│       │   ├── rds-postgresql/      # banco de origem e replicação lógica de customers
│       │   ├── lambda-producer/     # producer Kafka do fluxo transactions
│       │   └── confluent-ingestion/ # Kafka, tópicos, CDC, ACLs e S3 Sinks
│       └── environments/
│           └── prod/               # único root ativo inicialmente; estado isolado
│               ├── backend.tf
│               ├── main.tf
│               ├── outputs.tf
│               ├── providers.tf
│               ├── variables.tf
│               ├── versions.tf
│               ├── backend.hcl.example
│               └── terraform.tfvars.example
│
├── output/                         # evidências operacionais não versionadas
│   ├── checkpoints/
│   ├── logs/
│   ├── manifests/
│   ├── reports/
│   └── validations/
│
├── scripts/                        # utilitários operacionais que não duplicam regras da aplicação
│   ├── simulate_customer_changes.py
│   └── validate_environment.py
│
├── src/lfi/
│   ├── cli.py                      # entrada única para os comandos operacionais
│   ├── application/                # coordenação dos quatro fluxos de ingestão
│   │   ├── ingest_batch.py
│   │   ├── load_customers.py
│   │   ├── replay_transactions.py
│   │   └── reprocess_transactions_dlq.py
│   ├── batch/
│   │   ├── countries.py
│   │   ├── fraud_report.py
│   │   ├── manifest.py
│   │   ├── quarantine.py
│   │   └── s3_delivery.py
│   ├── customers/
│   │   ├── loader.py
│   │   └── validator.py
│   ├── contracts/
│   │   ├── registry.py
│   │   └── validator.py
│   ├── dlq/
│   │   ├── envelope.py
│   │   ├── publisher.py
│   │   └── retry.py
│   ├── checkpoints/
│   │   ├── base.py
│   │   └── dynamodb.py
│   ├── transactions/
│   │   ├── reader.py
│   │   └── replay.py
│   ├── producers/
│   │   └── lambda_handler.py       # AWS Lambda Producer
│   ├── handlers/
│   │   └── countries.py            # adapter AWS Lambda do primeiro fluxo
│   ├── manifests/
│   │   ├── ingestion.py
│   │   └── validation_report.py
│   └── shared/
│       ├── config.py
│       ├── errors.py
│       ├── idempotency.py
│       ├── logging.py
│       ├── metrics.py
│       ├── retry.py
│       └── tracing.py
│
├── tests/
│   ├── contract/
│   ├── e2e/
│   │   ├── test_countries_flow.py
│   │   ├── test_customers_cdc_flow.py
│   │   ├── test_fraud_report_flow.py
│   │   └── test_transactions_replay_flow.py
│   ├── integration/
│   │   └── cloud/                  # AWS e Confluent, execução manual ou protegida
│   ├── unit/
│   └── test_smoke.py               # validação mínima do ambiente
│
├── .editorconfig
├── .env.example
├── .gitignore
├── AGENTS.md                       # instruções globais dos agentes Codex
├── Dockerfile                      # build reproduzível do artefato de execução
├── LICENSE
├── Makefile
├── poetry.lock
├── pyproject.toml
└── README.md
```

Essa árvore representa a direção arquitetural e não declara que os componentes já
existem. A implementação deve criar primeiro apenas os componentes transversais e os do
fluxo `countries`; os componentes de `fraud_report`, clientes, CDC e transações entram nos
incrementos correspondentes. Todos os diretórios de pacotes Python deverão conter
`__init__.py`.

O `AGENTS.md` da raiz centraliza as instruções globais de contexto, comandos,
convenções, restrições e critérios de conclusão aplicáveis a todo o repositório.
Essa centralização fornece as instruções comuns a todos os agentes Codex sem
duplicá-las nos perfis especializados nem nas skills.

As skills em `.agents/skills/` concentram os procedimentos reutilizáveis
dos agentes Codex, com recursos auxiliares carregados somente quando necessários.
A skill `learning-documenter` mantém seu template em `assets/module-learning.md`.
Os arquivos em `.codex/agents/` definem os sete perfis especializados do Codex;
cada perfil delimita seu papel e referencia a skill correspondente sem repetir
o procedimento nem as regras globais do `AGENTS.md`.

## 4. Componentes da solução

Os componentes abaixo representam responsabilidades previstas no estado-alvo
da solução e não indicam que suas implementações já estejam disponíveis.

| Área                                                    | Responsabilidade prevista                                                       |
| ------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `.agents/skills/`                                       | procedimentos reutilizáveis dos agentes Codex                                  |
| `.codex/agents/`                                        | perfis dos sete agentes no OpenAI Codex                                         |
| `.codex/agents/learning-documenter.toml`                | perfil responsável pela documentação de aprendizagem de módulos integrados     |
| `.codex/agents/module-builder.toml`                     | perfil responsável pela construção de cada módulo                              |
| `.codex/agents/technical-documenter.toml`               | perfil responsável pela documentação técnica afetada por cada módulo           |
| `.codex/agents/module-reviewer.toml`                    | perfil responsável pela revisão independente de cada módulo construído         |
| `.github/workflows/`                                    | CI, segurança, plan e deploy aprovado no ambiente protegido `production`       |
| `AGENTS.md`                                             | instruções globais aplicáveis aos agentes Codex                             |
| `config/`                                               | comportamento da aplicação e parâmetros não sensíveis dos serviços gerenciados |
| `contracts/`                                            | esquemas executáveis das fontes, eventos, DLQ, manifestos e relatórios          |
| `docs/assets/`                                          | imagem de capa e demais recursos visuais versionados da documentação pública    |
| `infrastructure/terraform/bootstrap/`                   | backend remoto e identidade OIDC do pipeline                                   |
| `infrastructure/terraform/modules/`                     | módulos reutilizáveis, sem valores fixos de ambiente                            |
| `infrastructure/terraform/modules/confluent-ingestion/` | Kafka, PostgreSQL CDC Source, tópicos, DLQ, ACLs e S3 Sink Connectors            |
| `infrastructure/terraform/environments/prod/`           | único root ativo inicialmente, com backend e estado próprios                   |
| `scripts/`                                              | validação do ambiente e simulação controlada de alterações de clientes         |
| `src/lfi/cli.py`                                        | entrada única para batch, carga de clientes, replay e reprocessamento de DLQ   |
| `src/lfi/application/`                                  | coordenação mínima dos quatro fluxos, sem regras duplicadas                    |
| `src/lfi/batch/`                                        | validação, checksum, manifesto e envio ao S3                                   |
| `src/lfi/customers/`                                    | validação e carga do CSV no Amazon RDS for PostgreSQL                          |
| `src/lfi/transactions/`                                 | leitura JSON Lines, cadência e replay                                          |
| `src/lfi/producers/`                                    | handler do AWS Lambda Producer                                                 |
| `src/lfi/checkpoints/`                                  | contrato de checkpoint e armazenamento durável da Lambda                       |
| `src/lfi/dlq/`                                          | envelope, publicação e reprocessamento de transações permanentemente inválidas |
| `tests/`                                                | testes unitários, contratuais, de integração e E2E essenciais                  |

### 4.1 Isolamento e promoção de ambientes

O ambiente `prod` deve utilizar estado Terraform remoto próprio, credenciais próprias,
recursos nomeados e etiquetados com o ambiente e proteção contra exclusão nos componentes
que mantêm dados. Segredos reais permanecem no serviço de segredos e nos environments do
pipeline; nunca em `config/`, `.env`, `terraform.tfvars` ou no estado exibido em logs.

Quando `dev` e `staging` forem necessários, serão adicionados como novos root modules:

```text
infrastructure/terraform/environments/
├── dev/
├── staging/
└── prod/
```

Cada root consumirá os mesmos módulos, mas terá backend, estado, conta ou fronteira de
acesso, chaves, dados e capacidade independentes. Não deve haver referência de
`terraform_remote_state` entre ambientes operacionais. A promoção será feita pelo CI/CD,
usando o mesmo artefato imutável identificado por versão, commit e digest.

### 4.2 Controles mínimos comuns aos fluxos

Os controles desta seção são requisitos arquiteturais para todos os fluxos. Sua presença
no documento não significa que todos já estejam implementados. Cada incremento somente
será considerado apto para produção quando demonstrar, dentro do próprio escopo:

- infraestrutura provisionada por Terraform e protegida por revisão de `plan`;
- autenticação do pipeline por OIDC, sem chaves permanentes de acesso à AWS;
- criptografia em trânsito e em repouso e bloqueio de acesso público;
- IAM, ACLs e demais autorizações com privilégio mínimo e segregação entre implantação e execução;
- contratos de dados executáveis, versionados e com política de compatibilidade definida;
- processamento idempotente e estado durável para recuperação após falhas;
- artefato imutável, versionado e implantado sem rebuild durante a promoção;
- logs estruturados com `run_id` e `ingestion_id`, métricas, dashboards e alarmes acionáveis;
- reconciliação entre origem, processamento, manifesto ou checkpoint e entrega oficial;
- retenção, descarte, replay, backup e recuperação definidos de acordo com o fluxo;
- testes unitários, contratuais, de integração, E2E, resiliência e smoke test pós-deploy;
- runbooks objetivos para falha, replay, rollback, recuperação e intervenção manual;
- responsáveis operacionais, SLOs e critérios verificáveis de sucesso documentados.

### 4.3 Controles de `countries` — incremento atual

O primeiro incremento funcional de produção deve entregar:

- S3 com versionamento, lifecycle e zonas `incoming`, `landing`, `quarantine`, `manifests` e `validation-reports`;
- Lambda acionada somente por objetos concluídos no prefixo `incoming/countries/`;
- proteção contra acionamentos recursivos causados pelos prefixos de saída;
- validação de CSV, esquema, cabeçalho, tipos, contagem e unicidade dos códigos de país;
- checksum do arquivo e identidade composta por dataset, checksum e versão do contrato;
- controle durável de idempotência para suportar a reentrega de eventos do S3;
- publicação do arquivo original na landing zone ou envio à quarentena com relatório;
- manifesto associado à entrega oficial e reconciliação por arquivo e quantidade de registros;
- limites suportados de tamanho e tempo de processamento documentados;
- alarmes para falha, quarentena, ausência de processamento e divergência de reconciliação;
- runbooks específicos de falha, quarentena, replay e recuperação do fluxo.

### 4.4 Controles de `fraud_report` — incremento planejado

Além dos controles comuns, o fluxo deverá possuir:

- processamento controlado de múltiplos arquivos e identificação do lote de origem;
- detecção de arquivos ausentes, incompletos, repetidos ou recebidos fora da janela esperada;
- validação de CSV, esquema, contagem, IDs e compatibilidade com as transações;
- checksum e idempotência por arquivo, com estado consolidado do lote quando aplicável;
- manifesto e reconciliação da quantidade de arquivos e registros do lote;
- quarentena que preserve o arquivo original, o motivo da rejeição e o relatório de validação;
- replay seguro de um arquivo ou lote sem duplicar entregas já concluídas;
- alarmes de atraso, falha, quarentena e divergência de reconciliação.

### 4.5 Controles de `customers` — incremento planejado

Além dos controles comuns, o fluxo deverá possuir:

- validação de esquema, chave primária e unicidade antes da carga no PostgreSQL;
- carga transacional e repetível, com estratégia explícita de `insert`, `upsert` ou staging;
- rollback ou recuperação segura quando uma carga for concluída apenas parcialmente;
- replicação lógica, publication e replication slot configurados e monitorados;
- snapshot inicial e retomada do CDC com comportamento conhecido e testado;
- contratos para chaves, envelopes CDC, inserts, updates, deletes e tombstones;
- ordenação por chave e política de compatibilidade de schema no Kafka;
- monitoramento do connector, do atraso do CDC, do replication slot e da retenção do WAL;
- tratamento separado para falhas transitórias e permanentes, com alertas acionáveis;
- reconciliação entre tabela de origem, eventos publicados, offsets e arquivo no S3;
- procedimento testado para reiniciar o connector ou refazer o snapshot sem perda silenciosa.

### 4.6 Controles de `transactions` — incremento planejado

Além dos controles comuns, o fluxo deverá possuir:

- definição explícita da origem dos arquivos, formato JSON Lines, trigger e limites operacionais;
- validação do contrato antes da publicação e uso do `id` como chave Kafka;
- producer com `acks=all`, idempotência quando suportada, retry limitado e confirmação de entrega;
- avanço do checkpoint somente depois da confirmação da publicação;
- controle de backpressure, concorrência, batching, timeouts e reutilização de conexões;
- classificação objetiva de erros transitórios e permanentes;
- DLQ com payload original, chave, versão do contrato, motivo, tentativa e contexto do erro;
- replay idempotente com limite de tentativas e proteção contra ciclos entre origem e DLQ;
- reconciliação entre eventos lidos, publicados, rejeitados, arquivados e registrados no checkpoint;
- métricas e alarmes de throughput, latência, falhas, atraso, checkpoint e crescimento da DLQ.

### 4.7 Construção, documentação e revisão dos módulos por agentes Codex

Cada módulo será conduzido por três agentes Codex com responsabilidades
separadas:

- `module-builder` implementa um módulo por vez conforme o escopo aprovado,
  incluindo código, infraestrutura, contratos e testes aplicáveis, e identifica
  a documentação técnica afetada;
- `technical-documenter` cria, atualiza ou revisa, no mesmo Pull Request, somente
  a documentação técnica afetada pelo módulo, incluindo README, docstrings de
  interfaces públicas não óbvias, contratos, configuração, ADRs, runbooks e
  guias de migração quando aplicáveis. O agente usa código, testes, contratos,
  configurações e decisões registradas como evidência, não altera a implementação
  e não cria documentação de aprendizagem;
- `module-reviewer` revisa de forma independente o módulo entregue, verificando
  também a consistência da documentação técnica com o comportamento implementado.
  Primeiro, verifica se o módulo corresponde exatamente ao próximo incremento previsto e se
  nenhum diretório, arquivo, contrato, workflow, infraestrutura, ambiente ou
  stub de módulos posteriores foi antecipado. Essa verificação de fronteira é
  sua finalidade; ele não atua como revisor genérico de Pull Requests.

A ordem funcional dos incrementos é `countries`, `fraud_report`,
`customers`/CDC e `transactions`. O próximo módulo deve ser determinado pela
comparação entre essa sequência e o estado realmente implementado na base do
Pull Request. A estrutura-alvo não autoriza sua materialização antecipada: cada
entrega cria somente os componentes peculiares ao módulo atual e os fundamentos
transversais indispensáveis ao seu funcionamento completo e verificável.

O `module-builder` deve entregar ao `technical-documenter` o escopo executado,
os arquivos alterados, as validações realizadas, os resultados obtidos e os
riscos ou desvios conhecidos. O `technical-documenter` deve registrar os
documentos alterados e eventuais divergências encontradas sem corrigir o código.
Em seguida, essas evidências são entregues ao `module-reviewer`, que não deve presumir que a seleção do
módulo nem a validação do construtor são suficientes: deve determinar o próximo
módulo de forma independente, comparar as árvores anterior e resultante,
classificar os caminhos alterados e executar verificações somente leitura
proporcionais ao risco e à fronteira arquitetural.

A revisão deve resultar em aprovação objetiva, reprovação por módulo incorreto,
incompleto, documentalmente inconsistente ou com avanço de escopo, ou impedimento
quando não houver um único próximo módulo comprovável. Pendências de implementação
retornam ao `module-builder`; pendências exclusivamente documentais retornam ao
`technical-documenter`. Depois das correções, o módulo passa por nova revisão. O
mesmo agente não pode construir e aprovar sozinho o mesmo módulo.

---

## Conteúdo que poderá ser especializado futuramente

As seções desta parte permanecem na arquitetura enquanto forem a visão
consolidada da solução. Quando os detalhes operacionais e contratuais
amadurecerem, eles poderão ser extraídos para os locais indicados sem remover
da arquitetura os respectivos resumos e links.

## 5. Entregas, destinos e recuperação

### 5.1 Entregas oficiais e consumo downstream

**Local recomendado para detalhamento:** `docs/landing-zone.md` para entregas
no S3 e `docs/contracts.md` para tópicos, eventos e consumidores.

| Conjunto de dados | Entrega oficial                                                       | Cópia secundária                     | Consumo downstream                             |
| -------------- | ------------------------------------------------------------------------ | ------------------------------------ | ---------------------------------------------- |
| `countries`    | `landing/reference/countries/` no S3                                     | Manifesto e relatório de validação   | Databricks: `country_coordinates`              |
| `customers`    | `fraud.customers.cdc.v1` no Apache Kafka gerenciado pela Confluent Cloud | `archive/customers/cdc/` no S3       | Databricks: `banking_customers` com SCD Tipo 2 |
| `fraud_report` | `landing/fraud_report/batch/` no S3                                      | Não se aplica                        | Databricks: `fraud_reports`                    |
| `transactions` | `fraud.transactions.v1` no Apache Kafka gerenciado pela Confluent Cloud  | `archive/transactions/events/` no S3 | Databricks: `bronze_transactions`              |

### 5.2 Tratamento de falhas e recuperação

**Local recomendado para detalhamento:** `docs/runbooks/`.

| Tipo de falha                                | Conjunto de dados | Destino                                                        |
| -------------------------------------------- | -------------- | ----------------------------------------------------------------- |
| Arquivo batch estruturalmente inválido       | `countries`    | `quarantine/countries/` no S3 + relatório de validação            |
| Arquivo batch estruturalmente inválido       | `fraud_report` | `quarantine/fraud_report/` no S3 + relatório de validação         |
| Falha transitória no conector de origem       | `customers`    | Retry sem avanço do offset + logs e métricas                      |
| Falha permanente no conector de origem        | `customers`    | Conector interrompido + logs, métricas e alerta operacional       |
| Evento de transação permanentemente inválido | `transactions` | `fraud.transactions.dlq.v1` no Kafka                              |
| Falha transitória de publicação              | `transactions` | Retry sem avanço do checkpoint                                    |

## 6. Contratos de dados das fontes

**Local recomendado para detalhamento:** contratos executáveis em `contracts/`
e orientação humana complementar em `docs/contracts.md`.

Os dados devem ser validados e transportados sem transformação.

| Conjunto de dados | Formato                | Campos ou regras essenciais                                                       |
| -------------- | ------------------------- | --------------------------------------------------------------------------------- |
| `countries`    | CSV                       | esquema esperado, contagem, códigos únicos e checksum                              |
| `customers`    | CSV com campos multilinha | esquema esperado; `id` obrigatório, único e chave primária no PostgreSQL           |
| `fraud_report` | CSV                       | esquema esperado, contagem, IDs e checksum; compatibilidade de `id` com transações |
| `transactions` | JSON Lines                | campos da origem; `id` obrigatório e usado como chave Kafka                       |

`step` permanece numérico e não representa um timestamp. Não deve ser criado `customer_id`: a fonte utiliza `nameOrig` e `nameDest`. Metadados operacionais ficam em headers Kafka, manifestos ou checkpoints, nunca no payload.

## 7. Integração Kafka e arquivamento no S3

**Local recomendado para detalhamento:** `docs/contracts.md` para eventos e
tópicos Kafka, `docs/landing-zone.md` para prefixos e arquivamento no S3, e
`infrastructure/` para a configuração executável.

A solução requer estes tópicos:

| Tópico                      | Chave             |
| --------------------------- | ----------------- |
| `fraud.transactions.v1`     | `id` da transação |
| `fraud.customers.cdc.v1`    | `id` do cliente   |
| `fraud.transactions.dlq.v1` | chave original    |

Partições, retenção e capacidade devem começar com valores mínimos de produção,
documentados a partir do volume conhecido e acompanhados por métricas e alarmes que
permitam recalibração segura. O producer deve usar `acks=all`, idempotência quando
suportada, tentativas limitadas e confirmação antes do avanço do checkpoint.

Os Amazon S3 Sink Connectors devem preservar JSON nos prefixos:

```text
archive/customers/cdc/
archive/transactions/events/
```

Falhas do arquivamento não devem interromper o consumo Kafka → Databricks.
