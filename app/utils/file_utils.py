"""
Utilidades para manejo de archivos en DataCleaner Pro.
"""

from pathlib import Path

from app.config import SUPPORTED_EXTENSIONS


def get_file_extension(file_path: str) -> str:
    """
    Devuelve la extensión de un archivo en minúscula.
    """

    return Path(file_path).suffix.lower()


def get_file_name(file_path: str) -> str:
    """
    Devuelve el nombre del archivo con extensión.
    """

    return Path(file_path).name


def get_file_stem(file_path: str) -> str:
    """
    Devuelve el nombre del archivo sin extensión.
    """

    return Path(file_path).stem


def file_exists(file_path: str) -> bool:
    """
    Valida si una ruta existe y es archivo.
    """

    path = Path(file_path)
    return path.exists() and path.is_file()


def is_supported_file(file_path: str) -> bool:
    """
    Valida si la extensión del archivo es soportada.
    """

    extension = get_file_extension(file_path)
    return extension in SUPPORTED_EXTENSIONS


def format_file_size(size_bytes: int) -> str:
    """
    Convierte bytes a un formato legible.
    """

    if size_bytes <= 0:
        return "0 B"

    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size = size / 1024
        unit_index += 1

    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"

    return f"{size:.2f} {units[unit_index]}"


def get_file_size_label(file_path: str) -> str:
    """
    Devuelve el tamaño del archivo en formato legible.
    """

    path = Path(file_path)

    if not path.exists():
        return "0 B"

    return format_file_size(path.stat().st_size)


def validate_file_path(file_path: str):
    """
    Valida una ruta de archivo para DataCleaner Pro.
    Devuelve una tupla: (es_valido, mensaje).
    """

    if not file_path:
        return False, "No se seleccionó ningún archivo."

    if not file_exists(file_path):
        return False, "El archivo seleccionado no existe."

    if not is_supported_file(file_path):
        supported = ", ".join(SUPPORTED_EXTENSIONS)
        return False, f"Formato no soportado. Formatos permitidos: {supported}"

    return True, "Archivo válido."


def create_safe_output_name(original_file_path: str, suffix: str = "clean") -> str:
    """
    Crea un nombre seguro para exportar un archivo limpio.
    """

    path = Path(original_file_path)
    stem = path.stem
    extension = path.suffix.lower() or ".xlsx"

    return f"{stem}_{suffix}{extension}"