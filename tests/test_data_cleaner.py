"""
Tests para el motor de limpieza automática.
"""

import pandas as pd

from app.core.data_cleaner import clean_dataframe


def test_clean_dataframe_removes_duplicates_and_trims_text():
    dataframe = pd.DataFrame({
        " Nombre Cliente ": [" Juan Perez ", " Juan Perez ", " Ana Gomez "],
        " Email ": [" juan@test.com ", " juan@test.com ", " ana@test.com "],
    })

    cleaned, result = clean_dataframe(dataframe)

    assert result.success is True
    assert result.removed_duplicates == 1
    assert cleaned.shape[0] == 2
    assert "nombre_cliente" in cleaned.columns
    assert "email" in cleaned.columns
    assert cleaned.loc[0, "nombre_cliente"] == "Juan Perez"


def test_clean_dataframe_removes_empty_rows_and_columns():
    dataframe = pd.DataFrame({
        "nombre": ["Juan", "", None],
        "vacia": ["", "", ""],
    })

    cleaned, result = clean_dataframe(dataframe)

    assert result.success is True
    assert result.removed_empty_columns >= 1
    assert "vacia" not in cleaned.columns


def test_clean_dataframe_normalizes_dates():
    dataframe = pd.DataFrame({
        "fecha": ["15/05/2026", "2026-05-16"],
        "cliente": ["A", "B"],
    })

    cleaned, result = clean_dataframe(dataframe)

    assert result.success is True
    assert result.normalized_dates >= 1