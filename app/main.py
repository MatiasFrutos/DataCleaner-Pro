"""
DataCleaner Pro
Punto principal interno de la aplicación.

Inicializa la interfaz gráfica principal con CustomTkinter.
"""

from app.config import ensure_project_directories
from app.services.log_service import log_service
from app.ui.app_window import DataCleanerApp


def main():
    ensure_project_directories()

    try:
        log_service.info("Iniciando DataCleaner Pro.")
        app = DataCleanerApp()
        app.mainloop()
        log_service.info("DataCleaner Pro cerrado correctamente.")

    except Exception as error:
        log_service.exception(f"Error crítico iniciando DataCleaner Pro: {error}")
        raise


if __name__ == "__main__":
    main()