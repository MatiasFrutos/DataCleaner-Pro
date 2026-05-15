"""
Servicio de limpieza para DataCleaner Pro.

Conecta la interfaz con el motor de limpieza automática.
"""

from app.core.data_cleaner import clean_dataframe, DataCleanerError
from app.models.cleaning_result import CleaningResult


class CleaningService:
    """
    Servicio encargado de ejecutar y recordar la última limpieza.
    """

    def __init__(self):
        self.last_result: CleaningResult | None = None

    def clean(self, dataframe, options=None):
        """
        Ejecuta limpieza sobre un DataFrame.
        """

        if options is None:
            options = {}

        try:
            cleaned_dataframe, result = clean_dataframe(
                dataframe,
                remove_empty_rows=options.get("remove_empty_rows", True),
                remove_empty_columns=options.get("remove_empty_columns", True),
                remove_duplicates=options.get("remove_duplicates", True),
                trim_text=options.get("trim_text", True),
                normalize_columns=options.get("normalize_columns", True),
                normalize_missing_values=options.get("normalize_missing_values", True),
                normalize_dates=options.get("normalize_dates", True),
            )

            self.last_result = result

            return cleaned_dataframe, result

        except DataCleanerError as error:
            result = CleaningResult(success=False, error=str(error))
            self.last_result = result
            return None, result

        except Exception as error:
            result = CleaningResult(success=False, error=f"Error inesperado: {error}")
            self.last_result = result
            return None, result

    def get_last_result(self):
        """
        Devuelve el último resultado.
        """

        return self.last_result

    def reset(self):
        """
        Limpia el estado del servicio.
        """

        self.last_result = None


cleaning_service = CleaningService()