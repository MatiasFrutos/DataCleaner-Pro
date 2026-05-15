"""
Vista de carga y preview de archivos para DataCleaner Pro.
"""

import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk

from app.config import DEFAULT_PREVIEW_ROWS
from app.ui.styles import COLORS, FONTS, SIZES
from app.ui.components import AppButton, AppCard, Badge, EmptyState
from app.utils.dataframe_utils import (
    get_preview_columns,
    get_preview_records,
    safe_cell_value,
    get_memory_usage_label,
)


class FilePreviewView(ctk.CTkFrame):
    """
    Pantalla para cargar archivos y mostrar vista previa.
    """

    def __init__(self, master, file_service, on_file_loaded=None, on_navigate=None, **kwargs):
        super().__init__(
            master,
            fg_color="transparent",
            corner_radius=0,
            **kwargs
        )

        self.file_service = file_service
        self.on_file_loaded = on_file_loaded
        self.on_navigate = on_navigate

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build()

    def _build(self):
        self._build_header()

        if self.file_service.is_loaded():
            self._build_preview()
        else:
            self._build_empty_state()

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
            text="Cargar archivo",
            font=FONTS["title"],
            text_color=COLORS["text"],
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="ew", padx=22, pady=(18, 4))

        subtitle = ctk.CTkLabel(
            header,
            text="Seleccioná un archivo Excel, CSV o TXT para leerlo con Pandas y generar una vista previa.",
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

        upload_button = AppButton(
            actions,
            text="Seleccionar archivo",
            command=self._select_file,
        )
        upload_button.grid(row=0, column=0, padx=(0, 10))

        if self.file_service.is_loaded():
            analysis_button = AppButton(
                actions,
                text="Analizar datos",
                variant="secondary",
                command=lambda: self._go_to("analysis"),
            )
            analysis_button.grid(row=0, column=1)

    def _build_empty_state(self):
        current_file = self.file_service.get_current_file()

        if current_file.error:
            title = "No se pudo cargar el archivo"
            message = current_file.error
        else:
            title = "Todavía no hay archivo cargado"
            message = (
                "Cargá un Excel, CSV o TXT para visualizar filas, columnas, "
                "metadata técnica y preparar el análisis de calidad."
            )

        empty = EmptyState(
            self,
            title=title,
            message=message,
            action_text="Seleccionar archivo",
            action_command=self._select_file,
        )
        empty.grid(row=1, column=0, sticky="nsew")

    def _build_preview(self):
        dataframe = self.file_service.get_original_dataframe()
        current_file = self.file_service.get_current_file()
        metadata = self.file_service.get_load_metadata()

        content = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)

        info_grid = ctk.CTkFrame(
            content,
            fg_color="transparent",
        )
        info_grid.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        info_grid.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="info")

        info_items = [
            ("Archivo", current_file.name, "primary"),
            ("Filas", str(current_file.rows), "success"),
            ("Columnas", str(current_file.columns), "primary"),
            ("Memoria", get_memory_usage_label(dataframe), "warning"),
        ]

        for index, (label, value, variant) in enumerate(info_items):
            card = AppCard(info_grid)
            card.grid(
                row=0,
                column=index,
                sticky="ew",
                padx=(0 if index == 0 else 8, 0 if index == 3 else 8),
            )

            badge = Badge(card, text=label, variant=variant)
            badge.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

            value_label = ctk.CTkLabel(
                card,
                text=value,
                font=FONTS["subtitle"],
                text_color=COLORS["text"],
                anchor="w",
            )
            value_label.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))

        metadata_card = AppCard(
            content,
            title="Metadata de carga",
            subtitle=(
                f"Tipo: {metadata.get('source_type', 'N/A')} · "
                f"Encoding: {metadata.get('encoding') or 'N/A'} · "
                f"Separador: {metadata.get('separator') or 'N/A'}"
            ),
        )
        metadata_card.grid(row=1, column=0, sticky="ew", pady=(0, 18))

        table_card = AppCard(
            content,
            title="Vista previa",
            subtitle=f"Primeras {DEFAULT_PREVIEW_ROWS} filas del archivo cargado.",
        )
        table_card.grid(row=2, column=0, sticky="nsew")

        self._render_table(table_card, dataframe)

    def _render_table(self, master, dataframe):
        columns = get_preview_columns(dataframe)
        records = get_preview_records(dataframe, DEFAULT_PREVIEW_ROWS)

        if not columns:
            no_data = ctk.CTkLabel(
                master,
                text="No hay columnas disponibles para mostrar.",
                font=FONTS["body"],
                text_color=COLORS["text_muted"],
            )
            no_data.grid(row=2, column=0, sticky="ew", padx=18, pady=18)
            return

        table_wrapper = ctk.CTkScrollableFrame(
            master,
            fg_color=COLORS["surface_soft"],
            corner_radius=SIZES["radius_md"],
            orientation="horizontal",
            height=380,
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

        if len(columns) > max_columns:
            helper = ctk.CTkLabel(
                master,
                text=f"Vista limitada a {max_columns} columnas para mantener rendimiento visual.",
                font=FONTS["small"],
                text_color=COLORS["text_faint"],
                anchor="w",
            )
            helper.grid(row=3, column=0, sticky="ew", padx=18, pady=(0, 18))

    def _select_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[
                ("Archivos soportados", "*.xlsx *.xls *.csv *.txt"),
                ("Excel", "*.xlsx *.xls"),
                ("CSV", "*.csv"),
                ("Texto", "*.txt"),
                ("Todos los archivos", "*.*"),
            ],
        )

        if not file_path:
            return

        self.file_service.load_selected_file(file_path)

        if self.on_file_loaded:
            self.on_file_loaded()

    def _go_to(self, view_key):
        if self.on_navigate:
            self.on_navigate(view_key)