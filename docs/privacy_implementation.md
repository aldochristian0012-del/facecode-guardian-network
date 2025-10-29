# IMPLEMENTACIÓN TÉCNICA — PRIVACIDAD FACECODE®

**Objetivo:** Proveer snippets de código funcionales para implementar el sistema de consentimiento, logging cifrado, job de eliminación y verificación de borrado.

**Stack tecnológico sugerido:**
- Backend: Node.js + Express / Python + FastAPI
- Base de datos: PostgreSQL 15+ (con extensiones pgcrypto para cifrado)
- Cache: Redis 7+
- Jobs: BullMQ / Celery
- Monitoreo: Prometheus + Grafana
- Auditoría: ELK Stack (Elasticsearch + Logstash + Kibana)

---

## TABLA DE CONTENIDOS

1. [Modelo de datos (SQL Schema)](#1-modelo-de-datos-sql-schema)
2. [Sistema de registro de consentimiento (Node.js)](#2-sistema-de-registro-de-consentimiento-nodejs)
3. [Job de eliminación automática (24 horas)](#3-job-de-eliminación-automática-24-horas)
4. [Endpoint de verificación de eliminación](#4-endpoint-de-verificación-de-eliminación)
5. [Logging cifrado de auditoría](#5-logging-cifrado-de-auditoría)
6. [Implementación de derechos ARCO](#6-implementación-de-derechos-arco)
7. [SDK móvil (iOS/Android)](#7-sdk-móvil-iosandroid)
8. [Monitoring y alertas](#8-monitoring-y-alertas)

---

## 1. MODELO DE DATOS (SQL SCHEMA)

### 1.1 Tabla de usuarios

```sql
-- Tabla principal de usuarios
CREATE TABLE users (
  user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  status VARCHAR(50) NOT NULL DEFAULT 'active', -- active, suspended, deleted
  country_code CHAR(2), -- ISO 3166-1 alpha-2 (MX, US, BR, etc.)
  CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_created_at ON users(created_at);
```

### 1.2 Tabla de templates biométricos (datos sensibles)

```sql
-- Tabla de templates biométricos (FaceCodes)
-- CRÍTICO: Retención máxima 24 horas, cifrado en reposo
CREATE TABLE biometric_templates (
  template_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  template_vector BYTEA NOT NULL, -- Vector cifrado con AES-256
  template_version VARCHAR(50) NOT NULL, -- Versión del modelo ML (e.g., "mobilenet-v3-2025-10")
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  expires_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '24 hours'),
  device_id VARCHAR(255),
  retention_override BOOLEAN DEFAULT FALSE, -- Usuario autorizó retención mayor
  retention_override_expires_at TIMESTAMPTZ,
  CONSTRAINT valid_expiration CHECK (expires_at > created_at)
);

-- Índices para performance
CREATE INDEX idx_biometric_templates_user_id ON biometric_templates(user_id);
CREATE INDEX idx_biometric_templates_expires_at ON biometric_templates(expires_at);
CREATE INDEX idx_biometric_templates_created_at ON biometric_templates(created_at);

-- Trigger para auto-eliminación después de expires_at (backup de cron job)
CREATE OR REPLACE FUNCTION delete_expired_templates()
RETURNS TRIGGER AS $$
BEGIN
  DELETE FROM biometric_templates WHERE expires_at < NOW();
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Ejecutar trigger cada hora
-- Nota: En producción usar cron job externo (más confiable)
```

### 1.3 Tabla de consentimientos (logs de auditoría)

```sql
-- Tabla de logs de consentimiento (retención 5 años)
CREATE TABLE consent_logs (
  consent_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT, -- NO eliminar si hay consentimientos
  timestamp_utc TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ip_address INET NOT NULL, -- Tipo nativo de PostgreSQL para IPs
  device_id VARCHAR(255),
  tos_version VARCHAR(50) NOT NULL, -- e.g., "v2025-10-29"
  consent_text_hash CHAR(64) NOT NULL, -- SHA-256 del texto del consentimiento
  acceptance_method VARCHAR(50) NOT NULL, -- 'explicit_checkbox', 'biometric', 'electronic_signature'
  geolocation CHAR(2), -- ISO 3166-1 alpha-2
  user_agent TEXT,
  revoked_at TIMESTAMPTZ, -- NULL si no ha sido revocado
  revocation_reason TEXT,

  -- Cifrado del payload completo (JSON con todos los campos) para auditoría forense
  encrypted_payload BYTEA, -- JSON cifrado con key de auditoría separada

  CONSTRAINT valid_acceptance_method CHECK (
    acceptance_method IN ('explicit_checkbox', 'biometric', 'electronic_signature', 'parental_consent')
  )
);

-- Índices
CREATE INDEX idx_consent_logs_user_id ON consent_logs(user_id);
CREATE INDEX idx_consent_logs_timestamp ON consent_logs(timestamp_utc DESC);
CREATE INDEX idx_consent_logs_tos_version ON consent_logs(tos_version);
CREATE INDEX idx_consent_logs_revoked ON consent_logs(revoked_at) WHERE revoked_at IS NOT NULL;

-- Particionado por año para mejor performance (opcional para alta escala)
-- CREATE TABLE consent_logs_2025 PARTITION OF consent_logs FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
```

### 1.4 Tabla de solicitudes ARCO

```sql
-- Tabla de solicitudes ARCO (Acceso, Rectificación, Cancelación, Oposición)
CREATE TABLE arco_requests (
  request_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
  request_type VARCHAR(50) NOT NULL, -- 'access', 'rectification', 'cancellation', 'opposition', 'portability'
  status VARCHAR(50) NOT NULL DEFAULT 'pending', -- 'pending', 'in_progress', 'completed', 'rejected'
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  deadline TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '20 days'), -- LFPDPPP 2025: 20 días hábiles
  request_details JSONB, -- Detalles específicos de la solicitud
  response_details JSONB, -- Respuesta generada
  assigned_to VARCHAR(255), -- Email del responsable de privacidad asignado

  CONSTRAINT valid_request_type CHECK (
    request_type IN ('access', 'rectification', 'cancellation', 'opposition', 'portability', 'limitation')
  ),
  CONSTRAINT valid_status CHECK (
    status IN ('pending', 'in_progress', 'completed', 'rejected', 'expired')
  )
);

CREATE INDEX idx_arco_requests_user_id ON arco_requests(user_id);
CREATE INDEX idx_arco_requests_status ON arco_requests(status);
CREATE INDEX idx_arco_requests_deadline ON arco_requests(deadline);
```

### 1.5 Tabla de certificados de eliminación

```sql
-- Tabla de certificados de eliminación verificables
CREATE TABLE deletion_certificates (
  certificate_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL, -- No FOREIGN KEY porque el usuario ya fue eliminado
  deletion_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  job_id VARCHAR(255) UNIQUE NOT NULL, -- ID del job de eliminación (e.g., "del-20251029-143200-abc123")
  records_deleted JSONB NOT NULL, -- {"biometric_templates": 1, "metadata": 47, "logs": 0}
  verification_hash CHAR(64) NOT NULL, -- SHA-256 del certificado completo
  certificate_pdf BYTEA, -- PDF generado y firmado digitalmente
  certificate_url TEXT, -- URL pública para verificación
  blockchain_tx_hash VARCHAR(255), -- Opcional: hash de transacción en blockchain para inmutabilidad

  CONSTRAINT positive_records CHECK ((records_deleted::jsonb->>'biometric_templates')::int >= 0)
);

CREATE INDEX idx_deletion_certificates_job_id ON deletion_certificates(job_id);
CREATE INDEX idx_deletion_certificates_timestamp ON deletion_certificates(deletion_timestamp DESC);
```

---

## 2. SISTEMA DE REGISTRO DE CONSENTIMIENTO (NODE.JS)

### 2.1 Endpoint para registrar consentimiento

```javascript
// src/routes/consent.js
const express = require('express');
const crypto = require('crypto');
const { body, validationResult } = require('express-validator');
const db = require('../db'); // PostgreSQL client
const redis = require('../redis'); // Redis client para cache
const logger = require('../logger');

const router = express.Router();

/**
 * POST /api/v1/consent
 * Registra consentimiento explícito del usuario para tratamiento de datos biométricos
 *
 * Body:
 * {
 *   "user_id": "uuid-v4",
 *   "tos_version": "v2025-10-29",
 *   "consent_text": "Texto completo del consentimiento...",
 *   "acceptance_method": "explicit_checkbox",
 *   "device_id": "device-fingerprint-hash",
 *   "geolocation": "MX"
 * }
 */
router.post(
  '/consent',
  [
    body('user_id').isUUID(4).withMessage('Invalid user_id'),
    body('tos_version').matches(/^v\d{4}-\d{2}-\d{2}$/).withMessage('Invalid tos_version format'),
    body('consent_text').isLength({ min: 100 }).withMessage('Consent text too short'),
    body('acceptance_method').isIn(['explicit_checkbox', 'biometric', 'electronic_signature', 'parental_consent']),
    body('device_id').optional().isString(),
    body('geolocation').optional().isISO31661Alpha2(),
  ],
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const {
      user_id,
      tos_version,
      consent_text,
      acceptance_method,
      device_id,
      geolocation,
    } = req.body;

    try {
      // 1. Generar hash del texto de consentimiento (SHA-256)
      const consent_text_hash = crypto
        .createHash('sha256')
        .update(consent_text)
        .digest('hex');

      // 2. Obtener IP del cliente
      const ip_address = req.ip || req.connection.remoteAddress;

      // 3. Obtener User-Agent
      const user_agent = req.headers['user-agent'];

      // 4. Crear payload para cifrado
      const payload = {
        user_id,
        timestamp_utc: new Date().toISOString(),
        ip_address,
        device_id,
        tos_version,
        consent_text_hash,
        acceptance_method,
        geolocation,
        user_agent,
      };

      // 5. Cifrar payload completo para auditoría (AES-256-GCM)
      const encrypted_payload = encryptPayload(JSON.stringify(payload));

      // 6. Insertar en base de datos
      const query = `
        INSERT INTO consent_logs (
          user_id,
          timestamp_utc,
          ip_address,
          device_id,
          tos_version,
          consent_text_hash,
          acceptance_method,
          geolocation,
          user_agent,
          encrypted_payload
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        RETURNING consent_id, timestamp_utc
      `;

      const values = [
        user_id,
        new Date(),
        ip_address,
        device_id,
        tos_version,
        consent_text_hash,
        acceptance_method,
        geolocation || null,
        user_agent,
        encrypted_payload,
      ];

      const result = await db.query(query, values);
      const { consent_id, timestamp_utc } = result.rows[0];

      // 7. Cachear consentimiento activo en Redis (TTL 24 horas)
      await redis.setex(
        `consent:${user_id}:${tos_version}`,
        86400, // 24 horas
        JSON.stringify({ consent_id, timestamp_utc, tos_version })
      );

      // 8. Log de auditoría
      logger.info('Consent registered', {
        user_id,
        consent_id,
        tos_version,
        acceptance_method,
        ip_address,
      });

      // 9. Respuesta
      res.status(201).json({
        success: true,
        consent_id,
        timestamp_utc,
        message: 'Consent registered successfully',
      });

    } catch (error) {
      logger.error('Error registering consent', { error: error.message, user_id });
      res.status(500).json({
        success: false,
        error: 'Failed to register consent',
      });
    }
  }
);

/**
 * Cifrado de payload con AES-256-GCM
 * @param {string} plaintext - Texto a cifrar
 * @returns {Buffer} - Payload cifrado
 */
function encryptPayload(plaintext) {
  const algorithm = 'aes-256-gcm';
  const key = Buffer.from(process.env.AUDIT_ENCRYPTION_KEY, 'hex'); // 32 bytes (256 bits)
  const iv = crypto.randomBytes(16); // Initialization vector de 16 bytes

  const cipher = crypto.createCipheriv(algorithm, key, iv);

  let encrypted = cipher.update(plaintext, 'utf8');
  encrypted = Buffer.concat([encrypted, cipher.final()]);

  const authTag = cipher.getAuthTag();

  // Formato: [IV (16 bytes)][AuthTag (16 bytes)][Encrypted Data]
  return Buffer.concat([iv, authTag, encrypted]);
}

/**
 * POST /api/v1/consent/revoke
 * Revoca consentimiento previamente otorgado
 */
router.post(
  '/consent/revoke',
  [
    body('user_id').isUUID(4),
    body('consent_id').optional().isUUID(4),
    body('revocation_reason').optional().isString(),
  ],
  async (req, res) => {
    const { user_id, consent_id, revocation_reason } = req.body;

    try {
      // Actualizar registro de consentimiento
      const query = consent_id
        ? `UPDATE consent_logs SET revoked_at = NOW(), revocation_reason = $1
           WHERE consent_id = $2 AND user_id = $3 RETURNING consent_id`
        : `UPDATE consent_logs SET revoked_at = NOW(), revocation_reason = $1
           WHERE user_id = $2 AND revoked_at IS NULL RETURNING consent_id`;

      const values = consent_id
        ? [revocation_reason, consent_id, user_id]
        : [revocation_reason, user_id];

      const result = await db.query(query, values);

      if (result.rowCount === 0) {
        return res.status(404).json({
          success: false,
          error: 'Consent not found or already revoked',
        });
      }

      // Eliminar cache de Redis
      const keys = await redis.keys(`consent:${user_id}:*`);
      if (keys.length > 0) {
        await redis.del(...keys);
      }

      logger.info('Consent revoked', { user_id, consent_id: result.rows[0].consent_id });

      res.status(200).json({
        success: true,
        message: 'Consent revoked successfully',
        revoked_consents: result.rowCount,
      });

    } catch (error) {
      logger.error('Error revoking consent', { error: error.message, user_id });
      res.status(500).json({
        success: false,
        error: 'Failed to revoke consent',
      });
    }
  }
);

/**
 * GET /api/v1/consent/status/:user_id
 * Verifica si el usuario tiene consentimiento activo
 */
router.get('/consent/status/:user_id', async (req, res) => {
  const { user_id } = req.params;
  const { tos_version } = req.query;

  try {
    // 1. Verificar cache en Redis primero
    const cacheKey = `consent:${user_id}:${tos_version || 'latest'}`;
    const cached = await redis.get(cacheKey);

    if (cached) {
      return res.status(200).json({
        success: true,
        has_consent: true,
        consent: JSON.parse(cached),
        source: 'cache',
      });
    }

    // 2. Consultar base de datos
    const query = tos_version
      ? `SELECT consent_id, timestamp_utc, tos_version, revoked_at
         FROM consent_logs
         WHERE user_id = $1 AND tos_version = $2 AND revoked_at IS NULL
         ORDER BY timestamp_utc DESC LIMIT 1`
      : `SELECT consent_id, timestamp_utc, tos_version, revoked_at
         FROM consent_logs
         WHERE user_id = $1 AND revoked_at IS NULL
         ORDER BY timestamp_utc DESC LIMIT 1`;

    const values = tos_version ? [user_id, tos_version] : [user_id];
    const result = await db.query(query, values);

    if (result.rowCount === 0) {
      return res.status(200).json({
        success: true,
        has_consent: false,
        message: 'No active consent found',
      });
    }

    const consent = result.rows[0];

    // 3. Cachear resultado
    await redis.setex(cacheKey, 86400, JSON.stringify(consent));

    res.status(200).json({
      success: true,
      has_consent: true,
      consent,
      source: 'database',
    });

  } catch (error) {
    logger.error('Error checking consent status', { error: error.message, user_id });
    res.status(500).json({
      success: false,
      error: 'Failed to check consent status',
    });
  }
});

module.exports = router;
```

### 2.2 Configuración de variables de entorno

```bash
# .env (NUNCA commitear a Git)
# Generar key de cifrado: openssl rand -hex 32

AUDIT_ENCRYPTION_KEY=a1b2c3d4e5f6... (64 caracteres hex = 32 bytes)
DATABASE_URL=postgresql://user:password@localhost:5432/facecode_db
REDIS_URL=redis://localhost:6379
NODE_ENV=production
```

---

## 3. JOB DE ELIMINACIÓN AUTOMÁTICA (24 HORAS)

### 3.1 Job con BullMQ (Node.js)

```javascript
// src/jobs/deleteExpiredTemplates.js
const { Queue, Worker } = require('bullmq');
const db = require('../db');
const logger = require('../logger');

// Cola de jobs de eliminación
const deletionQueue = new Queue('biometric-deletion', {
  connection: {
    host: process.env.REDIS_HOST || 'localhost',
    port: process.env.REDIS_PORT || 6379,
  },
});

/**
 * Worker que procesa eliminaciones de templates expirados
 */
const deletionWorker = new Worker(
  'biometric-deletion',
  async (job) => {
    const { template_id, user_id, expires_at } = job.data;

    logger.info('Processing deletion job', { template_id, user_id });

    try {
      // 1. Eliminar template de base de datos
      const deleteQuery = `
        DELETE FROM biometric_templates
        WHERE template_id = $1 AND expires_at <= NOW()
        RETURNING template_id, user_id, created_at
      `;
      const deleteResult = await db.query(deleteQuery, [template_id]);

      if (deleteResult.rowCount === 0) {
        logger.warn('Template not found or not expired yet', { template_id });
        return { success: false, reason: 'not_found_or_not_expired' };
      }

      const deletedTemplate = deleteResult.rows[0];

      // 2. Registrar eliminación en tabla de auditoría
      const auditQuery = `
        INSERT INTO deletion_audit_log (
          template_id,
          user_id,
          deleted_at,
          deletion_reason,
          job_id
        ) VALUES ($1, $2, NOW(), $3, $4)
      `;
      await db.query(auditQuery, [
        template_id,
        user_id,
        'auto_expiration',
        job.id,
      ]);

      // 3. Emitir métrica de Prometheus
      deletionCounter.inc({ reason: 'auto_expiration' });

      logger.info('Template deleted successfully', {
        template_id,
        user_id,
        created_at: deletedTemplate.created_at,
      });

      return {
        success: true,
        template_id,
        user_id,
        deleted_at: new Date().toISOString(),
      };

    } catch (error) {
      logger.error('Error deleting template', {
        error: error.message,
        template_id,
        user_id,
      });
      throw error; // BullMQ reintentará el job
    }
  },
  {
    connection: {
      host: process.env.REDIS_HOST || 'localhost',
      port: process.env.REDIS_PORT || 6379,
    },
    concurrency: 10, // Procesar hasta 10 eliminaciones en paralelo
    limiter: {
      max: 100, // Máximo 100 jobs por ventana
      duration: 60000, // Ventana de 1 minuto
    },
  }
);

/**
 * Cron job que programa eliminaciones automáticas cada hora
 * Ejecutar con: node-cron o sistema externo (Kubernetes CronJob, AWS EventBridge)
 */
async function scheduleExpiredTemplatesDeletion() {
  try {
    // Buscar templates que expiran en las próximas 2 horas (buffer de seguridad)
    const query = `
      SELECT template_id, user_id, expires_at
      FROM biometric_templates
      WHERE expires_at <= NOW() + INTERVAL '2 hours'
        AND expires_at > NOW() - INTERVAL '1 hour' -- Evitar duplicados de ejecuciones previas
      ORDER BY expires_at ASC
      LIMIT 1000 -- Procesar máximo 1000 por ejecución
    `;

    const result = await db.query(query);

    logger.info(`Found ${result.rowCount} templates to schedule for deletion`);

    // Agendar job de eliminación para cada template
    const jobs = result.rows.map((row) => ({
      name: 'delete-template',
      data: {
        template_id: row.template_id,
        user_id: row.user_id,
        expires_at: row.expires_at,
      },
      opts: {
        // Programar job para ejecutarse exactamente en expires_at
        delay: Math.max(0, new Date(row.expires_at) - Date.now()),
        attempts: 3, // Reintentar hasta 3 veces si falla
        backoff: {
          type: 'exponential',
          delay: 5000, // Esperar 5s, 10s, 20s entre reintentos
        },
      },
    }));

    await deletionQueue.addBulk(jobs);

    logger.info(`Scheduled ${jobs.length} deletion jobs`);

    return { scheduled: jobs.length };

  } catch (error) {
    logger.error('Error scheduling deletion jobs', { error: error.message });
    throw error;
  }
}

// Exportar para uso en cron job externo
module.exports = {
  deletionQueue,
  deletionWorker,
  scheduleExpiredTemplatesDeletion,
};

// Si se ejecuta directamente (para testing)
if (require.main === module) {
  scheduleExpiredTemplatesDeletion()
    .then((result) => {
      console.log('Deletion scheduling completed:', result);
      process.exit(0);
    })
    .catch((error) => {
      console.error('Deletion scheduling failed:', error);
      process.exit(1);
    });
}
```

### 3.2 Cron job para ejecutar cada hora (Kubernetes CronJob)

```yaml
# k8s/cronjobs/biometric-deletion.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: biometric-template-deletion
  namespace: facecode-prod
spec:
  schedule: "0 * * * *" # Cada hora en punto
  concurrencyPolicy: Forbid # No permitir ejecuciones concurrentes
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: deletion-scheduler
            image: facecode/backend:latest
            command: ["node", "src/jobs/deleteExpiredTemplates.js"]
            env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: facecode-secrets
                  key: database-url
            - name: REDIS_HOST
              value: "redis-master.facecode-prod.svc.cluster.local"
            - name: AUDIT_ENCRYPTION_KEY
              valueFrom:
                secretKeyRef:
                  name: facecode-secrets
                  key: audit-encryption-key
            resources:
              requests:
                memory: "256Mi"
                cpu: "100m"
              limits:
                memory: "512Mi"
                cpu: "500m"
          restartPolicy: OnFailure
```

---

## 4. ENDPOINT DE VERIFICACIÓN DE ELIMINACIÓN

```javascript
// src/routes/deletion.js
const express = require('express');
const PDFDocument = require('pdfkit');
const QRCode = require('qrcode');
const crypto = require('crypto');
const db = require('../db');
const logger = require('../logger');

const router = express.Router();

/**
 * POST /api/v1/deletion/request
 * Solicita eliminación completa de datos biométricos
 */
router.post('/deletion/request', async (req, res) => {
  const { user_id } = req.body;

  try {
    // 1. Verificar que el usuario existe
    const userCheck = await db.query('SELECT user_id FROM users WHERE user_id = $1', [user_id]);
    if (userCheck.rowCount === 0) {
      return res.status(404).json({ success: false, error: 'User not found' });
    }

    // 2. Contar registros a eliminar
    const countQuery = `
      SELECT
        (SELECT COUNT(*) FROM biometric_templates WHERE user_id = $1) as templates,
        (SELECT COUNT(*) FROM user_metadata WHERE user_id = $1) as metadata,
        (SELECT COUNT(*) FROM usage_logs WHERE user_id = $1) as logs
    `;
    const countResult = await db.query(countQuery, [user_id]);
    const records = countResult.rows[0];

    // 3. Generar job_id único
    const timestamp = new Date().toISOString().replace(/[-:]/g, '').split('.')[0];
    const randomPart = crypto.randomBytes(6).toString('hex');
    const job_id = `del-${timestamp}-${randomPart}`;

    // 4. Ejecutar eliminación en transacción
    await db.query('BEGIN');

    try {
      // Eliminar templates biométricos
      await db.query('DELETE FROM biometric_templates WHERE user_id = $1', [user_id]);

      // Eliminar metadatos (si aplica)
      await db.query('DELETE FROM user_metadata WHERE user_id = $1', [user_id]);

      // NO eliminar logs de consentimiento (retención legal 5 años)
      // NO eliminar logs de auditoría

      // 5. Crear certificado de eliminación
      const certQuery = `
        INSERT INTO deletion_certificates (
          user_id,
          job_id,
          records_deleted,
          verification_hash
        ) VALUES ($1, $2, $3, $4)
        RETURNING certificate_id, deletion_timestamp
      `;

      const records_deleted = {
        biometric_templates: parseInt(records.templates),
        metadata: parseInt(records.metadata),
        logs: 0, // Logs de consentimiento no se eliminan
      };

      const verification_hash = crypto
        .createHash('sha256')
        .update(JSON.stringify({ user_id, job_id, records_deleted }))
        .digest('hex');

      const certResult = await db.query(certQuery, [
        user_id,
        job_id,
        JSON.stringify(records_deleted),
        verification_hash,
      ]);

      const { certificate_id, deletion_timestamp } = certResult.rows[0];

      // 6. Generar PDF del certificado
      const pdf = await generateDeletionCertificatePDF({
        certificate_id,
        user_id,
        job_id,
        deletion_timestamp,
        records_deleted,
        verification_hash,
      });

      // 7. Almacenar PDF en base de datos (o S3)
      await db.query(
        'UPDATE deletion_certificates SET certificate_pdf = $1, certificate_url = $2 WHERE certificate_id = $3',
        [
          pdf,
          `https://facecode.app/verify-deletion?token=${verification_hash}`,
          certificate_id,
        ]
      );

      await db.query('COMMIT');

      logger.info('User data deleted successfully', {
        user_id,
        job_id,
        records_deleted,
      });

      res.status(200).json({
        success: true,
        job_id,
        certificate_id,
        deletion_timestamp,
        records_deleted,
        verification_url: `https://facecode.app/verify-deletion?token=${verification_hash}`,
        download_url: `/api/v1/deletion/certificate/${certificate_id}`,
      });

    } catch (error) {
      await db.query('ROLLBACK');
      throw error;
    }

  } catch (error) {
    logger.error('Error deleting user data', { error: error.message, user_id });
    res.status(500).json({
      success: false,
      error: 'Failed to delete user data',
    });
  }
});

/**
 * GET /api/v1/deletion/verify
 * Verifica un certificado de eliminación
 */
router.get('/deletion/verify', async (req, res) => {
  const { token } = req.query; // token = verification_hash

  try {
    const query = `
      SELECT
        certificate_id,
        user_id,
        job_id,
        deletion_timestamp,
        records_deleted,
        verification_hash
      FROM deletion_certificates
      WHERE verification_hash = $1
    `;

    const result = await db.query(query, [token]);

    if (result.rowCount === 0) {
      return res.status(404).json({
        success: false,
        error: 'Certificate not found',
      });
    }

    const cert = result.rows[0];

    // Verificar integridad del hash
    const computed_hash = crypto
      .createHash('sha256')
      .update(JSON.stringify({
        user_id: cert.user_id,
        job_id: cert.job_id,
        records_deleted: cert.records_deleted,
      }))
      .digest('hex');

    const is_valid = computed_hash === cert.verification_hash;

    res.status(200).json({
      success: true,
      valid: is_valid,
      certificate: {
        job_id: cert.job_id,
        deletion_timestamp: cert.deletion_timestamp,
        records_deleted: cert.records_deleted,
        user_id_hash: crypto.createHash('sha256').update(cert.user_id).digest('hex'), // Proteger user_id
      },
    });

  } catch (error) {
    logger.error('Error verifying deletion certificate', { error: error.message });
    res.status(500).json({
      success: false,
      error: 'Failed to verify certificate',
    });
  }
});

/**
 * GET /api/v1/deletion/certificate/:certificate_id
 * Descarga PDF del certificado de eliminación
 */
router.get('/deletion/certificate/:certificate_id', async (req, res) => {
  const { certificate_id } = req.params;

  try {
    const query = 'SELECT certificate_pdf, job_id FROM deletion_certificates WHERE certificate_id = $1';
    const result = await db.query(query, [certificate_id]);

    if (result.rowCount === 0) {
      return res.status(404).json({ success: false, error: 'Certificate not found' });
    }

    const { certificate_pdf, job_id } = result.rows[0];

    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader('Content-Disposition', `attachment; filename="facecode-deletion-${job_id}.pdf"`);
    res.send(certificate_pdf);

  } catch (error) {
    logger.error('Error downloading certificate', { error: error.message });
    res.status(500).json({ success: false, error: 'Failed to download certificate' });
  }
});

/**
 * Genera PDF del certificado de eliminación
 */
async function generateDeletionCertificatePDF(data) {
  const {
    certificate_id,
    user_id,
    job_id,
    deletion_timestamp,
    records_deleted,
    verification_hash,
  } = data;

  return new Promise(async (resolve, reject) => {
    try {
      const doc = new PDFDocument({ size: 'A4', margin: 50 });
      const chunks = [];

      doc.on('data', (chunk) => chunks.push(chunk));
      doc.on('end', () => resolve(Buffer.concat(chunks)));
      doc.on('error', reject);

      // Header
      doc.fontSize(24).font('Helvetica-Bold').text('CERTIFICADO DE ELIMINACIÓN', { align: 'center' });
      doc.fontSize(16).font('Helvetica').text('FaceCode® Guardian Network', { align: 'center' });
      doc.moveDown(2);

      // Información del certificado
      doc.fontSize(12).font('Helvetica-Bold').text('Información del Certificado:');
      doc.font('Helvetica').text(`ID de Certificado: ${certificate_id}`);
      doc.text(`ID de Job: ${job_id}`);
      doc.text(`Fecha de Eliminación: ${new Date(deletion_timestamp).toLocaleString('es-MX')}`);
      doc.moveDown();

      // Usuario (hash por privacidad)
      const user_id_hash = crypto.createHash('sha256').update(user_id).digest('hex');
      doc.fontSize(12).font('Helvetica-Bold').text('Usuario (hash SHA-256):');
      doc.font('Courier').fontSize(8).text(user_id_hash);
      doc.fontSize(12).moveDown();

      // Registros eliminados
      doc.font('Helvetica-Bold').text('Registros Eliminados:');
      doc.font('Helvetica');
      Object.entries(records_deleted).forEach(([key, value]) => {
        doc.text(`  • ${key}: ${value} registro(s)`);
      });
      doc.moveDown();

      // Verificación
      doc.font('Helvetica-Bold').text('Hash de Verificación (SHA-256):');
      doc.font('Courier').fontSize(8).text(verification_hash);
      doc.fontSize(12).moveDown();

      // QR Code para verificación
      const qr_url = `https://facecode.app/verify-deletion?token=${verification_hash}`;
      const qrCode = await QRCode.toDataURL(qr_url);
      doc.font('Helvetica-Bold').text('Verificar en línea:');
      doc.image(qrCode, { width: 150, align: 'center' });
      doc.moveDown();

      // Footer legal
      doc.fontSize(10).font('Helvetica-Oblique').text(
        'Este certificado es válido y puede ser verificado en https://facecode.app/verify-deletion',
        { align: 'center' }
      );
      doc.text('© 2025 FaceCode® S.A. de C.V. — Protección de Datos Personales LFPDPPP 2025', {
        align: 'center',
      });

      doc.end();

    } catch (error) {
      reject(error);
    }
  });
}

module.exports = router;
```

---

## 5. LOGGING CIFRADO DE AUDITORÍA

```javascript
// src/logger/auditLogger.js
const winston = require('winston');
const crypto = require('crypto');
const { ElasticsearchTransport } = require('winston-elasticsearch');

/**
 * Logger especializado para eventos de auditoría de privacidad
 * - Cifra datos sensibles antes de enviar a Elasticsearch
 * - Cumple con retención de 5 años para logs de consentimiento
 */

// Configuración de Elasticsearch
const esTransportOpts = {
  level: 'info',
  clientOpts: {
    node: process.env.ELASTICSEARCH_URL || 'http://localhost:9200',
    auth: {
      username: process.env.ELASTICSEARCH_USER,
      password: process.env.ELASTICSEARCH_PASSWORD,
    },
  },
  index: 'facecode-audit-logs',
  dataStream: true, // Usar Elasticsearch Data Streams para mejor retención
};

const esTransport = new ElasticsearchTransport(esTransportOpts);

// Crear logger de Winston
const auditLogger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DDTHH:mm:ss.SSSZ' }),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'facecode-audit' },
  transports: [
    esTransport,
    new winston.transports.File({
      filename: 'logs/audit.log',
      maxsize: 10485760, // 10MB
      maxFiles: 10,
    }),
    new winston.transports.Console({
      format: winston.format.combine(winston.format.colorize(), winston.format.simple()),
    }),
  ],
});

/**
 * Logs eventos de consentimiento
 */
function logConsent(data) {
  const encrypted = encryptSensitiveFields(data, ['user_id', 'ip_address', 'device_id']);

  auditLogger.info('consent_event', {
    event_type: 'consent',
    ...encrypted,
    retention_years: 5,
  });
}

/**
 * Logs eventos de eliminación
 */
function logDeletion(data) {
  const encrypted = encryptSensitiveFields(data, ['user_id']);

  auditLogger.info('deletion_event', {
    event_type: 'deletion',
    ...encrypted,
    retention_years: 5,
  });
}

/**
 * Logs eventos de acceso ARCO
 */
function logARCORequest(data) {
  const encrypted = encryptSensitiveFields(data, ['user_id', 'request_details']);

  auditLogger.info('arco_request', {
    event_type: 'arco',
    ...encrypted,
    retention_years: 5,
  });
}

/**
 * Cifra campos sensibles de un objeto
 */
function encryptSensitiveFields(obj, fields) {
  const result = { ...obj };

  fields.forEach((field) => {
    if (result[field]) {
      result[`${field}_encrypted`] = encryptField(String(result[field]));
      delete result[field]; // Eliminar campo original
    }
  });

  return result;
}

/**
 * Cifra un campo individual con AES-256-GCM
 */
function encryptField(plaintext) {
  const algorithm = 'aes-256-gcm';
  const key = Buffer.from(process.env.AUDIT_ENCRYPTION_KEY, 'hex');
  const iv = crypto.randomBytes(16);

  const cipher = crypto.createCipheriv(algorithm, key, iv);
  let encrypted = cipher.update(plaintext, 'utf8', 'hex');
  encrypted += cipher.final('hex');

  const authTag = cipher.getAuthTag().toString('hex');

  // Formato: iv:authTag:encryptedData
  return `${iv.toString('hex')}:${authTag}:${encrypted}`;
}

/**
 * Descifra un campo cifrado
 * (Solo para uso por personal autorizado con acceso a AUDIT_ENCRYPTION_KEY)
 */
function decryptField(encryptedData) {
  const algorithm = 'aes-256-gcm';
  const key = Buffer.from(process.env.AUDIT_ENCRYPTION_KEY, 'hex');

  const [ivHex, authTagHex, encrypted] = encryptedData.split(':');
  const iv = Buffer.from(ivHex, 'hex');
  const authTag = Buffer.from(authTagHex, 'hex');

  const decipher = crypto.createDecipheriv(algorithm, key, iv);
  decipher.setAuthTag(authTag);

  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');

  return decrypted;
}

module.exports = {
  auditLogger,
  logConsent,
  logDeletion,
  logARCORequest,
  encryptField,
  decryptField,
};
```

---

## 6. IMPLEMENTACIÓN DE DERECHOS ARCO

```javascript
// src/routes/arco.js
const express = require('express');
const { body, validationResult } = require('express-validator');
const db = require('../db');
const logger = require('../logger');
const { logARCORequest } = require('../logger/auditLogger');

const router = express.Router();

/**
 * POST /api/v1/arco/request
 * Crea una solicitud ARCO
 */
router.post(
  '/arco/request',
  [
    body('user_id').isUUID(4),
    body('request_type').isIn(['access', 'rectification', 'cancellation', 'opposition', 'portability', 'limitation']),
    body('request_details').isObject(),
  ],
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { user_id, request_type, request_details } = req.body;

    try {
      // Calcular deadline: 20 días hábiles (aproximadamente 28 días calendario)
      const deadline = new Date();
      deadline.setDate(deadline.getDate() + 28);

      const query = `
        INSERT INTO arco_requests (
          user_id,
          request_type,
          request_details,
          deadline
        ) VALUES ($1, $2, $3, $4)
        RETURNING request_id, created_at, deadline
      `;

      const result = await db.query(query, [
        user_id,
        request_type,
        JSON.stringify(request_details),
        deadline,
      ]);

      const arco = result.rows[0];

      // Log de auditoría
      logARCORequest({
        user_id,
        request_id: arco.request_id,
        request_type,
        created_at: arco.created_at,
      });

      res.status(201).json({
        success: true,
        request_id: arco.request_id,
        created_at: arco.created_at,
        deadline: arco.deadline,
        message: `Solicitud ARCO creada. Responderemos antes del ${arco.deadline.toLocaleDateString('es-MX')}`,
      });

    } catch (error) {
      logger.error('Error creating ARCO request', { error: error.message, user_id });
      res.status(500).json({ success: false, error: 'Failed to create ARCO request' });
    }
  }
);

/**
 * GET /api/v1/arco/request/:request_id
 * Consulta el estado de una solicitud ARCO
 */
router.get('/arco/request/:request_id', async (req, res) => {
  const { request_id } = req.params;

  try {
    const query = `
      SELECT
        request_id,
        user_id,
        request_type,
        status,
        created_at,
        deadline,
        completed_at,
        response_details
      FROM arco_requests
      WHERE request_id = $1
    `;

    const result = await db.query(query, [request_id]);

    if (result.rowCount === 0) {
      return res.status(404).json({ success: false, error: 'ARCO request not found' });
    }

    res.status(200).json({
      success: true,
      request: result.rows[0],
    });

  } catch (error) {
    logger.error('Error fetching ARCO request', { error: error.message, request_id });
    res.status(500).json({ success: false, error: 'Failed to fetch ARCO request' });
  }
});

/**
 * POST /api/v1/arco/export
 * Exporta datos personales del usuario (portabilidad)
 */
router.post('/arco/export', async (req, res) => {
  const { user_id } = req.body;

  try {
    // 1. Obtener datos del usuario
    const userData = await db.query('SELECT * FROM users WHERE user_id = $1', [user_id]);

    // 2. Obtener templates biométricos (solo metadatos, no el vector)
    const templates = await db.query(
      'SELECT template_id, template_version, created_at, expires_at FROM biometric_templates WHERE user_id = $1',
      [user_id]
    );

    // 3. Obtener consentimientos
    const consents = await db.query(
      'SELECT consent_id, timestamp_utc, tos_version, acceptance_method, revoked_at FROM consent_logs WHERE user_id = $1',
      [user_id]
    );

    // 4. Generar archivo de exportación (JSON)
    const exportData = {
      user: userData.rows[0],
      biometric_templates: templates.rows,
      consents: consents.rows,
      exported_at: new Date().toISOString(),
      format_version: '1.0',
    };

    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Content-Disposition', `attachment; filename="facecode-data-${user_id}.json"`);
    res.send(JSON.stringify(exportData, null, 2));

    // Log de auditoría
    logARCORequest({
      user_id,
      request_type: 'portability',
      exported_at: new Date(),
    });

  } catch (error) {
    logger.error('Error exporting user data', { error: error.message, user_id });
    res.status(500).json({ success: false, error: 'Failed to export user data' });
  }
});

module.exports = router;
```

---

## 7. SDK MÓVIL (iOS/ANDROID)

### 7.1 SDK iOS (Swift)

```swift
// FaceCodePrivacySDK.swift
import Foundation
import CryptoKit

public class FaceCodePrivacySDK {

    private let apiBaseURL: String
    private let apiKey: String

    public init(apiBaseURL: String, apiKey: String) {
        self.apiBaseURL = apiBaseURL
        self.apiKey = apiKey
    }

    /// Registra consentimiento del usuario
    public func registerConsent(
        userId: String,
        tosVersion: String,
        consentText: String,
        acceptanceMethod: AcceptanceMethod,
        completion: @escaping (Result<ConsentResponse, Error>) -> Void
    ) {
        guard let url = URL(string: "\(apiBaseURL)/api/v1/consent") else {
            completion(.failure(FaceCodeError.invalidURL))
            return
        }

        let deviceId = UIDevice.current.identifierForVendor?.uuidString ?? "unknown"

        let payload: [String: Any] = [
            "user_id": userId,
            "tos_version": tosVersion,
            "consent_text": consentText,
            "acceptance_method": acceptanceMethod.rawValue,
            "device_id": deviceId,
            "geolocation": Locale.current.regionCode ?? "XX"
        ]

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.httpBody = try? JSONSerialization.data(withJSONObject: payload)

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let data = data else {
                completion(.failure(FaceCodeError.noData))
                return
            }

            do {
                let consentResponse = try JSONDecoder().decode(ConsentResponse.self, from: data)
                completion(.success(consentResponse))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }

    /// Revoca consentimiento
    public func revokeConsent(
        userId: String,
        reason: String?,
        completion: @escaping (Result<RevocationResponse, Error>) -> Void
    ) {
        guard let url = URL(string: "\(apiBaseURL)/api/v1/consent/revoke") else {
            completion(.failure(FaceCodeError.invalidURL))
            return
        }

        let payload: [String: Any] = [
            "user_id": userId,
            "revocation_reason": reason ?? "User requested revocation"
        ]

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.httpBody = try? JSONSerialization.data(withJSONObject: payload)

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let data = data else {
                completion(.failure(FaceCodeError.noData))
                return
            }

            do {
                let revocationResponse = try JSONDecoder().decode(RevocationResponse.self, from: data)
                completion(.success(revocationResponse))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }

    /// Solicita eliminación de datos
    public func requestDeletion(
        userId: String,
        completion: @escaping (Result<DeletionResponse, Error>) -> Void
    ) {
        guard let url = URL(string: "\(apiBaseURL)/api/v1/deletion/request") else {
            completion(.failure(FaceCodeError.invalidURL))
            return
        }

        let payload: [String: Any] = ["user_id": userId]

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.httpBody = try? JSONSerialization.data(withJSONObject: payload)

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let data = data else {
                completion(.failure(FaceCodeError.noData))
                return
            }

            do {
                let deletionResponse = try JSONDecoder().decode(DeletionResponse.self, from: data)
                completion(.success(deletionResponse))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }
}

// MARK: - Models

public enum AcceptanceMethod: String, Codable {
    case explicitCheckbox = "explicit_checkbox"
    case biometric = "biometric"
    case electronicSignature = "electronic_signature"
    case parentalConsent = "parental_consent"
}

public struct ConsentResponse: Codable {
    let success: Bool
    let consentId: String
    let timestampUtc: String
    let message: String

    enum CodingKeys: String, CodingKey {
        case success
        case consentId = "consent_id"
        case timestampUtc = "timestamp_utc"
        case message
    }
}

public struct RevocationResponse: Codable {
    let success: Bool
    let message: String
    let revokedConsents: Int

    enum CodingKeys: String, CodingKey {
        case success, message
        case revokedConsents = "revoked_consents"
    }
}

public struct DeletionResponse: Codable {
    let success: Bool
    let jobId: String
    let certificateId: String
    let deletionTimestamp: String
    let recordsDeleted: RecordsDeleted
    let verificationUrl: String
    let downloadUrl: String

    enum CodingKeys: String, CodingKey {
        case success
        case jobId = "job_id"
        case certificateId = "certificate_id"
        case deletionTimestamp = "deletion_timestamp"
        case recordsDeleted = "records_deleted"
        case verificationUrl = "verification_url"
        case downloadUrl = "download_url"
    }
}

public struct RecordsDeleted: Codable {
    let biometricTemplates: Int
    let metadata: Int
    let logs: Int

    enum CodingKeys: String, CodingKey {
        case biometricTemplates = "biometric_templates"
        case metadata, logs
    }
}

public enum FaceCodeError: Error {
    case invalidURL
    case noData
    case invalidResponse
}
```

---

## 8. MONITORING Y ALERTAS

### 8.1 Métricas de Prometheus

```javascript
// src/metrics/privacyMetrics.js
const client = require('prom-client');

// Registro de Prometheus
const register = new client.Registry();

// Contador de consentimientos registrados
const consentCounter = new client.Counter({
  name: 'facecode_consents_total',
  help: 'Total de consentimientos registrados',
  labelNames: ['acceptance_method', 'tos_version'],
  registers: [register],
});

// Contador de revocaciones
const revocationCounter = new client.Counter({
  name: 'facecode_revocations_total',
  help: 'Total de revocaciones de consentimiento',
  labelNames: ['reason'],
  registers: [register],
});

// Contador de eliminaciones
const deletionCounter = new client.Counter({
  name: 'facecode_deletions_total',
  help: 'Total de eliminaciones de datos biométricos',
  labelNames: ['reason'], // 'auto_expiration', 'user_request', 'admin'
  registers: [register],
});

// Gauge de templates activos
const activeTemplatesGauge = new client.Gauge({
  name: 'facecode_active_templates',
  help: 'Número de templates biométricos activos',
  registers: [register],
});

// Histograma de tiempo de respuesta ARCO
const arcoResponseTime = new client.Histogram({
  name: 'facecode_arco_response_time_days',
  help: 'Tiempo de respuesta a solicitudes ARCO en días',
  buckets: [1, 3, 7, 14, 20, 30], // Días
  labelNames: ['request_type'],
  registers: [register],
});

// Actualizar gauge de templates activos cada 5 minutos
const db = require('../db');
setInterval(async () => {
  try {
    const result = await db.query('SELECT COUNT(*) as count FROM biometric_templates WHERE expires_at > NOW()');
    activeTemplatesGauge.set(parseInt(result.rows[0].count));
  } catch (error) {
    console.error('Error updating active templates gauge:', error);
  }
}, 300000); // 5 minutos

module.exports = {
  register,
  consentCounter,
  revocationCounter,
  deletionCounter,
  activeTemplatesGauge,
  arcoResponseTime,
};
```

### 8.2 Dashboard de Grafana (JSON)

```json
{
  "dashboard": {
    "title": "FaceCode Privacy Metrics",
    "panels": [
      {
        "title": "Consentimientos registrados (últimas 24h)",
        "targets": [
          {
            "expr": "rate(facecode_consents_total[24h])",
            "legendFormat": "{{acceptance_method}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Templates activos",
        "targets": [
          {
            "expr": "facecode_active_templates"
          }
        ],
        "type": "stat"
      },
      {
        "title": "Tiempo promedio de respuesta ARCO (días)",
        "targets": [
          {
            "expr": "avg(facecode_arco_response_time_days)",
            "legendFormat": "{{request_type}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Eliminaciones por tipo",
        "targets": [
          {
            "expr": "facecode_deletions_total",
            "legendFormat": "{{reason}}"
          }
        ],
        "type": "piechart"
      }
    ]
  }
}
```

---

## CONCLUSIÓN

Esta documentación técnica provee:

✅ **Schemas SQL completos** para PostgreSQL con retenciones diferenciadas
✅ **Endpoints RESTful** para consentimiento, ARCO y eliminación
✅ **Jobs automatizados** para eliminación de templates expirados
✅ **Logging cifrado** con AES-256-GCM para auditoría
✅ **SDK móvil** (iOS) listo para integración
✅ **Monitoring** con Prometheus + Grafana
✅ **Certificados de eliminación** verificables con QR y PDF

**Próximos pasos:**

1. Implementar endpoints en backend (Node.js/Python)
2. Configurar cron jobs de eliminación
3. Integrar SDK en apps móviles iOS/Android
4. Configurar dashboards de Grafana
5. Realizar pruebas end-to-end del flujo ARCO
6. Validar con auditor de seguridad externo

---

**© 2025 FaceCode® Guardian Network**
*Implementación técnica alineada con LFPDPPP 2025*

**Última actualización:** 2025-10-29
**Stack:** Node.js + PostgreSQL + Redis + BullMQ + Prometheus
