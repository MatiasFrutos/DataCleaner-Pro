"""
Motor de validación de calidad de datos para DataCleaner Pro.

Agrega validaciones adicionales sobre el DataFrame:
- emails posiblemente inválidos
- columnas con demasiados vacíos
- columnas duplicadas por nombre
- fechas inconsistentes
- columnas con un único valor dominante
"""

import re

import pandas as pd

from app.utils.date_utils import looks_like_date_column, try_parse_date


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_dataframe_quality(dataframe: pd.DataFrame):
    """
    Ejecuta validaciones de calidad adicionales.
    Devuelve un diccionario con warnings y recomendaciones.
    """

    result = {
        "warnings": [],
        "recommendations": [],
        "risk_points": 0,
    }

    if dataframe is None:
        result["warnings"].append("No hay DataFrame para validar.")
        result["risk_points"] += 40
        return result

    if dataframe.empty:
        result["warnings"].append("El archivo está vacío.")
        result["risk_points"] += 40
        return result

    _validate_duplicate_column_names(dataframe, result)
    _validate_high_empty_columns(dataframe, result)
    _validate_email_columns(dataframe, result)
    _validate_date_columns(dataframe, result)
    _validate_dominant_values(dataframe, result)

    if not result["recommendations"]:
        result["recommendations"].append("No se detectaron riesgos avanzados críticos.")

    return result


def _validate_duplicate_column_names(dataframe: pd.DataFrame, result: dict):
    normalized_names = {}

    for column in dataframe.columns:
        key = str(column).strip().lower()
        normalized_names[key] = normalized_names.get(key, 0) + 1

    duplicated = [
        name
        for name, count in normalized_names.items()
        if count > 1
    ]

    if duplicated:
        result["warnings"].append(
            "Se detectaron columnas con nombres duplicados o equivalentes."
        )
        result["recommendations"].append(
            "Normalizar nombres de columnas para evitar conflictos al exportar o importar a base de datos."
        )
        result["risk_points"] += 10


def _validate_high_empty_columns(dataframe: pd.DataFrame, result: dict):
    normalized = dataframe.replace(r"^\s*$", pd.NA, regex=True)
    total_rows = normalized.shape[0]

    if total_rows <= 0:
        return

    risky_columns = []

    for column in normalized.columns:
        empty_count = int(normalized[column].isna().sum())
        percentage = (empty_count / total_rows) * 100

        if percentage >= 70:
            risky_columns.append(str(column))

    if risky_columns:
        result["warnings"].append(
            "Columnas con más del 70% de valores vacíos: "
            + ", ".join(risky_columns[:6])
        )
        result["recommendations"].append(
            "Evaluar si esas columnas deben eliminarse o completarse antes de exportar."
        )
        result["risk_points"] += min(len(risky_columns) * 5, 20)


def _validate_email_columns(dataframe: pd.DataFrame, result: dict):
    email_columns = [
        column
        for column in dataframe.columns
        if "email" in str(column).strip().lower() or "mail" in str(column).strip().lower()
    ]

    for column in email_columns:
        series = dataframe[column].dropna().astype(str).str.strip()
        series = series[series != ""]

        if series.empty:
            continue

        invalid_count = int(
            series.map(lambda value: not bool(EMAIL_PATTERN.match(value))).sum()
        )

        if invalid_count > 0:
            result["warnings"].append(
                f"La columna '{column}' tiene {invalid_count} emails posiblemente inválidos."
            )
            result["recommendations"].append(
                f"Revisar formato de emails en la columna '{column}'."
            )
            result["risk_points"] += min(invalid_count, 15)


def _validate_date_columns(dataframe: pd.DataFrame, result: dict):
    for column in dataframe.columns:
        if not looks_like_date_column(column):
            continue

        series = dataframe[column].dropna().astype(str).str.strip()
        series = series[series != ""]

        if series.empty:
            continue

        sample = series.head(100)
        parseable = sample.map(lambda value: try_parse_date(value) is not None)
        invalid_count = int((~parseable).sum())

        if invalid_count > 0:
            result["warnings"].append(
                f"La columna '{column}' tiene fechas posiblemente inconsistentes."
            )
            result["recommendations"].append(
                f"Normalizar fechas en la columna '{column}' antes de importar a sistemas."
            )
            result["risk_points"] += min(invalid_count, 15)


def _validate_dominant_values(dataframe: pd.DataFrame, result: dict):
    total_rows = dataframe.shape[0]

    if total_rows <= 0:
        return

    dominant_columns = []

    for column in dataframe.columns:
        series = dataframe[column].dropna().astype(str).str.strip()
        series = series[series != ""]

        if series.empty:
            continue

        top_frequency = int(series.value_counts().iloc[0])
        dominance = (top_frequency / total_rows) * 100

        if dominance >= 95 and total_rows >= 20:
            dominant_columns.append(str(column))

    if dominant_columns:
        result["warnings"].append(
            "Columnas con un valor dominante superior al 95%: "
            + ", ".join(dominant_columns[:6])
        )
        result["recommendations"].append(
            "Revisar si esas columnas aportan valor o pueden simplificarse."
        )
        result["risk_points"] += min(len(dominant_columns) * 3, 12)