"""
Modelo de resultado de exportación para DataCleaner Pro.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class ExportResult:
    """
    Representa el resultado de una exportación.
    """

    success: bool = False
    output_path: str = ""
    export_format: str = ""
    rows: int = 0
    columns: int = 0
    file_size_label: str = ""
    error: str | None = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el resultado en diccionario.
        """

        return asdict(self)

    def get_summary(self) -> str:
        """
        Devuelve resumen corto.
        """

        if not self.success:
            return self.error or "La exportación no se pudo completar."

        return (
            f"Archivo exportado · {self.rows} filas · "
            f"{self.columns} columnas · {self.file_size_label}"
        )