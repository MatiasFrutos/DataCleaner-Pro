"""
Servicio de logs para DataCleaner Pro.

Centraliza el registro de eventos, errores y acciones principales
de la aplicación.
"""

import logging
from pathlib import Path

from app.config import LOG_FILE, LOG_DATE_FORMAT, ensure_project_directories


class LogService:
    """
    Servicio centralizado de logging.
    """

    def __init__(self):
        ensure_project_directories()
        self.logger = logging.getLogger("DataCleanerPro")
        self.logger.setLevel(logging.INFO)
        self._configure_logger()

    def _configure_logger(self):
        """
        Configura handlers solo una vez.
        """

        if self.logger.handlers:
            return

        log_path = Path(LOG_FILE)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(message)s",
            datefmt=LOG_DATE_FORMAT,
        )

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message: str):
        """
        Registra mensaje informativo.
        """

        self.logger.info(message)

    def warning(self, message: str):
        """
        Registra advertencia.
        """

        self.logger.warning(message)

    def error(self, message: str):
        """
        Registra error.
        """

        self.logger.error(message)

    def exception(self, message: str):
        """
        Registra excepción con traceback.
        """

        self.logger.exception(message)


log_service = LogService()