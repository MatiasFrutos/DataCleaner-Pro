"""
Vista de limpieza automática para DataCleaner Pro.
"""

import customtkinter as ctk

from app.services.cleaning_service import cleaning_service
from app.ui.styles import COLORS, FONTS, SIZES
from app.ui.components import AppButton, AppCard, EmptyState, StatCard, Badge
from app.utils.dataframe_utils import get_preview_columns, get_preview_records, safe_cell_value


class CleaningView(ctk.CTkFrame):
    """
    Pantalla para ejecutar limpieza automática sobre el archivo cargado.
    """

    def __init__(self, master, file_service, on_cleaned=None, on_navigate=None, **kwargs):
        super().__init__(
            master,
            fg_color="transparent",
            corner_radius=0,
            **kwargs
        )

        self.file_service = file_service
        self.on_cleaned = on_cleaned
        self.on_navigate = on_navigate

        self.option_remove_empty_rows = ctk.BooleanVar(value=True)
        self.option_remove_empty_columns = ctk.BooleanVar(value=True)
        self.option_remove_duplicates = ctk.BooleanVar(value=True)
        self.option_trim_text = ctk.BooleanVar(value=True)
        self.option_normalize_columns = ctk.BooleanVar(value=True)
        self.option_normalize_missing_values = ctk.BooleanVar(value=True)
        self.option_normalize_dates = ctk.BooleanVar(value=True)

        self.result = cleaning_service.get_last_result()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build()

    def _build(self):
        self._build_header()

        if not self.file_service.is_loaded():
            self._build_empty_state()
            return

        self._build_content()

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
            text="Limpieza automática",
            font=FONTS["title"],
            text_color=COLORS["text"],
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="ew", padx=22, pady=(18, 4))

        subtitle = ctk.CTkLabel(
            header,
            text="Aplicá reglas seguras para ordenar el archivo antes de exportarlo.",
            font=FONTS["body"],
            text_color=COLORS["text_muted"],
            anchor="w",
            wraplength=760,
            justify="left",
        )
        subtitle.grid(row=1, column=0, sticky="ew", padx=22, pady=(0, 18))

        actions = ctk.CTkFrame(
            header,
            fg_color="transparent",
        )
        actions.grid(row=0, column=1, rowspan=2, sticky="e", padx=22, pady=18)

        clean_button = AppButton(
            actions,
            text="Ejecutar limpieza",
            command=self._run_cleaning,
        )
        clean_button.grid(row=0, column=0, padx=(0, 10))

        export_button = AppButton(
            actions,
            text="Exportar",
            variant="secondary",
            command=lambda: self._go_to("export"),
        )
        export_button.grid(row=0, column=1)

    def _build_empty_state(self):
        empty = EmptyState(
            self,
            title="No hay archivo para limpiar",
            message="Primero cargá un archivo y ejecutá el análisis. Después vas a poder aplicar limpieza automática.",
            action_text="Cargar archivo",
            action_command=lambda: self._go_to("file_preview"),
        )
        empty.grid(row=1, column=0, sticky="nsew")

    def _build_content(self):
        content = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)

        self._build_options(content)
        self._build_result(content)

        if self.file_service.get_cleaned_dataframe() is not None:
            self._build_clean_preview(content)

    def _build_options(self, master):
        card = AppCard(
            master,
            title="Reglas de limpieza",
            subtitle="Podés activar o desactivar reglas antes de ejecutar. Por defecto vienen las más seguras.",
        )
        card.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        card.grid_columnconfigure(0, weight=1)

        options_frame = ctk.CTkFrame(
            card,
            fg_color="transparent",
        )
        options_frame.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))
        options_frame.grid_columnconfigure((0, 1), weight=1)

        options = [
            ("Eliminar filas vacías", self.option_remove_empty_rows),
            ("Eliminar columnas vacías", self.option_remove_empty_columns),
            ("Eliminar duplicados", self.option_remove_duplicates),
            ("Limpiar espacios en textos", self.option_trim_text),
            ("Normalizar nombres de columnas", self.option_normalize_columns),
            ("Normalizar valores faltantes", self.option_normalize_missing_values),
            ("Normalizar fechas detectadas", self.option_normalize_dates),
        ]

        for index, (label, variable) in enumerate(options):
            checkbox = ctk.CTkCheckBox(
                options_frame,
                text=label,
                variable=variable,
                font=FONTS["body"],
                text_color=COLORS["text_soft"],
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_hover"],
                border_color=COLORS["border"],
            )
            checkbox.grid(
                row=index // 2,
                column=index % 2,
                sticky="w",
                padx=8,
                pady=8,
            )

    def _build_result(self, master):
        result = self.result

        if result is None:
            card = AppCard(
                master,
                title="Resultado de limpieza",
                subtitle="Todavía no se ejecutó ninguna limpieza.",
            )
            card.grid(row=1, column=0, sticky="ew", pady=(0, 18))

            helper = ctk.CTkLabel(
                card,
                text="Cuando ejecutes la limpieza, acá vas a ver el resumen antes/después.",
                font=FONTS["body"],
                text_color=COLORS["text_muted"],
                anchor="w",
            )
            helper.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))
            return

        if not result.success:
            empty = EmptyState(
                master,
                title="No se pudo limpiar el archivo",
                message=result.error or "Error desconocido durante la limpieza.",
                action_text="Reintentar limpieza",
                action_command=self._run_cleaning,
            )
            empty.grid(row=1, column=0, sticky="ew", pady=(0, 18))
            return

        stats_grid = ctk.CTkFrame(
            master,
            fg_color="transparent",
        )
        stats_grid.grid(row=1, column=0, sticky="ew", pady=(0, 18))
        stats_grid.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="clean_stats")

        stats = [
            ("Filas", str(result.cleaned_rows), f"Antes: {result.original_rows}", "success"),
            ("Columnas", str(result.cleaned_columns), f"Antes: {result.original_columns}", "primary"),
            ("Duplicados", str(result.removed_duplicates), "Removidos", "warning"),
            ("Textos", str(result.cleaned_text_cells), "Celdas limpiadas", "primary"),
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

        actions_card = AppCard(
            master,
            title="Acciones aplicadas",
            subtitle=result.get_summary(),
        )
        actions_card.grid(row=2, column=0, sticky="ew", pady=(0, 18))

        actions_text = "\n".join([f"• {action}" for action in result.actions]) or "• Sin acciones registradas."

        label = ctk.CTkLabel(
            actions_card,
            text=actions_text,
            font=FONTS["body"],
            text_color=COLORS["text_soft"],
            anchor="w",
            justify="left",
        )
        label.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))

        if result.warnings:
            warning_badge = Badge(
                actions_card,
                text="Revisar advertencias",
                variant="warning",
            )
            warning_badge.grid(row=3, column=0, sticky="w", padx=18, pady=(0, 8))

            warnings_text = "\n".join([f"• {warning}" for warning in result.warnings])

            warning_label = ctk.CTkLabel(
                actions_card,
                text=warnings_text,
                font=FONTS["body"],
                text_color=COLORS["warning"],
                anchor="w",
                justify="left",
            )
            warning_label.grid(row=4, column=0, sticky="ew", padx=18, pady=(0, 18))

    def _build_clean_preview(self, master):
        dataframe = self.file_service.get_cleaned_dataframe()

        card = AppCard(
            master,
            title="Preview del archivo limpio",
            subtitle="Primeras filas del resultado limpio antes de exportar.",
        )
        card.grid(row=3, column=0, sticky="ew", pady=(0, 18))

        columns = get_preview_columns(dataframe)
        records = get_preview_records(dataframe, 30)

        if not columns:
            helper = ctk.CTkLabel(
                card,
                text="No hay columnas para mostrar.",
                font=FONTS["body"],
                text_color=COLORS["text_muted"],
            )
            helper.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))
            return

        table_wrapper = ctk.CTkScrollableFrame(
            card,
            fg_color=COLORS["surface_soft"],
            corner_radius=SIZES["radius_md"],
            orientation="horizontal",
            height=340,
        )
        table_wrapper.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))

        table = ctk.CTkFrame(
            table_wrapper,
            fg_color="transparent",
        )
        table.grid(row=0, column=0, sticky="nw")

        max_columns = min(len(columns), 12)

        for column_index, column_name in enumerate(columns[:max_columns]):
            header = ctk.CTkLabel(
                table,
                text=safe_cell_value(column_name, 28),
                font=FONTS["small_bold"],
                text_color=COLORS["text"],
                fg_color=COLORS["surface_muted"],
                corner_radius=6,
                width=150,
                height=34,
                anchor="w",
            )
            header.grid(row=0, column=column_index, padx=2, pady=2, sticky="ew")

        for row_index, record in enumerate(records, start=1):
            for column_index, column_name in enumerate(columns[:max_columns]):
                value = safe_cell_value(record.get(column_name, ""), 32)

                cell = ctk.CTkLabel(
                    table,
                    text=value,
                    font=FONTS["small"],
                    text_color=COLORS["text_soft"],
                    fg_color=COLORS["surface"],
                    corner_radius=6,
                    width=150,
                    height=30,
                    anchor="w",
                )
                cell.grid(row=row_index, column=column_index, padx=2, pady=2, sticky="ew")

    def _run_cleaning(self):
        options = {
            "remove_empty_rows": self.option_remove_empty_rows.get(),
            "remove_empty_columns": self.option_remove_empty_columns.get(),
            "remove_duplicates": self.option_remove_duplicates.get(),
            "trim_text": self.option_trim_text.get(),
            "normalize_columns": self.option_normalize_columns.get(),
            "normalize_missing_values": self.option_normalize_missing_values.get(),
            "normalize_dates": self.option_normalize_dates.get(),
        }

        dataframe = self.file_service.get_original_dataframe()
        cleaned_dataframe, result = cleaning_service.clean(dataframe, options)

        self.result = result

        if cleaned_dataframe is not None:
            self.file_service.set_cleaned_dataframe(cleaned_dataframe)

        if self.on_cleaned:
            self.on_cleaned()

        self._reload()

    def _reload(self):
        for widget in self.winfo_children():
            widget.destroy()

        self._build()

    def _go_to(self, view_key):
        if self.on_navigate:
            self.on_navigate(view_key)