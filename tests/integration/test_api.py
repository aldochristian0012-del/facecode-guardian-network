"""
Tests de integración para la API
"""
import pytest
import base64
import io
from PIL import Image
import numpy as np
from fastapi.testclient import TestClient

from facecode_guardian.main import app

client = TestClient(app)


def create_test_image(width=640, height=480):
    """Crea una imagen de prueba en base64"""
    # Crear imagen simple
    image = Image.new('RGB', (width, height), color='white')

    # Convertir a base64
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/jpeg;base64,{image_base64}"


class TestAPIEndpoints:
    """Tests de integración para endpoints de la API"""

    def test_root_endpoint(self):
        """Test: Endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200
        assert "FaceCode Guardian Network" in response.text

    def test_health_endpoint(self):
        """Test: Endpoint de salud"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200

        data = response.json()
        assert data['status'] == 'healthy'
        assert 'version' in data
        assert 'ethical_features' in data
        assert 'compliance' in data

    def test_detect_faces_endpoint(self):
        """Test: Endpoint de detección facial"""
        image_base64 = create_test_image()

        response = client.post(
            "/api/v1/detect",
            json={
                "image_base64": image_base64,
                "require_human_approval": False,
                "user_id": "test-user"
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert 'success' in data
        assert 'detections' in data
        assert 'bias_metrics' in data
        assert isinstance(data['detections'], list)

    def test_red_button_stats(self):
        """Test: Endpoint de estadísticas del Botón Ético Rojo"""
        response = client.get("/api/v1/red-button/stats")
        assert response.status_code == 200

        data = response.json()
        assert 'total_requests' in data
        assert 'approved' in data
        assert 'vetoed' in data
        assert 'approval_rate' in data

    def test_bias_report(self):
        """Test: Endpoint de reporte de bias"""
        response = client.get("/api/v1/bias/report")
        assert response.status_code == 200

        data = response.json()
        assert 'compliance_status' in data
        assert 'recommendations' in data

    def test_audit_summary(self):
        """Test: Endpoint de resumen de auditoría"""
        response = client.get("/api/v1/audit/summary?days=7")
        assert response.status_code == 200

        data = response.json()
        assert 'period_days' in data

    def test_invalid_image(self):
        """Test: Enviar imagen inválida"""
        response = client.post(
            "/api/v1/detect",
            json={
                "image_base64": "invalid_base64",
                "require_human_approval": False
            }
        )

        assert response.status_code == 400

    def test_approval_nonexistent_request(self):
        """Test: Intentar aprobar solicitud inexistente"""
        response = client.post(
            "/api/v1/approve",
            json={
                "request_id": "nonexistent-123",
                "approved": True,
                "approver_id": "test-admin"
            }
        )

        assert response.status_code == 404


class TestEthicalLimits:
    """Tests para límites éticos"""

    def test_human_approval_workflow(self):
        """Test: Flujo completo de aprobación humana"""
        image_base64 = create_test_image()

        # 1. Solicitar detección con aprobación humana
        detect_response = client.post(
            "/api/v1/detect",
            json={
                "image_base64": image_base64,
                "require_human_approval": True,
                "user_id": "test-user"
            }
        )

        assert detect_response.status_code == 200
        detect_data = detect_response.json()

        # Si se generó request de aprobación
        if detect_data.get('approval_request_id'):
            request_id = detect_data['approval_request_id']

            # 2. Verificar estado pendiente
            status_response = client.get(f"/api/v1/approval/{request_id}")
            assert status_response.status_code == 200
            assert status_response.json()['status'] == 'pending'

            # 3. Aprobar
            approve_response = client.post(
                "/api/v1/approve",
                json={
                    "request_id": request_id,
                    "approved": True,
                    "approver_id": "test-admin",
                    "notes": "Test approval"
                }
            )

            assert approve_response.status_code == 200
            assert approve_response.json()['status'] == 'approved'


class TestCompliance:
    """Tests de cumplimiento regulatorio"""

    def test_gdpr_compliance(self):
        """Test: Verificar flags de cumplimiento GDPR"""
        response = client.get("/api/v1/health")
        data = response.json()

        assert data['compliance']['gdpr_compliant'] is True

    def test_eu_ai_act_compliance(self):
        """Test: Verificar cumplimiento AI Act"""
        response = client.get("/api/v1/health")
        data = response.json()

        assert data['compliance']['eu_ai_act_compliant'] is True
        assert data['ethical_features']['red_button_enabled'] is True
        assert data['ethical_features']['bias_detection_enabled'] is True
