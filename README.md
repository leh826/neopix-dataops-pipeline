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

Este repositório contém o pipeline de conciliação de transações da NeoPix, que
já existe mas tem problemas. A missão do time é assumir, estabilizar,
monitorar e dar visibilidade a ele.

## Stack

- **PySpark** - leitura, validação e conciliação dos dados
- **Orquestração** - em definição (ver nota abaixo)
- **Streamlit** - dashboard de monitoramento
- **pytest** - testes automatizados
- **Logging estruturado (JSON)** - observabilidade

> ⚠️ **Decisão em aberto:** a orquestração ainda não está definida entre
> Airflow (via Docker Compose) ou um script próprio. O `docker-compose.yml`
> permanece no repo como esqueleto e a flag `USE_AIRFLOW` no `.env.example`
> documenta esse estado. Decisão final até a Sprint 4 (issues #14/#15).

## Estrutura do repositório

```

neopix-pipeline-monitor/
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── docker-compose.yml # Airflow local (esqueleto — decisão pendente)
│
├── data/
│ ├── raw/ # dados originais com falhas (não versionado)
│ │ └── .gitkeep
│ └── processed/ # dados conciliados + relatórios
│ └── .gitkeep
│
├── src/
│ ├── init.py
│ ├── config.py
│ ├── ingestao.py # leitura PySpark com schema validation
│ ├── validacao.py # detecção das falhas
│ ├── conciliacao.py # lógica de conciliação
│ └── logging_config.py # logging estruturado (JSON)
│
├── dags/
│ └── .gitkeep # pipeline_neopix_dag.py vem na Issue 15 (se Airflow)
│
├── dashboard/
│ └── .gitkeep # app.py vem na Issue 13
│
├── tests/
│ ├── init.py
│ ├── fixtures/
│ │ └── .gitkeep # transacoes_sample.csv vem na Issue 07
│ ├── test_validacao.py
│ └── test_conciliacao.py
│
├── logs/
│ └── .gitkeep # logs gerados em runtime (não versionado)
│
└── docs/
└── .gitkeep # runbook.md vem na Issue 16



```

## Como começar

### 1. Fork e clone

```bash
git clone https://github.com/SEU-USUARIO/neopix-dataops-pipeline.git
cd neopix-dataops-pipeline
git remote add upstream https://github.com/Starlight-git-project/neopix-dataops-pipeline.git
```

### 2. Ambiente Python

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows

pip install -r requirements.txt
cp .env.example .env
```

### 3. Dataset

O dataset **não está no repositório** (dados sintéticos de produção, não
versionados). Baixe `transacoes.csv` e salve em `data/raw/transacoes.csv`.
`transacoes_sample.csv` vai em `tests/fixtures/`.

> 🚨 `data/raw/` está no `.gitignore` — nunca commite esse arquivo.

### 4. Orquestração (Airflow — enquanto decisão não é fechada)

```bash
docker-compose up
```

> O `docker-compose.yml` ainda é só esqueleto — não está funcional. A decisão
> entre Airflow e script próprio de orquestração está em aberto (ver Stack).

### 5. Dashboard

```bash
streamlit run dashboard/app.py
```

### 6. Testes

```bash
pytest tests/
```

## Entregáveis

| # | Entregável | O que avalia |
|---|---|---|
| 01 | Repositório público com README claro | Documentação |
| 02 | Pipeline em PySpark — leitura, validação, conciliação | Stack técnica da vaga |
| 03 | Sistema de logging estruturado | Observabilidade |
| 04 | Orquestração (Airflow ou script próprio — decisão pendente) | Orquestração real |
| 05 | Dashboard de visualização (Streamlit) | DataViz |
| 06 | Testes automatizados com pytest | Qualidade |
| 07 | `docs/runbook.md` | Operação/DataOps |

## Contribuindo

Cada issue tem uma branch e um critério de aceite específico. Consulte o
`CONTRIBUTING.md` para o fluxo completo de branch e PR.

---

⭐ Starlight Git Project · open source · feito para profissionais de dados
