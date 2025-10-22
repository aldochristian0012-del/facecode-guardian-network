"""
Configuración del FaceCode Guardian Network
"""
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    """Configuración de la aplicación con validaciones éticas"""

    # API Settings
    API_TITLE: str = "FaceCode Guardian Network API"
    API_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4

    # Security
    API_KEY: Optional[str] = None
    CORS_ORIGINS: list = ["*"]

    # MediaPipe Settings
    MEDIAPIPE_MODEL_SELECTION: int = 0  # 0=frontal, 1=full range
    MEDIAPIPE_MIN_DETECTION_CONFIDENCE: float = 0.5

    # Ethical Limits
    MAX_FACES_PER_REQUEST: int = 10  # Límite anti-vigilancia masiva
    MAX_REQUESTS_PER_MINUTE: int = 30
    REQUIRE_HUMAN_APPROVAL: bool = True  # Botón Ético Rojo activo
    ENABLE_BIAS_DETECTION: bool = True

    # Audit Settings
    AUDIT_LOG_PATH: Path = Path("./logs/audit")
    ENABLE_AUDIT_LOG: bool = True
    LOG_RETENTION_DAYS: int = 90  # Cumplimiento GDPR

    # Database (opcional para persistencia)
    DATABASE_URL: Optional[str] = None

    # Compliance
    GDPR_COMPLIANT: bool = True
    EU_AI_ACT_COMPLIANT: bool = True
    EAA_COMPLIANT: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
