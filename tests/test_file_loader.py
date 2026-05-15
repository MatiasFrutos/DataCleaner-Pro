"""
Tests para el cargador de archivos.
"""

from pathlib import Path

import pandas as pd

from app.core.file_loader import load_file


def test_load_csv_file(tmp_path):
    file_path = tmp_path / "sample.csv"
    file_path.write_text("nombre,email\nJuan,juan@test.com\nAna,ana@test.com", encoding="utf-8")

    dataframe, metadata = load_file(str(file_path))

    assert isinstance(dataframe, pd.DataFrame)
    assert dataframe.shape[0] == 2
    assert dataframe.shape[1] == 2
    assert metadata["rows"] == 2
    assert metadata["columns"] == 2


def test_load_txt_file_with_semicolon(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("nombre;email\nJuan;juan@test.com\nAna;ana@test.com", encoding="utf-8")

    dataframe, metadata = load_file(str(file_path))

    assert isinstance(dataframe, pd.DataFrame)
    assert dataframe.shape[0] == 2
    assert dataframe.shape[1] == 2
    assert metadata["separator"] == "punto y coma (;)"


def test_load_xlsx_file(tmp_path):
    file_path = tmp_path / "sample.xlsx"

    original = pd.DataFrame({
        "nombre": ["Juan", "Ana"],
        "email": ["juan@test.com", "ana@test.com"],
    })

    original.to_excel(file_path, index=False)

    dataframe, metadata = load_file(str(file_path))

    assert isinstance(dataframe, pd.DataFrame)
    assert dataframe.shape[0] == 2
    assert dataframe.shape[1] == 2
    assert metadata["source_type"] == "excel"