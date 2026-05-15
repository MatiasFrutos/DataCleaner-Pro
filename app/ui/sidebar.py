"""
Sidebar principal de DataCleaner Pro.

Contiene la navegación lateral de la aplicación.
"""

import customtkinter as ctk

from app.ui.styles import COLORS, FONTS, SIZES
from app.ui.components import Badge


class Sidebar(ctk.CTkFrame):
    """
    Menú lateral de navegación.
    """

    def __init__(self, master, on_navigate=None, **kwargs):
        super().__init__(
            master,
            width=SIZES["sidebar_width"],
            fg_color=COLORS["sidebar_bg"],
            corner_radius=0,
            border_width=0,
            **kwargs
        )

        self.on_navigate = on_navigate
        self.active_view = "dashboard"
        self.nav_buttons = {}

        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_brand()
        self._build_navigation()
        self._build_footer()

    def _build_brand(self):
        brand_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        brand_frame.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 14))
        brand_frame.grid_columnconfigure(1, weight=1)

        logo = ctk.CTkFrame(
            brand_frame,
            width=42,
            height=42,
            fg_color=COLORS["primary"],
            corner_radius=14,
        )
        logo.grid(row=0, column=0, rowspan=2, sticky="w")
        logo.grid_propagate(False)

        logo_label = ctk.CTkLabel(
            logo,
            text="D",
            font=("Segoe UI", 20, "bold"),
            text_color="#ffffff",
        )
        logo_label.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(
            brand_frame,
            text="DataCleaner",
            font=FONTS["subtitle"],
            text_color=COLORS["text"],
            anchor="w",
        )
        title.grid(row=0, column=1, sticky="ew", padx=(12, 0))

        subtitle = ctk.CTkLabel(
            brand_frame,
            text="Pro",
            font=FONTS["small_bold"],
            text_color=COLORS["text_muted"],
            anchor="w",
        )
        subtitle.grid(row=1, column=1, sticky="ew", padx=(12, 0))

        divider = ctk.CTkFrame(
            self,
            height=1,
            fg_color=COLORS["border_soft"],
            corner_radius=0,
        )
        divider.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 12))

    def _build_navigation(self):
        nav_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        nav_frame.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        nav_frame.grid_columnconfigure(0, weight=1)

        items = [
            {
                "key": "dashboard",
                "label": "Dashboard",
                "description": "Resumen general",
                "icon": "⌂",
            },
            {
                "key": "file_preview",
                "label": "Cargar archivo",
                "description": "Excel, CSV o TXT",
                "icon": "▣",
            },
            {
                "key": "analysis",
                "label": "Análisis",
                "description": "Calidad del dato",
                "icon": "◎",
            },
            {
                "key": "cleaning",
                "label": "Limpieza",
                "description": "Corrección automática",
                "icon": "✦",
            },
            {
                "key": "export",
                "label": "Exportar",
                "description": "Archivo limpio",
                "icon": "⇩",
            },
        ]

        for index, item in enumerate(items):
            button = self._create_nav_button(nav_frame, item)
            button.grid(row=index, column=0, sticky="ew", pady=4)
            self.nav_buttons[item["key"]] = button

        self._refresh_active_button()

    def _create_nav_button(self, master, item):
        button = ctk.CTkButton(
            master,
            text="",
            height=58,
            corner_radius=14,
            fg_color="transparent",
            hover_color=COLORS["sidebar_hover"],
            command=lambda key=item["key"]: self.navigate(key),
        )

        button.grid_columnconfigure(1, weight=1)

        icon = ctk.CTkLabel(
            button,
            text=item["icon"],
            font=("Segoe UI", 18, "bold"),
            text_color=COLORS["text_muted"],
            width=34,
        )
        icon.grid(row=0, column=0, rowspan=2, sticky="w", padx=(12, 8), pady=8)

        label = ctk.CTkLabel(
            button,
            text=item["label"],
            font=FONTS["body_bold"],
            text_color=COLORS["text"],
            anchor="w",
        )
        label.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=(8, 0))

        description = ctk.CTkLabel(
            button,
            text=item["description"],
            font=FONTS["small"],
            text_color=COLORS["text_muted"],
            anchor="w",
        )
        description.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(0, 8))

        button.icon_label = icon
        button.title_label = label
        button.description_label = description

        return button

    def _build_footer(self):
        footer = ctk.CTkFrame(
            self,
            fg_color=COLORS["surface_soft"],
            corner_radius=18,
            border_width=1,
            border_color=COLORS["border_soft"],
        )
        footer.grid(row=3, column=0, sticky="ew", padx=14, pady=(0, 16))
        footer.grid_columnconfigure(0, weight=1)

        status = Badge(
            footer,
            text="MVP local",
            variant="success",
        )
        status.grid(row=0, column=0, sticky="w", padx=14, pady=(14, 8))

        title = ctk.CTkLabel(
            footer,
            text="Flujo recomendado",
            font=FONTS["small_bold"],
            text_color=COLORS["text"],
            anchor="w",
        )
        title.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 2))

        helper = ctk.CTkLabel(
            footer,
            text="Cargar → Analizar → Limpiar → Exportar",
            font=FONTS["small"],
            text_color=COLORS["text_muted"],
            anchor="w",
            wraplength=200,
            justify="left",
        )
        helper.grid(row=2, column=0, sticky="ew", padx=14, pady=(0, 14))

    def navigate(self, view_key):
        self.active_view = view_key
        self._refresh_active_button()

        if self.on_navigate:
            self.on_navigate(view_key)

    def _refresh_active_button(self):
        for key, button in self.nav_buttons.items():
            is_active = key == self.active_view

            button.configure(
                fg_color=COLORS["sidebar_active"] if is_active else "transparent",
                hover_color=COLORS["sidebar_active"] if is_active else COLORS["sidebar_hover"],
            )

            button.icon_label.configure(
                text_color=COLORS["primary"] if is_active else COLORS["text_muted"]
            )
            button.title_label.configure(
                text_color=COLORS["primary"] if is_active else COLORS["text"]
            )
            button.description_label.configure(
                text_color=COLORS["text_soft"] if is_active else COLORS["text_muted"]
            )