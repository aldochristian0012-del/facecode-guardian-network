# Inicio Rápido - FaceCode Guardian Network

## Instalación Local

### Prerequisitos
- Python 3.9+
- pip

### Pasos

1. **Clonar repositorio**
```bash
git clone https://github.com/facecode/guardian-network.git
cd guardian-network
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env según necesidades
```

5. **Ejecutar servidor**
```bash
python -m uvicorn src.facecode_guardian.main:app --reload
```

6. **Acceder a la API**
- API: http://localhost:8000
- Documentación: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Instalación con Docker

### Opción 1: Docker Compose (recomendado)
```bash
docker-compose up -d
```

### Opción 2: Docker manual
```bash
docker build -t facecode-guardian .
docker run -p 8000:8000 facecode-guardian
```

## Uso con Makefile

```bash
# Instalar dependencias
make install

# Ejecutar tests
make test

# Ejecutar servidor en desarrollo
make run

# Construir y ejecutar Docker
make docker-build
make docker-run

# Ver logs
make docker-logs
```

## Ejemplo de Uso

### Detectar rostros en una imagen

```python
import requests
import base64

# Leer imagen
with open("foto.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode()

# Solicitar detección
response = requests.post(
    "http://localhost:8000/api/v1/detect",
    json={
        "image_base64": f"data:image/jpeg;base64,{image_base64}",
        "require_human_approval": True,
        "user_id": "user-123"
    }
)

result = response.json()
print(f"Rostros detectados: {len(result['detections'])}")
print(f"Requiere aprobación: {result['human_approval_required']}")
```

### Aprobar una detección (Botón Ético Rojo)

```python
# Si requiere aprobación
if result['human_approval_required']:
    approval_response = requests.post(
        "http://localhost:8000/api/v1/approve",
        json={
            "request_id": result['approval_request_id'],
            "approved": True,
            "approver_id": "admin-001",
            "notes": "Uso legítimo confirmado"
        }
    )
```

## Tests

```bash
# Todos los tests
pytest

# Solo unitarios
pytest tests/unit/

# Con cobertura
pytest --cov=facecode_guardian --cov-report=html
```

## Características Éticas Activadas

- ✅ **Botón Ético Rojo**: Requiere aprobación humana
- ✅ **Límite de rostros**: Máximo 10 por imagen (anti-vigilancia)
- ✅ **Detección de bias**: Análisis automático de sesgos
- ✅ **Auditoría completa**: Logs de todas las operaciones
- ✅ **Cumplimiento GDPR**: Protección de datos personales
- ✅ **EU AI Act**: Sistema de alto riesgo auditado

## Soporte

Para problemas o preguntas:
- Issues: https://github.com/facecode/guardian-network/issues
- Email: support@facecode.com

---

© 2025 Christian - Fundador de FaceCode®
