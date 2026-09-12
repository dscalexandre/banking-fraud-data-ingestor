---
name: learning-documenter
description: >-
  Criar ou atualizar em docs/learning/modules/ a documentação de um módulo
  concluído, validado e integrado à main por um ou mais Pull Requests com
  estado MERGED.
  Não usar para trabalho em construção, planejamento ou implementação.
---

# Documentar aprendizagem de um módulo

## Entrada

A solicitação deve fornecer estes parâmetros:

```text
Módulo: <nome ou descrição do módulo integrado> (opcional)
Operação: criar | atualizar
Pull Requests: <número ou URL>[, <número ou URL>...] (opcional)
```

- Informar pelo menos um entre `Módulo` e `Pull Requests`. `Módulo` identifica a
  entrega por nome ou descrição; o agente localiza os Pull Requests integrados
  que a compõem, incluindo todos os incrementos necessários, e os usa como
  evidência. `Pull Requests` permite identificar a entrega diretamente.
- `Operação` é opcional somente para um módulo ainda sem documento, quando o
  padrão é `criar`. Atualizar exige solicitação explícita.
- Quando receber somente `Módulo`, localizar os Pull Requests relacionados.
  Quando receber somente `Pull Requests`, identificar o módulo e localizar
  incrementos relacionados que estejam ausentes. Quando receber ambos, conferir
  se identificam a mesma entrega. Em qualquer caso, se não conseguir comprovar
  um conjunto completo e inequívoco, não modificar arquivos e relatar o
  impedimento. Não incluir o Pull Request usado exclusivamente para entregar
  esta documentação. Issues, branches, commits e descrições podem complementar o
  contexto, mas não substituem as evidências localizadas.

## Operações

- `criar`: criar o documento de um módulo integrado que ainda não possua
  documento canônico, consolidando as evidências de todos os Pull Requests que
  o agente localizou para o módulo.
- `atualizar`: atualizar um documento existente com base no conjunto de Pull
  Requests que originou o módulo ou em mudanças posteriores já integradas que o
  agente localizou para ele.

A documentação deve ser produzida depois da integração, em Issue, branch e Pull
Request próprios, separados da entrega da implementação.

## Elegibilidade do módulo

Antes de modificar qualquer arquivo, identificar o módulo e localizar seus Pull
Requests conforme a forma de pesquisa recebida. Confirmar que cada Pull Request
selecionado está com estado `MERGED` e foi integrado à `main`. Aplicar também os
controles específicos da operação:

- `criar`: confirmar que o conjunto de Pull Requests representa exatamente um
  módulo concluído, cobre todos os seus incrementos integrados, teve os checks
  obrigatórios de cada commit integrado aprovados e não possui falhas ou
  pendências funcionais conhecidas. As fontes devem evidenciar o comportamento
  entregue como um todo. Quando houver Issue vinculada, confirmar que está
  concluída e que os Pull Requests localizados cobrem seus incrementos do módulo;
- `atualizar`: confirmar que o documento canônico existe, corresponde ao módulo
  e que o conjunto localizado é o da entrega original ou representa mudanças
  posteriores nesse módulo. Para a entrega original, usar somente as evidências
  de seus Pull Requests para corrigir ou aprimorar o conteúdo, sem introduzir
  comportamento novo. Para mudanças posteriores, confirmar os checks
  obrigatórios de cada Pull Request, a ausência de falhas ou pendências
  funcionais conhecidas relacionadas à mudança e evidências suficientes para
  atualizar os trechos afetados. Não reconstruir a elegibilidade da entrega
  inicial; confrontar o documento resultante com o estado atual da `main`.

Se qualquer condição aplicável não puder ser comprovada, não modificar arquivos
e relatar o impedimento.

## Resultado

Quando houver alteração, criar ou modificar exatamente um arquivo Markdown em
`docs/learning/modules/`, com no máximo 300 linhas, seguindo
`assets/module-learning.md`. Em qualquer operação, o template é o contrato
estrutural do documento: preservar os nomes, os níveis e a ordem das seções e
subseções, assim como as colunas da tabela de documentação oficial. Não
renomear, reordenar, fundir nem criar seções fora do template. Somente a seção
`Alternativas consideradas` pode ser omitida quando não houver evidência.

Na operação `atualizar`, modificar o documento somente quando houver necessidade
material comprovada. Caso contrário, manter o arquivo intacto e informar que já
está atualizado.

## Procedimento

1. Ler `AGENTS.md`, `docs/architecture/solution-design.md` e as demais fontes
   de verdade aplicáveis ao módulo.
2. Identificar o módulo, localizar ou completar seus Pull Requests e consultar
   as demais evidências exigidas em `Elegibilidade do módulo` para a operação
   solicitada.
3. Localizar o documento do módulo pelo padrão `NN-nome-do-modulo.md`. Priorizar
   o caminho definido pelas fontes de verdade, o documento existente associado
   ao módulo e a posição arquitetural comprovada, nessa ordem. Somente
   quando nenhuma dessas fontes definir a numeração, usar o próximo número
   disponível e um nome descritivo em minúsculas, separado por hífens.
4. Inspecionar a implementação, os testes, os contratos, as ADRs e a
   documentação operacional relacionados a todos os Pull Requests localizados.
   Não documentar estado planejado como se estivesse implementado.
5. Em `criar` e `atualizar`, consultar os checks e as validações já concluídos
   em cada Pull Request aplicável; não reexecutar localmente as validações da
   implementação, como `poetry check`, Ruff ou pytest. Depois de modificar o
   documento, executar somente verificações não mutantes diretamente
   relacionadas ao Markdown produzido e registrar apenas os resultados
   observados.
6. Em qualquer operação, ler `assets/module-learning.md` antes de modificar o
   documento. Ao criar um arquivo, copiar sua estrutura e remover os comentários
   de orientação do resultado. Ao atualizar, preservar a estrutura e o conteúdo
   não afetado, modificando somente os trechos necessários para representar a
   mudança integrada.
7. Explicar como os componentes colaboram e relacionar somente os conceitos
   necessários para compreender as decisões da implementação.
8. Registrar alternativas somente quando houver evidência de que foram
   consideradas durante a implementação, incluindo funcionamento, vantagens,
   desvantagens e motivo da não adoção. Remover a seção do documento quando
   não houver evidência.
9. Referenciar arquivos do repositório com caminhos relativos. Preencher
   `Documentação oficial` com links diretos para fontes primárias ou oficiais
   da tecnologia e dos componentes efetivamente implementados; não aceitar
   blogs, páginas de busca, URLs genéricas quando houver página específica nem
   placeholders.
10. Conferir o documento para eliminar repetição, alegações sem evidência e
    conteúdo fora do módulo. Antes de concluir, comparar sua estrutura com o
    template e confirmar que todas as seções obrigatórias permanecem presentes,
    com os mesmos nomes, níveis e ordem.

## Restrições

- Tratar todos os demais caminhos como somente leitura; relatar problemas sem
  corrigi-los.
- Não completar, corrigir, revisar tecnicamente ou alterar a implementação.
- Não usar a documentação como requisito para autorizar o merge do módulo.
- Não inventar resultados, links, decisões ou comportamento da solução.
- Não reproduzir as instruções de `AGENTS.md` no documento gerado.
- Não fazer commit, push, merge ou qualquer operação remota.

## Critérios de conclusão

- Ao concluir, informar na resposta final o documento alterado, as fontes
  consultadas, a documentação oficial referenciada e as validações realmente
  executadas.
- Informar todos os Pull Requests localizados que compõem o módulo e consolidar
  suas evidências, sem tratar um incremento isolado como a entrega completa.
- Todas as seções mantidas do template contêm conteúdo verificável.
- O documento resultante preserva a estrutura definida pelo template.
- As evidências distinguem arquivos inspecionados de comandos executados.
