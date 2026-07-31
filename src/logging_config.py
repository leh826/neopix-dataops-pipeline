import logging
import json
from datetime import datetime, timezone

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        
        if hasattr(record, "caminho_transacoes"):
            log_data["caminho_transacoes"] = record.caminho_transacoes
        if hasattr(record, "erro"):
            log_data["erro"] = record.erro
        return json.dumps(log_data, ensure_ascii=False)


def setup_logging():
    """Configura o logging da aplicação inteira. Chamado uma vez, no início."""
    handler_arquivo = logging.FileHandler("logs/pipeline.log")
    handler_arquivo.setFormatter(JSONFormatter())

    handler_console = logging.StreamHandler()
    handler_console.setFormatter(JSONFormatter())

    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler_arquivo, handler_console]
    )