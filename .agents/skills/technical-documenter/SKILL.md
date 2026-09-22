---
name: technical-documenter
description: >-
  Criar ou atualizar a documentação técnica de uma entrega referenciada por
  Issue, Pull Request aberto ou ambos. Usar para README, interfaces públicas,
  contratos, configuração, ADRs, runbooks e migrações aplicáveis. Não usar
  para implementar código.
---

# Documentar tecnicamente uma entrega

## Entrada

Aceite linguagem natural ou a forma estruturada abaixo:

```text
Issue: <número ou URL> (opcional)
Pull Request: <número ou URL> (opcional)
Operação: criar | atualizar (opcional)
Público: <um ou mais públicos, opcional>
```

- Exija ao menos uma `Issue` ou um `Pull Request`. Aceite também uma descrição
  inequívoca da Issue; se não puder localizá-la com segurança, peça
  esclarecimento sem modificar arquivos.
- Quando ambos existirem, confirme que tratam da mesma entrega. Com somente um
  deles, use seu escopo como contexto e consulte o outro apenas se necessário.
- Infira `Operação` e o público principal somente quando isso for inequívoco;
  caso contrário, peça esclarecimento ou registre a suposição.

## Condições para atuar

1. Ler e cumprir o `AGENTS.md`.
2. Se houver PR, confirmar que está aberto, não é rascunho e corresponde à
   branch atual. Recusar entregas de governança, manutenção genérica ou
   documentação de aprendizagem.
3. Consultar a Issue, o diff do PR e as fontes de verdade aplicáveis; ler
   `docs/architecture/solution-design.md` quando a entrega afetar arquitetura,
   fluxos, contratos, destinos, falhas, recuperação ou infraestrutura.
4. Com somente uma Issue, documentar apenas fatos verificáveis em fontes
   versionadas ou nela explicitamente aprovados. Se não houver evidência
   suficiente, não modificar arquivos e relatar o impedimento.

## Procedimento

1. Identificar públicos afetados e avaliar o impacto em guia, interface,
   contrato, configuração, ADR, runbook, migração, changelog ou diagrama.
2. Determinar a fonte canônica de cada informação; não editar documentação
   gerada cujo código, schema ou contrato executável seja a fonte.
3. Criar ou atualizar somente a documentação necessária. Use docstrings para
   contratos públicos, comentários para razões não evidentes e guias para uso
   ou operação.
4. Ao criar ADR, runbook ou guia de migração, use respectivamente
   `templates/adr.md`, `templates/runbook.md` ou `templates/migration.md`;
   substitua marcadores e remova seções não aplicáveis.
5. Conferir documentação contra código, testes, contratos e configuração;
   verificar links, exemplos e comandos quando houver validação segura.
6. Revisar o diff documental e relatar documentos alterados, fontes,
   validações, públicos, suposições e divergências.

## Limites

- Altere somente documentação aplicável e docstrings ou comentários; não altere
  lógica, assinaturas, dependências, testes, contratos executáveis ou
  infraestrutura.
- Não documente código autoexplicativo, decisões pendentes ou comportamento não
  verificável; não crie documentos vazios, placeholders ou arquivos em
  `docs/learning/modules/`.
- Preserve a estrutura de documentos existentes e não invente fatos, comandos,
  links ou justificativas.

## Conclusão

- A documentação deve corresponder às evidências verificáveis e cobrir somente
  os impactos aplicáveis.
- Interfaces públicas, contratos e procedimentos operacionais não óbvios devem
  estar documentados quando afetados.
- Havendo divergência material ou evidência insuficiente, não conclua a
  documentação; relate o impedimento.
