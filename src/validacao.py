# Detecção das falhas propositais no dataset
"""
validacao.py

STUB TEMPORÁRIO — Issue #8 ainda não foi mergeada.

Este arquivo existe só para permitir que a Issue de conciliação seja
desenvolvida e testada de forma independente. Quando a Issue #8 for
mergeada de verdade, este arquivo deve ser substituído pela
implementação real de `executar_validacoes`, sem necessidade de
alterar `conciliacao.py` (a assinatura da função é mantida igual).
"""

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def executar_validacoes(df: pd.DataFrame) -> pd.DataFrame:
    """
    STUB temporário. Deve ser substituído pela implementação real da
    Issue #8, que valida regras de negócio (nulos em campos
    obrigatórios, duplicatas, valores fora do esperado, etc).

    Por enquanto, apenas repassa o DataFrame recebido sem alterações,
    para permitir o desenvolvimento e teste da camada de conciliação.

    Args:
        df: DataFrame já lido pela camada de ingestão.

    Returns:
        DataFrame "validado" (sem alterações, nesta versão stub).
    """
    logger.warning(
        "Usando stub de executar_validacoes — Issue #8 ainda não mergeada",
        extra={"linhas": len(df)},
    )
    return df