# FaceCode Guardian Network - Production Dockerfile
# ==================================================

FROM python:3.11-slim

LABEL maintainer="Christian - Fundador de FaceCode®"
LABEL description="Sistema de reconocimiento facial ético con cumplimiento del AI Act"

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema para OpenCV y MediaPipe
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY src/ /app/src/
COPY docs/ /app/docs/
COPY diagrams/ /app/diagrams/

# Crear directorios para logs
RUN mkdir -p /app/logs/audit

# Variables de entorno por defecto
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8000
ENV PYTHONPATH=/app

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/v1/health')"

# Comando de inicio
CMD ["python", "-m", "uvicorn", "src.facecode_guardian.main:app", "--host", "0.0.0.0", "--port", "8000"]
