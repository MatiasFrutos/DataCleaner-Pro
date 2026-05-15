"""
Motor de limpieza automática para DataCleaner Pro.

Aplica reglas básicas y seguras:
- eliminar filas completamente vacías
- eliminar columnas completamente vacías
- eliminar duplicados
- limpiar espacios en textos
- normalizar nombres de columnas
- normalizar textos que representan valores vacíos
- normalizar fechas en columnas detectadas como fecha
"""

import pandas as pd

from app.models.cleaning_result import CleaningResult
from app.utils.text_utils import (
    clean_text_value,
    normalize_column_name,
    make_unique_names,
    normalize_missing_text,
)
from app.utils.date_utils import looks_like_date_column, normalize_date_value


class DataCleanerError(Exception):
    """
    Error personalizado para fallos durante limpieza.
    """


def clean_dataframe(
    dataframe: pd.DataFrame,
    remove_empty_rows: bool = True,
    remove_empty_columns: bool = True,
    remove_duplicates: bool = True,
    trim_text: bool = True,
    normalize_columns: bool = True,
    normalize_missing_values: bool = True,
    normalize_dates: bool = True,
):
    """
    Limpia un DataFrame y devuelve:
    - DataFrame limpio
    - CleaningResult
    """

    if dataframe is None:
        result = CleaningResult(success=False, error="No hay DataFrame para limpiar.")
        raise DataCleanerError(result.error)

    cleaned = dataframe.copy()

    original_rows, original_columns = cleaned.shape

    result = CleaningResult(
        original_rows=int(original_rows),
        original_columns=int(original_columns),
    )

    try:
        if normalize_missing_values:
            cleaned = _normalize_missing_values(cleaned)
            result.actions.append("Valores faltantes textuales normalizados.")

        if trim_text:
            cleaned, cleaned_text_cells = _trim_text_cells(cleaned)
            result.cleaned_text_cells = cleaned_text_cells
            result.actions.append(f"Textos limpiados: {cleaned_text_cells} celdas.")

        if remove_empty_rows:
            before_rows = cleaned.shape[0]
            cleaned = cleaned.replace(r"^\s*$", pd.NA, regex=True)
            cleaned = cleaned.dropna(how="all")
            after_rows = cleaned.shape[0]

            result.removed_empty_rows = int(before_rows - after_rows)
            result.actions.append(f"Filas vacías eliminadas: {result.removed_empty_rows}.")

        if remove_empty_columns:
            before_columns = cleaned.shape[1]
            cleaned = cleaned.replace(r"^\s*$", pd.NA, regex=True)
            cleaned = cleaned.dropna(axis=1, how="all")
            after_columns = cleaned.shape[1]

            result.removed_empty_columns = int(before_columns - after_columns)
            result.actions.append(f"Columnas vacías eliminadas: {result.removed_empty_columns}.")

        if remove_duplicates:
            before_rows = cleaned.shape[0]
            cleaned = cleaned.drop_duplicates()
            after_rows = cleaned.shape[0]

            result.removed_duplicates = int(before_rows - after_rows)
            result.actions.append(f"Duplicados eliminados: {result.removed_duplicates}.")

        if normalize_columns:
            cleaned, renamed_columns = _normalize_columns(cleaned)
            result.renamed_columns = renamed_columns
            result.normalized_columns = len(renamed_columns)
            result.actions.append(f"Columnas normalizadas: {result.normalized_columns}.")

        if normalize_dates:
            cleaned, normalized_dates_count = _normalize_date_columns(cleaned)
            result.normalized_dates = normalized_dates_count
            result.actions.append(f"Fechas normalizadas: {normalized_dates_count} valores.")

        cleaned = cleaned.reset_index(drop=True)

        cleaned_rows, cleaned_columns = cleaned.shape

        result.cleaned_rows = int(cleaned_rows)
        result.cleaned_columns = int(cleaned_columns)

        if cleaned.empty:
            result.warnings.append("El resultado quedó vacío después de aplicar la limpieza.")

        if result.cleaned_columns == 0:
            result.warnings.append("No quedaron columnas disponibles después de la limpieza.")

        return cleaned, result

    except Exception as error:
        result.success = False
        result.error = str(error)
        raise DataCleanerError(f"No se pudo limpiar el DataFrame: {error}") from error


def _normalize_missing_values(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza valores textuales equivalentes a vacío.
    """

    cleaned = dataframe.copy()

    for column in cleaned.columns:
        if cleaned[column].dtype == "object":
            cleaned[column] = cleaned[column].map(normalize_missing_text)

    return cleaned


def _trim_text_cells(dataframe: pd.DataFrame):
    """
    Limpia espacios de celdas textuales.
    """

    cleaned = dataframe.copy()
    cleaned_count = 0

    for column in cleaned.columns:
        if cleaned[column].dtype != "object":
            continue

        original_values = cleaned[column].copy()
        cleaned[column] = cleaned[column].map(clean_text_value)

        changed = original_values.astype(str) != cleaned[column].astype(str)
        cleaned_count += int(changed.sum())

    return cleaned, cleaned_count


def _normalize_columns(dataframe: pd.DataFrame):
    """
    Normaliza nombres de columnas.
    """

    cleaned = dataframe.copy()

    original_columns = [str(column) for column in cleaned.columns]

    normalized_columns = [
        normalize_column_name(column, fallback=f"column_{index + 1}")
        for index, column in enumerate(original_columns)
    ]

    normalized_columns = make_unique_names(normalized_columns)

    renamed_columns = {}

    for old_name, new_name in zip(original_columns, normalized_columns):
        if old_name != new_name:
            renamed_columns[old_name] = new_name

    cleaned.columns = normalized_columns

    return cleaned, renamed_columns


def _normalize_date_columns(dataframe: pd.DataFrame):
    """
    Normaliza columnas cuyo nombre parece de fecha.
    """

    cleaned = dataframe.copy()
    normalized_count = 0

    for column in cleaned.columns:
        if not looks_like_date_column(column):
            continue

        if cleaned[column].dtype != "object":
            continue

        original_values = cleaned[column].copy()
        cleaned[column] = cleaned[column].map(normalize_date_value)

        changed = original_values.astype(str) != cleaned[column].astype(str)
        normalized_count += int(changed.sum())

    return cleaned, normalized_count