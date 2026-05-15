"""
Servicio de archivo actual para DataCleaner Pro.

Administra el estado del archivo seleccionado y centraliza operaciones
relacionadas con el archivo activo.
"""

from app.core.file_loader import load_file, FileLoaderError
from app.models.file_model import FileModel
from app.utils.file_utils import (
    validate_file_path,
    get_file_size_label,
)


class FileService:
    """
    Servicio encargado de mantener el archivo actual de la aplicación.
    """

    def __init__(self):
        self.current_file: FileModel = FileModel.empty()
        self.original_dataframe = None
        self.cleaned_dataframe = None
        self.load_metadata = {}

    def reset(self):
        """
        Reinicia el estado del servicio.
        """

        self.current_file = FileModel.empty()
        self.original_dataframe = None
        self.cleaned_dataframe = None
        self.load_metadata = {}

    def set_selected_file(self, file_path: str) -> FileModel:
        """
        Guarda un archivo seleccionado luego de validar su ruta.
        """

        is_valid, message = validate_file_path(file_path)

        if not is_valid:
            self.current_file = FileModel.empty()
            self.current_file.set_error(message)
            self.original_dataframe = None
            self.cleaned_dataframe = None
            self.load_metadata = {}
            return self.current_file

        size_label = get_file_size_label(file_path)
        self.current_file = FileModel.from_path(file_path, size_label)

        return self.current_file

    def load_selected_file(self, file_path: str) -> FileModel:
        """
        Valida, carga y guarda un archivo real usando Pandas.
        """

        self.set_selected_file(file_path)

        if self.current_file.error:
            return self.current_file

        try:
            dataframe, metadata = load_file(file_path)

            self.original_dataframe = dataframe
            self.cleaned_dataframe = None
            self.load_metadata = metadata

            rows, columns = dataframe.shape
            self.current_file.update_shape(int(rows), int(columns))

            return self.current_file

        except FileLoaderError as error:
            self.original_dataframe = None
            self.cleaned_dataframe = None
            self.load_metadata = {}
            self.current_file.set_error(str(error))
            return self.current_file

        except Exception as error:
            self.original_dataframe = None
            self.cleaned_dataframe = None
            self.load_metadata = {}
            self.current_file.set_error(f"Error inesperado al cargar archivo: {error}")
            return self.current_file

    def mark_loaded(self, rows: int, columns: int):
        """
        Marca el archivo actual como cargado.
        """

        self.current_file.update_shape(rows, columns)
        return self.current_file

    def set_error(self, message: str):
        """
        Marca un error sobre el archivo actual.
        """

        self.current_file.set_error(message)
        return self.current_file

    def has_file(self) -> bool:
        """
        Indica si existe un archivo seleccionado.
        """

        return self.current_file.has_file()

    def is_loaded(self) -> bool:
        """
        Indica si el archivo está cargado correctamente.
        """

        return self.current_file.loaded

    def get_current_file(self) -> FileModel:
        """
        Devuelve el archivo actual.
        """

        return self.current_file

    def get_original_dataframe(self):
        """
        Devuelve el DataFrame original.
        """

        return self.original_dataframe

    def set_original_dataframe(self, dataframe):
        """
        Guarda el DataFrame original.
        """

        self.original_dataframe = dataframe

        if dataframe is not None:
            rows, columns = dataframe.shape
            self.mark_loaded(rows, columns)

    def get_cleaned_dataframe(self):
        """
        Devuelve el DataFrame limpio.
        """

        return self.cleaned_dataframe

    def set_cleaned_dataframe(self, dataframe):
        """
        Guarda el DataFrame limpio.
        """

        self.cleaned_dataframe = dataframe

    def get_load_metadata(self):
        """
        Devuelve metadata técnica de la carga.
        """

        return self.load_metadata

    def get_file_summary(self) -> str:
        """
        Devuelve un resumen corto del archivo actual.
        """

        return self.current_file.get_summary()

    def get_status_variant(self) -> str:
        """
        Devuelve una variante visual para el estado del archivo.
        """

        if self.current_file.error:
            return "danger"

        if self.current_file.loaded:
            return "success"

        if self.current_file.has_file():
            return "warning"

        return "muted"


file_service = FileService()