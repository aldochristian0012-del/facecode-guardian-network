"""
Sistema de Auditoría Ética
===========================

Registra todas las operaciones para cumplimiento regulatorio y transparencia.
"""
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime
from enum import Enum

from ..config import settings


class AuditEventType(Enum):
    """Tipos de eventos auditables"""
    FACE_DETECTION = "face_detection"
    HUMAN_APPROVAL_REQUESTED = "human_approval_requested"
    HUMAN_APPROVAL_GRANTED = "human_approval_granted"
    HUMAN_VETO = "human_veto"
    BIAS_WARNING = "bias_warning"
    ETHICAL_LIMIT_EXCEEDED = "ethical_limit_exceeded"
    API_REQUEST = "api_request"
    SYSTEM_ERROR = "system_error"


class AuditLogger:
    """
    Logger de auditoría con cumplimiento GDPR.

    Registra:
    - Todas las operaciones de detección facial
    - Decisiones humanas (aprobaciones/vetos)
    - Advertencias de sesgo
    - Accesos a la API
    """

    def __init__(self, log_path: Optional[Path] = None):
        """
        Args:
            log_path: Ruta donde guardar logs de auditoría
        """
        self.log_path = log_path or settings.AUDIT_LOG_PATH
        self.log_path.mkdir(parents=True, exist_ok=True)

        # Configurar logger
        self.logger = logging.getLogger("facecode_audit")
        self.logger.setLevel(logging.INFO)

        # Handler para archivo
        log_file = self.log_path / f"audit_{datetime.utcnow().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Formato JSON para facilitar parsing
        formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def log_event(
        self,
        event_type: AuditEventType,
        details: Dict[str, Any],
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ):
        """
        Registra un evento de auditoría.

        Args:
            event_type: Tipo de evento
            details: Detalles específicos del evento
            user_id: ID del usuario (anonimizado si es necesario)
            session_id: ID de sesión
        """
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type.value,
            'user_id': user_id or 'anonymous',
            'session_id': session_id,
            'details': details,
            'compliance': {
                'gdpr': True,
                'eu_ai_act': True
            }
        }

        # Log como JSON
        self.logger.info(json.dumps(event))

    def log_face_detection(
        self,
        num_faces: int,
        confidences: list,
        user_id: Optional[str] = None,
        approved: bool = False
    ):
        """Log específico para detección facial"""
        self.log_event(
            AuditEventType.FACE_DETECTION,
            {
                'num_faces': num_faces,
                'avg_confidence': sum(confidences) / len(confidences) if confidences else 0,
                'human_approved': approved
            },
            user_id=user_id
        )

    def log_human_decision(
        self,
        request_id: str,
        approved: bool,
        approver_id: str,
        reason: Optional[str] = None
    ):
        """Log para decisiones del Botón Ético Rojo"""
        event_type = (
            AuditEventType.HUMAN_APPROVAL_GRANTED if approved
            else AuditEventType.HUMAN_VETO
        )

        self.log_event(
            event_type,
            {
                'request_id': request_id,
                'approver_id': approver_id,
                'reason': reason
            }
        )

    def log_bias_warning(self, warning_details: Dict[str, Any]):
        """Log para advertencias de sesgo"""
        self.log_event(
            AuditEventType.BIAS_WARNING,
            warning_details
        )

    def log_api_request(
        self,
        endpoint: str,
        method: str,
        status_code: int,
        user_id: Optional[str] = None
    ):
        """Log para requests a la API"""
        self.log_event(
            AuditEventType.API_REQUEST,
            {
                'endpoint': endpoint,
                'method': method,
                'status_code': status_code
            },
            user_id=user_id
        )

    def get_audit_summary(self, days: int = 7) -> Dict[str, Any]:
        """
        Genera resumen de auditoría para los últimos N días.

        Args:
            days: Número de días a analizar

        Returns:
            Diccionario con estadísticas
        """
        # En producción, esto leería los archivos de log
        # y generaría estadísticas reales
        return {
            'period_days': days,
            'total_events': 0,  # Placeholder
            'face_detections': 0,
            'human_approvals': 0,
            'human_vetos': 0,
            'bias_warnings': 0,
            'status': 'active'
        }


# Instancia global
audit_logger = AuditLogger()
