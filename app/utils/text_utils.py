"""
Utilidades de texto para DataCleaner Pro.

Funciones para normalizar nombres de columnas, limpiar strings
y preparar valores de texto antes de exportar.
"""

import re
import unicodedata


def clean_text_value(value):
    """
    Limpia un valor textual:
    - quita espacios al inicio y final
    - compacta espacios múltiples
    - conserva valores no string sin modificarlos
    """

    if not isinstance(value, str):
        return value

    text = value.strip()
    text = re.sub(r"\s+", " ", text)

    return text


def normalize_column_name(column_name: str, fallback: str = "column") -> str:
    """
    Normaliza nombres de columnas para que sean más seguros:
    - minúsculas
    - sin acentos
    - espacios convertidos en _
    - caracteres raros removidos
    """

    text = str(column_name).strip()

    if not text:
        text = fallback

    text = remove_accents(text)
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s-]+", "_", text)
    text = re.sub(r"_+", "_", text)
    text = text.strip("_")

    if not text:
        text = fallback

    return text


def remove_accents(text: str) -> str:
    """
    Remueve acentos de un texto.
    """

    normalized = unicodedata.normalize("NFKD", str(text))

    return "".join(
        character
        for character in normalized
        if not unicodedata.combining(character)
    )


def make_unique_names(names):
    """
    Recibe una lista de nombres y garantiza que no estén duplicados.

    Ejemplo:
    cliente, cliente, cliente -> cliente, cliente_2, cliente_3
    """

    seen = {}
    result = []

    for name in names:
        base_name = str(name).strip() or "column"

        if base_name not in seen:
            seen[base_name] = 1
            result.append(base_name)
            continue

        seen[base_name] += 1
        result.append(f"{base_name}_{seen[base_name]}")

    return result


def is_empty_text(value) -> bool:
    """
    Indica si un valor textual está vacío.
    """

    if value is None:
        return True

    if not isinstance(value, str):
        return False

    return value.strip() == ""


def normalize_missing_text(value):
    """
    Normaliza textos que representan valores faltantes.
    """

    if not isinstance(value, str):
        return value

    text = value.strip()
    lowered = text.lower()

    missing_values = {
        "",
        "nan",
        "none",
        "null",
        "n/a",
        "na",
        "sin dato",
        "sin datos",
        "-",
        "--",
    }

    if lowered in missing_values:
        return ""

    return text