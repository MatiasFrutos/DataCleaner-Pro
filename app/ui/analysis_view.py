"""
Vista de análisis de datos para DataCleaner Pro.
"""

import customtkinter as ctk

from app.services.analysis_service import analysis_service
from app.ui.styles import COLORS, FONTS, SIZES
from app.ui.components import AppButton, AppCard, Badge, EmptyState, StatCard


class AnalysisView(ctk.CTkFrame):
    """
    Pantalla para mostrar análisis de calidad del archivo cargado.
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
        self.result = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build()

    def _build(self):
        self._build_header()

        if not self.file_service.is_loaded():
            self._build_empty_state()
            return

        dataframe = self.file_service.get_original_dataframe()
        self.result = analysis_service.analyze(dataframe)

        self._build_analysis()

    def _build_header(self):
        header = ctk.CTkFrame(
            self,
            fg_color=COLORS["surface"],
            corner_radius=SIZES["radius_xl"],
            border_width=1,
            border_color=COLORS["border_soft"],
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="Análisis de datos",
            font=FONTS["title"],
            text_color=COLORS["text"],
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="ew", padx=22, pady=(18, 4))

        subtitle = ctk.CTkLabel(
            header,
            text="Detecta vacíos, duplicados, tipos de datos, riesgo y recomendaciones de limpieza.",
            font=FONTS["body"],
            text_color=COLORS["text_muted"],
            anchor="w",
            wraplength=780,
            justify="left",
        )
        subtitle.grid(row=1, column=0, sticky="ew", padx=22, pady=(0, 18))

        actions = ctk.CTkFrame(
            header,
            fg_color="transparent",
        )
        actions.grid(row=0, column=1, rowspan=2, sticky="e", padx=22, pady=18)

        reload_button = AppButton(
            actions,
            text="Reanalizar",
            variant="secondary",
            command=self._reload,
        )
        reload_button.grid(row=0, column=0, padx=(0, 10))

        clean_button = AppButton(
            actions,
            text="Ir a limpieza",
            command=lambda: self._go_to("cleaning"),
        )
        clean_button.grid(row=0, column=1)

    def _build_empty_state(self):
        empty = EmptyState(
            self,
            title="No hay archivo para analizar",
            message="Primero cargá un archivo Excel, CSV o TXT. Después el análisis se ejecuta automáticamente.",
            action_text="Cargar archivo",
            action_command=lambda: self._go_to("file_preview"),
        )
        empty.grid(row=1, column=0, sticky="nsew")

    def _build_analysis(self):
        content = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)

        self._build_score_card(content)
        self._build_stats(content)
        self._build_warnings_and_recommendations(content)
        self._build_columns_table(content)

    def _build_score_card(self, master):
        risk_variant = {
            "Bajo": "success",
            "Medio": "warning",
            "Alto": "danger",
        }.get(self.result.risk_level, "muted")

        card = AppCard(
            master,
            title="Resultado general",
            subtitle=self.result.get_summary(),
        )
        card.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        card.grid_columnconfigure(0, weight=1)

        score_frame = ctk.CTkFrame(
            card,
            fg_color="transparent",
        )
        score_frame.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))
        score_frame.grid_columnconfigure(0, weight=1)

        score_label = ctk.CTkLabel(
            score_frame,
            text=f"{self.result.quality_score}%",
            font=("Segoe UI", 42, "bold"),
            text_color=COLORS["primary"],
            anchor="w",
        )
        score_label.grid(row=0, column=0, sticky="w")

        risk_badge = Badge(
            score_frame,
            text=f"Riesgo {self.result.risk_level}",
            variant=risk_variant,
        )
        risk_badge.grid(row=0, column=1, sticky="e")

    def _build_stats(self, master):
        stats_grid = ctk.CTkFrame(
            master,
            fg_color="transparent",
        )
        stats_grid.grid(row=1, column=0, sticky="ew", pady=(0, 18))
        stats_grid.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="stats")

        stats = [
            ("Filas", str(self.result.total_rows), "Total detectado", "primary"),
            ("Columnas", str(self.result.total_columns), "Estructura base", "primary"),
            ("Vacíos", str(self.result.empty_cells), "Celdas sin valor", "warning"),
            ("Duplicados", str(self.result.duplicated_rows), "Filas repetidas", "danger"),
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

    def _build_warnings_and_recommendations(self, master):
        grid = ctk.CTkFrame(
            master,
            fg_color="transparent",
        )
        grid.grid(row=2, column=0, sticky="ew", pady=(0, 18))
        grid.grid_columnconfigure((0, 1), weight=1, uniform="cards")

        warnings_card = AppCard(
            grid,
            title="Advertencias",
            subtitle="Problemas detectados automáticamente.",
        )
        warnings_card.grid(row=0, column=0, sticky="nsew", padx=(0, 9))

        warnings_text = "\n".join(
            [f"• {warning}" for warning in self.result.warnings]
        ) if self.result.warnings else "• No se detectaron advertencias críticas."

        warnings_label = ctk.CTkLabel(
            warnings_card,
            text=warnings_text,
            font=FONTS["body"],
            text_color=COLORS["text_soft"],
            anchor="w",
            justify="left",
            wraplength=480,
        )
        warnings_label.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))

        recommendations_card = AppCard(
            grid,
            title="Recomendaciones",
            subtitle="Acciones sugeridas antes de exportar.",
        )
        recommendations_card.grid(row=0, column=1, sticky="nsew", padx=(9, 0))

        recommendations_text = "\n".join(
            [f"• {recommendation}" for recommendation in self.result.recommendations]
        )

        recommendations_label = ctk.CTkLabel(
            recommendations_card,
            text=recommendations_text,
            font=FONTS["body"],
            text_color=COLORS["text_soft"],
            anchor="w",
            justify="left",
            wraplength=480,
        )
        recommendations_label.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))

    def _build_columns_table(self, master):
        card = AppCard(
            master,
            title="Análisis por columna",
            subtitle="Tipos de datos y porcentaje de valores vacíos.",
        )
        card.grid(row=3, column=0, sticky="ew", pady=(0, 18))

        table = ctk.CTkScrollableFrame(
            card,
            fg_color=COLORS["surface_soft"],
            corner_radius=SIZES["radius_md"],
            height=320,
        )
        table.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))
        table.grid_columnconfigure((0, 1, 2, 3), weight=1)

        headers = ["Columna", "Tipo", "Vacíos", "% vacío"]

        for index, header in enumerate(headers):
            label = ctk.CTkLabel(
                table,
                text=header,
                font=FONTS["small_bold"],
                text_color=COLORS["text"],
                fg_color=COLORS["surface_muted"],
                corner_radius=6,
                height=32,
                anchor="w",
            )
            label.grid(row=0, column=index, sticky="ew", padx=2, pady=2)

        columns = list(self.result.column_types.keys())

        for row_index, column_name in enumerate(columns, start=1):
            dtype = self.result.column_types.get(column_name, "N/A")
            nulls = self.result.nulls_by_column.get(column_name, 0)
            percentage = self.result.empty_percentage_by_column.get(column_name, 0)

            values = [
                column_name,
                dtype,
                str(nulls),
                f"{percentage}%",
            ]

            for column_index, value in enumerate(values):
                cell = ctk.CTkLabel(
                    table,
                    text=str(value),
                    font=FONTS["small"],
                    text_color=COLORS["text_soft"],
                    fg_color=COLORS["surface"],
                    corner_radius=6,
                    height=30,
                    anchor="w",
                )
                cell.grid(row=row_index, column=column_index, sticky="ew", padx=2, pady=2)

    def _reload(self):
        for widget in self.winfo_children():
            widget.destroy()

        self._build()

    def _go_to(self, view_key):
        if self.on_navigate:
            self.on_navigate(view_key)