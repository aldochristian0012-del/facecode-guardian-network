"""
Modelos Pydantic para la API
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


# Request Models
class FaceDetectionRequest(BaseModel):
    """Request para detección facial"""
    image_base64: str = Field(..., description="Imagen codificada en base64")
    require_human_approval: bool = Field(
        default=True,
        description="Si requiere aprobación humana (Botón Ético Rojo)"
    )
    user_id: Optional[str] = Field(None, description="ID del usuario solicitante")
    session_id: Optional[str] = Field(None, description="ID de sesión")


class ApprovalDecisionRequest(BaseModel):
    """Request para aprobar/vetar una detección"""
    request_id: str
    approved: bool
    approver_id: str
    reason: Optional[str] = None
    notes: Optional[str] = None


# Response Models
class BoundingBox(BaseModel):
    """Coordenadas de bounding box"""
    x: float
    y: float
    width: float
    height: float


class Landmark(BaseModel):
    """Punto de referencia facial"""
    x: float
    y: float


class EthicalFlags(BaseModel):
    """Flags éticos de validación"""
    max_faces_check: str
    total_faces_in_image: int
    confidence_threshold: float


class FaceDetectionResult(BaseModel):
    """Resultado de una detección facial individual"""
    bounding_box: BoundingBox
    confidence: float
    landmarks: Optional[List[Landmark]] = None
    timestamp: str
    ethical_flags: EthicalFlags


class BiasMetricsResponse(BaseModel):
    """Métricas de sesgo"""
    total_detections: int
    confidence_stats: Dict[str, float]
    bias_score: float
    warnings: List[str]
    timestamp: str


class FaceDetectionResponse(BaseModel):
    """Response completa de detección facial"""
    success: bool
    detections: List[FaceDetectionResult]
    bias_metrics: BiasMetricsResponse
    human_approval_required: bool
    approval_request_id: Optional[str] = None
    message: Optional[str] = None


class ApprovalStatusResponse(BaseModel):
    """Estado de una solicitud de aprobación"""
    request_id: str
    status: str  # 'pending', 'approved', 'vetoed', 'expired'
    approved: Optional[bool] = None
    approver_id: Optional[str] = None
    timestamp: str


class SystemHealthResponse(BaseModel):
    """Estado de salud del sistema"""
    status: str
    version: str
    ethical_features: Dict[str, bool]
    compliance: Dict[str, bool]
    statistics: Dict[str, Any]


class RedButtonStatsResponse(BaseModel):
    """Estadísticas del Botón Ético Rojo"""
    total_requests: int
    approved: int
    vetoed: int
    approval_rate: float
    pending: int
    veto_reasons: Dict[str, int]
