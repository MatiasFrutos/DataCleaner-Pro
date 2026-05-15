"""
Tests para el exportador de datos.
"""

import pandas as pd

from app.core.data_exporter import export_dataframe


def test_export_dataframe_to_csv(tmp_path):
    dataframe = pd.DataFrame({
        "nombre": ["Juan", "Ana"],
        "email": ["juan@test.com", "ana@test.com"],
    })

    output_path = tmp_path / "output.csv"

    result = export_dataframe(dataframe, str(output_path), "csv")

    assert result.success is True
    assert output_path.exists()
    assert result.rows == 2
    assert result.columns == 2


def test_export_dataframe_to_xlsx(tmp_path):
    dataframe = pd.DataFrame({
        "nombre": ["Juan", "Ana"],
        "email": ["juan@test.com", "ana@test.com"],
    })

    output_path = tmp_path / "output.xlsx"

    result = export_dataframe(dataframe, str(output_path), "xlsx")

    assert result.success is True
    assert output_path.exists()
    assert result.rows == 2
    assert result.columns == 2