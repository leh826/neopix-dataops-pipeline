"""
conciliacao.py
 
Camada de conciliação do pipeline NeoPix.
Agrupa transações já validadas por banco de origem/destino, calcula
métricas de saúde (taxa de sucesso, tempo médio de processamento) e
persiste o resultado consolidado em data/processed/.
"""
 
import pandas as pd
 
from src.config import CAMINHO_TRANSACOES, CAMINHO_CONCILIACAO
from src.ingestao import ler_transacoes
from src.logging_config import get_logger
from src.validacao import executar_validacoes  # Issue #8 — stub por enquanto
 
logger = get_logger("conciliacao")
 
 
def conciliar_por_banco(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa transações por banco de origem e destino, somando o valor
    total (amount) e contando a quantidade de transações em cada par.
 
    Args:
        df: DataFrame de transações já validado.
 
    Returns:
        DataFrame agrupado por (origin_bank, destination_bank), com as
        colunas total_amount e qtd_transacoes.
    """
    return (
        df.groupby(["origin_bank", "destination_bank"])
        .agg(
            total_amount=("amount", "sum"),
            qtd_transacoes=("amount", "count"),
        )
        .reset_index()
    )

def calcular_taxa_sucesso(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula o percentual de transações com status "completed" em
    relação ao total de transações, agrupado por banco de origem.
 
    Args:
        df: DataFrame de transações já validado.
 
    Returns:
        DataFrame agrupado por origin_bank, com as colunas
        qtd_completed, qtd_total e taxa_sucesso (0 a 100).
    """
    df_temp = df.copy()
    df_temp["completed"] = df_temp["status"] == "completed"
 
    resultado = (
        df_temp.groupby("origin_bank")
        .agg(
            qtd_completed=("completed", "sum"),
            qtd_total=("completed", "count"),
        )
        .reset_index()
    )
    resultado["taxa_sucesso"] = (
        (resultado["qtd_completed"] / resultado["qtd_total"]) * 100
    ).round(2)
 
    return resultado


def tempo_medio_processamento(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula o tempo médio de processamento (em milissegundos) das
    transações, agrupado por banco de origem.
 
    Args:
        df: DataFrame de transações já validado.
 
    Returns:
        DataFrame agrupado por origin_bank, com a coluna tempo_medio_ms.
    """
    return (
        df.groupby("origin_bank")
        .agg(tempo_medio_ms=("processing_time_ms", "mean"))
        .round(2)
        .reset_index()
    )

def salvar_conciliacao(df: pd.DataFrame, caminho: str) -> None:
    """
    Salva o resultado da conciliação em disco, em formato CSV.
 
    Args:
        df: DataFrame com o resultado a ser salvo.
        caminho: caminho completo do arquivo de destino
            (ex: data/processed/conciliacao_bancos.csv).
 
    Raises:
        Exception: se ocorrer qualquer erro durante a escrita em disco.
    """
    try:
        df.to_csv(caminho, index=False)
        logger.info("Conciliação salva com sucesso", extra={"caminho": caminho})
    except Exception as e:
        logger.error(
            "Falha ao salvar conciliação",
            extra={"caminho": caminho, "erro": str(e)},
        )
        raise


    