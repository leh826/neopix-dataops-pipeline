"""
logging_config.py

Logger central estruturado (JSON) para todo o pipeline NeoPix.

Por que logging estruturado?
Em DataOps, logs de texto livre (ex: print("erro")) não servem pra nada em
produção: ninguém consegue buscar, filtrar ou criar alertas em cima disso.
Logando em JSON, cada evento vira um registro com campos fixos
(timestamp, level, module, message + contexto extra), que pode ser
consultado por qualquer ferramenta de observabilidade (ELK, Datadog, etc.)
sem precisar de regex.

Uso básico:
    from src.logging_config import get_logger

    logger = get_logger("ingestao")

    logger.info("Arquivo carregado com sucesso", extra={"linhas": 10050})

    logger.warning(
        "Coluna com valores nulos detectada",
        extra={"coluna": "amount", "qtd_nulos": 12},
    )

    logger.error(
        "Falha ao processar transação",
        extra={"transaction_id": "abc123", "error_type": "SchemaError"},
    )

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception(
            "Erro inesperado ao dividir valores",
            extra={"transaction_id": "abc123"},
        )
"""

import logging
import os
from logging import Logger
from logging.handlers import RotatingFileHandler

from pythonjsonlogger import jsonlogger

LOG_DIR = "logs"
LOG_FILE_PATH = os.path.join(LOG_DIR, "pipeline.log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


class ContextJsonFormatter(jsonlogger.JsonFormatter):
    """
    Formatter JSON customizado que garante a presença dos campos
    obrigatórios (timestamp, level, module, message) em todo log,
    além de qualquer campo extra passado via `extra={...}`.
    """

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        log_record["timestamp"] = self.formatTime(record, self.datefmt)
        log_record["level"] = record.levelname
        log_record["module"] = record.name
        log_record["message"] = record.getMessage()


def get_logger(nome_modulo: str) -> Logger:
    """
    Retorna um logger configurado para saída estruturada em JSON,
    escrevendo simultaneamente no console e em `logs/pipeline.log`.

    A função é idempotente: chamar `get_logger` várias vezes com o mesmo
    nome de módulo não duplica handlers nem duplica linhas de log.

    Args:
        nome_modulo: nome do módulo que está logando (ex: "ingestao",
            "validacao", "conciliacao"). Aparece no campo "module" do JSON.

    Returns:
        Uma instância de `logging.Logger` pronta para uso, com métodos
        `.info()`, `.warning()`, `.error()`, `.exception()`, `.debug()`.

    Exemplo:
        >>> logger = get_logger("ingestao")
        >>> logger.info("Iniciando leitura do CSV")
        >>> logger.error(
        ...     "Transação com status inválido",
        ...     extra={"transaction_id": "abc123", "error_type": "StatusInvalido"},
        ... )
    """
    logger = logging.getLogger(nome_modulo)

    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)
    logger.propagate = False

    formatter = ContextJsonFormatter()

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    os.makedirs(LOG_DIR, exist_ok=True)
    file_handler = RotatingFileHandler(
        LOG_FILE_PATH,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
