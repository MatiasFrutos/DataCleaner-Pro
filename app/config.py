"""
Configuración global de DataCleaner Pro.

Este archivo concentra valores reutilizables de la aplicación:
nombre, versión, rutas, tamaños, extensiones permitidas y configuración base.
"""

from pathlib import Path


# ============================================================
# Información general de la aplicación
# ============================================================

APP_NAME = "DataCleaner Pro"
APP_VERSION = "0.1.0"
APP_AUTHOR = "Matias Isaac Frutos Gonzalez"
APP_DESCRIPTION = "Aplicación de escritorio para analizar, limpiar y exportar archivos Excel, CSV y TXT."


# ============================================================
# Rutas principales del proyecto
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

APP_DIR = BASE_DIR / "app"
ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
DOCS_DIR = BASE_DIR / "docs"
TESTS_DIR = BASE_DIR / "tests"

INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
SAMPLES_DIR = DATA_DIR / "samples"
REPORTS_DIR = DATA_DIR / "reports"

THEMES_DIR = ASSETS_DIR / "themes"
ICONS_DIR = ASSETS_DIR / "icons"
IMAGES_DIR = ASSETS_DIR / "images"


# ============================================================
# Configuración de ventana
# ============================================================

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 760
WINDOW_MIN_WIDTH = 980
WINDOW_MIN_HEIGHT = 640

WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"


# ============================================================
# Archivos soportados
# ============================================================

SUPPORTED_EXTENSIONS = [".xlsx", ".xls", ".csv", ".txt"]

EXCEL_EXTENSIONS = [".xlsx", ".xls"]
CSV_EXTENSIONS = [".csv"]
TEXT_EXTENSIONS = [".txt"]


# ============================================================
# Configuración de datos
# ============================================================

DEFAULT_PREVIEW_ROWS = 50
MAX_PREVIEW_ROWS = 500

DEFAULT_EXPORT_FORMAT = "xlsx"

CSV_DEFAULT_ENCODING = "utf-8"
CSV_FALLBACK_ENCODINGS = ["utf-8", "latin-1", "cp1252"]

CSV_SEPARATORS = [",", ";", "\t", "|"]


# ============================================================
# Configuración visual base
# ============================================================

DEFAULT_THEME = "light"

LIGHT_THEME_FILE = THEMES_DIR / "light.json"
DARK_THEME_FILE = THEMES_DIR / "dark.json"

FONT_FAMILY = "Segoe UI"
FONT_SIZE_BASE = 13
FONT_SIZE_TITLE = 22
FONT_SIZE_SUBTITLE = 16


# ============================================================
# Logs
# ============================================================

LOG_FILE = LOGS_DIR / "app.log"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ============================================================
# Helpers de configuración
# ============================================================

def ensure_project_directories():
    """
    Crea las carpetas necesarias si no existen.
    Sirve para evitar errores cuando la app intenta exportar,
    guardar logs o leer recursos.
    """

    directories = [
        DATA_DIR,
        INPUT_DIR,
        OUTPUT_DIR,
        SAMPLES_DIR,
        REPORTS_DIR,
        LOGS_DIR,
        ASSETS_DIR,
        ICONS_DIR,
        IMAGES_DIR,
        THEMES_DIR,
        DOCS_DIR,
        TESTS_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def get_app_info():
    """
    Devuelve información general de la aplicación.
    """

    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "author": APP_AUTHOR,
        "description": APP_DESCRIPTION,
        "base_dir": str(BASE_DIR),
    }