"""
Servicio de análisis para DataCleaner Pro.

Conecta la UI con el motor de análisis de datos y suma validaciones
avanzadas de calidad.
"""

from app.core.data_analyzer import analyze_dataframe
from app.core.validation_engine import validate_dataframe_quality
from app.models.analysis_result import AnalysisResult


class AnalysisService:
    """
    Servicio encargado de ejecutar análisis sobre el DataFrame actual.
    """

    def __init__(self):
        self.last_result: AnalysisResult | None = None

    def analyze(self, dataframe) -> AnalysisResult:
        """
        Ejecuta análisis básico + validaciones avanzadas.
        """

        result = analyze_dataframe(dataframe)
        validation_result = validate_dataframe_quality(dataframe)

        for warning in validation_result.get("warnings", []):
            if warning not in result.warnings:
                result.warnings.append(warning)

        for recommendation in validation_result.get("recommendations", []):
            if recommendation not in result.recommendations:
                result.recommendations.append(recommendation)

        risk_points = int(validation_result.get("risk_points", 0) or 0)

        if risk_points:
            result.quality_score = max(0, result.quality_score - risk_points)

            if result.quality_score >= 85:
                result.risk_level = "Bajo"
            elif result.quality_score >= 65:
                result.risk_level = "Medio"
            else:
                result.risk_level = "Alto"

        self.last_result = result
        return self.last_result

    def get_last_result(self) -> AnalysisResult | None:
        """
        Devuelve el último resultado de análisis.
        """

        return self.last_result

    def reset(self):
        """
        Limpia el último análisis.
        """

        self.last_result = None


analysis_service = AnalysisService()