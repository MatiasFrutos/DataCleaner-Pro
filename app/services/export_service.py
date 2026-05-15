"""
Servicio de exportación para DataCleaner Pro.

Conecta la interfaz con el exportador de datos y genera reporte final
cuando la exportación se completa correctamente.
"""

from app.core.data_exporter import export_dataframe, DataExporterError
from app.core.report_builder import build_process_report
from app.models.export_result import ExportResult
from app.services.log_service import log_service


class ExportService:
    """
    Servicio encargado de exportar y recordar la última exportación.
    """

    def __init__(self):
        self.last_result: ExportResult | None = None
        self.last_report_path: str | None = None

    def export(
        self,
        dataframe,
        output_path: str,
        export_format: str,
        file_model=None,
        analysis_result=None,
        cleaning_result=None,
    ):
        """
        Ejecuta exportación y genera reporte de proceso.
        """

        try:
            log_service.info(f"Iniciando exportación: {output_path}")

            result = export_dataframe(dataframe, output_path, export_format)
            self.last_result = result

            self.last_report_path = build_process_report(
                file_model=file_model,
                analysis_result=analysis_result,
                cleaning_result=cleaning_result,
                export_result=result,
            )

            log_service.info(f"Exportación completada: {result.output_path}")
            log_service.info(f"Reporte generado: {self.last_report_path}")

            return result

        except DataExporterError as error:
            log_service.error(f"Error de exportación: {error}")

            result = ExportResult(
                success=False,
                export_format=export_format,
                error=str(error),
            )
            self.last_result = result
            return result

        except Exception as error:
            log_service.exception(f"Error inesperado exportando archivo: {error}")

            result = ExportResult(
                success=False,
                export_format=export_format,
                error=f"Error inesperado: {error}",
            )
            self.last_result = result
            return result

    def get_last_result(self):
        """
        Devuelve el último resultado de exportación.
        """

        return self.last_result

    def get_last_report_path(self):
        """
        Devuelve la ruta del último reporte generado.
        """

        return self.last_report_path

    def reset(self):
        """
        Reinicia el estado del servicio.
        """

        self.last_result = None
        self.last_report_path = None


export_service = ExportService()