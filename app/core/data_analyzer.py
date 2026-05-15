"""
Motor de análisis de datos para DataCleaner Pro.

Detecta problemas básicos de calidad del dato:
- celdas vacías
- filas vacías
- columnas vacías
- duplicados
- tipos de datos
- columnas con alto porcentaje de faltantes
"""

import pandas as pd

from app.models.analysis_result import AnalysisResult
from app.utils.dataframe_utils import (
    count_empty_cells,
    count_empty_rows,
    count_empty_columns,
    get_column_types,
)


def analyze_dataframe(dataframe: pd.DataFrame) -> AnalysisResult:
    """
    Analiza un DataFrame y devuelve un AnalysisResult.
    """

    if dataframe is None:
        result = AnalysisResult()
        result.quality_score = 0
        result.risk_level = "Alto"
        result.warnings.append("No hay datos cargados para analizar.")
        result.recommendations.append("Cargá un archivo válido antes de ejecutar el análisis.")
        return result

    rows, columns = dataframe.shape
    total_cells = int(rows * columns)

    result = AnalysisResult(
        total_rows=int(rows),
        total_columns=int(columns),
        total_cells=total_cells,
    )

    normalized = dataframe.replace(r"^\s*$", pd.NA, regex=True)

    result.empty_cells = count_empty_cells(dataframe)
    result.empty_rows = count_empty_rows(dataframe)
    result.empty_columns = count_empty_columns(dataframe)
    result.duplicated_rows = int(dataframe.duplicated().sum())

    result.column_types = get_column_types(dataframe)
    result.nulls_by_column = {
        str(column): int(normalized[column].isna().sum())
        for column in normalized.columns
    }

    result.empty_percentage_by_column = _calculate_empty_percentages(
        result.nulls_by_column,
        result.total_rows,
    )

    _add_warnings(result)
    _add_recommendations(result)
    _calculate_quality_score(result)

    return result


def _calculate_empty_percentages(nulls_by_column, total_rows):
    """
    Calcula porcentaje de vacíos por columna.
    """

    if total_rows <= 0:
        return {
            column: 0.0
            for column in nulls_by_column
        }

    return {
        column: round((empty_count / total_rows) * 100, 2)
        for column, empty_count in nulls_by_column.items()
    }


def _add_warnings(result: AnalysisResult):
    """
    Agrega advertencias según problemas detectados.
    """

    if result.total_rows == 0:
        result.warnings.append("El archivo no contiene filas de datos.")

    if result.total_columns == 0:
        result.warnings.append("El archivo no contiene columnas.")

    if result.empty_rows > 0:
        result.warnings.append(f"Se detectaron {result.empty_rows} filas completamente vacías.")

    if result.empty_columns > 0:
        result.warnings.append(f"Se detectaron {result.empty_columns} columnas completamente vacías.")

    if result.duplicated_rows > 0:
        result.warnings.append(f"Se detectaron {result.duplicated_rows} filas duplicadas.")

    if result.empty_cells > 0:
        result.warnings.append(f"Se detectaron {result.empty_cells} celdas vacías o sin valor.")

    high_empty_columns = [
        column
        for column, percentage in result.empty_percentage_by_column.items()
        if percentage >= 50
    ]

    if high_empty_columns:
        result.warnings.append(
            "Hay columnas con más del 50% de valores vacíos: "
            + ", ".join(high_empty_columns[:5])
        )

    duplicated_column_names = _find_duplicated_column_names(result.column_types.keys())

    if duplicated_column_names:
        result.warnings.append(
            "Hay nombres de columnas repetidos o muy similares: "
            + ", ".join(duplicated_column_names[:5])
        )


def _add_recommendations(result: AnalysisResult):
    """
    Agrega recomendaciones de limpieza.
    """

    if result.empty_rows > 0:
        result.recommendations.append("Eliminar filas completamente vacías.")

    if result.empty_columns > 0:
        result.recommendations.append("Eliminar columnas completamente vacías.")

    if result.duplicated_rows > 0:
        result.recommendations.append("Revisar y eliminar registros duplicados.")

    if result.empty_cells > 0:
        result.recommendations.append("Revisar columnas con valores faltantes antes de importar a un sistema.")

    if not result.recommendations:
        result.recommendations.append("El archivo no presenta problemas críticos básicos.")

    result.recommendations.append("Normalizar nombres de columnas antes de exportar.")
    result.recommendations.append("Aplicar limpieza automática en la siguiente etapa del flujo.")


def _calculate_quality_score(result: AnalysisResult):
    """
    Calcula un score simple de calidad de datos.
    """

    score = 100

    if result.total_cells > 0:
        empty_ratio = result.empty_cells / result.total_cells
        score -= int(empty_ratio * 35)

    if result.total_rows > 0:
        duplicate_ratio = result.duplicated_rows / result.total_rows
        score -= int(duplicate_ratio * 30)

    score -= min(result.empty_rows * 2, 15)
    score -= min(result.empty_columns * 5, 20)

    score = max(0, min(100, score))

    result.quality_score = score

    if score >= 85:
        result.risk_level = "Bajo"
    elif score >= 65:
        result.risk_level = "Medio"
    else:
        result.risk_level = "Alto"


def _find_duplicated_column_names(columns):
    """
    Detecta nombres de columnas duplicados normalizando texto básico.
    """

    seen = set()
    duplicated = []

    for column in columns:
        normalized = str(column).strip().lower()

        if normalized in seen:
            duplicated.append(str(column))
        else:
            seen.add(normalized)

    return duplicated