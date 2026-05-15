"""
Utilidades para trabajar con Pandas DataFrames en DataCleaner Pro.
"""

from typing import List, Dict, Any

import pandas as pd


def dataframe_shape(dataframe: pd.DataFrame) -> Dict[str, int]:
    """
    Devuelve cantidad de filas y columnas.
    """

    if dataframe is None:
        return {
            "rows": 0,
            "columns": 0,
        }

    rows, columns = dataframe.shape

    return {
        "rows": int(rows),
        "columns": int(columns),
    }


def get_preview_records(dataframe: pd.DataFrame, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Devuelve registros de vista previa limitados.
    """

    if dataframe is None or dataframe.empty:
        return []

    preview = dataframe.head(limit).copy()
    preview = preview.fillna("")

    return preview.to_dict(orient="records")


def get_preview_columns(dataframe: pd.DataFrame) -> List[str]:
    """
    Devuelve columnas del DataFrame.
    """

    if dataframe is None:
        return []

    return [str(column) for column in dataframe.columns]


def safe_cell_value(value, max_length: int = 80) -> str:
    """
    Convierte un valor de celda en texto seguro para UI.
    """

    if pd.isna(value):
        return ""

    text = str(value)

    if len(text) > max_length:
        return text[:max_length - 3] + "..."

    return text


def get_column_types(dataframe: pd.DataFrame) -> Dict[str, str]:
    """
    Devuelve tipos de datos por columna.
    """

    if dataframe is None:
        return {}

    return {
        str(column): str(dtype)
        for column, dtype in dataframe.dtypes.items()
    }


def count_empty_cells(dataframe: pd.DataFrame) -> int:
    """
    Cuenta celdas vacías o nulas.
    """

    if dataframe is None:
        return 0

    null_count = dataframe.isna().sum().sum()

    empty_string_count = 0

    for column in dataframe.columns:
        if dataframe[column].dtype == "object":
            empty_string_count += dataframe[column].astype(str).str.strip().eq("").sum()

    return int(null_count + empty_string_count)


def count_empty_rows(dataframe: pd.DataFrame) -> int:
    """
    Cuenta filas completamente vacías.
    """

    if dataframe is None:
        return 0

    normalized = dataframe.replace(r"^\s*$", pd.NA, regex=True)

    return int(normalized.isna().all(axis=1).sum())


def count_empty_columns(dataframe: pd.DataFrame) -> int:
    """
    Cuenta columnas completamente vacías.
    """

    if dataframe is None:
        return 0

    normalized = dataframe.replace(r"^\s*$", pd.NA, regex=True)

    return int(normalized.isna().all(axis=0).sum())


def get_memory_usage_label(dataframe: pd.DataFrame) -> str:
    """
    Devuelve uso de memoria del DataFrame en formato legible.
    """

    if dataframe is None:
        return "0 B"

    size_bytes = int(dataframe.memory_usage(deep=True).sum())

    units = ["B", "KB", "MB", "GB"]
    size = float(size_bytes)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size = size / 1024
        unit_index += 1

    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"

    return f"{size:.2f} {units[unit_index]}"