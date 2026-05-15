"""
Cargador de archivos para DataCleaner Pro.

Permite leer archivos Excel, CSV y TXT usando Pandas.
Incluye soporte defensivo para archivos .xls exportados desde sistemas
que en realidad pueden venir como HTML, CSV o texto separado por columnas.
"""

from pathlib import Path
from typing import Dict, Any, Tuple

import pandas as pd

from app.config import (
    EXCEL_EXTENSIONS,
    CSV_EXTENSIONS,
    TEXT_EXTENSIONS,
    CSV_FALLBACK_ENCODINGS,
    CSV_SEPARATORS,
)


class FileLoaderError(Exception):
    """
    Error personalizado para fallos durante la carga de archivos.
    """


def load_file(file_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Carga un archivo soportado y devuelve:
    - DataFrame
    - metadata técnica de carga
    """

    path = Path(file_path)

    if not path.exists():
        raise FileLoaderError("El archivo seleccionado no existe.")

    if not path.is_file():
        raise FileLoaderError("La ruta seleccionada no corresponde a un archivo.")

    extension = path.suffix.lower()

    if extension in EXCEL_EXTENSIONS:
        return _load_excel_with_fallbacks(path)

    if extension in CSV_EXTENSIONS:
        return _load_csv_or_txt(path)

    if extension in TEXT_EXTENSIONS:
        return _load_csv_or_txt(path)

    raise FileLoaderError(f"Formato no soportado: {extension}")


def _load_excel_with_fallbacks(path: Path) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Carga archivos Excel reales y también intenta resolver .xls problemáticos.

    Algunos sistemas exportan archivos con extensión .xls, pero internamente
    el contenido puede ser:
    - HTML con tabla
    - CSV separado por coma, punto y coma, tabulación o pipe
    - texto plano
    """

    extension = path.suffix.lower()
    errors = []

    engine_candidates = []

    if extension == ".xlsx":
        engine_candidates = ["openpyxl", None]

    elif extension == ".xls":
        engine_candidates = ["xlrd", None]

    else:
        engine_candidates = [None]

    for engine in engine_candidates:
        try:
            read_options = {}

            if engine:
                read_options["engine"] = engine

            dataframe = pd.read_excel(path, **read_options)
            dataframe = _prepare_dataframe(dataframe)

            metadata = {
                "source_type": "excel",
                "encoding": None,
                "separator": None,
                "sheet": "primera hoja",
                "engine": engine or "auto",
                "fallback": False,
                "rows": int(dataframe.shape[0]),
                "columns": int(dataframe.shape[1]),
            }

            return dataframe, metadata

        except Exception as error:
            errors.append(f"Excel engine {engine or 'auto'}: {error}")

    try:
        return _load_html_table(path)
    except Exception as error:
        errors.append(f"HTML table fallback: {error}")

    try:
        dataframe, metadata = _load_csv_or_txt(path)
        metadata["source_type"] = "excel_fallback_text"
        metadata["fallback"] = True
        metadata["engine"] = "text_parser"

        return dataframe, metadata

    except Exception as error:
        errors.append(f"Text fallback: {error}")

    readable_errors = "\n".join(f"- {error}" for error in errors)

    raise FileLoaderError(
        "No se pudo leer el archivo Excel. "
        "El archivo puede estar dañado o tener extensión .xls pero contenido no compatible.\n\n"
        f"Detalle técnico:\n{readable_errors}"
    )


def _load_html_table(path: Path) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Intenta leer archivos exportados como HTML aunque tengan extensión .xls.
    """

    last_error = None

    for encoding in CSV_FALLBACK_ENCODINGS:
        try:
            tables = pd.read_html(path, encoding=encoding)

            if not tables:
                raise FileLoaderError("No se encontraron tablas HTML dentro del archivo.")

            dataframe = tables[0]
            dataframe = _prepare_dataframe(dataframe)

            metadata = {
                "source_type": "html_table",
                "encoding": encoding,
                "separator": None,
                "sheet": "tabla HTML 1",
                "engine": "read_html",
                "fallback": True,
                "rows": int(dataframe.shape[0]),
                "columns": int(dataframe.shape[1]),
            }

            return dataframe, metadata

        except Exception as error:
            last_error = error

    raise FileLoaderError(f"No se pudo leer como tabla HTML: {last_error}")


def _load_csv_or_txt(path: Path) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Carga archivos CSV o TXT probando diferentes codificaciones y separadores.
    También sirve como fallback para .xls exportados como texto.
    """

    last_error = None

    for encoding in CSV_FALLBACK_ENCODINGS:
        try:
            sample_text = path.read_text(encoding=encoding, errors="replace")[:12000]
            separator = detect_separator(sample_text)

            dataframe = pd.read_csv(
                path,
                sep=separator,
                encoding=encoding,
                engine="python",
                dtype=str,
                keep_default_na=False,
                on_bad_lines="skip",
            )

            dataframe = _prepare_dataframe(dataframe)

            metadata = {
                "source_type": "text",
                "encoding": encoding,
                "separator": _separator_label(separator),
                "sheet": None,
                "engine": "python",
                "fallback": False,
                "rows": int(dataframe.shape[0]),
                "columns": int(dataframe.shape[1]),
            }

            return dataframe, metadata

        except Exception as error:
            last_error = error

    raise FileLoaderError(f"No se pudo leer el archivo CSV/TXT: {last_error}")


def detect_separator(sample_text: str) -> str:
    """
    Detecta el separador más probable contando ocurrencias por línea.
    """

    if not sample_text:
        return ","

    lines = [
        line
        for line in sample_text.splitlines()
        if line.strip()
    ]

    if not lines:
        return ","

    scores = {}

    for separator in CSV_SEPARATORS:
        counts = [line.count(separator) for line in lines[:30]]
        positive_counts = [count for count in counts if count > 0]

        if not positive_counts:
            scores[separator] = 0
            continue

        consistency_penalty = len(set(positive_counts))
        total_hits = sum(positive_counts)
        repeated_pattern_bonus = len(positive_counts)

        scores[separator] = total_hits + repeated_pattern_bonus - consistency_penalty

    best_separator = max(scores, key=scores.get)

    if scores[best_separator] <= 0:
        return ","

    return best_separator


def _prepare_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica preparación básica al DataFrame cargado sin limpiar datos todavía.
    La limpieza real llega en la etapa 6.
    """

    if dataframe is None:
        raise FileLoaderError("No se pudo crear el DataFrame.")

    dataframe = dataframe.copy()

    if dataframe.empty and len(dataframe.columns) == 0:
        raise FileLoaderError("El archivo no contiene datos legibles.")

    dataframe.columns = [
        _safe_column_name(column, index)
        for index, column in enumerate(dataframe.columns)
    ]

    dataframe = dataframe.dropna(how="all")

    return dataframe


def _safe_column_name(column, index: int) -> str:
    """
    Normaliza de forma mínima el nombre de una columna para evitar columnas vacías.
    """

    text = str(column).strip()

    if not text or text.lower().startswith("unnamed"):
        return f"column_{index + 1}"

    return text


def _separator_label(separator: str) -> str:
    """
    Devuelve una etiqueta legible para el separador detectado.
    """

    labels = {
        ",": "coma (,)",
        ";": "punto y coma (;)",
        "\t": "tabulación",
        "|": "pipe (|)",
    }

    return labels.get(separator, separator)