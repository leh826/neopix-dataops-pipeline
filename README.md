<table>
<tr>
<td width="140">

<img width="120" height="150" alt="NeoPix" src="https://github.com/user-attachments/assets/5102e303-7844-4099-83f9-89fd7d873adb" />

</td>
<td>

# NeoPix - Monitoramento e Operação de Pipelines de Pagamento

> Desafio técnico inspirado em vaga real de **Engenheiro(a) de Dados Júnior - DataOps**  
> Trilha **[Starlight Git Project](https://github.com/Starlight-git-project)**

</td>
</tr>
</table>

## Contexto

A **NeoPix** é uma fintech de pagamentos instantâneos (estilo Pix) com mais de 10 milhões de transações diárias.

O time de **DataOps** é responsável por manter os pipelines que alimentam os dashboards de monitoramento usados pelo time de operações 24/7. Diferente de um time de desenvolvimento que constrói pipelines do zero, o DataOps **herda pipelines existentes** e precisa:

- Garantir que rodem todos os dias sem falha
- Detectar e alertar quando algo quebra
- Dar visibilidade via dashboards
- Orquestrar a execução de forma confiável

Você foi contratada para o time de DataOps. O pipeline de **conciliação de transações** já existe, mas tem problemas. Sua missão é assumir, estabilizar, monitorar e dar visibilidade a ele.

---

## Diferença fundamental do desafio anterior ([VoughtGuard](https://github.com/Starlight-git-project/voughtguard-pipeline-fraud-detection))

| VoughtGuard | NeoPix |
|---|---|
| Construir pipeline do zero | **Herdar e estabilizar** pipeline existente |
| Foco em transformação de dados | Foco em **monitoramento, logging e operação** |
| pandas | **PySpark** |
| Sem orquestração real | **Airflow rodando de fato (Docker Compose)** |
| Relatório em CSV | **Dashboard de visualização** |
| Dados "limpos" desde o início | Dados com **falhas propositais** para você detectar |

---

## Dataset

O dataset não está incluído no repositório, ele contém dados sintéticos de produção e não deve ser versionado no Git.

**Como baixar**

Acesse: Dataset NeoPix - [Google Drive](https://drive.google.com/drive/folders/13u1WjeODVBNVj07C2YwrftflgZxIA29L)
- Faça o download de `transacoes.csv` 
- Salve em `data/raw/transacoes.csv`

A pasta também contém `transacoes_sample.csv`,usado nas fixtures de teste (Issue 07). Esse arquivo vai em `tests/fixtures/transacoes_sample.csv.`

``` bash
Estrutura esperada após o download
data/
└── raw/
    └── transacoes.csv

🚨 data/raw/ está no .gitignore - nunca commite este arquivo.
```

Sobre o dataset

O arquivo contém 10.050 transações Pix simuladas, representando dados
reais de produção, incluindo inconsistências que ocorrem no dia a dia de qualquer pipeline.

| Coluna              | Descrição                                      |
|---------------------|------------------------------------------------|
| `transaction_id`    | Identificador único da transação.              |
| `timestamp`         | Data e hora da transação.                       |
| `amount`            | Valor da transação.                             |
| `status`            | `completed`, `failed`, `pending` ou `reversed`. |
| `origin_bank`       | Banco de origem.                               |
| `destination_bank`  | Banco de destino.                              |
| `processing_time_ms`| Tempo de processamento em milissegundos.       |


> Parte da sua missão é **investigar e identificar inconsistências** neste
dataset através da **camada de validação** que você vai construir.
Você não vai receber uma lista de problemas, vai **construir o sistema
que os encontra**. É exatamente isso que o time de DataOps faz: não sabe o que vai encontrar até monitorar.

## O pipeline tem problemas

O dataset fornecido não é o mesmo dataset "limpo" do desafio anterior, 
ele contém **dados reais de produção**, com inconsistências que 
acontecem no dia a dia de qualquer pipeline.

Algumas perguntas que vão guiar sua investigação:
- Todos os timestamps estão em formato e ordem consistentes?
- Existe algum valor de `amount` que não faz sentido?
- O campo `status` sempre tem um valor dentro do esperado?
- Há transações duplicadas?
- Algum `processing_time_ms` indica que algo travou?

Aqui ninguém te entrega uma lista do que está quebrado. Você recebe o pipeline e descobre os problemas rodando, lendo logs, validando.
---

## Entregáveis

| # | Entregável | O que avalia |
|---|-----------|-------------|
| 01 | Repositório público com README claro | Documentação |
| 02 | Pipeline em **PySpark** - leitura, validação, conciliação | Stack técnica da vaga |
| 03 | Sistema de **logging estruturado** - todo erro registrado com contexto | Observabilidade |
| 04 | **DAG do Airflow** rodando via Docker Compose | Orquestração real |
| 05 | **Dashboard de visualização** (Streamlit) com métricas de saúde do pipeline | DataViz |
| 06 | Testes automatizados com `pytest` | Qualidade |
| 07 | `docs/runbook.md` — o que fazer quando o pipeline falha | Operação/DataOps |

---

## Estrutura do repositório

```
neopix-pipeline-monitor/
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── docker-compose.yml          # Airflow local
│
├── data/
│   ├── raw/                    # dados originais com falhas
│   │   └── .gitkeep
│   └── processed/              # dados conciliados + relatórios
│       └── .gitkeep
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── ingestao.py             # leitura PySpark com schema validation
│   ├── validacao.py            # detecção das falhas
│   ├── conciliacao.py          # lógica de conciliação
│   └── logging_config.py       # logging estruturado (JSON)
│
├── dags/
│   └── pipeline_neopix_dag.py  # DAG do Airflow
│
├── dashboard/
│   └── app.py                  # Streamlit - saúde do pipeline
│
├── tests/
│   ├── fixtures/
│   │   └── transacoes_sample.csv
│   ├── test_validacao.py
│   └── test_conciliacao.py
│
├── logs/
│   └── .gitkeep                # logs gerados em runtime, não commitados
│
└── docs/
    └── runbook.md              # guia de operação e troubleshooting
```

---

## Como começar

### 1. Faça fork deste repositório

```bash
# No GitHub: clique em Fork (canto superior direito)
```

### 2. Clone o seu fork

```bash
git clone https://github.com/SEU-USUARIO/neopix-dataops-pipeline.git
cd neopix-dataops-pipeline
```

### 3. Configure o remote original

```bash
git remote add upstream https://github.com/Starlight-git-project/neopix-dataops-pipeline.git
```

### 4. Configure o ambiente

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows

pip install -r requirements.txt
cp .env.example .env
```

### 5. Suba o Airflow local

```bash
docker-compose up
```

Acesse a UI do Airflow em `http://localhost:8080`

### 6. Execute o dashboard

```bash
streamlit run dashboard/app.py
```

### 7. Rode os testes

```bash
pytest tests/
```

---

## Métricas mínimas do dashboard

- Total de transações processadas
- Taxa de sucesso vs falha (`completed` / `failed` / `pending` / `reversed`)
- Tempo médio de processamento (`processing_time_ms`)
- Quantidade de registros rejeitados pela validação (com motivo)
- Gráfico de transações por banco de origem/destino
- Status da última execução do pipeline (sucesso/falha + timestamp)

---

## Critérios de avaliação

| Critério | O que será observado |
|----------|---------------------|
| **PySpark aplicado corretamente** | Uso de DataFrame API, schema explícito, não é só pandas com nome trocado |
| **Logging estruturado** | Logs em JSON com nível, contexto, timestamp - não `print()` |
| **DAG funcional no Airflow** | `docker-compose up` sobe o Airflow e o DAG executa |
| **Dashboard funcional** | Roda localmente e reflete dados reais do pipeline |
| **Tratamento de falhas propositais** | Cada falha do dataset é detectada e tratada, não ignorada |
| **Runbook** | Documento claro, qualquer pessoa do time consegue seguir |
| **Git e colaboração** | Commits, branches, PRs e code review - mesma régua da Trilha 02 |

---

## Pré-requisitos técnicos

- Docker e Docker Compose instalados
- Python 3.11
- PySpark (`pip install pyspark`)
- Apache Airflow (via Docker)

---

## Entrega

Cada issue tem uma branch e um critério de aceite específico. Consulte o **[CONTRIBUTING.md](./CONTRIBUTING.md)** para o fluxo completo: como pegar uma issue, criar a branch, e abrir o PR.

---

## Antes de começar

Esse desafio assume domínio das três trilhas:

→ **[Trilha 01 — Fundamentos](https://github.com/Starlight-git-project/trilha-01-fundamentos)**

→ **[Trilha 02 — Governança](https://github.com/Starlight-git-project/trilha-02-governanca)**

→ **[Trilha 03 — Infraestrutura](https://github.com/Starlight-git-project/trilha-03-infraestrutura)**

Além disso, recomenda-se ter concluído o **[VoughtGuard](https://github.com/Starlight-git-project/voughtguard-pipeline-fraud-detection)** - o NeoPix assume que você já sabe estruturar um repositório de dados e trabalhar com PRs.

---

<div align="center">

⭐ [Starlight Git Project](https://github.com/Starlight-git-project) · open source · feito para profissionais de dados

</div>
