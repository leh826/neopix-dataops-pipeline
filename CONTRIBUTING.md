# Guia de Contribuição - NeoPix DataOps Pipeline

Bem-vinda ao projeto! Leia este guia com atenção antes de começar.
O fluxo descrito aqui é exatamente o que será avaliado.

---

## Pré-requisitos

Antes de começar, certifique-se de ter concluído:

- [ ] **[Trilha 01 — Fundamentos](https://github.com/Starlight-git-project/trilha-01-fundamentos)** — commits, `.gitignore`, variáveis de ambiente

- [ ] **[Trilha 02 — Governança](https://github.com/Starlight-git-project/trilha-02-governanca)** — branches, PRs, code review

- [ ] **[Trilha 03 — Infraestrutura](https://github.com/Starlight-git-project/trilha-03-infraestrutura)** — GitHub Org, políticas, audit log

- [ ] **[VoughtGuard](https://github.com/Starlight-git-project/voughtguard-pipeline-fraud-detection)** — desafio anterior, base para este projeto

---

## Suas issues

Cada uma tem issues atribuídas. Veja a sua antes de começar qualquer coisa.

| Issue | Responsável | Semana |
|-------|------------|--------|
| #1 - Estrutura do repositório | Aluna A | Semana 1 |
| #2 - `ingestao.py` (PySpark) | Aluna B | Semana 1 |
| #3 - `logging_config.py` | Aluna C | Semana 1 |
| #4 - `validacao.py` | Aluna A | Semana 2 |
| #5 - `conciliacao.py` | Aluna B | Semana 2 |
| #6 - Relatório de rejeições | Aluna C | Semana 2 |
| #7 - Testes de validação | Aluna B | Semana 3 |
| #8 - Testes de conciliação | Aluna C | Semana 3 |
| #9 - Dashboard Streamlit | Aluna A | Semana 3 |
| #10 - Docker + Airflow local | Aluna A | Semana 4 |
| #11 - DAG de orquestração | Aluna B | Semana 4 |
| #12 - Runbook operacional | Aluna C | Semana 4 |

Respeite as dependências - algumas issues só podem começar depois de outras mergeadas.

---

## Passo 0 - Pegue sua issue

Antes de escrever qualquer linha de código, se atribua à issue:

1. Acesse a aba **Issues** do repositório
2. Filtre pela sua label: `aluna-a`, `aluna-b` ou `aluna-c`

```
Issues → Filters → Label → aluna-a (ou b, ou c)
```

3. Abra a issue da semana atual
4. No lado direito, clique em **Assignees → assign yourself**
5. Leia todas as tarefas e critérios de aceite antes de começar

**Nunca comece a trabalhar sem se atribuir à issue primeiro.**

---

## Passo 1 - Fork do repositório

1. Clique em **Fork** no canto superior direito
2. Selecione sua conta como destino

---

## Passo 2 - Clone do fork

```bash
git clone https://github.com/SEU-USUARIO/neopix-dataops-pipeline.git
cd neopix-dataops-pipeline
```

---

## Passo 3 - Configure o remote original

```bash
git remote add upstream https://github.com/Starlight-git-project/neopix-dataops-pipeline.git

# Verifique os remotes
git remote -v
```

---

## Passo 4 - Configure o ambiente

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows

pip install -r requirements.txt
cp .env.example .env
```

---

## Passo 5 - Baixe o dataset

Acesse: [Dataset NeoPix — Google Drive](https://drive.google.com/drive/folders/13u1WjeODVBNVj07C2YwrftflgZxIA29L?usp=sharing)

- `transacoes.csv` → salve em `data/raw/transacoes.csv`
- `transacoes_sample.csv` → salve em `tests/fixtures/transacoes_sample.csv`

`data/raw/` está no `.gitignore` - **nunca commite dados**.

---

## Passo 6 - Crie sua branch a partir do upstream

```bash
# Garante que você está na develop atualizada
git fetch upstream
git switch develop
git merge upstream/develop

# Cria sua branch
git switch -c feature/nome-da-sua-branch
```

---

## Branches

### Branches principais

| Branch | Finalidade |
|--------|-----------|
| `main` | Código estável, pronto para produção. Nunca commitar diretamente aqui. |
| `develop` | Integração contínua. Todas as features passam por aqui antes da `main`. |

### Branches de trabalho

| Branch | Finalidade |
|--------|-----------|
| `feat/nome` | Nova funcionalidade. Criada a partir da `develop`. |
| `fix/nome` | Correção de bug. Criada a partir da `develop` ou `main`. |
| `docs/nome` | Somente documentação. |
| `test/nome` | Adição ou ajuste de testes. |
| `refactor/nome` | Refatoração sem mudança de comportamento. |

### Boas práticas de nomenclatura

- Use letras minúsculas e hífens: `feat/limpar-coluna-amount`
- Seja descritivo: `fix/corrigir-valor-nulo-timestamp`
- Evite nomes genéricos: `feature1`, `teste`, `novo`
- Inclua sempre o tipo: `feat/`, `fix/`, `docs/`, `test/`, `refactor/`

### Branches por issue - Apenas exemplos

| Issue | Branch |
|-------|--------|
| #1 | `feat/estrutura-repositorio` |
| #2 | `feat/ingestao-pyspark` |
| #3 | `feat/logging-estruturado` |
| #4 | `feat/validacao-dados` |
| #5 | `feat/conciliacao-dados` |
| #6 | `feat/relatorio-rejeicoes` |
| #7 | `test/validacao` |
| #8 | `test/conciliacao` |
| #9 | `feat/dashboard-streamlit` |
| #10 | `feat/docker-airflow` |
| #11 | `feat/airflow-dag` |
| #12 | `docs/runbook-operacional` |

**Nunca trabalhe diretamente na `main` ou na `develop`.**

---

## Commits

### Tipos de commit

| Tipo | Quando usar |
|------|------------|
| `feat:` | Nova funcionalidade |
| `fix:` | Correção de bug |
| `docs:` | Apenas documentação |
| `test:` | Adição ou correção de testes |
| `refactor:` | Refatoração sem mudar comportamento |
| `style:` | Formatação, espaços, vírgulas |
| `chore:` | Tarefas de manutenção, dependências |

### Formato

```
tipo(escopo): descrição curta no imperativo
O '"escopo" é opcional

# Exemplos
feat(ingestao): adicionar leitura de CSV com schema explícito
fix(validacao): corrigir detecção de timestamp vazio
docs(readme): adicionar instruções de execução do Airflow
test(validacao): cobrir caso de amount negativo
refactor(conciliacao): extrair função de agrupamento por banco
chore(deps): adicionar pyspark ao requirements.txt
```

> ⚠️ **Use o imperativo: `adicionar`, `corrigir`, `remover`. NUNCA `adicionando`, `adicionei`, `Testando`, `finalizando`**

### Commits que serão apontados no review

```bash
# Serão comentados como [bloqueante]
git commit -m "fix"
git commit -m "arrumei"
git commit -m "wip"
git commit -m "."
git commit -m "adicionando função"   # gerúndio - use imperativo
git commit -m "adicionei função"     # passado - use imperativo
```

---

## Passo 7 - Verifique antes de enviar

```bash
pytest tests/ -v
git status
git diff --staged
```

**Checklist antes do PR:**
- [ ] Nenhum `.env` aparece em `git status`
- [ ] Nenhuma credencial hardcoded
- [ ] `pytest tests/` passa sem erros
- [ ] Commits semânticos no imperativo
- [ ] Funções com type hints e docstrings

---

## Passo 8 - Envie para o repositório original

```bash
# Envia para a branch develop do upstream — não para a main
git push upstream feat/nome-da-sua-branch
```

Seus commits vão direto para o repositório original - aparecem no seu perfil e contam para badges. EEEEH!

---

## Passo 9 - Abra o Pull Request

No GitHub, acesse o repositório original da Starlight:

1. Clique em **Compare & pull request**
2. **Base:** `develop` ← `feat/nome-da-sua-branch`
3. Preencha título e descrição usando o template automático
4. Em **Development**, adicione `Closes #número-da-issue`
5. Clique em **Create pull request**

> ⚠️ O PR vai para `develop`, não para `main`. PRs direto para `main` serão rejeitados.

---

## O que esperar do review

| Prefixo | O que significa |
|---------|----------------|
| `[bloqueante]` | Precisa ser resolvido antes do merge |
| `[sugestão]` | Melhoria desejável, não bloqueia |
| `[dúvida]` | Pedido de esclarecimento |
| `[elogio]` | Boa prática que merece destaque |

### Como responder

**Bloqueante:** implemente e confirme com o hash do commit.
```
Corrigido no commit abc1234
```

**Sugestão:** implemente se concordar, ou justifique.
```
Mantive a abordagem porque X. Posso ajustar se preferir.
```

Marque a conversa como resolvida **só depois** de implementar ou justificar.

### ⚠️ Aprovação cancelada após novos commits

Se você fizer novos commits **depois de receber uma aprovação**, a aprovação será cancelada automaticamente. Isso é intencional,  garante que o revisor sempre vê o código final.

Se precisar ajustar após a aprovação:
1. Faça as correções
2. Commite: `fix(validacao): corrigir tipo de retorno conforme review`
3. Avise o revisor pedindo novo review

Isso não é punição é como funciona em times profissionais.

---

## Regras do projeto

1. **Nunca commite na `main` ou `develop` diretamente** - todo código passa por PR
2. **Nunca commite o `.env`** - credenciais ficam fora do repositório
3. **Nunca commite dados** - `data/` está no `.gitignore`
4. **Se atribua à issue antes de começar** — use o self-assign
5. **Um PR por issue** - não misture responsabilidades
6. **PRs vão para `develop`**, não para `main`
7. **Sempre envie para o `upstream`** - garante badges e avaliação

---

## Dúvidas

Comente na issue correspondente ou abra uma **Discussion** no repositório.

---

<div align="center">

⭐ [Starlight Git Project](https://github.com/Starlight-git-project) · open source · feito para profissionais de dados

</div>