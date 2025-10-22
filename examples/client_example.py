#!/usr/bin/env python3
"""
Ejemplo de cliente para FaceCode Guardian Network API
======================================================

Demuestra cómo usar la API de detección facial ética.
"""
import requests
import base64
import json
import time
from pathlib import Path


class FaceCodeGuardianClient:
    """Cliente para interactuar con FaceCode Guardian Network API"""

    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        self.base_url = base_url
        self.api_prefix = "/api/v1"
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def health_check(self) -> dict:
        """Verifica el estado de salud del sistema"""
        response = requests.get(f"{self.base_url}{self.api_prefix}/health")
        response.raise_for_status()
        return response.json()

    def detect_faces(
        self,
        image_path: str,
        require_human_approval: bool = True,
        user_id: str = None
    ) -> dict:
        """
        Detecta rostros en una imagen.

        Args:
            image_path: Ruta a la imagen
            require_human_approval: Si requiere aprobación humana
            user_id: ID del usuario solicitante

        Returns:
            Resultado de la detección
        """
        # Leer y codificar imagen
        with open(image_path, "rb") as f:
            image_data = f.read()
            image_base64 = base64.b64encode(image_data).decode()

        # Preparar request
        payload = {
            "image_base64": f"data:image/jpeg;base64,{image_base64}",
            "require_human_approval": require_human_approval,
            "user_id": user_id
        }

        # Enviar request
        response = requests.post(
            f"{self.base_url}{self.api_prefix}/detect",
            json=payload,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def approve_request(
        self,
        request_id: str,
        approved: bool,
        approver_id: str,
        reason: str = None,
        notes: str = None
    ) -> dict:
        """
        Aprueba o veta una solicitud (Botón Ético Rojo).

        Args:
            request_id: ID de la solicitud
            approved: True para aprobar, False para vetar
            approver_id: ID del aprobador
            reason: Razón del veto (si approved=False)
            notes: Notas adicionales

        Returns:
            Estado de la aprobación
        """
        payload = {
            "request_id": request_id,
            "approved": approved,
            "approver_id": approver_id,
            "reason": reason,
            "notes": notes
        }

        response = requests.post(
            f"{self.base_url}{self.api_prefix}/approve",
            json=payload,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_approval_status(self, request_id: str) -> dict:
        """Consulta el estado de una solicitud de aprobación"""
        response = requests.get(
            f"{self.base_url}{self.api_prefix}/approval/{request_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_red_button_stats(self) -> dict:
        """Obtiene estadísticas del Botón Ético Rojo"""
        response = requests.get(
            f"{self.base_url}{self.api_prefix}/red-button/stats",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_bias_report(self) -> dict:
        """Obtiene reporte de equidad del sistema"""
        response = requests.get(
            f"{self.base_url}{self.api_prefix}/bias/report",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()


def main():
    """Ejemplo de uso del cliente"""
    # Crear cliente
    client = FaceCodeGuardianClient(base_url="http://localhost:8000")

    print("🛡️  FaceCode Guardian Network - Cliente de Ejemplo\n")

    # 1. Health check
    print("1. Verificando salud del sistema...")
    try:
        health = client.health_check()
        print(f"   ✅ Sistema: {health['status']}")
        print(f"   📦 Versión: {health['version']}")
        print(f"   🔴 Botón Ético: {'Activo' if health['ethical_features']['red_button_enabled'] else 'Inactivo'}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return

    # 2. Detectar rostros (ejemplo con imagen ficticia)
    print("\n2. Detectando rostros en imagen...")
    print("   ⚠️  Necesitas proporcionar una ruta de imagen válida")
    print("   Ejemplo: result = client.detect_faces('foto.jpg', user_id='user-123')")

    # Ejemplo de código (comentado porque necesita imagen real)
    """
    try:
        result = client.detect_faces(
            image_path="path/to/your/image.jpg",
            require_human_approval=True,
            user_id="user-123"
        )

        print(f"   ✅ Rostros detectados: {len(result['detections'])}")
        print(f"   📊 Bias score: {result['bias_metrics']['bias_score']:.2f}")

        if result['human_approval_required']:
            print(f"   🔴 Requiere aprobación humana")
            print(f"   🆔 Request ID: {result['approval_request_id']}")

            # Simular aprobación humana
            approval = client.approve_request(
                request_id=result['approval_request_id'],
                approved=True,
                approver_id="admin-001",
                notes="Uso legítimo confirmado"
            )
            print(f"   ✅ Solicitud aprobada: {approval['status']}")

    except Exception as e:
        print(f"   ❌ Error: {e}")
    """

    # 3. Estadísticas del Botón Ético Rojo
    print("\n3. Estadísticas del Botón Ético Rojo...")
    try:
        stats = client.get_red_button_stats()
        print(f"   📊 Total solicitudes: {stats['total_requests']}")
        print(f"   ✅ Aprobadas: {stats['approved']}")
        print(f"   ❌ Vetadas: {stats['vetoed']}")
        print(f"   📈 Tasa de aprobación: {stats['approval_rate']:.1%}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # 4. Reporte de bias
    print("\n4. Reporte de equidad (bias)...")
    try:
        report = client.get_bias_report()
        print(f"   📋 Compliance status: {report['compliance_status']['eu_ai_act_article_10']}")
        print(f"   🔍 Monitoreo de bias: {'Activo' if report['compliance_status']['bias_monitoring_active'] else 'Inactivo'}")
        if report['recommendations']:
            print(f"   💡 Recomendaciones: {len(report['recommendations'])}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n" + "="*60)
    print("© 2025 Christian - Fundador de FaceCode®")
    print("="*60)


if __name__ == "__main__":
    main()
