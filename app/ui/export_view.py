"""
Vista de exportación para DataCleaner Pro.
"""

import os
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk

from app.config import OUTPUT_DIR
from app.services.export_service import export_service
from app.ui.styles import COLORS, FONTS, SIZES
from app.ui.components import AppButton, AppCard, EmptyState, Badge
from app.utils.file_utils import get_file_stem


class ExportView(ctk.CTkFrame):
    """
    Pantalla para exportar el DataFrame limpio.
    """

    def __init__(self, master, file_service, on_exported=None, on_navigate=None, **kwargs):
        super().__init__(
            master,
            fg_color="transparent",
            corner_radius=0,
            **kwargs
        )

        self.file_service = file_service
        self.on_exported = on_exported
        self.on_navigate = on_navigate

        self.export_format = ctk.StringVar(value="xlsx")
        self.output_path = ctk.StringVar(value=self._get_default_output_path("xlsx"))

        self.result = export_service.get_last_result()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build()

    def _build(self):
        self._build_header()

        if not self.file_service.is_loaded():
            self._build_empty_state(
                title="No hay archivo para exportar",
                message="Primero cargá un archivo, analizalo y ejecutá la limpieza.",
                action_text="Cargar archivo",
                action_command=lambda: self._go_to("file_preview"),
            )
            return

        if self.file_service.get_cleaned_dataframe() is None:
            self._build_empty_state(
                title="Todavía no hay datos limpios",
                message="Ejecutá la limpieza automática antes de exportar. Así no mandamos basura premium a producción.",
                action_text="Ir a limpieza",
                action_command=lambda: self._go_to("cleaning"),
            )
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
            text="Exportar archivo limpio",
            font=FONTS["title"],
            text_color=COLORS["text"],
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="ew", padx=22, pady=(18, 4))

        subtitle = ctk.CTkLabel(
            header,
            text="Guardá el resultado limpio como Excel o CSV para usarlo en reportes, sistemas o bases de datos.",
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

        export_button = AppButton(
            actions,
            text="Exportar ahora",
            command=self._export,
        )
        export_button.grid(row=0, column=0)

    def _build_empty_state(self, title, message, action_text, action_command):
        empty = EmptyState(
            self,
            title=title,
            message=message,
            action_text=action_text,
            action_command=action_command,
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

        self._build_export_options(content)
        self._build_result(content)

    def _build_export_options(self, master):
        card = AppCard(
            master,
            title="Configuración de exportación",
            subtitle="Elegí formato y ubicación del archivo final.",
        )
        card.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        card.grid_columnconfigure(0, weight=1)

        form = ctk.CTkFrame(
            card,
            fg_color="transparent",
        )
        form.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))
        form.grid_columnconfigure(1, weight=1)

        format_label = ctk.CTkLabel(
            form,
            text="Formato",
            font=FONTS["body_bold"],
            text_color=COLORS["text"],
            anchor="w",
        )
        format_label.grid(row=0, column=0, sticky="w", padx=(0, 14), pady=8)

        format_menu = ctk.CTkOptionMenu(
            form,
            values=["xlsx", "csv"],
            variable=self.export_format,
            command=self._on_format_change,
            fg_color=COLORS["primary"],
            button_color=COLORS["primary_hover"],
            button_hover_color=COLORS["primary_hover"],
            font=FONTS["body"],
        )
        format_menu.grid(row=0, column=1, sticky="w", pady=8)

        path_label = ctk.CTkLabel(
            form,
            text="Destino",
            font=FONTS["body_bold"],
            text_color=COLORS["text"],
            anchor="w",
        )
        path_label.grid(row=1, column=0, sticky="w", padx=(0, 14), pady=8)

        path_entry = ctk.CTkEntry(
            form,
            textvariable=self.output_path,
            height=40,
            corner_radius=SIZES["radius_md"],
            border_color=COLORS["border"],
            fg_color=COLORS["surface"],
            text_color=COLORS["text"],
            font=FONTS["body"],
        )
        path_entry.grid(row=1, column=1, sticky="ew", pady=8)

        browse_button = AppButton(
            form,
            text="Elegir ubicación",
            variant="secondary",
            command=self._select_output_path,
        )
        browse_button.grid(row=1, column=2, sticky="e", padx=(10, 0), pady=8)

        export_button = AppButton(
            form,
            text="Exportar archivo limpio",
            command=self._export,
        )
        export_button.grid(row=2, column=1, sticky="w", pady=(14, 0))

    def _build_result(self, master):
        result = self.result

        if result is None:
            card = AppCard(
                master,
                title="Resultado de exportación",
                subtitle="Todavía no se exportó ningún archivo.",
            )
            card.grid(row=1, column=0, sticky="ew", pady=(0, 18))

            helper = ctk.CTkLabel(
                card,
                text="Cuando exportes, acá vas a ver la ruta final, formato y tamaño del archivo.",
                font=FONTS["body"],
                text_color=COLORS["text_muted"],
                anchor="w",
            )
            helper.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))
            return

        variant = "success" if result.success else "danger"
        title = "Exportación completada" if result.success else "Exportación fallida"

        card = AppCard(
            master,
            title=title,
            subtitle=result.get_summary(),
        )
        card.grid(row=1, column=0, sticky="ew", pady=(0, 18))

        badge = Badge(
            card,
            text="OK" if result.success else "ERROR",
            variant=variant,
        )
        badge.grid(row=2, column=0, sticky="w", padx=18, pady=(0, 12))

        details = []

        if result.success:
            details = [
                f"Formato: {result.export_format}",
                f"Filas: {result.rows}",
                f"Columnas: {result.columns}",
                f"Tamaño: {result.file_size_label}",
                f"Ruta: {result.output_path}",
            ]
        else:
            details = [
                f"Error: {result.error}",
            ]

        details_label = ctk.CTkLabel(
            card,
            text="\n".join(details),
            font=FONTS["body"],
            text_color=COLORS["text_soft"] if result.success else COLORS["danger"],
            anchor="w",
            justify="left",
            wraplength=850,
        )
        details_label.grid(row=3, column=0, sticky="ew", padx=18, pady=(0, 18))

        if result.success:
            open_button = AppButton(
                card,
                text="Abrir carpeta",
                variant="secondary",
                command=lambda: self._open_output_folder(result.output_path),
            )
            open_button.grid(row=4, column=0, sticky="w", padx=18, pady=(0, 18))

    def _get_default_output_path(self, export_format: str):
        current_file = self.file_service.get_current_file()

        if current_file and current_file.path:
            stem = get_file_stem(current_file.path)
        else:
            stem = "datacleaner_output"

        file_name = f"{stem}_clean.{export_format}"

        return str(Path(OUTPUT_DIR) / file_name)

    def _on_format_change(self, selected_format):
        self.output_path.set(self._get_default_output_path(selected_format))

    def _select_output_path(self):
        selected_format = self.export_format.get()

        filetypes = [
            ("Excel", "*.xlsx"),
            ("CSV", "*.csv"),
        ]

        path = filedialog.asksaveasfilename(
            title="Guardar archivo limpio",
            defaultextension=f".{selected_format}",
            filetypes=filetypes,
            initialfile=Path(self.output_path.get()).name,
        )

        if path:
            self.output_path.set(path)

    def _export(self):
        dataframe = self.file_service.get_cleaned_dataframe()
        output_path = self.output_path.get()
        selected_format = self.export_format.get()

        self.result = export_service.export(dataframe, output_path, selected_format)

        if self.on_exported:
            self.on_exported()

        self._reload()

    def _reload(self):
        for widget in self.winfo_children():
            widget.destroy()

        self._build()

    def _open_output_folder(self, output_path):
        folder = Path(output_path).parent

        if folder.exists():
            os.startfile(str(folder))

    def _go_to(self, view_key):
        if self.on_navigate:
            self.on_navigate(view_key)