<table>
<tr>
<td width="140">

<img width="120" height="150" alt="NeoPix" src="https://github.com/user-attachments/assets/5102e303-7844-4099-83f9-89fd7d873adb" />

</td>
<td>

# NeoPix - Monitoramento e Operação de Pipelines de Pagamento

> Projeto inspirado em desafio técnico para vaga de **Engenheiro(a) de Dados Júnior - DataOps**  
> Trilha **[Starlight Git Project](https://github.com/Starlight-git-project)**

</td>
</tr>
</table>

## 📌 Contexto

A **NeoPix** é uma fintech de pagamentos instantâneos (estilo Pix) com mais de 10 milhões de transações diárias.

Este projeto simula a rotina do time de **DataOps**, responsável por manter os pipelines que alimentam os dashboards de monitoramento usados pela operação 24/7. Diferente de construir um pipeline do zero, aqui o desafio é **herdar um pipeline existente** e:

- Garantir que rode todos os dias sem falha
- Detectar e alertar quando algo quebra
- Dar visibilidade via dashboards
- Orquestrar a execução de forma confiável

A missão é assumir, estabilizar, monitorar e dar visibilidade ao pipeline de **conciliação de transações** que existe.

### Sobre o dataset

- 10.050 transações Pix simuladas, com inconsistências reais de pipeline.
- **Não versionado no Git** — baixado separadamente e salvo em `data/raw/transacoes.csv`.
- Um arquivo `transacoes_sample.csv` é usado nas fixtures de teste (`tests/fixtures/`).

| Coluna | Descrição |
|---|---|
| `transaction_id` | Identificador único da transação |
| `timestamp` | Data e hora da transação |
| `amount` | Valor da transação |
| `status` | `completed`, `failed`, `pending` ou `reversed` |
| `origin_bank` | Banco de origem |
| `destination_bank` | Banco de destino |
| `processing_time_ms` | Tempo de processamento em milissegundos |

---

## ⚙️ Instalação

### Pré-requisitos

- Python 3.11
- Docker e Docker Compose
- Java (JDK) instalado — necessário para o PySpark funcionar

### 1. Fork e clone do repositório

```bash
git clone https://github.com/SEU-USUARIO/neopix-dataops-pipeline.git
cd neopix-dataops-pipeline
```

### 2. Configurar o remote original (upstream)

```bash
git remote add upstream https://github.com/Starlight-git-project/neopix-dataops-pipeline.git
```

### 3. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

### 6. Baixar o dataset

- Baixar `transacoes.csv` do [Google Drive](https://drive.google.com/drive/folders/13u1WjeODVBNVj07C2YwrftflgZxIA29L)
- Salvar em `data/raw/transacoes.csv`
- Baixar `transacoes_sample.csv` e salvar em `tests/fixtures/transacoes_sample.csv`

> 🚨 `data/raw/` está no `.gitignore` — o dataset nunca deve ser commitado.

### 7. Subir o Airflow local

```bash
docker-compose up
```

Acessar a UI em `http://localhost:8080`

### 8. Executar o dashboard

```bash
streamlit run dashboard/app.py
```

### 9. Rodar os testes

```bash
pytest tests/
```

---

## 🗂️ Estrutura de pastas

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
│   │   ├── transacoes.csv
│   │   └── .gitkeep
│   └── processed/              # dados conciliados e relatórios
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
│   └── .gitkeep                # logs gerados em runtime
│
└── docs/
    ├── orientacoes.md
    └── runbook.md              # guia de operação e troubleshooting
```

---

## ✅ Tarefas do Projeto

Progresso das entregas em relação ao escopo do desafio.

- [x] **Repositório público com README claro** — documentação inicial do projeto
- [ ] **Pipeline em PySpark** — leitura, validação e conciliação usando DataFrame API
- [ ] **Sistema de logging estruturado** — todo erro registrado em JSON, com contexto
- [ ] **DAG do Airflow** — orquestração real, rodando via Docker Compose
- [ ] **Dashboard de visualização (Streamlit)** — métricas de saúde do pipeline
- [ ] **Testes automatizados (pytest)** — cobertura das regras de validação e conciliação
- [ ] **`docs/runbook.md`** — guia do que fazer quando o pipeline falha

## 📊 Métricas do dashboard

- Total de transações processadas
- Taxa de sucesso vs falha (`completed` / `failed` / `pending` / `reversed`)
- Tempo médio de processamento (`processing_time_ms`)
- Quantidade de registros rejeitados pela validação (com motivo)
- Gráfico de transações por banco de origem/destino
- Status da última execução do pipeline (sucesso/falha + timestamp)

