"""
Tests unitarios para el Botón Ético Rojo
"""
import pytest
from datetime import datetime
from facecode_guardian.ethics import RedButtonManager, VetoReason


class TestRedButton:
    """Tests para el sistema de veto humano"""

    def setup_method(self):
        """Configurar test"""
        self.red_button = RedButtonManager(timeout_seconds=5)

    def test_request_approval(self):
        """Test: Crear solicitud de aprobación"""
        request = self.red_button.request_approval(
            request_id="test-001",
            operation="face_detection",
            context={"num_faces": 3}
        )

        assert request.request_id == "test-001"
        assert request.operation == "face_detection"
        assert request.approved is None
        assert "test-001" in self.red_button.pending_requests

    def test_approve_request(self):
        """Test: Aprobar una solicitud"""
        # Crear solicitud
        self.red_button.request_approval(
            request_id="test-002",
            operation="face_detection",
            context={}
        )

        # Aprobar
        success = self.red_button.approve(
            request_id="test-002",
            approver_id="admin-001",
            notes="Looks good"
        )

        assert success is True
        assert "test-002" not in self.red_button.pending_requests
        assert len(self.red_button.approval_history) == 1
        assert self.red_button.approval_history[0].approved is True

    def test_veto_request(self):
        """Test: Vetar una solicitud"""
        # Crear solicitud
        self.red_button.request_approval(
            request_id="test-003",
            operation="face_detection",
            context={}
        )

        # Vetar
        success = self.red_button.veto(
            request_id="test-003",
            reason=VetoReason.ETHICAL_CONCERN,
            approver_id="admin-001",
            notes="Privacy violation"
        )

        assert success is True
        assert "test-003" not in self.red_button.pending_requests
        assert len(self.red_button.approval_history) == 1
        assert self.red_button.approval_history[0].approved is False
        assert self.red_button.approval_history[0].veto_reason == VetoReason.ETHICAL_CONCERN

    def test_approval_rate(self):
        """Test: Calcular tasa de aprobación"""
        # Crear y aprobar 3 solicitudes
        for i in range(3):
            self.red_button.request_approval(
                request_id=f"test-approve-{i}",
                operation="test",
                context={}
            )
            self.red_button.approve(f"test-approve-{i}", "admin", "ok")

        # Crear y vetar 1 solicitud
        self.red_button.request_approval(
            request_id="test-veto",
            operation="test",
            context={}
        )
        self.red_button.veto("test-veto", VetoReason.OTHER, "admin", "no")

        # Calcular tasa
        rate = self.red_button.get_approval_rate()
        assert rate == 0.75  # 3/4 = 75%

    def test_statistics(self):
        """Test: Obtener estadísticas"""
        # Crear solicitudes
        self.red_button.request_approval("stat-1", "op", {})
        self.red_button.approve("stat-1", "admin")

        self.red_button.request_approval("stat-2", "op", {})
        self.red_button.veto("stat-2", VetoReason.BIAS_DETECTED, "admin")

        stats = self.red_button.get_statistics()

        assert stats['total_requests'] == 2
        assert stats['approved'] == 1
        assert stats['vetoed'] == 1
        assert stats['approval_rate'] == 0.5
        assert 'veto_reasons' in stats

    def test_nonexistent_request(self):
        """Test: Intentar aprobar solicitud que no existe"""
        success = self.red_button.approve("nonexistent", "admin")
        assert success is False
