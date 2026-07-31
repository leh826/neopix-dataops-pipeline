from pyspark.sql import SparkSession


def get_spark_session(app_name: str = "neopix-pipeline") -> SparkSession:
    """
    Cria (ou reaproveita) uma sessão Spark local.

    Args:
        app_name: nome da aplicação Spark (aparece nos logs e na UI do Spark).

    Returns:
        SparkSession ativa e pronta para uso.
    """
    return (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .getOrCreate()
    )


# Caminhos do projeto (nunca hardcoded nos módulos que os usam)
CAMINHO_TRANSACOES = "data/raw/transacoes.csv"