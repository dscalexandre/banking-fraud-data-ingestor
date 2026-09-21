---
name: delivery-orchestrator
description: >-
  Coordenar a entrega versionada de artefatos por agentes
  especializados já integrados à main, sem executar suas responsabilidades.
---

# Orquestrar uma entrega com agentes especializados

## Finalidade

Selecione um especialista, delegue-lhe a entrega e coordene seu versionamento.
Não produza nem avalie conteúdo reservado ao especialista.

## Entrada e roteamento

Aceite linguagem natural, por exemplo:

```text
Criar a documentação do módulo de criação do agente de aprendizagem, sem fazer merge.
```

Aceite também esta forma estruturada:

```text
Solicitação: <resultado desejado> (opcional)
Pull Requests: <número ou URL>[, <número ou URL>...] (opcional)
Capacidade: <capacidade registrada> (opcional)
Perfil: <perfil registrado> (opcional)
Skill: <skill registrada> (opcional)
Template de Issue: <tipo de template registrado> (opcional)
Operação: criar | atualizar
Merge: sim | não
```

- Na forma estruturada, informe `Solicitação` ou `Pull Requests`, `Operação` e
  `Merge`. Normalize ambas as formas; se combinadas, exija coerência.
- Em linguagem natural, infira `criar` ou `atualizar` pelos verbos. Só normalize
  merge como `sim` com instrução explícita; sem ela, entregue o PR sem merge.
- O registro em `references/capabilities.yaml` autoriza o roteamento e informa
  o perfil a acionar. Selecione uma única entrada pela intenção descrita, por
  uma skill registrada ou por um perfil registrado citado na solicitação.
- Quando a entrada indicar um tipo de template de Issue, use-o somente se ele
  estiver registrado para a capacidade selecionada. Na ausência dessa
  indicação, use o tipo padrão da capacidade; em linguagem natural, considere
  também um tipo de template citado explicitamente.
- Sem correspondência única ou com dados conflitantes, peça esclarecimento sem
  criar recursos. Preserve a solicitação original para o especialista.

## Limites de responsabilidade

Antes de criar recursos, confirme uma única entrada compatível no registro e a
árvore limpa. A presença no registro comprova que o perfil está integrado à
`main`.

O especialista é a fonte de verdade para elegibilidade, evidências, seleção de
artefatos, conteúdo e validações da capacidade. Não repita essas ações, não
altere o módulo fonte nem produza conteúdo ou arquivos fora do que ele autorizar.

## Procedimento

1. Ler e cumprir o `AGENTS.md` antes de executar a entrega.
2. Normalize a entrada e selecione a única entrada registrada; caso contrário,
   informe o impedimento ou peça esclarecimento.
3. Antes de criar a Issue, selecione o tipo de template informado ou o padrão
   da capacidade, leia o caminho correspondente em `templates_issue` na entrada
   selecionada do registro e preencha suas seções com a solicitação normalizada
   e os critérios aplicáveis. Apresente o conteúdo para aprovação explícita e
   reapresente-o se houver alteração material.
4. Crie Issue e branch próprias a partir de `main`, então acione o especialista
   com a solicitação original e a operação normalizada.
5. Se o especialista não produzir arquivo ou relatar impedimento, encerre sem
   commit ou PR. Caso produza, adicione somente os artefatos autorizados,
   execute os checks de staging e crie o commit com referência à Issue.
6. Registre resultados observados na Issue. Antes de abrir o PR, leia
   `.github/pull_request_template.md`, preencha-o com os artefatos, as
   evidências e os impactos observados e apresente-o para aprovação explícita.
   Publique a branch, abra o PR, acompanhe a CI e, somente com merge normalizado
   como `sim`, integre por Merge Commit e confirme o encerramento da Issue.

## Critérios de conclusão

- A entrega contém somente resultados autorizados pelo especialista, em Issue,
  branch e PR próprios, preenchidos a partir do tipo de template de Issue
  selecionado no registro e do template de PR do repositório.
- A resposta final informa a capacidade, a solicitação, a operação normalizada,
  as evidências e os artefatos retornados, Issue, commit, PR, CI e merge.
