"""
Utilidades de fechas para DataCleaner Pro.

Incluye funciones para detectar columnas con fechas y normalizar valores
cuando sea seguro hacerlo.
"""

from dateutil import parser


DATE_KEYWORDS = [
    "fecha",
    "date",
    "created",
    "updated",
    "vencimiento",
    "emision",
    "alta",
    "baja",
]


def looks_like_date_column(column_name: str) -> bool:
    """
    Detecta si una columna parece ser de fecha por su nombre.
    """

    text = str(column_name).strip().lower()

    return any(keyword in text for keyword in DATE_KEYWORDS)


def try_parse_date(value):
    """
    Intenta convertir un valor a fecha.
    Si no puede, devuelve None.
    """

    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    try:
        parsed = parser.parse(text, dayfirst=True, fuzzy=False)
        return parsed.date()
    except Exception:
        return None


def normalize_date_value(value, output_format: str = "%Y-%m-%d"):
    """
    Normaliza una fecha a formato ISO simple.
    Si no puede convertirla, devuelve el valor original.
    """

    parsed = try_parse_date(value)

    if parsed is None:
        return value

    return parsed.strftime(output_format)


def count_parseable_dates(values) -> int:
    """
    Cuenta cuántos valores de una colección pueden interpretarse como fecha.
    """

    count = 0

    for value in values:
        if try_parse_date(value) is not None:
            count += 1

    return count