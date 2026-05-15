"""
Vista Dashboard de DataCleaner Pro.

Pantalla inicial del sistema con resumen del flujo, estado del archivo
y accesos rápidos a las secciones principales.
"""

import customtkinter as ctk

from app.ui.styles import COLORS, FONTS, SIZES
from app.ui.components import AppCard, StatCard, AppButton


class DashboardView(ctk.CTkFrame):
    """
    Dashboard principal de la aplicación.
    """

    def __init__(self, master, file_service, on_navigate=None, **kwargs):
        super().__init__(
            master,
            fg_color="transparent",
            corner_radius=0,
            **kwargs
        )

        self.file_service = file_service
        self.on_navigate = on_navigate

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build()

    def _build(self):
        wrapper = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        wrapper.grid(row=0, column=0, sticky="nsew")
        wrapper.grid_columnconfigure(0, weight=1)

        self._build_hero(wrapper)
        self._build_stats(wrapper)
        self._build_cards(wrapper)

    def _build_hero(self, master):
        hero = ctk.CTkFrame(
            master,
            fg_color=COLORS["surface"],
            corner_radius=SIZES["radius_xl"],
            border_width=1,
            border_color=COLORS["border_soft"],
        )
        hero.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        hero.grid_columnconfigure(0, weight=1)

        eyebrow = ctk.CTkLabel(
            hero,
            text="DATA QUALITY TOOLKIT",
            font=FONTS["small_bold"],
            text_color=COLORS["primary"],
            anchor="w",
        )
        eyebrow.grid(row=0, column=0, sticky="ew", padx=26, pady=(24, 4))

        title = ctk.CTkLabel(
            hero,
            text="Convertí archivos desordenados en datos listos para usar.",
            font=FONTS["display"],
            text_color=COLORS["text"],
            anchor="w",
            wraplength=780,
            justify="left",
        )
        title.grid(row=1, column=0, sticky="ew", padx=26, pady=(0, 8))

        description = ctk.CTkLabel(
            hero,
            text=(
                "Cargá archivos Excel, CSV o TXT, detectá problemas de calidad, "
                "aplicá limpieza automática y exportá una versión profesional del dataset."
            ),
            font=FONTS["body"],
            text_color=COLORS["text_muted"],
            anchor="w",
            wraplength=780,
            justify="left",
        )
        description.grid(row=2, column=0, sticky="ew", padx=26, pady=(0, 20))

        actions = ctk.CTkFrame(
            hero,
            fg_color="transparent",
        )
        actions.grid(row=3, column=0, sticky="w", padx=26, pady=(0, 26))

        primary = AppButton(
            actions,
            text="Cargar primer archivo",
            command=lambda: self._go_to("file_preview"),
        )
        primary.grid(row=0, column=0, padx=(0, 10))

        secondary = AppButton(
            actions,
            text="Ver análisis",
            variant="secondary",
            command=lambda: self._go_to("analysis"),
        )
        secondary.grid(row=0, column=1)

    def _build_stats(self, master):
        current_file = self.file_service.get_current_file()

        stats_grid = ctk.CTkFrame(
            master,
            fg_color="transparent",
        )
        stats_grid.grid(row=1, column=0, sticky="ew", pady=(0, 18))
        stats_grid.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="stats")

        file_value = "1" if current_file.has_file() else "0"
        file_helper = current_file.name if current_file.has_file() else "Sin carga actual"

        rows_value = str(current_file.rows) if current_file.loaded else "0"
        columns_value = str(current_file.columns) if current_file.loaded else "0"

        stats = [
            ("Archivos", file_value, file_helper, "primary"),
            ("Filas", rows_value, "Detectadas al cargar", "success"),
            ("Columnas", columns_value, "Detectadas al cargar", "primary"),
            ("Estado", "OK" if current_file.loaded else "Pendiente", current_file.get_summary(), "warning"),
        ]

        for index, (label, value, helper, accent) in enumerate(stats):
            card = StatCard(
                stats_grid,
                label=label,
                value=value,
                helper=helper,
                accent=accent,
            )
            card.grid(
                row=0,
                column=index,
                sticky="ew",
                padx=(0 if index == 0 else 8, 0 if index == 3 else 8),
            )

    def _build_cards(self, master):
        cards_grid = ctk.CTkFrame(
            master,
            fg_color="transparent",
        )
        cards_grid.grid(row=2, column=0, sticky="ew")
        cards_grid.grid_columnconfigure((0, 1), weight=1, uniform="cards")

        card_1 = AppCard(
            cards_grid,
            title="Flujo principal",
            subtitle=(
                "El MVP se enfoca en cargar, analizar, limpiar y exportar archivos. "
                "Simple, directo y con impacto operativo real."
            ),
        )
        card_1.grid(row=0, column=0, sticky="nsew", padx=(0, 9), pady=(0, 18))

        flow_text = ctk.CTkLabel(
            card_1,
            text="1. Cargar archivo\n2. Ver vista previa\n3. Analizar problemas\n4. Aplicar limpieza\n5. Exportar resultado",
            font=FONTS["body"],
            text_color=COLORS["text_soft"],
            anchor="w",
            justify="left",
        )
        flow_text.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))

        card_2 = AppCard(
            cards_grid,
            title="Valor del producto",
            subtitle=(
                "Pensado para preparar datos antes de llevarlos a CRM, ERP, bases de datos "
                "o reportes ejecutivos."
            ),
        )
        card_2.grid(row=0, column=1, sticky="nsew", padx=(9, 0), pady=(0, 18))

        value_text = ctk.CTkLabel(
            card_2,
            text=(
                "• Reduce errores humanos\n"
                "• Acelera tareas repetitivas\n"
                "• Mejora calidad del dato\n"
                "• Sirve para portfolio real\n"
                "• Puede escalar a producto comercial"
            ),
            font=FONTS["body"],
            text_color=COLORS["text_soft"],
            anchor="w",
            justify="left",
        )
        value_text.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))

        card_3 = AppCard(
            cards_grid,
            title="Estado actual del archivo",
            subtitle=self.file_service.get_file_summary(),
        )
        card_3.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 18))

        current_file = self.file_service.get_current_file()

        details = [
            f"Nombre: {current_file.name or 'No seleccionado'}",
            f"Extensión: {current_file.extension or 'N/A'}",
            f"Tamaño: {current_file.size_label}",
            f"Ruta: {current_file.path or 'N/A'}",
        ]

        details_text = ctk.CTkLabel(
            card_3,
            text="\n".join(details),
            font=FONTS["body"],
            text_color=COLORS["text_soft"],
            anchor="w",
            justify="left",
        )
        details_text.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))

    def _go_to(self, view_key):
        if self.on_navigate:
            self.on_navigate(view_key)