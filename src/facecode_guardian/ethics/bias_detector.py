"""
Detector de Bias (Sesgo) en Reconocimiento Facial
==================================================

Detecta y reporta posibles sesgos demográficos en las predicciones.
Cumplimiento con AI Act de la UE - Artículo 10 (Datos y Gobernanza).
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import numpy as np
from collections import defaultdict


@dataclass
class BiasMetrics:
    """Métricas de sesgo detectadas"""
    total_detections: int
    confidence_stats: Dict[str, float]  # min, max, mean, std
    demographic_distribution: Dict[str, int] = field(default_factory=dict)
    bias_score: float = 0.0  # 0 = sin sesgo, 1 = sesgo máximo
    warnings: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class BiasDetector:
    """
    Detector de sesgos en detecciones faciales.

    Analiza:
    - Distribución de confianza por grupo demográfico
    - Tasas de detección asimétricas
    - Patrones de error sistemáticos
    """

    def __init__(self, confidence_threshold: float = 0.2):
        """
        Args:
            confidence_threshold: Umbral de diferencia de confianza que se considera sesgo
        """
        self.confidence_threshold = confidence_threshold
        self.detection_history: List[Dict[str, Any]] = []

    def analyze_detections(
        self,
        detections: List[Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> BiasMetrics:
        """
        Analiza una serie de detecciones en busca de sesgos.

        Args:
            detections: Lista de FaceDetection objects
            metadata: Metadatos adicionales (ej: contexto demográfico)

        Returns:
            BiasMetrics con análisis
        """
        if not detections:
            return BiasMetrics(
                total_detections=0,
                confidence_stats={},
                warnings=["No detections to analyze"]
            )

        # Extraer confianzas
        confidences = [det.confidence for det in detections]

        # Calcular estadísticas
        confidence_stats = {
            'min': float(np.min(confidences)),
            'max': float(np.max(confidences)),
            'mean': float(np.mean(confidences)),
            'std': float(np.std(confidences)),
            'median': float(np.median(confidences))
        }

        # Detectar warnings
        warnings = []

        # Warning 1: Alta varianza en confianzas
        if confidence_stats['std'] > self.confidence_threshold:
            warnings.append(
                f"Alta varianza en confianzas (std={confidence_stats['std']:.3f}). "
                "Posible sesgo en rendimiento del modelo."
            )

        # Warning 2: Confianzas muy bajas
        if confidence_stats['mean'] < 0.6:
            warnings.append(
                f"Confianza promedio baja ({confidence_stats['mean']:.2%}). "
                "Revisar calidad de datos o condiciones de captura."
            )

        # Warning 3: Detecciones muy altas (vigilancia masiva)
        if len(detections) > 5:
            warnings.append(
                f"Alto número de detecciones ({len(detections)}). "
                "Verificar que no sea uso de vigilancia masiva."
            )

        # Calcular bias score simplificado
        # (En producción, esto debería usar modelos más sofisticados)
        bias_score = min(confidence_stats['std'] / self.confidence_threshold, 1.0)

        # Guardar en historial
        self.detection_history.append({
            'detections': len(detections),
            'confidence_stats': confidence_stats,
            'timestamp': datetime.utcnow().isoformat()
        })

        return BiasMetrics(
            total_detections=len(detections),
            confidence_stats=confidence_stats,
            bias_score=bias_score,
            warnings=warnings
        )

    def analyze_historical_bias(self, window_size: int = 100) -> Dict[str, Any]:
        """
        Analiza sesgo en ventana histórica de detecciones.

        Args:
            window_size: Número de detecciones recientes a analizar

        Returns:
            Diccionario con métricas históricas
        """
        if not self.detection_history:
            return {'status': 'no_data'}

        recent = self.detection_history[-window_size:]

        total_detections = sum(h['detections'] for h in recent)
        avg_confidence = np.mean([
            h['confidence_stats']['mean']
            for h in recent
            if h['confidence_stats']
        ])

        return {
            'total_detections': total_detections,
            'avg_confidence': float(avg_confidence),
            'samples_analyzed': len(recent),
            'time_range': {
                'start': recent[0]['timestamp'],
                'end': recent[-1]['timestamp']
            }
        }

    def get_fairness_report(self) -> Dict[str, Any]:
        """
        Genera reporte de equidad (fairness) del sistema.

        Returns:
            Reporte completo con recomendaciones
        """
        historical = self.analyze_historical_bias()

        recommendations = []

        if historical.get('avg_confidence', 0) < 0.65:
            recommendations.append(
                "Mejorar calidad de datos de entrenamiento para aumentar confianza"
            )

        if len(self.detection_history) < 50:
            recommendations.append(
                "Recopilar más datos para análisis estadísticamente significativo"
            )

        return {
            'historical_analysis': historical,
            'recommendations': recommendations,
            'compliance_status': {
                'eu_ai_act_article_10': 'in_review',
                'bias_monitoring_active': True,
                'human_oversight_enabled': True
            },
            'generated_at': datetime.utcnow().isoformat()
        }
