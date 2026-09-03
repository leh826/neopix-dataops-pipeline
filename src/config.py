"""
config.py

Configurações e schema esperado do projeto NeoPix.
"""

# Caminho do dataset (nunca hardcoded nos módulos que o usam)
CAMINHO_TRANSACOES = "data/raw/transacoes.csv"
CAMINHO_CONCILIACAO = "data/processed/conciliacao_bancos.csv"
# Schema esperado do dataset de transações.
# Em Pandas não existe StructType (isso é Spark) — o equivalente é
# declarar os dtypes esperados por coluna, usados na validação pós-leitura.
COLUNAS_ESPERADAS = [
    "transaction_id",
    "timestamp",
    "amount",
    "status",
    "origin_bank",
    "destination_bank",
    "processing_time_ms",
]

DTYPES_ESPERADOS = {
    "transaction_id": "object",       # string
    "amount": "float64",
    "status": "object",               # string
    "origin_bank": "object",
    "destination_bank": "object",
    "processing_time_ms": "float64",  # float pra tolerar NaN antes da validação
}
# "timestamp" fica de fora do dict acima de propósito: é convertido
# separadamente com pd.to_datetime (ver ingestao.py), pois datetime
# não se declara do mesmo jeito no read_csv/astype.
