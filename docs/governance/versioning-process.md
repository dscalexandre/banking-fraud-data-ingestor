# Processo de Versionamento

Este processo rege o versionamento de novos projetos, da preparação do repositório à conclusão da entrega.

Para módulos funcionais, inicie após uma descoberta sem escrita: analise `docs/architecture/solution-design.md`, o estado e o histórico do repositório, identifique a última implementação e proponha um único próximo módulo. Sem proposta inequívoca e aprovação explícita, não crie Issue, branch, commit ou Pull Request. Após a aprovação, execute as etapas abaixo somente no escopo necessário ao módulo.

## Padrão de apresentação dos comandos

- Preserve a sequência do guia e a governança por Issues, branches, commits e
  Pull Requests.
- Produza commits atômicos, reversíveis e semanticamente coerentes.
- Use uma célula `bash` por ação independente.
- Mantenha juntas apenas ações interdependentes ou comandos homogêneos de uma
  única verificação, como a consulta sucessiva das versões das ferramentas do
  ambiente.
- Acima de cada célula, escreva uma descrição objetiva, clara e sem negrito.
- Separe os blocos de execução com `---`.
- Quando relevante e previsível, descreva a saída imediatamente abaixo da
  célula, em texto corrido, no formato **RE:** descrição.
- Inclua o código de saída quando relevante; por exemplo, **RE:** nenhuma saída
  e código de saída zero.
- Nunca deixe **RE:** isoladamente nem represente saídas em células de código.
- Para condições, inclusive no tratamento de erros, use `test` e somente para
  essa finalidade.
- Execute comandos cotidianos do Git e da GitHub CLI (`gh`) diretamente, sem
  envolvê-los com `test`.

## 1. Preparar o repositório

Confirmar que a árvore de trabalho não possui alterações pendentes:

```bash
git status --short
```

**RE:** nenhuma saída e código de saída zero, indicando que a árvore de trabalho está limpa.

Mudar para a branch `main`:

```bash
git switch main
```

**RE:** a branch `main` é ativada ou já está ativa, com código de saída zero.

Atualizar a `main` a partir do repositório remoto somente por avanço direto:

```bash
git pull --ff-only origin main
```

**RE:** a `main` é atualizada por fast-forward ou já está atualizada, com código de saída zero.

## 2. Criar a Issue

Criar uma nova Issue a partir de um dos modelos abaixo. Copiar o modelo
adequado para o arquivo temporário, preencher todos os campos e remover os
comentários de orientação antes da criação.

Modelo para entrega:

```text
### Objetivo

<!-- Resultado verificável esperado. -->

### Escopo

<!-- Limites da entrega. Cada item deve estar coberto pelas alterações descritas
no Pull Request. -->

- [ ]

### Critérios de aceite

<!-- Condições objetivas e verificáveis. O Pull Request deve registrar a
evidência e o resultado correspondente a cada critério. -->

- [ ]
```

Modelo para defeito:

```text
### Objetivo

<!-- Correção verificável esperada. -->

### Comportamento observado

<!-- O que ocorreu, incluindo impacto e mensagens de erro não sensíveis. -->

### Comportamento esperado

<!-- O resultado que deveria ocorrer. -->

### Passos para reproduzir

1.

### Evidências

<!-- Logs sanitizados, métricas, versões e demais evidências sem segredos ou PII. -->

### Critérios de aceite

<!-- Condições objetivas e verificáveis. O Pull Request deve registrar a
evidência e o resultado correspondente a cada critério. -->

- [ ]
```

Criar o arquivo de corpo, copiar o modelo selecionado e preenchê-lo. Por
exemplo, para uma entrega:

```bash
issue_body_file=$(mktemp)

"${EDITOR:-vi}" "$issue_body_file"

test -s "$issue_body_file"
rg -q -e '^- \[ \]$' -e '^1\.$' "$issue_body_file"
unfilled_issue_fields_status=$?
test "$unfilled_issue_fields_status" -eq 1

issue_url=$(gh issue create \
  --title "[Entrega]: <título>" \
  --label "enhancement" \
  --body-file "$issue_body_file")

issue_number=${issue_url##*/}
rm "$issue_body_file"

printf 'Issue criada: #%s\n' "$issue_number"
```

Para um defeito, usar o modelo correspondente, o título com o prefixo `[Bug]:`
e o rótulo `bug`. O corpo deve preservar a estrutura do modelo selecionado e
conter todos os campos preenchidos. A validação interrompe o fluxo se encontrar
itens vazios de escopo ou critérios de aceite, ou passos de reprodução sem
descrição.

## 3. Criar a branch vinculada à Issue

Criar a branch de desenvolvimento a partir da `main`, vinculá-la à Issue e fazer checkout:

```bash
branch_name=".../${issue_number}-..."

gh issue develop "$issue_number" \
  --base main \
  --name "$branch_name" \
  --checkout
```

Confirmar o vínculo entre a branch e a Issue:

```bash
gh issue develop --list "$issue_number"
```

## 4. Validar e registrar as alterações

Realizar somente as alterações necessárias para atender ao escopo e aos critérios
de aceite da Issue.

Revisar o estado da árvore de trabalho:

```bash
git status
```

Adicionar somente os arquivos relacionados à Issue:

```bash
git add <arquivos>
```

Validar as alterações preparadas para commit:

```bash
git diff --cached --check
```

Criar um commit coeso e rastreável:

```bash
git commit \
  -m "..." \
  -m "Refs #${issue_number}"
```

Repetir esta seção para cada unidade de alteração coesa. Cada repetição deve
preparar somente os arquivos daquele commit e executar novamente a validação
do conteúdo preparado antes de registrá-lo. Não acumular alterações sem
relação no mesmo commit.

## 5. Preparar a validação dos critérios de aceite

### 5.1 Caminhos para preenchimento manual no GitHub

Obter a URL da Issue em revisão:

```bash
gh issue view "$issue_number" --json url --jq '.url'
```

**RE:** exibe a URL da Issue atual no GitHub.

Para preencher manualmente a entrega no GitHub, seguir os caminhos abaixo:

- `<proprietário> / <repositório> → Issues → Issue #${issue_number}`
- `<proprietário> / <repositório> → Pull requests → Pull Request #${pr_number}`

O Pull Request só estará disponível após sua criação na seção 7. A marcação
dos critérios de aceite, o preenchimento da validação no Pull Request e suas
confirmações programáticas ocorrem na seção 8, depois da CI.

### 5.2 Confirmar o preenchimento da Issue

Confirmar que a Issue preserva as seções obrigatórias e não contém campos
pendentes de preenchimento:

```bash
issue_body=$(gh issue view "$issue_number" --json body --jq '.body')

printf '%s\n' "$issue_body" | rg -q '^### Objetivo$'
printf '%s\n' "$issue_body" | rg -q '^### Critérios de aceite$'

printf '%s\n' "$issue_body" | rg -q '^### Escopo$'
has_scope_section=$?
printf '%s\n' "$issue_body" | rg -q '^### Comportamento observado$'
has_observed_behavior_section=$?

test "$has_scope_section" -eq 0 -o "$has_observed_behavior_section" -eq 0

printf '%s\n' "$issue_body" | rg -q -e '^- \[ \]$' -e '^1\.$'
unfilled_issue_fields_status=$?

test "$unfilled_issue_fields_status" -eq 1
```

**RE:** nenhuma saída e código de saída zero, confirmando que a Issue contém
as seções obrigatórias e não possui campos vazios de escopo, critérios de
aceite ou passos de reprodução.

## 6. Publicar a branch

Publicar a branch e configurar o upstream:

```bash
git push -u origin "$branch_name"
```

## 7. Criar e validar o Pull Request

Criar o Pull Request a partir do modelo abaixo. Copiá-lo para o arquivo
temporário, preencher todos os campos e substituir `{{ISSUE_NUMBER}}` antes da
criação:

```text
## Objetivo

Closes #{{ISSUE_NUMBER}}

<!-- Resultado verificável que esta entrega produz, alinhado ao objetivo da
Issue. -->

## Alterações

<!-- Liste arquivos ou componentes afetados e descreva a mudança. Cubra o
escopo aprovado na Issue sem repetir seus itens literalmente. -->

-

## Validação

<!-- Informe as evidências executadas e seus resultados de forma que comprovem
os critérios de aceite aplicáveis. Inclua o resultado da CI quando concluída. -->

-

## Impacto

<!-- Declare efeitos em comportamento funcional, infraestrutura e dados;
registre explicitamente a ausência de impacto quando aplicável. -->

-
```

Criar o arquivo de corpo, copiar o modelo e preenchê-lo:

```bash
pr_body_file=$(mktemp)
"${EDITOR:-vi}" "$pr_body_file"

test -s "$pr_body_file"
sed -i "s#{{ISSUE_NUMBER}}#${issue_number}#g" "$pr_body_file"
rg -q -F '{{ISSUE_NUMBER}}' "$pr_body_file"
unresolved_placeholder_status=$?
rg -q '^-$' "$pr_body_file"
unfilled_pr_fields_status=$?
test "$unresolved_placeholder_status" -eq 1
test "$unfilled_pr_fields_status" -eq 1

pr_url=$(gh pr create \
  --base main \
  --head "$branch_name" \
  --title "<tipo>: <título>" \
  --body-file "$pr_body_file")

pr_number=${pr_url##*/}
rm "$pr_body_file"

printf 'Pull Request: #%s\n' "$pr_number"
```

### 7.1 Caminho para preenchimento manual do Pull Request no GitHub

Obter a URL do Pull Request recém-criado:

```bash
gh pr view "$pr_number" --json url --jq '.url'
```

**RE:** exibe a URL do Pull Request atual no GitHub.

Para preenchê-lo manualmente no GitHub, seguir o caminho:

- `<proprietário> / <repositório> → Pull requests → Pull Request #${pr_number}`

O corpo deve preservar as seções e os campos do modelo; não criar Pull
Requests com corpo avulso. O link `Closes #<número>` deve permanecer na seção
`Objetivo`. Na seção `Validação`, incluir a linha
`- CI obrigatória: pendente na abertura deste Pull Request.` para que ela seja
substituída pela evidência observada após a aprovação da CI.

Confirmar que o Pull Request está configurado para encerrar a Issue:

```bash
closes_issue=$(gh pr view "$pr_number" \
  --json closingIssuesReferences \
  --jq ".closingIssuesReferences | any(.number == ${issue_number})")

test "$closes_issue" = "true"
```

A execução deve prosseguir somente se o vínculo estiver confirmado.

## 8. Validar e registrar a CI

Aguardar e confirmar todos os checks obrigatórios do Pull Request:

```bash
gh pr checks "$pr_number" \
  --required \
  --watch \
  --fail-fast
```

O merge somente pode ocorrer após a conclusão bem-sucedida dos checks obrigatórios.

Após a aprovação da CI, abrir primeiro a Issue no GitHub para marcar
manualmente cada critério comprovado, preservando o corpo e a estrutura da
Issue:

```bash
gh issue view "$issue_number" --web
```

**RE:** abre a Issue no GitHub para a marcação manual dos critérios de aceite comprovados.

---

Depois, abrir o Pull Request no GitHub para preencher manualmente a evidência
da CI na seção `Validação`, preservando as seções e os campos do modelo:

```bash
gh pr view "$pr_number" --web
```

**RE:** abre o Pull Request no GitHub para o preenchimento manual da validação.

---

Depois dos dois preenchimentos manuais, confirmar que nenhum critério de
aceite permanece pendente:

```bash
pending_issue_items=$(gh issue view "$issue_number" --json body --jq '.body' |
  awk '
    /^### Critérios de aceite$/ { in_acceptance_criteria = 1; next }
    in_acceptance_criteria && /^### / { in_acceptance_criteria = 0 }
    in_acceptance_criteria && /^- \[ \] / { pending_items++ }
    END { print pending_items + 0 }
  ')

test "$pending_issue_items" -eq 0
```

**RE:** nenhuma saída e código de saída zero, confirmando que todos os critérios de aceite foram marcados após comprovação.

Antes de prosseguir, confirmar que todos os critérios possuem evidências
verificáveis registradas na Issue ou no Pull Request.

Como a evidência foi preenchida manualmente no GitHub, conferir que a linha
pendente foi substituída antes de continuar:

```bash
pr_body=$(gh pr view "$pr_number" \
  --json body \
  --jq '.body')

printf '%s\n' "$pr_body" |
  rg -q -F -- '- CI obrigatória: pendente na abertura deste Pull Request.'
ci_evidence_pending_status=$?

test "$ci_evidence_pending_status" -eq 1
```

**RE:** nenhuma saída e código de saída zero, confirmando que a evidência da
CI foi preenchida manualmente no Pull Request.

## 9. Integrar o Pull Request

Integrar o Pull Request exclusivamente por **Merge Commit**:

```bash
gh pr merge "$pr_number" --merge
```

Confirmar o merge antes de continuar:

```bash
pr_state=$(gh pr view "$pr_number" --json state --jq '.state')
test "$pr_state" = "MERGED"
```

**RE:** nenhuma saída e código de saída zero, confirmando que o Pull Request foi integrado e fechado.

## 10. Sincronizar e validar a conclusão

Mudar para a branch `main`:

```bash
git switch main
```

Atualizar a `main` somente por avanço direto:

```bash
git pull --ff-only origin main
```

Atualizar e limpar as referências remotas:

```bash
git fetch --prune
```

Confirmar que a Issue foi encerrada:

```bash
gh issue view "$issue_number" \
  --json state \
  --jq '.state'
```

**RE:** `CLOSED` e código de saída zero.

Confirmar também que:

- todos os critérios de aceite estão concluídos;
- o Pull Request foi integrado e fechado;
- a `main` contém as alterações entregues.

Confirmar essas condições e que a cópia local está sincronizada com a remota:

```bash
issue_state=$(gh issue view "$issue_number" --json state --jq '.state')
pr_state=$(gh pr view "$pr_number" --json state --jq '.state')
current_branch=$(git branch --show-current)
local_head=$(git rev-parse HEAD)
remote_head=$(git rev-parse origin/main)

test "$issue_state" = "CLOSED"
test "$pr_state" = "MERGED"
test "$current_branch" = "main"
test "$local_head" = "$remote_head"
```

**RE:** nenhuma saída e código de saída zero, confirmando que a Issue está fechada, o Pull Request está integrado e fechado, e a `main` local está sincronizada com `origin/main`.

## 11. Finalizar

Remover a branch remota já integrada:

```bash
git push origin --delete "$branch_name"
```

**RE:** a branch remota é removida e o comando termina com código de saída zero.

Remover a branch local já integrada:

```bash
git branch -d "$branch_name"
```

**RE:** a branch local é removida e o comando termina com código de saída zero.

Atualizar as referências remotas após a exclusão da branch:

```bash
git fetch --prune
```

**RE:** as referências remotas obsoletas são removidas e o comando termina com código de saída zero.

Confirmar que a árvore de trabalho permanece limpa:

```bash
git status --short
```

**RE:** nenhuma saída e código de saída zero.

Confirmar programaticamente o estado final:

```bash
worktree_status=$(git status --short)
local_branch=$(git branch --list "$branch_name")
remote_branch=$(git ls-remote --heads origin "refs/heads/$branch_name")

test -z "$worktree_status"
test -z "$local_branch"
test -z "$remote_branch"
```

**RE:** nenhuma saída e código de saída zero, confirmando que a árvore de trabalho está limpa e que a branch não existe localmente nem em `origin`.

## Auditoria final

Consultar o histórico gráfico:

```bash
git log \
  --graph \
  --oneline \
  --decorate \
  --all \
  --date-order
```

O histórico deve permitir rastrear o fluxo:

```text
Issue
  ↓
Branch vinculada
  ↓
Alterações
  ↓
Commit
  ↓
Pull Request
  ↓
CI aprovada
  ↓
Merge Commit
  ↓
Issue encerrada
  ↓
main sincronizada
```

## Regra de conclusão

O processo de versionamento somente pode ser considerado concluído quando:

- todos os critérios de aceite estiverem concluídos;
- a CI obrigatória estiver aprovada;
- o Pull Request estiver integrado e a Issue encerrada;
- a `main` estiver sincronizada e a árvore de trabalho limpa.
