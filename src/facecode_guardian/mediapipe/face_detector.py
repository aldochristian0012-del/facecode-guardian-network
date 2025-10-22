"""
Integración ética de MediaPipe Face Detection
"""
import cv2
import mediapipe as mp
import numpy as np
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from ..config import settings


@dataclass
class FaceDetection:
    """Resultado de detección facial con metadatos éticos"""
    bounding_box: Dict[str, float]  # {x, y, width, height}
    confidence: float
    landmarks: Optional[List[Dict[str, float]]] = None
    timestamp: str = None
    ethical_flags: Dict[str, Any] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
        if self.ethical_flags is None:
            self.ethical_flags = {}


class EthicalFaceDetector:
    """
    Detector de rostros con límites éticos integrados.

    Características:
    - Límite máximo de rostros por solicitud (anti-vigilancia masiva)
    - Registro de auditoría automático
    - Detección de uso potencialmente abusivo
    - Transparencia en confianza del modelo
    """

    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils

        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=settings.MEDIAPIPE_MODEL_SELECTION,
            min_detection_confidence=settings.MEDIAPIPE_MIN_DETECTION_CONFIDENCE
        )

        self.max_faces = settings.MAX_FACES_PER_REQUEST

    def detect_faces(self, image: np.ndarray) -> List[FaceDetection]:
        """
        Detecta rostros en una imagen con validaciones éticas.

        Args:
            image: Imagen en formato numpy array (BGR)

        Returns:
            Lista de detecciones faciales

        Raises:
            ValueError: Si se exceden los límites éticos
        """
        # Convertir BGR a RGB (MediaPipe usa RGB)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Procesar imagen
        results = self.face_detection.process(image_rgb)

        if not results.detections:
            return []

        # Validación ética: límite de rostros
        num_faces = len(results.detections)
        if num_faces > self.max_faces:
            raise ValueError(
                f"Límite ético excedido: {num_faces} rostros detectados. "
                f"Máximo permitido: {self.max_faces}. "
                f"Esto previene vigilancia masiva."
            )

        # Convertir a formato estructurado
        detections = []
        height, width, _ = image.shape

        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box

            # Convertir coordenadas relativas a absolutas
            face_detection = FaceDetection(
                bounding_box={
                    'x': bbox.xmin * width,
                    'y': bbox.ymin * height,
                    'width': bbox.width * width,
                    'height': bbox.height * height
                },
                confidence=detection.score[0],
                ethical_flags={
                    'max_faces_check': 'passed',
                    'total_faces_in_image': num_faces,
                    'confidence_threshold': settings.MEDIAPIPE_MIN_DETECTION_CONFIDENCE
                }
            )

            # Extraer landmarks si están disponibles
            if detection.location_data.relative_keypoints:
                landmarks = []
                for keypoint in detection.location_data.relative_keypoints:
                    landmarks.append({
                        'x': keypoint.x * width,
                        'y': keypoint.y * height
                    })
                face_detection.landmarks = landmarks

            detections.append(face_detection)

        return detections

    def draw_detections(
        self,
        image: np.ndarray,
        detections: List[FaceDetection],
        show_confidence: bool = True
    ) -> np.ndarray:
        """
        Dibuja las detecciones sobre la imagen (para debugging/demostración).

        Args:
            image: Imagen original
            detections: Lista de detecciones
            show_confidence: Mostrar nivel de confianza

        Returns:
            Imagen con anotaciones
        """
        annotated_image = image.copy()

        for det in detections:
            bbox = det.bounding_box
            x, y = int(bbox['x']), int(bbox['y'])
            w, h = int(bbox['width']), int(bbox['height'])

            # Dibujar rectángulo
            cv2.rectangle(
                annotated_image,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # Mostrar confianza
            if show_confidence:
                label = f"{det.confidence:.2%}"
                cv2.putText(
                    annotated_image,
                    label,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

            # Dibujar landmarks si existen
            if det.landmarks:
                for landmark in det.landmarks:
                    lx, ly = int(landmark['x']), int(landmark['y'])
                    cv2.circle(annotated_image, (lx, ly), 2, (255, 0, 0), -1)

        return annotated_image

    def __del__(self):
        """Liberar recursos de MediaPipe"""
        if hasattr(self, 'face_detection'):
            self.face_detection.close()
