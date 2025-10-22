"""
Tests unitarios para el detector de bias
"""
import pytest
from facecode_guardian.ethics import BiasDetector
from facecode_guardian.mediapipe import FaceDetection


class TestBiasDetector:
    """Tests para detección de sesgos"""

    def setup_method(self):
        """Configurar test"""
        self.detector = BiasDetector(confidence_threshold=0.2)

    def test_analyze_empty_detections(self):
        """Test: Analizar lista vacía"""
        metrics = self.detector.analyze_detections([])

        assert metrics.total_detections == 0
        assert len(metrics.warnings) > 0
        assert "No detections" in metrics.warnings[0]

    def test_analyze_normal_detections(self):
        """Test: Analizar detecciones normales"""
        # Crear detecciones mock
        detections = [
            FaceDetection(
                bounding_box={'x': 10, 'y': 10, 'width': 100, 'height': 100},
                confidence=0.85
            ),
            FaceDetection(
                bounding_box={'x': 200, 'y': 10, 'width': 100, 'height': 100},
                confidence=0.90
            )
        ]

        metrics = self.detector.analyze_detections(detections)

        assert metrics.total_detections == 2
        assert 'mean' in metrics.confidence_stats
        assert metrics.confidence_stats['mean'] >= 0.85

    def test_high_variance_warning(self):
        """Test: Detectar alta varianza en confianzas"""
        detections = [
            FaceDetection(
                bounding_box={'x': 10, 'y': 10, 'width': 100, 'height': 100},
                confidence=0.3
            ),
            FaceDetection(
                bounding_box={'x': 200, 'y': 10, 'width': 100, 'height': 100},
                confidence=0.95
            )
        ]

        metrics = self.detector.analyze_detections(detections)

        # Debe generar warning por alta varianza
        assert any('varianza' in w.lower() for w in metrics.warnings)
        assert metrics.bias_score > 0

    def test_low_confidence_warning(self):
        """Test: Detectar confianzas bajas"""
        detections = [
            FaceDetection(
                bounding_box={'x': 10, 'y': 10, 'width': 100, 'height': 100},
                confidence=0.4
            ),
            FaceDetection(
                bounding_box={'x': 200, 'y': 10, 'width': 100, 'height': 100},
                confidence=0.5
            )
        ]

        metrics = self.detector.analyze_detections(detections)

        # Debe generar warning por baja confianza
        assert any('baja' in w.lower() for w in metrics.warnings)

    def test_mass_surveillance_warning(self):
        """Test: Detectar posible vigilancia masiva"""
        # Crear muchas detecciones
        detections = [
            FaceDetection(
                bounding_box={'x': i*50, 'y': 10, 'width': 40, 'height': 40},
                confidence=0.8
            )
            for i in range(10)
        ]

        metrics = self.detector.analyze_detections(detections)

        # Debe generar warning por alto número de detecciones
        assert any('alto número' in w.lower() or 'vigilancia' in w.lower() for w in metrics.warnings)

    def test_fairness_report(self):
        """Test: Generar reporte de equidad"""
        report = self.detector.get_fairness_report()

        assert 'historical_analysis' in report
        assert 'recommendations' in report
        assert 'compliance_status' in report
        assert report['compliance_status']['bias_monitoring_active'] is True
