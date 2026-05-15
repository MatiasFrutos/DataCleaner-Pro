"""
Tests para el motor de análisis de datos.
"""

import pandas as pd

from app.core.data_analyzer import analyze_dataframe


def test_analyze_dataframe_basic_metrics():
    dataframe = pd.DataFrame({
        "nombre": ["Juan", "Ana", "Ana"],
        "email": ["juan@test.com", "", ""],
    })

    result = analyze_dataframe(dataframe)

    assert result.total_rows == 3
    assert result.total_columns == 2
    assert result.total_cells == 6
    assert result.empty_cells >= 2
    assert result.duplicated_rows == 0
    assert result.quality_score <= 100


def test_analyze_dataframe_duplicates():
    dataframe = pd.DataFrame({
        "nombre": ["Juan", "Juan"],
        "email": ["juan@test.com", "juan@test.com"],
    })

    result = analyze_dataframe(dataframe)

    assert result.duplicated_rows == 1
    assert result.has_issues() is True


def test_analyze_none_dataframe():
    result = analyze_dataframe(None)

    assert result.quality_score == 0
    assert result.risk_level == "Alto"
    assert result.has_issues() is True