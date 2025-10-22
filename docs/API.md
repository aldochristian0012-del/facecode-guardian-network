# FaceCode Guardian Network - Documentación de API

## Visión General

La API REST de FaceCode Guardian Network proporciona endpoints para reconocimiento facial ético con cumplimiento del AI Act de la UE.

**Base URL**: `http://localhost:8000/api/v1`

## Autenticación

Actualmente la API es pública. En producción, usa:

```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### 1. Detección Facial

**POST** `/detect`

Detecta rostros en una imagen con validaciones éticas integradas.

#### Request Body

```json
{
  "image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "require_human_approval": true,
  "user_id": "user-123",
  "session_id": "session-456"
}
```

#### Response (200 OK)

```json
{
  "success": true,
  "detections": [
    {
      "bounding_box": {
        "x": 120.5,
        "y": 80.3,
        "width": 150.2,
        "height": 180.7
      },
      "confidence": 0.92,
      "landmarks": [
        {"x": 145.2, "y": 120.5},
        {"x": 165.8, "y": 122.1}
      ],
      "timestamp": "2025-10-22T10:30:00.000Z",
      "ethical_flags": {
        "max_faces_check": "passed",
        "total_faces_in_image": 2,
        "confidence_threshold": 0.5
      }
    }
  ],
  "bias_metrics": {
    "total_detections": 2,
    "confidence_stats": {
      "min": 0.85,
      "max": 0.92,
      "mean": 0.885,
      "std": 0.035,
      "median": 0.885
    },
    "bias_score": 0.175,
    "warnings": [],
    "timestamp": "2025-10-22T10:30:00.000Z"
  },
  "human_approval_required": true,
  "approval_request_id": "req-abc-123",
  "message": "Detected 2 face(s). Human approval required."
}
```

#### Error Responses

**403 Forbidden** - Límite ético excedido

```json
{
  "detail": "Límite ético excedido: 15 rostros detectados. Máximo permitido: 10. Esto previene vigilancia masiva."
}
```

**400 Bad Request** - Imagen inválida

```json
{
  "detail": "Error decoding image: Invalid base64 string"
}
```

---

### 2. Aprobar/Vetar Solicitud (Botón Ético Rojo)

**POST** `/approve`

Permite a un humano aprobar o vetar una operación de detección facial.

#### Request Body

```json
{
  "request_id": "req-abc-123",
  "approved": true,
  "approver_id": "admin-001",
  "reason": "ethical_concern",
  "notes": "Contexto verificado como legítimo"
}
```

**Valores de `reason` (para vetos):**
- `ethical_concern`
- `privacy_violation`
- `bias_detected`
- `unauthorized_use`
- `data_quality_issue`
- `other`

#### Response (200 OK)

```json
{
  "request_id": "req-abc-123",
  "status": "approved",
  "approved": true,
  "approver_id": "admin-001",
  "timestamp": "2025-10-22T10:31:00.000Z"
}
```

---

### 3. Consultar Estado de Aprobación

**GET** `/approval/{request_id}`

Consulta el estado de una solicitud de aprobación.

#### Response (200 OK)

```json
{
  "request_id": "req-abc-123",
  "status": "pending",
  "approved": null,
  "approver_id": null,
  "timestamp": "2025-10-22T10:30:00.000Z"
}
```

**Posibles estados:**
- `pending`: Esperando decisión humana
- `approved`: Aprobado
- `vetoed`: Vetado
- `expired`: Expirado (timeout)

---

### 4. Estado del Sistema

**GET** `/health`

Retorna el estado de salud del sistema y configuración ética.

#### Response (200 OK)

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "ethical_features": {
    "red_button_enabled": true,
    "bias_detection_enabled": true,
    "audit_logging_enabled": true
  },
  "compliance": {
    "gdpr_compliant": true,
    "eu_ai_act_compliant": true,
    "eaa_compliant": true
  },
  "statistics": {
    "total_requests": 42,
    "approved": 35,
    "vetoed": 7,
    "approval_rate": 0.833,
    "pending": 2,
    "veto_reasons": {
      "ethical_concern": 4,
      "privacy_violation": 2,
      "other": 1
    }
  }
}
```

---

### 5. Estadísticas del Botón Ético Rojo

**GET** `/red-button/stats`

Retorna estadísticas detalladas del sistema de veto humano.

#### Response (200 OK)

```json
{
  "total_requests": 42,
  "approved": 35,
  "vetoed": 7,
  "approval_rate": 0.833,
  "pending": 2,
  "veto_reasons": {
    "ethical_concern": 4,
    "privacy_violation": 2,
    "bias_detected": 0,
    "unauthorized_use": 0,
    "data_quality_issue": 1,
    "other": 0
  }
}
```

---

### 6. Reporte de Equidad (Bias)

**GET** `/bias/report`

Genera un reporte completo sobre el sesgo detectado en el sistema.

#### Response (200 OK)

```json
{
  "historical_analysis": {
    "total_detections": 128,
    "avg_confidence": 0.87,
    "samples_analyzed": 42,
    "time_range": {
      "start": "2025-10-20T00:00:00.000Z",
      "end": "2025-10-22T10:30:00.000Z"
    }
  },
  "recommendations": [
    "Recopilar más datos para análisis estadísticamente significativo"
  ],
  "compliance_status": {
    "eu_ai_act_article_10": "in_review",
    "bias_monitoring_active": true,
    "human_oversight_enabled": true
  },
  "generated_at": "2025-10-22T10:30:00.000Z"
}
```

---

### 7. Resumen de Auditoría

**GET** `/audit/summary?days=7`

Retorna resumen de auditoría para los últimos N días.

#### Query Parameters

- `days` (int, default=7): Número de días a analizar

#### Response (200 OK)

```json
{
  "period_days": 7,
  "total_events": 256,
  "face_detections": 128,
  "human_approvals": 102,
  "human_vetos": 26,
  "bias_warnings": 12,
  "status": "active"
}
```

---

## Límites Éticos

### Límite de Rostros por Imagen

**Máximo:** 10 rostros por imagen

**Razón:** Prevenir vigilancia masiva

**Error:** 403 Forbidden si se excede

### Rate Limiting

**Máximo:** 30 requests por minuto por usuario

**Error:** 429 Too Many Requests

### Timeout de Aprobación

**Timeout:** 30 segundos

**Comportamiento:** Veto automático si no hay respuesta humana

---

## Cumplimiento Regulatorio

### GDPR (Reglamento General de Protección de Datos)

- ✅ Logs de auditoría con retención de 90 días
- ✅ Anonimización de datos biométricos
- ✅ Derecho al olvido implementable

### EU AI Act (Sistemas de Alto Riesgo)

- ✅ Supervisión humana obligatoria (Botón Ético Rojo)
- ✅ Detección y mitigación de sesgos
- ✅ Transparencia algorítmica
- ✅ Documentación técnica completa

### Directiva de Accesibilidad Europea (EAA)

- ✅ API accesible y bien documentada
- ✅ Mensajes de error claros
- ✅ Múltiples formatos de salida

---

## Ejemplos de Uso

### Python

```python
import requests
import base64

# Preparar imagen
with open("foto.jpg", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

# Detectar rostros
response = requests.post(
    "http://localhost:8000/api/v1/detect",
    json={
        "image_base64": f"data:image/jpeg;base64,{image_b64}",
        "require_human_approval": True,
        "user_id": "user-123"
    }
)

result = response.json()
print(f"Rostros: {len(result['detections'])}")

# Aprobar si es necesario
if result['human_approval_required']:
    approval = requests.post(
        "http://localhost:8000/api/v1/approve",
        json={
            "request_id": result['approval_request_id'],
            "approved": True,
            "approver_id": "admin-001"
        }
    )
```

### cURL

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Detectar rostros
curl -X POST http://localhost:8000/api/v1/detect \
  -H "Content-Type: application/json" \
  -d '{
    "image_base64": "data:image/jpeg;base64,...",
    "require_human_approval": true,
    "user_id": "user-123"
  }'

# Aprobar solicitud
curl -X POST http://localhost:8000/api/v1/approve \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "req-abc-123",
    "approved": true,
    "approver_id": "admin-001"
  }'
```

---

## Soporte

- **Documentación interactiva**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Issues**: https://github.com/facecode/guardian-network/issues

© 2025 Christian - Fundador de FaceCode®
