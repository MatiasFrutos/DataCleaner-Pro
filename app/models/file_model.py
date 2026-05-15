"""
Modelo de archivo cargado para DataCleaner Pro.

Representa la información principal de un archivo seleccionado por el usuario.
Todavía no carga datos reales; eso se conecta en la etapa 4.
"""

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional


@dataclass
class FileModel:
    """
    Modelo simple para representar un archivo dentro de la aplicación.
    """

    name: str
    path: str
    extension: str
    size_bytes: int
    size_label: str
    rows: int = 0
    columns: int = 0
    loaded: bool = False
    error: Optional[str] = None

    @classmethod
    def empty(cls):
        """
        Devuelve un modelo vacío cuando todavía no hay archivo cargado.
        """

        return cls(
            name="",
            path="",
            extension="",
            size_bytes=0,
            size_label="0 B",
            rows=0,
            columns=0,
            loaded=False,
            error=None,
        )

    @classmethod
    def from_path(cls, file_path: str, size_label: str):
        """
        Crea un modelo base desde una ruta de archivo.
        """

        path = Path(file_path)

        return cls(
            name=path.name,
            path=str(path),
            extension=path.suffix.lower(),
            size_bytes=path.stat().st_size if path.exists() else 0,
            size_label=size_label,
            rows=0,
            columns=0,
            loaded=False,
            error=None,
        )

    def update_shape(self, rows: int, columns: int):
        """
        Actualiza cantidad de filas y columnas detectadas.
        """

        self.rows = rows
        self.columns = columns
        self.loaded = True
        self.error = None

    def set_error(self, message: str):
        """
        Marca el archivo con error de carga o validación.
        """

        self.loaded = False
        self.error = message

    def to_dict(self):
        """
        Convierte el modelo en diccionario.
        """

        return asdict(self)

    def has_file(self):
        """
        Indica si hay una ruta asociada al modelo.
        """

        return bool(self.path)

    def get_summary(self):
        """
        Devuelve un resumen legible para mostrar en la UI.
        """

        if not self.has_file():
            return "Sin archivo cargado"

        if self.loaded:
            return f"{self.name} · {self.rows} filas · {self.columns} columnas"

        return f"{self.name} · pendiente de carga"