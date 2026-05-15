"""
Exportador de datos para DataCleaner Pro.

Permite exportar DataFrames limpios a Excel o CSV.
"""

from pathlib import Path

import pandas as pd

from app.models.export_result import ExportResult
from app.utils.file_utils import get_file_size_label


class DataExporterError(Exception):
    """
    Error personalizado para fallos de exportación.
    """


def export_dataframe(dataframe: pd.DataFrame, output_path: str, export_format: str):
    """
    Exporta un DataFrame a XLSX o CSV.
    """

    if dataframe is None:
        raise DataExporterError("No hay datos para exportar.")

    if dataframe.empty:
        raise DataExporterError("El DataFrame está vacío. No se exportó el archivo.")

    export_format = str(export_format).lower().strip().replace(".", "")

    if export_format not in {"xlsx", "csv"}:
        raise DataExporterError("Formato de exportación no soportado. Usá xlsx o csv.")

    path = Path(output_path)

    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

    if path.suffix.lower() != f".{export_format}":
        path = path.with_suffix(f".{export_format}")

    try:
        if export_format == "xlsx":
            dataframe.to_excel(path, index=False, engine="openpyxl")

        elif export_format == "csv":
            dataframe.to_csv(path, index=False, encoding="utf-8-sig")

        rows, columns = dataframe.shape

        result = ExportResult(
            success=True,
            output_path=str(path),
            export_format=export_format,
            rows=int(rows),
            columns=int(columns),
            file_size_label=get_file_size_label(str(path)),
            error=None,
        )

        return result

    except Exception as error:
        raise DataExporterError(f"No se pudo exportar el archivo: {error}") from error