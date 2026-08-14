"""
ingestao.py

Camada de leitura dos dados brutos do pipeline NeoPix.
Porta de entrada dos dados: aplica schema explícito e nunca falha em
silêncio (todo erro é logado com contexto via logging_config.py).
"""

import os

import pandas as pd

from src.config import CAMINHO_TRANSACOES, COLUNAS_ESPERADAS, DTYPES_ESPERADOS
from src.logging_config import get_logger

logger = get_logger("ingestao")


def _validar_colunas(df: pd.DataFrame, caminho: str) -> None:
    """
    Valida se o DataFrame lido tem exatamente as colunas esperadas
    (nem faltando, nem a mais). Roda antes de qualquer conversão de
    tipo, pra evitar KeyError ao acessar uma coluna que não existe.

    Args:
        df: DataFrame recém-lido do CSV, ainda sem conversão de tipos.
        caminho: caminho de origem do arquivo (usado só para contexto no log).

    Raises:
        ValueError: se colunas estiverem faltando ou sobrando.
    """
    colunas_reais = set(df.columns)
    colunas_esperadas = set(COLUNAS_ESPERADAS)

    faltando = colunas_esperadas - colunas_reais
    extras = colunas_reais - colunas_esperadas

    if faltando or extras:
        logger.error(
            "Schema incompatível: colunas divergentes",
            extra={
                "caminho": caminho,
                "colunas_faltando": list(faltando),
                "colunas_extras": list(extras),
            },
        )
        raise ValueError(f"Schema incompatível no arquivo {caminho}: colunas divergentes")


def ler_transacoes(caminho: str = CAMINHO_TRANSACOES) -> pd.DataFrame:
    """
    Lê o arquivo CSV de transações, aplica os dtypes esperados e valida
    o schema resultante.

    Args:
        caminho: caminho do arquivo CSV (default: config.CAMINHO_TRANSACOES).

    Returns:
        DataFrame pandas com os dados carregados e o schema validado.

    Raises:
        FileNotFoundError: se o arquivo não existir no caminho informado.
        ValueError: se o schema do arquivo não corresponder ao esperado.
        Exception: se ocorrer qualquer outro erro durante a leitura.

    Exemplo:
        >>> df = ler_transacoes("data/raw/transacoes.csv")
        >>> df.shape
        (10050, 7)
    """
    if not os.path.exists(caminho):
        logger.error("Arquivo não encontrado", extra={"caminho": caminho})
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    try:
        # Lê sem dtype ainda: se colunas estiverem faltando, queremos que
        # isso vire um ValueError limpo em _validar_colunas(), não um
        # KeyError feio ao tentar acessar uma coluna inexistente.
        df = pd.read_csv(caminho)
        linhas = len(df)
        logger.info("Arquivo lido com sucesso", extra={"caminho": caminho, "linhas": linhas})
    except Exception as e:
        logger.error("Falha ao ler CSV", extra={"caminho": caminho, "erro": str(e)})
        raise

    _validar_colunas(df, caminho)

    # Só converte tipos depois de confirmar que as colunas existem.
    # timestamp usa errors="coerce": valores fora do formato viram NaT
    # (não quebram a leitura, mas ficam rastreáveis pela validação, issue #8).
    for coluna, dtype_esperado in DTYPES_ESPERADOS.items():
        try:
            df[coluna] = df[coluna].astype(dtype_esperado)
        except (ValueError, TypeError) as e:
            logger.error(
                "Falha ao converter tipo de coluna",
                extra={"caminho": caminho, "coluna": coluna, "erro": str(e)},
            )
            raise ValueError(
                f"Schema incompatível no arquivo {caminho}: "
                f"coluna '{coluna}' não pôde ser convertida para {dtype_esperado}"
            )

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    logger.info("Schema validado com sucesso", extra={"caminho": caminho})

    return df
