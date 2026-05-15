"""
Estilos visuales de DataCleaner Pro.

Centraliza colores, fuentes, tamaños, espaciados y estilos generales
para mantener una interfaz consistente y fácil de escalar.
"""

import customtkinter as ctk


# ============================================================
# Modo visual base
# ============================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ============================================================
# Colores principales
# ============================================================

COLORS = {
    "app_bg": "#f6f8fb",
    "surface": "#ffffff",
    "surface_soft": "#f8fafc",
    "surface_muted": "#eef2f7",
    "border": "#dbe3ef",
    "border_soft": "#edf2f7",

    "text": "#101827",
    "text_soft": "#334155",
    "text_muted": "#64748b",
    "text_faint": "#94a3b8",

    "primary": "#2563eb",
    "primary_hover": "#1d4ed8",
    "primary_soft": "#dbeafe",

    "success": "#16a34a",
    "success_soft": "#dcfce7",

    "warning": "#d97706",
    "warning_soft": "#fef3c7",

    "danger": "#dc2626",
    "danger_soft": "#fee2e2",

    "sidebar_bg": "#ffffff",
    "sidebar_active": "#eff6ff",
    "sidebar_hover": "#f1f5f9",

    "topbar_bg": "#ffffff",
}


# ============================================================
# Fuentes
# ============================================================

FONT_FAMILY = "Segoe UI"

FONTS = {
    "display": (FONT_FAMILY, 28, "bold"),
    "title": (FONT_FAMILY, 22, "bold"),
    "subtitle": (FONT_FAMILY, 16, "bold"),
    "body": (FONT_FAMILY, 13),
    "body_bold": (FONT_FAMILY, 13, "bold"),
    "small": (FONT_FAMILY, 11),
    "small_bold": (FONT_FAMILY, 11, "bold"),
    "button": (FONT_FAMILY, 13, "bold"),
}


# ============================================================
# Medidas
# ============================================================

SIZES = {
    "sidebar_width": 260,
    "topbar_height": 72,
    "radius_sm": 8,
    "radius_md": 12,
    "radius_lg": 18,
    "radius_xl": 24,
    "padding_sm": 8,
    "padding_md": 14,
    "padding_lg": 20,
    "padding_xl": 28,
}


# ============================================================
# Helpers visuales
# ============================================================

def apply_base_grid(widget, rows=1, columns=1):
    """
    Configura filas y columnas con peso para layouts responsivos.
    """

    for row in range(rows):
        widget.grid_rowconfigure(row, weight=1)

    for column in range(columns):
        widget.grid_columnconfigure(column, weight=1)


def get_color(name, fallback="#000000"):
    """
    Devuelve un color por nombre desde el diccionario global.
    """

    return COLORS.get(name, fallback)


def get_font(name):
    """
    Devuelve una fuente por nombre desde el diccionario global.
    """

    return FONTS.get(name, FONTS["body"])