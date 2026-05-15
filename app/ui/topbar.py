"""
Topbar principal de DataCleaner Pro.

Muestra el título de la sección activa, estado del archivo y acciones rápidas.
"""

import customtkinter as ctk

from app.config import APP_VERSION
from app.ui.styles import COLORS, FONTS, SIZES
from app.ui.components import Badge, AppButton


class Topbar(ctk.CTkFrame):
    """
    Barra superior de la aplicación.
    """

    def __init__(self, master, on_primary_action=None, **kwargs):
        super().__init__(
            master,
            height=SIZES["topbar_height"],
            fg_color=COLORS["topbar_bg"],
            corner_radius=0,
            border_width=0,
            **kwargs
        )

        self.on_primary_action = on_primary_action
        self.section_title = "Dashboard"
        self.file_status = "Sin archivo cargado"

        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        self._build_layout()

    def _build_layout(self):
        content = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        content.grid(row=0, column=0, sticky="nsew", padx=24, pady=12)
        content.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            content,
            text=self.section_title,
            font=FONTS["title"],
            text_color=COLORS["text"],
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, sticky="ew")

        self.subtitle_label = ctk.CTkLabel(
            content,
            text="Prepará tus archivos para análisis, limpieza y exportación.",
            font=FONTS["body"],
            text_color=COLORS["text_muted"],
            anchor="w",
        )
        self.subtitle_label.grid(row=1, column=0, sticky="ew", pady=(2, 0))

        actions = ctk.CTkFrame(
            content,
            fg_color="transparent",
            corner_radius=0,
        )
        actions.grid(row=0, column=1, rowspan=2, sticky="e")

        self.file_badge = Badge(
            actions,
            text=self.file_status,
            variant="muted",
        )
        self.file_badge.grid(row=0, column=0, padx=(0, 10))

        self.version_badge = Badge(
            actions,
            text=f"v{APP_VERSION}",
            variant="primary",
        )
        self.version_badge.grid(row=0, column=1, padx=(0, 10))

        self.primary_button = AppButton(
            actions,
            text="Cargar archivo",
            command=self._handle_primary_action,
        )
        self.primary_button.grid(row=0, column=2)

        divider = ctk.CTkFrame(
            self,
            height=1,
            fg_color=COLORS["border_soft"],
            corner_radius=0,
        )
        divider.grid(row=1, column=0, sticky="ew")

    def _handle_primary_action(self):
        if self.on_primary_action:
            self.on_primary_action()

    def set_section(self, title, subtitle=None):
        self.section_title = title
        self.title_label.configure(text=title)

        if subtitle:
            self.subtitle_label.configure(text=subtitle)

    def set_file_status(self, text, variant="muted"):
        self.file_status = text

        palette = {
            "primary": (COLORS["primary_soft"], COLORS["primary"]),
            "success": (COLORS["success_soft"], COLORS["success"]),
            "warning": (COLORS["warning_soft"], COLORS["warning"]),
            "danger": (COLORS["danger_soft"], COLORS["danger"]),
            "muted": (COLORS["surface_muted"], COLORS["text_muted"]),
        }

        bg, fg = palette.get(variant, palette["muted"])

        self.file_badge.configure(
            text=text,
            fg_color=bg,
            text_color=fg,
        )