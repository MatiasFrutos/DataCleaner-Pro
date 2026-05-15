"""
Ventana principal de DataCleaner Pro.

Define la estructura general de la aplicación:
sidebar, topbar y área central de contenido.
"""

import customtkinter as ctk

from app.config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    WINDOW_TITLE,
)
from app.services.file_service import file_service
from app.ui.styles import COLORS
from app.ui.sidebar import Sidebar
from app.ui.topbar import Topbar
from app.ui.components import EmptyState
from app.ui.dashboard_view import DashboardView
from app.ui.file_preview_view import FilePreviewView
from app.ui.analysis_view import AnalysisView
from app.ui.cleaning_view import CleaningView
from app.ui.export_view import ExportView


class DataCleanerApp(ctk.CTk):
    """
    Aplicación principal de escritorio.
    """

    def __init__(self):
        super().__init__()

        self.current_view = "dashboard"
        self.file_service = file_service

        self._setup_window()
        self._setup_layout()
        self._render_dashboard()

    def _setup_window(self):
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.configure(fg_color=COLORS["app_bg"])

    def _setup_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = Sidebar(
            self,
            on_navigate=self.navigate_to,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsw")

        self.main_area = ctk.CTkFrame(
            self,
            fg_color=COLORS["app_bg"],
            corner_radius=0,
        )
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_rowconfigure(1, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        self.topbar = Topbar(
            self.main_area,
            on_primary_action=lambda: self.navigate_to("file_preview"),
        )
        self.topbar.grid(row=0, column=0, sticky="ew")

        self.content = ctk.CTkFrame(
            self.main_area,
            fg_color=COLORS["app_bg"],
            corner_radius=0,
        )
        self.content.grid(row=1, column=0, sticky="nsew", padx=24, pady=24)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

    def navigate_to(self, view_key):
        self.current_view = view_key
        self.sidebar.active_view = view_key
        self.sidebar._refresh_active_button()

        self._clear_content()
        self._sync_topbar_file_status()

        views = {
            "dashboard": self._render_dashboard,
            "file_preview": self._render_file_preview,
            "analysis": self._render_analysis,
            "cleaning": self._render_cleaning,
            "export": self._render_export,
        }

        render = views.get(view_key, self._render_dashboard)
        render()

    def _clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def _sync_topbar_file_status(self):
        self.topbar.set_file_status(
            self.file_service.get_file_summary(),
            self.file_service.get_status_variant(),
        )

    def _on_file_loaded(self):
        self._sync_topbar_file_status()
        self.navigate_to("file_preview")

    def _on_cleaned(self):
        self._sync_topbar_file_status()

    def _on_exported(self):
        self._sync_topbar_file_status()

    def _render_dashboard(self):
        self.topbar.set_section(
            "Dashboard",
            "Vista general del flujo de limpieza de datos.",
        )
        self._sync_topbar_file_status()

        view = DashboardView(
            self.content,
            file_service=self.file_service,
            on_navigate=self.navigate_to,
        )
        view.grid(row=0, column=0, sticky="nsew")

    def _render_file_preview(self):
        self.topbar.set_section(
            "Cargar archivo",
            "Selección y vista previa de Excel, CSV o TXT.",
        )
        self._sync_topbar_file_status()

        view = FilePreviewView(
            self.content,
            file_service=self.file_service,
            on_file_loaded=self._on_file_loaded,
            on_navigate=self.navigate_to,
        )
        view.grid(row=0, column=0, sticky="nsew")

    def _render_analysis(self):
        self.topbar.set_section(
            "Análisis",
            "Detección de problemas, duplicados y valores vacíos.",
        )
        self._sync_topbar_file_status()

        view = AnalysisView(
            self.content,
            file_service=self.file_service,
            on_navigate=self.navigate_to,
        )
        view.grid(row=0, column=0, sticky="nsew")

    def _render_cleaning(self):
        self.topbar.set_section(
            "Limpieza",
            "Corrección automática de datos desordenados.",
        )
        self._sync_topbar_file_status()

        view = CleaningView(
            self.content,
            file_service=self.file_service,
            on_cleaned=self._on_cleaned,
            on_navigate=self.navigate_to,
        )
        view.grid(row=0, column=0, sticky="nsew")

    def _render_export(self):
        self.topbar.set_section(
            "Exportar",
            "Guardar archivo limpio como Excel o CSV.",
        )
        self._sync_topbar_file_status()

        view = ExportView(
            self.content,
            file_service=self.file_service,
            on_exported=self._on_exported,
            on_navigate=self.navigate_to,
        )
        view.grid(row=0, column=0, sticky="nsew")

    def _render_fallback(self):
        empty = EmptyState(
            self.content,
            title="Pantalla no disponible",
            message="La sección solicitada no está registrada en el router interno.",
            action_text="Volver al dashboard",
            action_command=lambda: self.navigate_to("dashboard"),
        )
        empty.grid(row=0, column=0, sticky="nsew")