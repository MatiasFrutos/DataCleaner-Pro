"""
Generador de reportes para DataCleaner Pro.

Crea reportes simples en formato TXT con el resumen del proceso:
archivo cargado, limpieza aplicada y exportación generada.
"""

from datetime import datetime
from pathlib import Path

from app.config import REPORTS_DIR


def build_process_report(
    file_model=None,
    analysis_result=None,
    cleaning_result=None,
    export_result=None,
):
    """
    Genera un reporte TXT del proceso completo.
    Devuelve la ruta del reporte generado.
    """

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = Path(REPORTS_DIR) / f"datacleaner_report_{timestamp}.txt"

    lines = []
    lines.append("============================================================")
    lines.append("DATA CLEANER PRO - REPORTE DE PROCESO")
    lines.append("============================================================")
    lines.append(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    lines.extend(_build_file_section(file_model))
    lines.extend(_build_analysis_section(analysis_result))
    lines.extend(_build_cleaning_section(cleaning_result))
    lines.extend(_build_export_section(export_result))

    lines.append("")
    lines.append("============================================================")
    lines.append("FIN DEL REPORTE")
    lines.append("============================================================")

    report_path.write_text("\n".join(lines), encoding="utf-8")

    return str(report_path)


def _build_file_section(file_model):
    lines = []
    lines.append("ARCHIVO")
    lines.append("------------------------------------------------------------")

    if not file_model:
        lines.append("Sin información de archivo.")
        lines.append("")
        return lines

    lines.append(f"Nombre: {getattr(file_model, 'name', 'N/A')}")
    lines.append(f"Ruta: {getattr(file_model, 'path', 'N/A')}")
    lines.append(f"Extensión: {getattr(file_model, 'extension', 'N/A')}")
    lines.append(f"Tamaño: {getattr(file_model, 'size_label', 'N/A')}")
    lines.append(f"Filas: {getattr(file_model, 'rows', 0)}")
    lines.append(f"Columnas: {getattr(file_model, 'columns', 0)}")
    lines.append(f"Cargado: {getattr(file_model, 'loaded', False)}")

    error = getattr(file_model, "error", None)

    if error:
        lines.append(f"Error: {error}")

    lines.append("")
    return lines


def _build_analysis_section(analysis_result):
    lines = []
    lines.append("ANÁLISIS")
    lines.append("------------------------------------------------------------")

    if not analysis_result:
        lines.append("No se registró análisis.")
        lines.append("")
        return lines

    lines.append(f"Filas totales: {analysis_result.total_rows}")
    lines.append(f"Columnas totales: {analysis_result.total_columns}")
    lines.append(f"Celdas totales: {analysis_result.total_cells}")
    lines.append(f"Celdas vacías: {analysis_result.empty_cells}")
    lines.append(f"Filas vacías: {analysis_result.empty_rows}")
    lines.append(f"Columnas vacías: {analysis_result.empty_columns}")
    lines.append(f"Duplicados: {analysis_result.duplicated_rows}")
    lines.append(f"Score de calidad: {analysis_result.quality_score}%")
    lines.append(f"Nivel de riesgo: {analysis_result.risk_level}")
    lines.append("")

    lines.append("Advertencias:")
    if analysis_result.warnings:
        for warning in analysis_result.warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- Sin advertencias.")

    lines.append("")

    lines.append("Recomendaciones:")
    if analysis_result.recommendations:
        for recommendation in analysis_result.recommendations:
            lines.append(f"- {recommendation}")
    else:
        lines.append("- Sin recomendaciones.")

    lines.append("")
    return lines


def _build_cleaning_section(cleaning_result):
    lines = []
    lines.append("LIMPIEZA")
    lines.append("------------------------------------------------------------")

    if not cleaning_result:
        lines.append("No se registró limpieza.")
        lines.append("")
        return lines

    lines.append(f"Éxito: {cleaning_result.success}")
    lines.append(f"Filas originales: {cleaning_result.original_rows}")
    lines.append(f"Columnas originales: {cleaning_result.original_columns}")
    lines.append(f"Filas limpias: {cleaning_result.cleaned_rows}")
    lines.append(f"Columnas limpias: {cleaning_result.cleaned_columns}")
    lines.append(f"Filas vacías eliminadas: {cleaning_result.removed_empty_rows}")
    lines.append(f"Columnas vacías eliminadas: {cleaning_result.removed_empty_columns}")
    lines.append(f"Duplicados eliminados: {cleaning_result.removed_duplicates}")
    lines.append(f"Celdas de texto limpiadas: {cleaning_result.cleaned_text_cells}")
    lines.append(f"Columnas normalizadas: {cleaning_result.normalized_columns}")
    lines.append(f"Fechas normalizadas: {cleaning_result.normalized_dates}")

    if cleaning_result.error:
        lines.append(f"Error: {cleaning_result.error}")

    lines.append("")

    lines.append("Acciones aplicadas:")
    if cleaning_result.actions:
        for action in cleaning_result.actions:
            lines.append(f"- {action}")
    else:
        lines.append("- Sin acciones registradas.")

    if cleaning_result.warnings:
        lines.append("")
        lines.append("Advertencias de limpieza:")
        for warning in cleaning_result.warnings:
            lines.append(f"- {warning}")

    lines.append("")
    return lines


def _build_export_section(export_result):
    lines = []
    lines.append("EXPORTACIÓN")
    lines.append("------------------------------------------------------------")

    if not export_result:
        lines.append("No se registró exportación.")
        lines.append("")
        return lines

    lines.append(f"Éxito: {export_result.success}")
    lines.append(f"Formato: {export_result.export_format}")
    lines.append(f"Ruta de salida: {export_result.output_path}")
    lines.append(f"Filas exportadas: {export_result.rows}")
    lines.append(f"Columnas exportadas: {export_result.columns}")
    lines.append(f"Tamaño final: {export_result.file_size_label}")

    if export_result.error:
        lines.append(f"Error: {export_result.error}")

    lines.append("")
    return lines