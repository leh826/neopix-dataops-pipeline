import logging
import os

from pyspark.sql import DataFrame
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    IntegerType,
    TimestampType,
)

from src.config import get_spark_session, CAMINHO_TRANSACOES

logger = logging.getLogger(__name__)

schema_transacoes = StructType([
    StructField("transaction_id", StringType(), nullable=False),
    StructField("timestamp", TimestampType(), nullable=True),
    StructField("amount", DoubleType(), nullable=True),
    StructField("status", StringType(), nullable=True),
    StructField("origin_bank", StringType(), nullable=True),
    StructField("destination_bank", StringType(), nullable=True),
    StructField("processing_time_ms", IntegerType(), nullable=True),
])


def validar_schema(df: DataFrame, caminho: str, schema_esperado: StructType) -> None:
    """
    Valida se o schema real do DataFrame bate com o schema esperado.

    Args:
        df: DataFrame a ser validado.
        caminho: caminho de origem do arquivo (usado só para contexto no log).
        schema_esperado: schema que o DataFrame deveria ter.

    Raises:
        ValueError: se o schema real não corresponder ao esperado.
    """
    schema_real = df.schema
    if schema_real != schema_esperado:
        colunas_esperadas = set(f.name for f in schema_esperado.fields)
        colunas_reais = set(f.name for f in schema_real.fields)

        faltando = colunas_esperadas - colunas_reais
        extras = colunas_reais - colunas_esperadas

        logger.error(
            "Schema incompatível",
            extra={
                "caminho": caminho,
                "colunas_faltando": list(faltando),
                "colunas_extras": list(extras),
            },
        )
        raise ValueError(f"Schema incompatível no arquivo {caminho}")

    logger.info("Schema validado com sucesso", extra={"caminho": caminho})


def ler_transacoes(
    caminho: str = CAMINHO_TRANSACOES,
    schema: StructType = schema_transacoes,
) -> DataFrame:
    """
    Lê o arquivo CSV de transações usando schema explícito e valida
    se o schema real do arquivo corresponde ao esperado.

    Args:
        caminho: caminho do arquivo CSV (default: config.CAMINHO_TRANSACOES).
        schema: schema explícito esperado (default: schema_transacoes).

    Returns:
        DataFrame com os dados carregados.

    Raises:
        FileNotFoundError: se o arquivo não existir no caminho informado.
        ValueError: se o schema do arquivo não corresponder ao esperado.
        Exception: se ocorrer qualquer outro erro durante a leitura pelo Spark.
    """
    if not os.path.exists(caminho):
        logger.error("Arquivo não encontrado", extra={"caminho": caminho})
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    spark = get_spark_session()

    try:
        df = spark.read.csv(caminho, header=True, schema=schema)
        linhas = df.count()
        logger.info(
            "Arquivo lido com sucesso",
            extra={"caminho": caminho, "linhas": linhas},
        )
    except Exception as e:
        logger.error(
            "Falha ao ler CSV",
            extra={"caminho": caminho, "erro": str(e)},
        )
        raise

    validar_schema(df, caminho, schema)

    return df