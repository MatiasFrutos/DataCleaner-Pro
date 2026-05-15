"""
Modelo de resultado de análisis para DataCleaner Pro.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any


@dataclass
class AnalysisResult:
    """
    Representa el resultado del análisis de calidad de datos.
    """

    total_rows: int = 0
    total_columns: int = 0
    total_cells: int = 0

    empty_cells: int = 0
    empty_rows: int = 0
    empty_columns: int = 0
    duplicated_rows: int = 0

    column_types: Dict[str, str] = field(default_factory=dict)
    nulls_by_column: Dict[str, int] = field(default_factory=dict)
    empty_percentage_by_column: Dict[str, float] = field(default_factory=dict)

    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    quality_score: int = 100
    risk_level: str = "Bajo"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el resultado en diccionario.
        """

        return asdict(self)

    def has_issues(self) -> bool:
        """
        Indica si el análisis encontró problemas.
        """

        return bool(
            self.empty_cells
            or self.empty_rows
            or self.empty_columns
            or self.duplicated_rows
            or self.warnings
        )

    def get_summary(self) -> str:
        """
        Devuelve resumen corto del análisis.
        """

        return (
            f"{self.total_rows} filas · "
            f"{self.total_columns} columnas · "
            f"{self.quality_score}% calidad · "
            f"riesgo {self.risk_level.lower()}"
        )