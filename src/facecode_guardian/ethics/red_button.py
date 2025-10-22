"""
Botón Ético Rojo - Sistema de Veto Humano
==========================================

Implementa el concepto de "human-in-the-loop" obligatorio para operaciones sensibles.
"""
import time
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import asyncio


class VetoReason(Enum):
    """Razones posibles para veto humano"""
    ETHICAL_CONCERN = "ethical_concern"
    PRIVACY_VIOLATION = "privacy_violation"
    BIAS_DETECTED = "bias_detected"
    UNAUTHORIZED_USE = "unauthorized_use"
    DATA_QUALITY_ISSUE = "data_quality_issue"
    OTHER = "other"


@dataclass
class HumanApprovalRequest:
    """Solicitud de aprobación humana"""
    request_id: str
    operation: str
    context: Dict[str, Any]
    timestamp: datetime
    expires_at: datetime
    approved: Optional[bool] = None
    veto_reason: Optional[VetoReason] = None
    approver_id: Optional[str] = None
    notes: Optional[str] = None


class RedButtonManager:
    """
    Gestor del Botón Ético Rojo.

    Permite a humanos vetar operaciones en tiempo real y mantiene
    un registro de todas las decisiones tomadas.
    """

    def __init__(self, timeout_seconds: int = 30):
        """
        Args:
            timeout_seconds: Tiempo máximo de espera para aprobación humana
        """
        self.timeout_seconds = timeout_seconds
        self.pending_requests: Dict[str, HumanApprovalRequest] = {}
        self.approval_history: list = []

    def request_approval(
        self,
        request_id: str,
        operation: str,
        context: Dict[str, Any]
    ) -> HumanApprovalRequest:
        """
        Crea una solicitud de aprobación humana.

        Args:
            request_id: ID único de la solicitud
            operation: Nombre de la operación que requiere aprobación
            context: Contexto adicional para la decisión

        Returns:
            HumanApprovalRequest creada
        """
        now = datetime.utcnow()
        request = HumanApprovalRequest(
            request_id=request_id,
            operation=operation,
            context=context,
            timestamp=now,
            expires_at=now + timedelta(seconds=self.timeout_seconds)
        )

        self.pending_requests[request_id] = request
        return request

    def approve(
        self,
        request_id: str,
        approver_id: str,
        notes: Optional[str] = None
    ) -> bool:
        """
        Aprueba una solicitud pendiente.

        Args:
            request_id: ID de la solicitud
            approver_id: ID del aprobador humano
            notes: Notas opcionales

        Returns:
            True si se aprobó exitosamente
        """
        if request_id not in self.pending_requests:
            return False

        request = self.pending_requests[request_id]

        # Verificar expiración
        if datetime.utcnow() > request.expires_at:
            self.veto(request_id, VetoReason.OTHER, approver_id, "Timeout expired")
            return False

        request.approved = True
        request.approver_id = approver_id
        request.notes = notes

        # Mover a historial
        self.approval_history.append(request)
        del self.pending_requests[request_id]

        return True

    def veto(
        self,
        request_id: str,
        reason: VetoReason,
        approver_id: str,
        notes: Optional[str] = None
    ) -> bool:
        """
        Veta (rechaza) una solicitud.

        Args:
            request_id: ID de la solicitud
            reason: Razón del veto
            approver_id: ID del persona que vetó
            notes: Notas adicionales

        Returns:
            True si se vetó exitosamente
        """
        if request_id not in self.pending_requests:
            return False

        request = self.pending_requests[request_id]
        request.approved = False
        request.veto_reason = reason
        request.approver_id = approver_id
        request.notes = notes

        # Mover a historial
        self.approval_history.append(request)
        del self.pending_requests[request_id]

        return True

    async def wait_for_approval(
        self,
        request_id: str,
        poll_interval: float = 0.5
    ) -> bool:
        """
        Espera (de forma asíncrona) la aprobación o rechazo.

        Args:
            request_id: ID de la solicitud
            poll_interval: Intervalo de polling en segundos

        Returns:
            True si fue aprobado, False si fue vetado o expiró
        """
        start_time = time.time()

        while request_id in self.pending_requests:
            # Verificar timeout
            if time.time() - start_time > self.timeout_seconds:
                self.veto(
                    request_id,
                    VetoReason.OTHER,
                    "system",
                    "Timeout: No human approval received"
                )
                return False

            await asyncio.sleep(poll_interval)

        # Buscar en historial
        for req in self.approval_history:
            if req.request_id == request_id:
                return req.approved is True

        return False

    def get_pending_count(self) -> int:
        """Retorna el número de solicitudes pendientes"""
        return len(self.pending_requests)

    def get_approval_rate(self) -> float:
        """
        Calcula la tasa de aprobación histórica.

        Returns:
            Porcentaje de solicitudes aprobadas (0.0 - 1.0)
        """
        if not self.approval_history:
            return 0.0

        approved = sum(1 for req in self.approval_history if req.approved)
        return approved / len(self.approval_history)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estadísticas del uso del Botón Ético Rojo.

        Returns:
            Diccionario con métricas
        """
        total = len(self.approval_history)
        approved = sum(1 for req in self.approval_history if req.approved)
        vetoed = total - approved

        veto_reasons = {}
        for req in self.approval_history:
            if req.veto_reason:
                reason = req.veto_reason.value
                veto_reasons[reason] = veto_reasons.get(reason, 0) + 1

        return {
            'total_requests': total,
            'approved': approved,
            'vetoed': vetoed,
            'approval_rate': self.get_approval_rate(),
            'pending': self.get_pending_count(),
            'veto_reasons': veto_reasons
        }


# Instancia global (singleton)
red_button = RedButtonManager()
