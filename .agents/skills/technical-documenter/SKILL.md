---
name: technical-documenter
description: >-
  Criar ou atualizar a documentação técnica afetada por uma implementação em
  Pull Request aberto, a partir de solicitação em linguagem natural ou entrada
  estruturada. Usar para README, interfaces públicas, contratos, configuração,
  ADRs, runbooks e migrações aplicáveis. Não usar para implementar código.
---

# Documentar tecnicamente uma implementação

## Entrada e normalização

Aceite uma solicitação em linguagem natural, por exemplo:

```text
Atualize a documentação técnica da entrega da Issue #42 no Pull Request #57
para os operadores. Não altere a implementação.
```

Ou pela descrição da Issue:

```text
Crie a documentação técnica da entrega que adiciona a ingestão de alertas de
fraude para os operadores. Não altere a implementação.
```

Aceite também esta forma estruturada:

```text
Issue: <número ou URL>
Pull Request: <número ou URL>
Operação: criar | atualizar (opcional)
Público: <um ou mais públicos, opcional>
```

- Nas duas formas, identifique uma `Issue` e um `Pull Request` da mesma entrega.
  Na linguagem natural, aceite números, URLs, referências inequívocas no
  contexto da tarefa ou a descrição do resultado, escopo ou título da Issue.
  Neste último caso, localize a Issue cuja descrição corresponda à solicitação
  e o Pull Request associado; se não houver uma correspondência única, peça
  esclarecimento sem modificar arquivos.
- Na forma estruturada, `Issue` e `Pull Request` são obrigatórios. `Operação`
  pode ser omitida quando o agente puder determiná-la sem ambiguidade pelo
  estado atual da documentação.
- Em linguagem natural, infira `criar` ou `atualizar` pelos verbos e pelo estado
  da documentação. Quando a inferência não for inequívoca, peça esclarecimento
  antes de modificar arquivos. Se as duas formas forem combinadas, exija que
  sejam coerentes.
- `Público` é opcional. Quando omitido, considerar todos os públicos afetados e
  adequar cada documento ao seu leitor principal, sem criar conteúdo apenas
  para cobrir todos eles. Quando informado explicitamente na entrada ou no
  contexto da tarefa, adequar linguagem, exemplos e nível de detalhe ao público
  solicitado sem omitir contratos, riscos ou procedimentos essenciais.

## Condições para atuar

1. Ler e cumprir o `AGENTS.md`.
2. Normalizar a solicitação e confirmar que a Issue e o Pull Request tratam de
   uma entrega funcional coesa e delimitada e que o PR está aberto, não é
   rascunho e corresponde à branch atual.
3. Recusar Pull Requests de governança, manutenção genérica ou documentação de
   aprendizagem. Pull Requests de configuração de agentes são elegíveis somente
   quando a alteração exigir documentação técnica verificável de arquitetura,
   operação, interfaces, configuração ou recuperação.
4. Ler `docs/architecture/solution-design.md`, a Issue, o diff completo do PR e
   as fontes de verdade aplicáveis.
5. Atuar quando o comportamento estiver verificável e antes da aprovação final
   e do merge. Se commits posteriores alterarem comportamento, contratos,
   configuração ou operação, reavaliar o impacto documental.
6. Se o comportamento implementado, os documentos afetados ou as evidências não
   puderem ser determinados, não modificar arquivos e relatar o impedimento. Se
   apenas o público for ambíguo, usar o público principal do documento existente
   e registrar a suposição.

## Documentação aplicável

Documentar somente o que a mudança exigir:

- `README.md` e guias de uso: propósito, instalação, configuração e execução;
- docstrings e comentários: contrato de módulos, classes, funções e métodos
  públicos quando intenção, parâmetros, retorno, exceções ou efeitos colaterais
  não forem evidentes; não repetir literalmente o código;
- contratos e referências: schemas, eventos, tópicos, arquivos, APIs, manifests
  e compatibilidade;
- configuração: variáveis, valores aceitos, defaults e exemplos sem segredos;
- ADRs: decisões duráveis de arquitetura, ferramenta, compatibilidade, operação
  ou trade-off relevante, com contexto, decisão, alternativas e consequências;
- runbooks: diagnóstico, falha, recuperação, replay, rollback, DLQ e intervenção;
- guias de migração ou changelog: somente quando consumidores precisarem agir
  diante de mudança incompatível ou alteração operacional relevante;
- diagramas: somente quando tornarem um fluxo ou relação materialmente mais
  claro do que texto breve.

## Templates

Usar um template somente ao criar o tipo de documento correspondente:

- `templates/adr.md` para ADRs;
- `templates/runbook.md` para runbooks;
- `templates/migration.md` para guias de migração.

Substituir todos os marcadores do template por informações verificáveis e
remover seções que não se apliquem. Ao atualizar um documento existente,
preservar sua estrutura canônica, salvo se a própria mudança exigir alterá-la.

## Procedimento

1. Comparar a base e o resultado do PR e identificar os públicos afetados:
   desenvolvedor, mantenedor, operador, consumidor de contrato ou responsável
   por incidentes. Priorizar um público específico somente quando isso tiver
   sido solicitado explicitamente na entrada ou no contexto da tarefa.
2. Avaliar explicitamente o impacto em README ou guia, interface pública,
   contrato, configuração, ADR, runbook, migração ou changelog. Se nenhum se
   aplicar, não alterar arquivos e justificar a conclusão.
3. Identificar a fonte canônica de cada informação. Não editar documentação
   gerada quando código, schema ou contrato executável for sua fonte.
4. Criar ou atualizar somente a documentação necessária à entrega. Ao criar
   um ADR, runbook ou guia de migração, partir do template correspondente. Uma
   atualização pode corrigir trechos documentais quando houver evidência;
   divergências cuja correção exija mudar a implementação devem ser somente
   relatadas.
5. Usar docstrings para contratos públicos, guias para uso e operação,
   comentários para razões ou restrições não evidentes e ADRs para o contexto e
   as consequências de decisões duráveis já aceitas.
6. Descrever comportamento observado, limites e efeitos colaterais; não repetir
   o código nem apresentar planos ou decisões pendentes como concluídos.
7. Usar exemplos mínimos, caminhos e comandos reais. Quando houver validação
   local oficial, segura e não mutante, verificar os exemplos e registrar apenas
   resultados observados.
8. Verificar links internos, âncoras, referências e nomes alterados. Usar links
   diretos para fontes oficiais quando uma referência externa for necessária.
9. Confrontar o resultado com código, testes, contratos e configurações e
   relatar divergências sem corrigir a implementação.
10. Antes de concluir, comparar novamente a branch com a base e inspecionar o diff
    documental para remover repetição, conteúdo obsoleto, afirmações sem
    evidência e dados sensíveis.

## Restrições

- Alterar somente arquivos documentais aplicáveis e trechos exclusivamente
  documentais do código, como docstrings e comentários; não alterar lógica,
  assinaturas, dependências, testes, contratos executáveis ou infraestrutura.
- Não documentar toda função interna ou código autoexplicativo.
- Não criar ADR para decisão local ou sem consequência durável.
- Não registrar como aceita uma decisão ainda pendente de aprovação.
- Não criar componentes, documentos vazios ou placeholders de módulos futuros.
- Não manter marcadores ou seções não aplicáveis ao usar um template.
- Não inventar comportamento, resultados, comandos, links ou justificativas.
- Não expor segredos, credenciais, PII, dados bancários reais ou detalhes
  exploráveis de vulnerabilidades.
- Não criar nem alterar arquivos em `docs/learning/modules/`.
- Não fazer commit, push, merge, comentários ou outras operações remotas.

## Critérios de conclusão

- A documentação corresponde ao estado resultante do Pull Request e mantém uma
  fonte canônica para cada informação.
- A avaliação de impacto cobre cada categoria aplicável ou justifica por que a
  entrega não exige alteração documental.
- Interfaces públicas não óbvias, contratos e procedimentos operacionais
  afetados estão documentados na medida necessária.
- Links, caminhos, exemplos e comandos mantidos são válidos ou foram relatados
  como não verificáveis.
- A documentação não está concluída enquanto houver divergência material com
  código, contratos, configuração ou testes; nesse caso, relatar o impedimento.
- A resposta final informa documentos alterados, fontes consultadas, validações
  executadas, públicos afetados, eventual público priorizado e divergências ou
  pendências encontradas.
