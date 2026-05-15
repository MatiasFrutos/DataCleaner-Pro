"""
Modelo de resultado de limpieza para DataCleaner Pro.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any


@dataclass
class CleaningResult:
    """
    Representa el resultado de una limpieza automática.
    """

    original_rows: int = 0
    original_columns: int = 0

    cleaned_rows: int = 0
    cleaned_columns: int = 0

    removed_empty_rows: int = 0
    removed_empty_columns: int = 0
    removed_duplicates: int = 0

    cleaned_text_cells: int = 0
    normalized_columns: int = 0
    normalized_dates: int = 0

    renamed_columns: Dict[str, str] = field(default_factory=dict)
    actions: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    success: bool = True
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
            return f"Limpieza fallida: {self.error}"

        return (
            f"{self.cleaned_rows} filas · "
            f"{self.cleaned_columns} columnas · "
            f"{self.removed_duplicates} duplicados removidos"
        )