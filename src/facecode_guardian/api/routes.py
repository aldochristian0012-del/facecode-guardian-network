"""
Rutas de la API REST
"""
import base64
import io
import uuid
from typing import List
import numpy as np
from PIL import Image
import cv2

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from .models import (
    FaceDetectionRequest,
    FaceDetectionResponse,
    FaceDetectionResult,
    BoundingBox,
    Landmark,
    EthicalFlags,
    BiasMetricsResponse,
    ApprovalDecisionRequest,
    ApprovalStatusResponse,
    SystemHealthResponse,
    RedButtonStatsResponse
)
from ..mediapipe import EthicalFaceDetector
from ..ethics import red_button, VetoReason, BiasDetector
from ..audit import audit_logger, AuditEventType
from ..config import settings

router = APIRouter()

# Instancias globales
face_detector = EthicalFaceDetector()
bias_detector = BiasDetector()


def decode_image(base64_string: str) -> np.ndarray:
    """Decodifica imagen base64 a numpy array"""
    try:
        # Remover prefijo si existe
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]

        # Decodificar
        image_bytes = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_bytes))

        # Convertir a numpy array (BGR para OpenCV)
        image_np = np.array(image)
        if len(image_np.shape) == 2:  # Grayscale
            image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)
        elif image_np.shape[2] == 4:  # RGBA
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)
        elif image_np.shape[2] == 3:  # RGB
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        return image_np
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error decoding image: {str(e)}")


@router.post("/detect", response_model=FaceDetectionResponse)
async def detect_faces(request: FaceDetectionRequest):
    """
    Detecta rostros en una imagen con validaciones éticas.

    **Características:**
    - Límite máximo de rostros (anti-vigilancia masiva)
    - Botón Ético Rojo (requiere aprobación humana)
    - Detección automática de bias
    - Auditoría completa

    **Cumplimiento:**
    - EU AI Act (Alto Riesgo - Artículo 6)
    - GDPR (Datos biométricos)
    - EAA (Accesibilidad)
    """
    try:
        # Decodificar imagen
        image = decode_image(request.image_base64)

        # Detectar rostros
        detections = face_detector.detect_faces(image)

        # Analizar bias
        bias_metrics = bias_detector.analyze_detections(detections)

        # Log bias warnings si existen
        if bias_metrics.warnings:
            audit_logger.log_bias_warning({
                'warnings': bias_metrics.warnings,
                'bias_score': bias_metrics.bias_score
            })

        # Convertir a formato response
        detection_results = []
        for det in detections:
            landmarks = None
            if det.landmarks:
                landmarks = [Landmark(x=l['x'], y=l['y']) for l in det.landmarks]

            detection_results.append(FaceDetectionResult(
                bounding_box=BoundingBox(**det.bounding_box),
                confidence=det.confidence,
                landmarks=landmarks,
                timestamp=det.timestamp,
                ethical_flags=EthicalFlags(**det.ethical_flags)
            ))

        # Verificar si requiere aprobación humana
        approval_request_id = None
        human_approval_required = (
            request.require_human_approval and
            settings.REQUIRE_HUMAN_APPROVAL and
            len(detections) > 0
        )

        if human_approval_required:
            # Crear solicitud de aprobación
            approval_request_id = str(uuid.uuid4())
            red_button.request_approval(
                request_id=approval_request_id,
                operation="face_detection",
                context={
                    'num_faces': len(detections),
                    'avg_confidence': bias_metrics.confidence_stats.get('mean', 0),
                    'user_id': request.user_id
                }
            )

            audit_logger.log_event(
                AuditEventType.HUMAN_APPROVAL_REQUESTED,
                {
                    'request_id': approval_request_id,
                    'num_faces': len(detections)
                },
                user_id=request.user_id
            )

        # Log detección
        audit_logger.log_face_detection(
            num_faces=len(detections),
            confidences=[d.confidence for d in detections],
            user_id=request.user_id,
            approved=not human_approval_required
        )

        return FaceDetectionResponse(
            success=True,
            detections=detection_results,
            bias_metrics=BiasMetricsResponse(
                total_detections=bias_metrics.total_detections,
                confidence_stats=bias_metrics.confidence_stats,
                bias_score=bias_metrics.bias_score,
                warnings=bias_metrics.warnings,
                timestamp=bias_metrics.timestamp
            ),
            human_approval_required=human_approval_required,
            approval_request_id=approval_request_id,
            message=(
                f"Detected {len(detections)} face(s). "
                f"{'Human approval required.' if human_approval_required else 'Approved.'}"
            )
        )

    except ValueError as e:
        # Límite ético excedido
        audit_logger.log_event(
            AuditEventType.ETHICAL_LIMIT_EXCEEDED,
            {'error': str(e)},
            user_id=request.user_id
        )
        raise HTTPException(status_code=403, detail=str(e))

    except Exception as e:
        audit_logger.log_event(
            AuditEventType.SYSTEM_ERROR,
            {'error': str(e), 'endpoint': '/detect'},
            user_id=request.user_id
        )
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/approve", response_model=ApprovalStatusResponse)
async def approve_request(decision: ApprovalDecisionRequest):
    """
    Aprueba o veta una solicitud de detección facial (Botón Ético Rojo).

    **Uso:**
    - approved=true: Aprobar la operación
    - approved=false: Vetar la operación (requiere reason)
    """
    success = False

    if decision.approved:
        success = red_button.approve(
            decision.request_id,
            decision.approver_id,
            decision.notes
        )
        status = "approved" if success else "not_found"
    else:
        # Veto
        reason = VetoReason.ETHICAL_CONCERN
        if decision.reason:
            try:
                reason = VetoReason(decision.reason)
            except ValueError:
                reason = VetoReason.OTHER

        success = red_button.veto(
            decision.request_id,
            reason,
            decision.approver_id,
            decision.notes
        )
        status = "vetoed" if success else "not_found"

    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Request {decision.request_id} not found or expired"
        )

    # Log decisión humana
    audit_logger.log_human_decision(
        request_id=decision.request_id,
        approved=decision.approved,
        approver_id=decision.approver_id,
        reason=decision.reason
    )

    return ApprovalStatusResponse(
        request_id=decision.request_id,
        status=status,
        approved=decision.approved,
        approver_id=decision.approver_id,
        timestamp=decision.notes or ""
    )


@router.get("/approval/{request_id}", response_model=ApprovalStatusResponse)
async def get_approval_status(request_id: str):
    """
    Consulta el estado de una solicitud de aprobación.
    """
    # Buscar en pendientes
    if request_id in red_button.pending_requests:
        req = red_button.pending_requests[request_id]
        return ApprovalStatusResponse(
            request_id=request_id,
            status="pending",
            timestamp=req.timestamp.isoformat()
        )

    # Buscar en historial
    for req in red_button.approval_history:
        if req.request_id == request_id:
            status = "approved" if req.approved else "vetoed"
            return ApprovalStatusResponse(
                request_id=request_id,
                status=status,
                approved=req.approved,
                approver_id=req.approver_id,
                timestamp=req.timestamp.isoformat()
            )

    raise HTTPException(status_code=404, detail="Request not found")


@router.get("/health", response_model=SystemHealthResponse)
async def health_check():
    """
    Estado de salud del sistema y estadísticas éticas.
    """
    stats = red_button.get_statistics()

    return SystemHealthResponse(
        status="healthy",
        version=settings.API_VERSION,
        ethical_features={
            'red_button_enabled': settings.REQUIRE_HUMAN_APPROVAL,
            'bias_detection_enabled': settings.ENABLE_BIAS_DETECTION,
            'audit_logging_enabled': settings.ENABLE_AUDIT_LOG
        },
        compliance={
            'gdpr_compliant': settings.GDPR_COMPLIANT,
            'eu_ai_act_compliant': settings.EU_AI_ACT_COMPLIANT,
            'eaa_compliant': settings.EAA_COMPLIANT
        },
        statistics=stats
    )


@router.get("/red-button/stats", response_model=RedButtonStatsResponse)
async def red_button_stats():
    """
    Estadísticas del Botón Ético Rojo.
    """
    stats = red_button.get_statistics()

    return RedButtonStatsResponse(**stats)


@router.get("/bias/report")
async def bias_report():
    """
    Reporte de equidad (fairness) del sistema.
    """
    return bias_detector.get_fairness_report()


@router.get("/audit/summary")
async def audit_summary(days: int = 7):
    """
    Resumen de auditoría para los últimos N días.
    """
    return audit_logger.get_audit_summary(days=days)
