## Por que isso existe?

O pipeline da NeoPix roda sozinho, todo dia, sem ninguém olhando em tempo
real. Ele processa milhões de transações Pix. Quando algo dá errado - um
dado corrompido, uma conexão que cai, uma transação com valor impossível -
**ninguém está na frente da tela vendo isso acontecer**.

O `src/logging_config.py` é a "caixa preta" do pipeline. Cada linha de log
gerada é um evento registrado de um jeito que dá pra:

1. **Buscar depois** - "me mostra todos os erros de hoje que envolvem o
   `transaction_id` X"
2. **Filtrar por gravidade** - separar `INFO` (aconteceu normal) de `ERROR`
   (algo quebrou)
3. **Criar alerta automático** - uma ferramenta de monitoramento pode ler
   esse log e avisar automaticamente (ex: Slack) toda vez que aparecer
   `"level": "ERROR"`
4. **Investigar incidente** - se o time de operações receber reclamação de
   um banco, dá pra buscar pelo `transaction_id` exato e ver a história
   completa daquela transação

Compara com a alternativa, `print("deu erro")`: isso só aparece no
terminal, na hora, e some. Se ninguém tava olhando naquele segundo, a
informação morre.

> Em fintech isso é inaceitável - precisa ter rastro!

## Por que JSON e não texto livre?

Texto livre (`"Erro ao processar transação 123"`) exige que alguém escreva
regex pra extrair informação dele depois. JSON já vem estruturado em
campos fixos, pronto pra ser lido por qualquer ferramenta sem parsing
manual:

```json
{"timestamp": "2026-08-14 16:15:37,526", "level": "ERROR", "module": "ingestao", "message": "Falha simulada", "transaction_id": "abc123", "error_type": "TesteManual"}
```

## Onde isso entra no resto do pipeline

Esse módulo é a **base** que as próximas etapas do pipeline usam. Nenhuma
delas configura logging por conta própria, todas importam e usam esse
logger central:

- `ingestao.py` usa `get_logger("ingestao")` pra logar quantas linhas
  foram carregadas, ou se o arquivo não foi encontrado
- `validacao.py` usa `get_logger("validacao")` pra logar cada falha
  detectada no dataset (ex: status inválido, timestamp fora de ordem)
- `conciliacao.py` usa `get_logger("conciliacao")` pra logar o resultado
  da conciliação

## Como usar

```python
from src.logging_config import get_logger

logger = get_logger("nome_do_seu_modulo")

logger.info("Arquivo carregado com sucesso", extra={"linhas": 10050})

logger.warning(
    "Coluna com valores nulos detectada",
    extra={"coluna": "amount", "qtd_nulos": 12},
)

logger.error(
    "Falha ao processar transação",
    extra={"transaction_id": "abc123", "error_type": "SchemaError"},
)
```

## Onde os logs aparecem

- **Console** — em tempo real, enquanto o pipeline roda
- **Arquivo** `logs/pipeline.log` - persistido em disco, com rotação
  automática (não cresce infinito). Essa pasta está no `.gitignore`:
  logs são gerados em runtime, não fazem parte do código versionado.

## Nível de log - quando usar qual

| Nível | Quando usar |
|---|---|
| `INFO` | Evento normal (ex: "arquivo carregado", "pipeline iniciado") |
| `WARNING` | Algo estranho, mas não impede o pipeline de continuar |
| `ERROR` | Algo quebrou e precisa de atenção |
| `EXCEPTION` | Erro capturado em `try/except`, inclui stack trace completo |

### O que é o logs/pipeline.log
É o arquivo de log gerado quando o pipeline roda.
Esse sim continua fora do Git, no .gitignore, porque é dado de runtime, não documentação.

