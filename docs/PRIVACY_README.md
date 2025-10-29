# 🔒 Privacidad y Protección de Datos — FaceCode® Guardian Network

Este directorio contiene toda la documentación legal, técnica y de implementación relacionada con **privacidad y protección de datos biométricos** para FaceCode® Guardian Network.

---

## 📋 Índice de Documentación

### 1. Documentos Legales

| Documento | Descripción | Audiencia | Extensión |
|-----------|-------------|-----------|-----------|
| [**Aviso de Privacidad Integral**](privacy_policy.md) | Política de privacidad completa que cumple con LFPDPPP (México), GDPR (UE), CCPA/CPRA (California) y AI Act (UE) | Usuarios finales, abogados, auditores | ~3,000 palabras |
| [**Aviso de Privacidad Corto**](privacy_notice_short.md) | Resumen de 250 palabras + microcopy para UI/UX (pantallas, modals, tooltips) | Diseñadores UX/UI, desarrolladores frontend | ~300 palabras + componentes UI |
| [**Plantillas de Consentimiento**](consent_templates.md) | Templates legales de consentimiento explícito para datos biométricos con ejemplos de código | Desarrolladores, equipos legales | ~20 plantillas |

### 2. Documentación Técnica

| Documento | Descripción | Audiencia | Tecnologías |
|-----------|-------------|-----------|-------------|
| [**Guía de Implementación Técnica**](privacy_implementation_guide.md) | Implementación paso a paso de las 5 acciones técnicas prioritarias con código listo para producción | Desarrolladores backend/frontend, arquitectos de software, DevOps | Node.js, TypeScript, PostgreSQL, React, Swift, Kotlin |

---

## 🎯 Acciones Técnicas Inmediatas (5 Prioridades)

Implementar en este orden:

### 1. ✅ Logging de Consentimiento Encriptado
**Objetivo:** Registrar consentimientos con cifrado AES-256 y retención de 5 años

**Componentes:**
- Tabla PostgreSQL `consent_logs` con cifrado
- Servicio de cifrado con AWS KMS
- API endpoints `/api/consent/grant` y `/api/consent/revoke`
- Job de anonimización de IPs (30 días)

**Documentación:** Ver [Guía de Implementación](privacy_implementation_guide.md#1-acción-técnica-1-logging-de-consentimiento-encriptado)

---

### 2. ✅ Eliminación Automática de Templates Biométricos (24h)
**Objetivo:** Auto-delete de plantillas biométricas tras 24 horas con verificación criptográfica

**Componentes:**
- Tabla PostgreSQL `biometric_templates` con TTL
- Cron job de limpieza (cada hora)
- Sobrescritura segura (3 pases DoD 5220.22-M)
- Generación de certificados de eliminación

**Documentación:** Ver [Guía de Implementación](privacy_implementation_guide.md#2-acción-técnica-2-eliminación-automática-de-templates-biométricos-24h)

---

### 3. ✅ Procesamiento On-Device con Fallback Zero-Knowledge
**Objetivo:** Reconocimiento facial 100% local en iOS/Android con fallback E2E si requiere servidor

**Componentes:**
- Implementación iOS (Swift + Core ML + FaceNet)
- Implementación Android (Kotlin + TensorFlow Lite)
- Cifrado E2E con claves locales (Keychain/KeyStore)
- Matching 1:1 local (sin servidor)

**Documentación:** Ver [Guía de Implementación](privacy_implementation_guide.md#3-acción-técnica-3-procesamiento-on-device-con-fallback-zero-knowledge)

---

### 4. ✅ Privacy Score Card UI + Botón "Eliminar Ahora"
**Objetivo:** Dashboard visual de privacidad con eliminación manual instantánea

**Componentes:**
- Componente React `<PrivacyScoreCard />`
- Métricas en tiempo real (nivel de privacidad, cifrado, auditorías)
- Botón "Eliminar ahora" con confirmación doble
- Descarga de certificado de eliminación

**Documentación:** Ver [Guía de Implementación](privacy_implementation_guide.md#4-acción-técnica-4-privacy-score-card-ui--botón-eliminar-ahora)

---

### 5. ✅ Endpoint ARCO Self-Service
**Objetivo:** Portal de autoservicio para derechos ARCO (Acceso, Rectificación, Cancelación, Oposición)

**Componentes:**
- `GET /api/arco/access` — Descargar datos (JSON/CSV)
- `POST /api/arco/rectify` — Corregir datos inexactos
- `DELETE /api/arco/cancel` — Eliminar cuenta + datos
- `POST /api/arco/oppose` — Oponerse a tratamientos

**Documentación:** Ver [Guía de Implementación](privacy_implementation_guide.md#5-acción-técnica-5-endpoint-arco-self-service)

---

## 📦 Estructura de Archivos del Proyecto

```
facecode-guardian-network/
├── docs/
│   ├── privacy_policy.md              # Aviso de Privacidad Integral (3000 palabras)
│   ├── privacy_notice_short.md        # Versión corta + UI microcopy
│   ├── consent_templates.md           # Templates legales + código
│   ├── privacy_implementation_guide.md # Guía técnica completa
│   └── PRIVACY_README.md              # Este archivo
│
├── src/ (próximamente)
│   ├── routes/
│   │   ├── consent.routes.ts          # Endpoints de consentimiento
│   │   ├── biometric.routes.ts        # Endpoints de datos biométricos
│   │   └── arco.routes.ts             # Endpoints ARCO
│   │
│   ├── services/
│   │   ├── encryption.service.ts      # Cifrado AES-256 + KMS
│   │   ├── consent.service.ts         # Lógica de consentimientos
│   │   ├── biometric.service.ts       # Procesamiento biométrico
│   │   ├── certificate.service.ts     # Generación de certificados
│   │   └── audit.service.ts           # Logging de auditoría
│   │
│   ├── jobs/
│   │   └── biometric-cleanup.job.ts   # Job de eliminación 24h
│   │
│   ├── components/ (Frontend)
│   │   ├── PrivacyScoreCard.tsx       # UI de Privacy Score Card
│   │   ├── ConsentModal.tsx           # Modal de consentimiento
│   │   └── ARCORequestForm.tsx        # Formulario ARCO
│   │
│   └── mobile/
│       ├── ios/
│       │   └── FacialRecognitionService.swift  # Procesamiento on-device iOS
│       │
│       └── android/
│           └── BiometricProcessor.kt            # Procesamiento on-device Android
│
└── database/
    └── migrations/
        ├── 001_create_consent_logs.sql
        ├── 002_create_biometric_templates.sql
        └── 003_create_arco_requests.sql
```

---

## 🔐 Cumplimiento Legal

Esta implementación cumple con:

### México
- ✅ **Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP)**
- ✅ Registro ante INAI (Instituto Nacional de Transparencia)
- ✅ Derechos ARCO (Acceso, Rectificación, Cancelación, Oposición)
- ✅ Consentimiento explícito para datos sensibles (biométricos)

### Unión Europea
- ✅ **Reglamento General de Protección de Datos (GDPR)**
- ✅ **Reglamento de Inteligencia Artificial (AI Act)** — Sistemas de alto riesgo
- ✅ Evaluación de Impacto (DPIA) para tratamiento de datos biométricos
- ✅ Cláusulas Contractuales Estándar (SCC) para transferencias internacionales
- ✅ Derecho al olvido (Art. 17 GDPR)

### Estados Unidos
- ✅ **California Consumer Privacy Act (CCPA) / California Privacy Rights Act (CPRA)**
- ✅ **Illinois Biometric Information Privacy Act (BIPA)** — Consentimiento escrito obligatorio
- ✅ **Health Insurance Portability and Accountability Act (HIPAA)** — Si aplica para salud

---

## 📊 Métricas de Privacidad

### Niveles de Privacidad (Privacy Score)

| Nivel | Score | Criterios |
|-------|-------|-----------|
| 🟢 **ALTO** | 80-100 | • Procesamiento 100% local<br>• Cero datos compartidos<br>• Cifrado activo<br>• Auditorías pasadas (100%) |
| 🟡 **MEDIO** | 50-79 | • Procesamiento híbrido (local + cloud E2E)<br>• Datos compartidos mínimos con DPA<br>• Cifrado activo<br>• Auditorías pasadas (>80%) |
| 🔴 **BAJO** | 0-49 | • Procesamiento en cloud sin E2E<br>• Datos compartidos sin cifrado<br>• Auditorías fallidas |

---

## 🚀 Roadmap de Implementación

### Fase 1: Fundamentos (Semanas 1-2)
- [x] Crear documentación legal completa
- [x] Diseñar arquitectura de privacidad
- [ ] Implementar tabla `consent_logs` con cifrado
- [ ] Implementar tabla `biometric_templates` con TTL
- [ ] Configurar AWS KMS para gestión de claves

### Fase 2: Backend Core (Semanas 3-4)
- [ ] Endpoints de consentimiento (`/api/consent/*`)
- [ ] Job de eliminación automática (24h)
- [ ] Endpoints ARCO (`/api/arco/*`)
- [ ] Sistema de auditoría inmutable
- [ ] Generación de certificados de eliminación

### Fase 3: Procesamiento On-Device (Semanas 5-6)
- [ ] Implementación iOS (Swift + Core ML)
- [ ] Implementación Android (Kotlin + TFLite)
- [ ] Testing de precisión y rendimiento
- [ ] Fallback E2E para casos edge

### Fase 4: Frontend UI (Semanas 7-8)
- [ ] Privacy Score Card component
- [ ] Modal de consentimiento biométrico
- [ ] Pantalla de configuración de privacidad
- [ ] Portal ARCO self-service
- [ ] Descarga de certificados

### Fase 5: Testing & Auditoría (Semanas 9-10)
- [ ] Testing E2E de flujos de privacidad
- [ ] Penetration testing (externo)
- [ ] Auditoría de seguridad (externo)
- [ ] Revisión legal (despacho especializado)
- [ ] A/B testing de comprensión de textos

### Fase 6: Deployment (Semana 11-12)
- [ ] Beta privada (100 usuarios)
- [ ] Monitoreo de métricas de privacidad
- [ ] Ajustes basados en feedback
- [ ] Lanzamiento público
- [ ] Publicación de Informe de Transparencia

---

## 🛠 Stack Tecnológico

### Backend
- **Node.js 18+** / TypeScript 5+
- **PostgreSQL 14+** con `pgcrypto` y `pg_cron`
- **Redis 7+** para caching y tracking
- **AWS KMS / Google Cloud KMS** para gestión de claves
- **Express.js** para API REST

### Frontend
- **React 18+** / React Native
- **TypeScript**
- **TailwindCSS** para styling
- **Lucide React** para iconos

### Mobile
- **iOS:** Swift 5+, Core ML, Vision Framework
- **Android:** Kotlin, TensorFlow Lite, ML Kit

### Seguridad
- **AES-256-GCM** para cifrado
- **TLS 1.3** para transporte
- **Ed25519** para firmas digitales
- **HSM** (Hardware Security Module) para claves críticas

### Monitoreo
- **Grafana** + **Prometheus** para métricas
- **ELK Stack** (Elasticsearch, Logstash, Kibana) para logs
- **PagerDuty** para alertas críticas

---

## 📧 Contacto

### Privacidad
- **Email general:** privacy@facecode.app
- **Oficial de Protección de Datos (DPO):** dpo@facecode.app
- **Solicitudes ARCO:** Portal web en facecode.app/privacy/arco

### Técnico
- **Engineering Lead:** engineering@facecode.app
- **Security Team:** security@facecode.app
- **Soporte técnico:** support@facecode.app

### Legal
- **Asuntos legales:** legal@facecode.app

---

## 📚 Referencias Legales

### Legislación Mexicana
- [LFPDPPP (texto completo)](https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf)
- [INAI — Instituto Nacional de Transparencia](https://home.inai.org.mx/)

### Legislación Europea
- [GDPR (Reglamento UE 2016/679)](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32016R0679)
- [AI Act (Reglamento UE 2024/1689)](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32024R1689)

### Legislación Estadounidense
- [CCPA/CPRA (California)](https://oag.ca.gov/privacy/ccpa)
- [BIPA (Illinois)](https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=3004)

---

## 🔗 Enlaces Útiles

- [Sitio web oficial](https://facecode.app) *(próximamente)*
- [Repositorio GitHub](https://github.com/facecode/guardian-network)
- [Documentación técnica completa](https://docs.facecode.app) *(próximamente)*
- [Informe de Transparencia](https://facecode.app/transparency) *(próximamente)*
- [Portal de auditorías públicas](https://facecode.app/audits) *(próximamente)*

---

## ⚖️ Licencia

Este proyecto se distribuye bajo la **Licencia Ética FaceCode® v1.0**, que prioriza el uso humano, no discriminatorio y alineado con los derechos fundamentales.

Ver [LICENSE.md](../LICENSE.md) para detalles completos.

---

> **© 2025 FaceCode® Guardian Network**
> *Privacidad por diseño • Transparencia radical • Código abierto*
>
> **Fundador:** Christian — Amigo del Mundo • Derecho a la dignidad digital
