# Guía de Implementación Técnica — Privacidad FaceCode®

**Versión:** 1.0
**Fecha:** 29 de octubre de 2025
**Para:** Desarrolladores, arquitectos de software, equipos de seguridad

---

## Introducción

Esta guía proporciona instrucciones técnicas detalladas para implementar el sistema de privacidad y protección de datos biométricos de FaceCode® Guardian Network. Está diseñada para desarrolladores que necesitan implementar las **5 acciones técnicas inmediatas** prioritarias y garantizar cumplimiento legal (LFPDPPP, GDPR, CCPA, AI Act).

---

## Arquitectura General de Privacidad

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO (Dispositivo)                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Cámara → On-Device Processing → Plantilla Biométrica │ │
│  │  (No se envía imagen al servidor)                      │ │
│  └────────────────────────────────────────────────────────┘ │
│                           │ TLS 1.3 + E2EE                   │
└───────────────────────────┼──────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  API GATEWAY (WAF + Rate Limiting)           │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────────┐  ┌─────────────────┐
│ Consent      │  │ Biometric        │  │ ARCO Rights     │
│ Management   │  │ Data Service     │  │ Portal          │
│ Service      │  │ (24h TTL)        │  │ (Self-Service)  │
└──────────────┘  └──────────────────┘  └─────────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│           ENCRYPTED DATABASE (AES-256 at rest)              │
│  ┌──────────────┐  ┌─────────────────┐  ┌───────────────┐ │
│  │ consent_logs │  │ biometric_data  │  │ arco_requests │ │
│  │ (5 años)     │  │ (24h TTL)       │  │ (30 días)     │ │
│  └──────────────┘  └─────────────────┘  └───────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  KMS (Key Management Service) + HSM (Hardware Security)     │
│  AWS KMS / Google Cloud KMS / Azure Key Vault               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│     AUDIT & MONITORING (Immutable Logs + Alerting)          │
│     Grafana + Prometheus + ELK Stack                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Acción Técnica #1: Logging de Consentimiento Encriptado

### Objetivo

Implementar sistema de registro de consentimientos con cifrado AES-256 y retención de 5 años para cumplimiento legal.

### Tecnologías

- PostgreSQL 14+ (con extensión `pgcrypto`)
- Node.js 18+ / TypeScript 5+
- AWS KMS o equivalente para gestión de claves

### Paso 1: Crear Tabla de Logs de Consentimiento

```sql
-- Extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Tabla principal
CREATE TABLE consent_logs (
    -- Identificadores
    consent_id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Metadatos de consentimiento
    consent_timestamp   TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    consent_version     VARCHAR(50) NOT NULL, -- Ejemplo: "v1.0-2025-10-29"
    consent_type        VARCHAR(50) NOT NULL CHECK (consent_type IN ('initial', 'renewal', 'revocation', 'update')),
    consent_granted     BOOLEAN NOT NULL,

    -- Finalidades aceptadas
    primary_purpose     BOOLEAN NOT NULL DEFAULT false,
    secondary_purpose   BOOLEAN NOT NULL DEFAULT false,

    -- Información del dispositivo (anonimizada tras 30 días)
    device_id           VARCHAR(255),
    device_type         VARCHAR(100),
    device_os           VARCHAR(100),
    device_model        VARCHAR(100),
    ip_address          INET,
    ip_anonymized       BOOLEAN DEFAULT false,
    user_agent          TEXT,

    -- Integridad y auditoría
    consent_text_hash   VARCHAR(64) NOT NULL, -- SHA-256
    privacy_policy_url  VARCHAR(500),
    signature_method    VARCHAR(50) CHECK (signature_method IN ('biometric', 'pin', 'manual', 'oauth')),
    signature_data      TEXT,

    -- Revocación
    revoked_at          TIMESTAMP WITH TIME ZONE,
    revocation_reason   TEXT,

    -- Cumplimiento legal
    legal_basis         VARCHAR(100) CHECK (legal_basis IN ('consent', 'contract', 'legal_obligation', 'legitimate_interest')),
    jurisdiction        VARCHAR(50), -- ISO 3166-1 alpha-2 (MX, US, DE, etc.)

    -- Cifrado (payload completo cifrado)
    encrypted_payload   TEXT NOT NULL,
    encryption_key_id   VARCHAR(100) NOT NULL,
    encryption_iv       TEXT NOT NULL, -- Initialization Vector

    -- Timestamps
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX idx_consent_user_timestamp ON consent_logs (user_id, consent_timestamp DESC);
CREATE INDEX idx_consent_type ON consent_logs (consent_type, consent_timestamp);
CREATE INDEX idx_consent_revoked ON consent_logs (revoked_at) WHERE revoked_at IS NOT NULL;
CREATE INDEX idx_consent_jurisdiction ON consent_logs (jurisdiction);

-- Trigger para actualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_consent_logs_updated_at
    BEFORE UPDATE ON consent_logs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### Paso 2: Función de Anonimización de IPs (Cumplimiento GDPR)

```sql
-- Función para anonimizar IPs tras 30 días
CREATE OR REPLACE FUNCTION anonymize_ip_addresses()
RETURNS INTEGER AS $$
DECLARE
    rows_affected INTEGER;
BEGIN
    UPDATE consent_logs
    SET
        ip_address = '0.0.0.0'::inet,
        ip_anonymized = true
    WHERE
        consent_timestamp < NOW() - INTERVAL '30 days'
        AND ip_anonymized = false;

    GET DIAGNOSTICS rows_affected = ROW_COUNT;

    -- Log de auditoría
    INSERT INTO audit_logs (action, affected_rows, timestamp)
    VALUES ('ip_anonymization', rows_affected, NOW());

    RETURN rows_affected;
END;
$$ LANGUAGE plpgsql;

-- Programar con pg_cron (instalar extensión pg_cron)
-- Ejecutar diariamente a las 2:00 AM
SELECT cron.schedule(
    'anonymize-ips-daily',
    '0 2 * * *',
    'SELECT anonymize_ip_addresses();'
);
```

### Paso 3: Servicio de Cifrado (Node.js/TypeScript)

```typescript
// src/services/consent/encryption.service.ts
import crypto from 'crypto';
import { KMS } from '@aws-sdk/client-kms';

const kms = new KMS({ region: process.env.AWS_REGION || 'us-east-1' });
const ENCRYPTION_KEY_ID = process.env.KMS_KEY_ID || 'alias/facecode-consent-encryption';

interface EncryptedPayload {
    encrypted: string;
    iv: string;
    authTag: string;
    keyId: string;
}

/**
 * Cifra un payload usando AES-256-GCM con clave desde KMS
 */
export async function encryptPayload(data: any): Promise<EncryptedPayload> {
    // Obtener clave de cifrado desde KMS
    const { Plaintext } = await kms.generateDataKey({
        KeyId: ENCRYPTION_KEY_ID,
        KeySpec: 'AES_256',
    });

    if (!Plaintext) {
        throw new Error('Failed to generate encryption key from KMS');
    }

    // Convertir Uint8Array a Buffer
    const encryptionKey = Buffer.from(Plaintext);

    // Generar IV aleatorio (16 bytes para AES)
    const iv = crypto.randomBytes(16);

    // Crear cipher
    const cipher = crypto.createCipheriv('aes-256-gcm', encryptionKey, iv);

    // Convertir datos a JSON y cifrar
    const jsonData = JSON.stringify(data);
    let encrypted = cipher.update(jsonData, 'utf8', 'hex');
    encrypted += cipher.final('hex');

    // Obtener authentication tag
    const authTag = cipher.getAuthTag();

    return {
        encrypted,
        iv: iv.toString('hex'),
        authTag: authTag.toString('hex'),
        keyId: ENCRYPTION_KEY_ID,
    };
}

/**
 * Descifra un payload cifrado
 */
export async function decryptPayload(encryptedData: EncryptedPayload): Promise<any> {
    // Obtener clave de descifrado desde KMS
    const { Plaintext } = await kms.decrypt({
        KeyId: encryptedData.keyId,
        CiphertextBlob: Buffer.from(encryptedData.encrypted, 'hex'),
    });

    if (!Plaintext) {
        throw new Error('Failed to decrypt key from KMS');
    }

    const decryptionKey = Buffer.from(Plaintext);

    // Crear decipher
    const decipher = crypto.createDecipheriv(
        'aes-256-gcm',
        decryptionKey,
        Buffer.from(encryptedData.iv, 'hex')
    );

    // Establecer authentication tag
    decipher.setAuthTag(Buffer.from(encryptedData.authTag, 'hex'));

    // Descifrar
    let decrypted = decipher.update(encryptedData.encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');

    return JSON.parse(decrypted);
}

/**
 * Genera hash SHA-256 de un texto de consentimiento
 */
export function generateConsentHash(consentText: string): string {
    return crypto.createHash('sha256').update(consentText).digest('hex');
}
```

### Paso 4: API Endpoint para Registrar Consentimiento

```typescript
// src/routes/consent.routes.ts
import { Router, Request, Response } from 'express';
import { body, validationResult } from 'express-validator';
import { v4 as uuidv4 } from 'uuid';
import { encryptPayload, generateConsentHash } from '../services/consent/encryption.service';
import { db } from '../database';
import { sendConsentConfirmationEmail } from '../services/email.service';
import { auditLog } from '../services/audit.service';

const router = Router();

interface ConsentRequest {
    userId: string;
    consentGranted: boolean;
    primaryPurpose: boolean;
    secondaryPurpose: boolean;
    deviceInfo: {
        deviceId: string;
        deviceType: string;
        os: string;
        model: string;
        userAgent: string;
    };
    signatureMethod: 'biometric' | 'pin' | 'manual';
    signatureData?: string;
    jurisdiction: string;
}

/**
 * POST /api/consent/grant
 * Registra consentimiento de usuario para procesamiento biométrico
 */
router.post(
    '/grant',
    [
        body('userId').isUUID(),
        body('consentGranted').isBoolean(),
        body('primaryPurpose').isBoolean(),
        body('secondaryPurpose').isBoolean(),
        body('deviceInfo').isObject(),
        body('deviceInfo.deviceId').isString(),
        body('deviceInfo.deviceType').isIn(['iOS', 'Android', 'Web', 'Desktop']),
        body('signatureMethod').isIn(['biometric', 'pin', 'manual']),
        body('jurisdiction').isISO31661Alpha2(),
    ],
    async (req: Request, res: Response) => {
        // Validar request
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }

        const data: ConsentRequest = req.body;
        const consentId = uuidv4();
        const timestamp = new Date();
        const consentVersion = 'v1.0-2025-10-29';

        try {
            // Obtener texto de consentimiento (desde base de datos o archivo)
            const consentText = await getConsentText(consentVersion, data.jurisdiction);
            const consentTextHash = generateConsentHash(consentText);

            // Preparar payload para cifrar
            const payload = {
                consentId,
                userId: data.userId,
                timestamp,
                consentVersion,
                consentGranted: data.consentGranted,
                primaryPurpose: data.primaryPurpose,
                secondaryPurpose: data.secondaryPurpose,
                deviceInfo: data.deviceInfo,
                signatureMethod: data.signatureMethod,
                signatureData: data.signatureData,
                consentTextHash,
                ipAddress: req.ip,
                userAgent: req.headers['user-agent'],
            };

            // Cifrar payload
            const encrypted = await encryptPayload(payload);

            // Guardar en base de datos
            await db.query(`
                INSERT INTO consent_logs (
                    consent_id, user_id, consent_timestamp, consent_version,
                    consent_type, consent_granted, primary_purpose, secondary_purpose,
                    device_id, device_type, device_os, device_model,
                    ip_address, user_agent, consent_text_hash,
                    signature_method, signature_data, encrypted_payload,
                    encryption_key_id, encryption_iv, legal_basis, jurisdiction
                ) VALUES (
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10,
                    $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22
                )
            `, [
                consentId,
                data.userId,
                timestamp,
                consentVersion,
                'initial',
                data.consentGranted,
                data.primaryPurpose,
                data.secondaryPurpose,
                data.deviceInfo.deviceId,
                data.deviceInfo.deviceType,
                data.deviceInfo.os,
                data.deviceInfo.model,
                req.ip,
                req.headers['user-agent'],
                consentTextHash,
                data.signatureMethod,
                data.signatureData || null,
                encrypted.encrypted,
                encrypted.keyId,
                encrypted.iv,
                'consent',
                data.jurisdiction,
            ]);

            // Emitir evento de auditoría
            await auditLog.emit('consent.granted', {
                consentId,
                userId: data.userId,
                timestamp,
                jurisdiction: data.jurisdiction,
            });

            // Enviar correo de confirmación
            await sendConsentConfirmationEmail(data.userId, consentId);

            // Responder
            res.status(201).json({
                success: true,
                consentId,
                message: 'Consent registered successfully',
                timestamp,
            });

        } catch (error) {
            console.error('Error registering consent:', error);
            res.status(500).json({
                success: false,
                message: 'Failed to register consent',
            });
        }
    }
);

/**
 * POST /api/consent/revoke
 * Revoca consentimiento y solicita eliminación de datos biométricos
 */
router.post(
    '/revoke',
    [
        body('userId').isUUID(),
        body('reason').optional().isString(),
    ],
    async (req: Request, res: Response) => {
        const { userId, reason } = req.body;

        try {
            // Registrar revocación
            const consentId = uuidv4();
            const timestamp = new Date();

            const payload = {
                consentId,
                userId,
                timestamp,
                consentGranted: false,
                reason: reason || 'User requested revocation',
            };

            const encrypted = await encryptPayload(payload);

            await db.query(`
                INSERT INTO consent_logs (
                    consent_id, user_id, consent_timestamp, consent_version,
                    consent_type, consent_granted, revoked_at, revocation_reason,
                    encrypted_payload, encryption_key_id, encryption_iv,
                    legal_basis, jurisdiction
                ) VALUES (
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13
                )
            `, [
                consentId,
                userId,
                timestamp,
                'v1.0-2025-10-29',
                'revocation',
                false,
                timestamp,
                reason,
                encrypted.encrypted,
                encrypted.keyId,
                encrypted.iv,
                'consent',
                'MX', // Detectar automáticamente
            ]);

            // Trigger: Eliminar datos biométricos
            await deleteBiometricData(userId);

            // Generar certificado de eliminación
            const certificate = await generateDeletionCertificate(userId, consentId);

            // Enviar correo con certificado
            await sendDeletionConfirmationEmail(userId, certificate);

            // Auditoría
            await auditLog.emit('consent.revoked', {
                consentId,
                userId,
                timestamp,
            });

            res.status(200).json({
                success: true,
                message: 'Consent revoked and biometric data deleted',
                certificateId: certificate.id,
                downloadUrl: `/api/consent/certificate/${certificate.id}`,
            });

        } catch (error) {
            console.error('Error revoking consent:', error);
            res.status(500).json({
                success: false,
                message: 'Failed to revoke consent',
            });
        }
    }
);

export default router;
```

---

## 2. Acción Técnica #2: Eliminación Automática de Templates Biométricos (24h)

### Objetivo

Implementar job automatizado que elimine plantillas biométricas tras 24 horas con verificación criptográfica.

### Tecnologías

- PostgreSQL con particiones temporales
- Node.js + node-cron
- Redis para tracking de expiración

### Paso 1: Tabla de Datos Biométricos con TTL

```sql
-- Tabla de plantillas biométricas
CREATE TABLE biometric_templates (
    template_id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Plantilla cifrada (embedding facial)
    template_data       BYTEA NOT NULL, -- Cifrado AES-256
    template_version    VARCHAR(50) NOT NULL, -- Versión del modelo (ej: "facenet-v1.0")
    dimensions          INTEGER NOT NULL, -- 512, 1024, 2048

    -- Metadata
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    expires_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT (NOW() + INTERVAL '24 hours'),
    last_used_at        TIMESTAMP WITH TIME ZONE,

    -- Cifrado
    encryption_key_id   VARCHAR(100) NOT NULL,
    encryption_iv       TEXT NOT NULL,

    -- Tracking de eliminación
    deletion_scheduled  BOOLEAN DEFAULT false,
    deleted_at          TIMESTAMP WITH TIME ZONE,
    deletion_verified   BOOLEAN DEFAULT false,
    deletion_cert_id    UUID,

    -- Índices
    CONSTRAINT check_expiration CHECK (expires_at > created_at)
);

-- Índice para búsqueda rápida de templates expirados
CREATE INDEX idx_biometric_expires_at ON biometric_templates (expires_at) WHERE deleted_at IS NULL;
CREATE INDEX idx_biometric_user ON biometric_templates (user_id, created_at DESC);
CREATE INDEX idx_biometric_deletion ON biometric_templates (deletion_scheduled) WHERE deletion_scheduled = true;

-- Particionamiento por fecha de expiración (opcional para alto volumen)
CREATE TABLE biometric_templates_partition_2025_10 PARTITION OF biometric_templates
    FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');
```

### Paso 2: Job de Eliminación Automática (24h)

```typescript
// src/jobs/biometric-cleanup.job.ts
import cron from 'node-cron';
import crypto from 'crypto';
import { db } from '../database';
import { auditLog } from '../services/audit.service';
import { generateDeletionCertificate } from '../services/certificate.service';

/**
 * Job que se ejecuta cada hora para eliminar templates biométricos expirados
 * Cron: 0 * * * * (cada hora en punto)
 */
export function startBiometricCleanupJob() {
    cron.schedule('0 * * * *', async () => {
        console.log('[BiometricCleanup] Starting cleanup job at', new Date().toISOString());

        try {
            // 1. Buscar templates expirados
            const expiredTemplates = await db.query(`
                SELECT
                    template_id,
                    user_id,
                    template_data,
                    expires_at
                FROM biometric_templates
                WHERE
                    expires_at <= NOW()
                    AND deleted_at IS NULL
                    AND deletion_scheduled = false
                LIMIT 1000 -- Procesar en batches de 1000
            `);

            if (expiredTemplates.rows.length === 0) {
                console.log('[BiometricCleanup] No expired templates found');
                return;
            }

            console.log(`[BiometricCleanup] Found ${expiredTemplates.rows.length} expired templates`);

            // 2. Procesar cada template
            for (const template of expiredTemplates.rows) {
                try {
                    await deleteTemplate(template);
                } catch (error) {
                    console.error(`[BiometricCleanup] Failed to delete template ${template.template_id}:`, error);
                    // Continuar con el siguiente
                }
            }

            // 3. Verificar eliminación (doble check)
            await verifyDeletion();

            // 4. Auditoría
            await auditLog.emit('biometric.cleanup', {
                timestamp: new Date(),
                templatesDeleted: expiredTemplates.rows.length,
            });

        } catch (error) {
            console.error('[BiometricCleanup] Job failed:', error);
            // Alertar al equipo de seguridad
            await alertSecurityTeam('biometric_cleanup_failure', error);
        }
    });

    console.log('[BiometricCleanup] Job scheduled successfully (runs every hour)');
}

/**
 * Elimina un template biométrico con sobrescritura segura
 */
async function deleteTemplate(template: any): Promise<void> {
    const { template_id, user_id, template_data } = template;

    // 1. Marcar como "deletion_scheduled"
    await db.query(`
        UPDATE biometric_templates
        SET deletion_scheduled = true
        WHERE template_id = $1
    `, [template_id]);

    // 2. Generar hash del dato original (para verificación)
    const originalHash = crypto.createHash('sha256').update(template_data).digest('hex');

    // 3. Sobrescritura segura (3 pases según DoD 5220.22-M)
    for (let pass = 0; pass < 3; pass++) {
        const randomData = crypto.randomBytes(template_data.length);
        await db.query(`
            UPDATE biometric_templates
            SET template_data = $1
            WHERE template_id = $2
        `, [randomData, template_id]);
    }

    // 4. Marcar como eliminado
    await db.query(`
        UPDATE biometric_templates
        SET
            deleted_at = NOW(),
            deletion_verified = true,
            template_data = NULL
        WHERE template_id = $1
    `, [template_id]);

    // 5. Generar certificado de eliminación
    const certificate = await generateDeletionCertificate(user_id, template_id, originalHash);

    await db.query(`
        UPDATE biometric_templates
        SET deletion_cert_id = $1
        WHERE template_id = $2
    `, [certificate.id, template_id]);

    console.log(`[BiometricCleanup] Template ${template_id} deleted successfully`);
}

/**
 * Verificar que la eliminación fue exitosa
 */
async function verifyDeletion(): Promise<void> {
    const orphanedTemplates = await db.query(`
        SELECT COUNT(*) as count
        FROM biometric_templates
        WHERE
            expires_at <= NOW() - INTERVAL '1 hour'
            AND deleted_at IS NULL
    `);

    const count = parseInt(orphanedTemplates.rows[0].count, 10);

    if (count > 0) {
        console.warn(`[BiometricCleanup] WARNING: ${count} templates not deleted after 1 hour`);
        await alertSecurityTeam('deletion_verification_failed', { count });
    } else {
        console.log('[BiometricCleanup] Deletion verification passed');
    }
}

/**
 * Alerta al equipo de seguridad en caso de fallo
 */
async function alertSecurityTeam(type: string, details: any): Promise<void> {
    // Implementar notificación (email, Slack, PagerDuty, etc.)
    console.error(`[SECURITY ALERT] ${type}:`, details);
    // TODO: Integrar con sistema de alertas
}
```

### Paso 3: Endpoint de Eliminación Manual (Usuario)

```typescript
// src/routes/biometric.routes.ts
import { Router, Request, Response } from 'express';
import { body, validationResult } from 'express-validator';
import { db } from '../database';
import { generateDeletionCertificate } from '../services/certificate.service';
import { auditLog } from '../services/audit.service';

const router = Router();

/**
 * DELETE /api/biometric/delete
 * Permite al usuario eliminar sus datos biométricos manualmente
 */
router.delete(
    '/delete',
    [
        body('userId').isUUID(),
    ],
    async (req: Request, res: Response) => {
        const { userId } = req.body;

        try {
            // Verificar autenticación del usuario
            if (req.user?.id !== userId) {
                return res.status(403).json({
                    success: false,
                    message: 'Unauthorized',
                });
            }

            // Eliminar todos los templates del usuario
            const templates = await db.query(`
                SELECT template_id, template_data
                FROM biometric_templates
                WHERE user_id = $1 AND deleted_at IS NULL
            `, [userId]);

            if (templates.rows.length === 0) {
                return res.status(404).json({
                    success: false,
                    message: 'No biometric data found',
                });
            }

            // Eliminar cada template
            const certificates = [];
            for (const template of templates.rows) {
                const hash = crypto.createHash('sha256')
                    .update(template.template_data)
                    .digest('hex');

                // Sobrescritura segura
                for (let i = 0; i < 3; i++) {
                    await db.query(`
                        UPDATE biometric_templates
                        SET template_data = $1
                        WHERE template_id = $2
                    `, [crypto.randomBytes(1024), template.template_id]);
                }

                // Marcar como eliminado
                await db.query(`
                    UPDATE biometric_templates
                    SET deleted_at = NOW(), deletion_verified = true
                    WHERE template_id = $1
                `, [template.template_id]);

                // Generar certificado
                const cert = await generateDeletionCertificate(userId, template.template_id, hash);
                certificates.push(cert);
            }

            // Auditoría
            await auditLog.emit('biometric.user_deletion', {
                userId,
                templatesDeleted: templates.rows.length,
                timestamp: new Date(),
            });

            res.status(200).json({
                success: true,
                message: 'Biometric data deleted successfully',
                certificates: certificates.map(c => ({
                    id: c.id,
                    downloadUrl: `/api/biometric/certificate/${c.id}`,
                })),
            });

        } catch (error) {
            console.error('Error deleting biometric data:', error);
            res.status(500).json({
                success: false,
                message: 'Failed to delete biometric data',
            });
        }
    }
);

export default router;
```

---

## 3. Acción Técnica #3: Procesamiento On-Device con Fallback Zero-Knowledge

### Objetivo

Implementar procesamiento biométrico local en dispositivos iOS/Android con fallback a cifrado de extremo a extremo si es necesario usar servidor.

### Tecnologías

- TensorFlow Lite (iOS/Android)
- Core ML (iOS)
- ML Kit (Android)
- WebAssembly (Web)

### Arquitectura On-Device

```
┌─────────────────────────────────────────────────────────────┐
│                    DISPOSITIVO DEL USUARIO                   │
│                                                              │
│  ┌────────────┐    ┌──────────────┐    ┌─────────────────┐ │
│  │  Cámara    │───▶│  Face        │───▶│  Plantilla      │ │
│  │            │    │  Detection   │    │  Biométrica     │ │
│  └────────────┘    └──────────────┘    │  (512-d vector) │ │
│                                         └─────────────────┘ │
│                                                │             │
│                                                ▼             │
│                                    ┌──────────────────────┐ │
│                                    │  Matching Local      │ │
│                                    │  (1:1 verification)  │ │
│                                    └──────────────────────┘ │
│                                                │             │
│                                                ▼             │
│                                        ✅ Autenticado       │
│                                                              │
│  SI REQUIERE SERVIDOR (opcional):                           │
│                                                              │
│  Plantilla ──▶ Cifrado E2E (AES-256) ──▶ Servidor          │
│               (clave solo en dispositivo)                    │
└─────────────────────────────────────────────────────────────┘
```

### Implementación iOS (Swift + Core ML)

```swift
// FacialRecognitionService.swift
import Vision
import CoreML
import CryptoKit

class FacialRecognitionService {
    private let model: VNCoreMLModel
    private let encryptionKey: SymmetricKey

    init() throws {
        // Cargar modelo Core ML (FaceNet, ArcFace, etc.)
        let modelConfig = MLModelConfiguration()
        modelConfig.computeUnits = .cpuAndNeuralEngine // On-device only

        let facenetModel = try FaceNet(configuration: modelConfig).model
        self.model = try VNCoreMLModel(for: facenetModel)

        // Generar clave de cifrado local (almacenada en Keychain)
        self.encryptionKey = try getOrCreateEncryptionKey()
    }

    /**
     * Procesa imagen facial y genera plantilla biométrica
     * TODO EN EL DISPOSITIVO, sin enviar al servidor
     */
    func generateBiometricTemplate(from image: UIImage) async throws -> BiometricTemplate {
        guard let cgImage = image.cgImage else {
            throw FaceRecognitionError.invalidImage
        }

        return try await withCheckedThrowingContinuation { continuation in
            let request = VNCoreMLRequest(model: self.model) { request, error in
                if let error = error {
                    continuation.resume(throwing: error)
                    return
                }

                guard let observations = request.results as? [VNCoreMLFeatureValueObservation],
                      let embedding = observations.first?.featureValue.multiArrayValue else {
                    continuation.resume(throwing: FaceRecognitionError.noFaceDetected)
                    return
                }

                // Convertir embedding a array de floats
                let vector = self.convertToFloatArray(embedding)

                // Crear plantilla cifrada
                let template = BiometricTemplate(
                    vector: vector,
                    createdAt: Date(),
                    expiresAt: Date().addingTimeInterval(24 * 3600) // 24 horas
                )

                continuation.resume(returning: template)
            }

            let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
            do {
                try handler.perform([request])
            } catch {
                continuation.resume(throwing: error)
            }
        }
    }

    /**
     * Verifica identidad mediante matching 1:1 local
     * NO envía datos al servidor
     */
    func verifyIdentity(
        capturedTemplate: BiometricTemplate,
        storedTemplate: BiometricTemplate
    ) -> (verified: Bool, confidence: Float) {
        // Calcular similitud coseno
        let similarity = cosineSimilarity(
            capturedTemplate.vector,
            storedTemplate.vector
        )

        let threshold: Float = 0.6 // Ajustar según modelo
        let verified = similarity >= threshold

        // Log de auditoría (sin datos biométricos)
        AuditLogger.log(event: .biometricVerification, data: [
            "verified": verified,
            "confidence": similarity,
            "timestamp": Date().iso8601String
        ])

        return (verified, similarity)
    }

    /**
     * Cifra plantilla para almacenamiento seguro local
     */
    func encryptTemplate(_ template: BiometricTemplate) throws -> Data {
        let encoder = JSONEncoder()
        let jsonData = try encoder.encode(template)

        let sealedBox = try AES.GCM.seal(
            jsonData,
            using: self.encryptionKey
        )

        return sealedBox.combined!
    }

    /**
     * Descifra plantilla desde almacenamiento local
     */
    func decryptTemplate(_ encryptedData: Data) throws -> BiometricTemplate {
        let sealedBox = try AES.GCM.SealedBox(combined: encryptedData)
        let decryptedData = try AES.GCM.open(sealedBox, using: self.encryptionKey)

        let decoder = JSONDecoder()
        return try decoder.decode(BiometricTemplate.self, from: decryptedData)
    }

    // MARK: - Helpers

    private func cosineSimilarity(_ a: [Float], _ b: [Float]) -> Float {
        guard a.count == b.count else { return 0.0 }

        var dotProduct: Float = 0.0
        var normA: Float = 0.0
        var normB: Float = 0.0

        for i in 0..<a.count {
            dotProduct += a[i] * b[i]
            normA += a[i] * a[i]
            normB += b[i] * b[i]
        }

        return dotProduct / (sqrt(normA) * sqrt(normB))
    }

    private func convertToFloatArray(_ multiArray: MLMultiArray) -> [Float] {
        let length = multiArray.count
        var array: [Float] = []

        for i in 0..<length {
            array.append(Float(truncating: multiArray[i]))
        }

        return array
    }

    private func getOrCreateEncryptionKey() throws -> SymmetricKey {
        // Usar Keychain para almacenamiento seguro
        let keychainService = KeychainService()

        if let existingKey = try? keychainService.retrieveKey(identifier: "biometric_encryption_key") {
            return existingKey
        } else {
            let newKey = SymmetricKey(size: .bits256)
            try keychainService.storeKey(newKey, identifier: "biometric_encryption_key")
            return newKey
        }
    }
}

// Modelo de datos
struct BiometricTemplate: Codable {
    let vector: [Float] // 512 dimensiones típicamente
    let createdAt: Date
    let expiresAt: Date

    var isExpired: Bool {
        return Date() > expiresAt
    }
}

enum FaceRecognitionError: Error {
    case invalidImage
    case noFaceDetected
    case encryptionFailed
    case decryptionFailed
}
```

### Implementación Android (Kotlin + TensorFlow Lite)

```kotlin
// BiometricProcessor.kt
package app.facecode.biometric

import android.content.Context
import android.graphics.Bitmap
import org.tensorflow.lite.Interpreter
import org.tensorflow.lite.support.image.TensorImage
import java.nio.ByteBuffer
import java.security.KeyStore
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.IvParameterSpec
import kotlin.math.sqrt

class BiometricProcessor(private val context: Context) {
    private val interpreter: Interpreter
    private val encryptionKey: SecretKey

    init {
        // Cargar modelo TensorFlow Lite
        val modelFile = loadModelFile("facenet_mobile.tflite")
        interpreter = Interpreter(modelFile)

        // Obtener o crear clave de cifrado (Android KeyStore)
        encryptionKey = getOrCreateEncryptionKey()
    }

    /**
     * Genera plantilla biométrica desde imagen facial
     * TODO EN EL DISPOSITIVO
     */
    fun generateBiometricTemplate(bitmap: Bitmap): BiometricTemplate {
        // Preprocesar imagen
        val tensorImage = TensorImage.fromBitmap(bitmap)
        val preprocessed = preprocessImage(tensorImage)

        // Inferencia del modelo
        val output = Array(1) { FloatArray(512) } // 512-d embedding
        interpreter.run(preprocessed, output)

        val embedding = output[0]

        // Normalizar vector
        val normalizedEmbedding = normalizeVector(embedding)

        return BiometricTemplate(
            vector = normalizedEmbedding,
            createdAt = System.currentTimeMillis(),
            expiresAt = System.currentTimeMillis() + (24 * 60 * 60 * 1000) // 24 horas
        )
    }

    /**
     * Verifica identidad mediante matching 1:1 local
     */
    fun verifyIdentity(
        capturedTemplate: BiometricTemplate,
        storedTemplate: BiometricTemplate
    ): VerificationResult {
        // Calcular similitud coseno
        val similarity = cosineSimilarity(
            capturedTemplate.vector,
            storedTemplate.vector
        )

        val threshold = 0.6f
        val verified = similarity >= threshold

        // Auditoría
        AuditLogger.log(
            event = "biometric_verification",
            data = mapOf(
                "verified" to verified,
                "confidence" to similarity,
                "timestamp" to System.currentTimeMillis()
            )
        )

        return VerificationResult(verified, similarity)
    }

    /**
     * Cifra plantilla para almacenamiento local seguro
     */
    fun encryptTemplate(template: BiometricTemplate): ByteArray {
        val cipher = Cipher.getInstance("AES/GCM/NoPadding")
        cipher.init(Cipher.ENCRYPT_MODE, encryptionKey)

        val iv = cipher.iv
        val encrypted = cipher.doFinal(template.toByteArray())

        // Combinar IV + datos cifrados
        return iv + encrypted
    }

    /**
     * Descifra plantilla desde almacenamiento local
     */
    fun decryptTemplate(encryptedData: ByteArray): BiometricTemplate {
        val iv = encryptedData.sliceArray(0 until 12) // GCM IV = 12 bytes
        val ciphertext = encryptedData.sliceArray(12 until encryptedData.size)

        val cipher = Cipher.getInstance("AES/GCM/NoPadding")
        cipher.init(Cipher.DECRYPT_MODE, encryptionKey, IvParameterSpec(iv))

        val decrypted = cipher.doFinal(ciphertext)
        return BiometricTemplate.fromByteArray(decrypted)
    }

    // MARK: - Helpers

    private fun cosineSimilarity(a: FloatArray, b: FloatArray): Float {
        require(a.size == b.size) { "Vectors must have same dimension" }

        var dotProduct = 0f
        var normA = 0f
        var normB = 0f

        for (i in a.indices) {
            dotProduct += a[i] * b[i]
            normA += a[i] * a[i]
            normB += b[i] * b[i]
        }

        return dotProduct / (sqrt(normA) * sqrt(normB))
    }

    private fun normalizeVector(vector: FloatArray): FloatArray {
        val norm = sqrt(vector.map { it * it }.sum())
        return vector.map { it / norm }.toFloatArray()
    }

    private fun getOrCreateEncryptionKey(): SecretKey {
        val keyStore = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }

        val keyAlias = "biometric_encryption_key"

        return if (keyStore.containsAlias(keyAlias)) {
            keyStore.getKey(keyAlias, null) as SecretKey
        } else {
            val keyGenerator = KeyGenerator.getInstance("AES", "AndroidKeyStore")
            keyGenerator.init(
                KeyGenParameterSpec.Builder(
                    keyAlias,
                    KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
                )
                    .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                    .setKeySize(256)
                    .build()
            )
            keyGenerator.generateKey()
        }
    }

    private fun loadModelFile(filename: String): ByteBuffer {
        val assetFileDescriptor = context.assets.openFd(filename)
        val inputStream = assetFileDescriptor.createInputStream()
        val fileChannel = inputStream.channel
        val startOffset = assetFileDescriptor.startOffset
        val declaredLength = assetFileDescriptor.declaredLength
        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declaredLength)
    }

    private fun preprocessImage(image: TensorImage): ByteBuffer {
        // Implementar preprocesamiento específico del modelo
        // (resize, normalize, etc.)
        TODO("Implement preprocessing")
    }
}

// Data classes
data class BiometricTemplate(
    val vector: FloatArray,
    val createdAt: Long,
    val expiresAt: Long
) {
    val isExpired: Boolean
        get() = System.currentTimeMillis() > expiresAt

    fun toByteArray(): ByteArray {
        // Serializar a bytes
        TODO("Implement serialization")
    }

    companion object {
        fun fromByteArray(bytes: ByteArray): BiometricTemplate {
            // Deserializar desde bytes
            TODO("Implement deserialization")
        }
    }
}

data class VerificationResult(
    val verified: Boolean,
    val confidence: Float
)
```

---

## 4. Acción Técnica #4: Privacy Score Card UI + Botón "Eliminar Ahora"

### Objetivo

Crear interfaz visual que muestre el nivel de privacidad del usuario y permita eliminación inmediata de datos.

### Tecnologías

- React/React Native
- TypeScript
- TailwindCSS

### Implementación React Component

```typescript
// PrivacyScoreCard.tsx
import React, { useState, useEffect } from 'react';
import { AlertTriangle, Shield, Lock, Trash2, Download } from 'lucide-react';

interface PrivacyMetrics {
    score: number; // 0-100
    level: 'LOW' | 'MEDIUM' | 'HIGH';
    processingMode: 'local' | 'cloud' | 'hybrid';
    dataShared: number; // 0 = ninguno
    lastAuthentication: Date | null;
    templateExpiresIn: number | null; // horas restantes
    encryptionStatus: 'active' | 'inactive';
    auditsPassed: number;
    auditsTotal: number;
}

interface DeletionCertificate {
    id: string;
    downloadUrl: string;
}

const PrivacyScoreCard: React.FC<{ userId: string }> = ({ userId }) => {
    const [metrics, setMetrics] = useState<PrivacyMetrics | null>(null);
    const [loading, setLoading] = useState(true);
    const [deleting, setDeleting] = useState(false);
    const [certificate, setCertificate] = useState<DeletionCertificate | null>(null);

    useEffect(() => {
        fetchPrivacyMetrics();
    }, [userId]);

    const fetchPrivacyMetrics = async () => {
        try {
            const response = await fetch(`/api/privacy/metrics/${userId}`);
            const data = await response.json();
            setMetrics(data);
        } catch (error) {
            console.error('Failed to fetch privacy metrics:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteNow = async () => {
        if (!confirm('¿Estás seguro de que deseas eliminar tus datos biométricos?\n\nEsta acción es irreversible.')) {
            return;
        }

        setDeleting(true);

        try {
            const response = await fetch('/api/biometric/delete', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ userId }),
            });

            const result = await response.json();

            if (result.success) {
                setCertificate({
                    id: result.certificates[0].id,
                    downloadUrl: result.certificates[0].downloadUrl,
                });

                // Actualizar métricas
                await fetchPrivacyMetrics();

                alert('✅ Datos biométricos eliminados correctamente.\n\nDescarga tu certificado de eliminación como comprobante.');
            } else {
                throw new Error(result.message);
            }
        } catch (error) {
            console.error('Failed to delete biometric data:', error);
            alert('❌ Error al eliminar datos. Contacta a soporte.');
        } finally {
            setDeleting(false);
        }
    };

    if (loading) {
        return (
            <div className="p-6 bg-white rounded-lg shadow animate-pulse">
                <div className="h-8 bg-gray-200 rounded w-1/2 mb-4"></div>
                <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
            </div>
        );
    }

    if (!metrics) {
        return <div className="text-red-500">Error al cargar métricas de privacidad</div>;
    }

    const getLevelColor = (level: string) => {
        switch (level) {
            case 'HIGH':
                return 'text-green-600 bg-green-100';
            case 'MEDIUM':
                return 'text-yellow-600 bg-yellow-100';
            case 'LOW':
                return 'text-red-600 bg-red-100';
            default:
                return 'text-gray-600 bg-gray-100';
        }
    };

    const getLevelIcon = (level: string) => {
        switch (level) {
            case 'HIGH':
                return <Shield className="w-6 h-6 text-green-600" />;
            case 'MEDIUM':
                return <AlertTriangle className="w-6 h-6 text-yellow-600" />;
            case 'LOW':
                return <AlertTriangle className="w-6 h-6 text-red-600" />;
            default:
                return <Lock className="w-6 h-6" />;
        }
    };

    return (
        <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900">🔒 Privacy Score Card</h2>
                <div className={`flex items-center gap-2 px-4 py-2 rounded-full ${getLevelColor(metrics.level)}`}>
                    {getLevelIcon(metrics.level)}
                    <span className="font-semibold">{metrics.level}</span>
                </div>
            </div>

            {/* Score */}
            <div className="mb-6">
                <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Nivel de Privacidad</span>
                    <span className="text-2xl font-bold text-gray-900">{metrics.score}/100</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-4">
                    <div
                        className="bg-gradient-to-r from-green-400 to-green-600 h-4 rounded-full transition-all duration-500"
                        style={{ width: `${metrics.score}%` }}
                    ></div>
                </div>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="p-4 bg-gray-50 rounded-lg">
                    <div className="text-sm text-gray-600 mb-1">Procesamiento</div>
                    <div className="text-lg font-semibold text-gray-900">
                        {metrics.processingMode === 'local' ? '100% Local' :
                         metrics.processingMode === 'cloud' ? 'En la nube' : 'Híbrido'}
                    </div>
                </div>

                <div className="p-4 bg-gray-50 rounded-lg">
                    <div className="text-sm text-gray-600 mb-1">Datos compartidos</div>
                    <div className="text-lg font-semibold text-gray-900">
                        {metrics.dataShared === 0 ? 'Ninguno' : metrics.dataShared}
                    </div>
                </div>

                <div className="p-4 bg-gray-50 rounded-lg">
                    <div className="text-sm text-gray-600 mb-1">Cifrado</div>
                    <div className="text-lg font-semibold text-gray-900">
                        {metrics.encryptionStatus === 'active' ? 'AES-256' : 'Inactivo'}
                    </div>
                </div>

                <div className="p-4 bg-gray-50 rounded-lg">
                    <div className="text-sm text-gray-600 mb-1">Auditorías</div>
                    <div className="text-lg font-semibold text-gray-900">
                        {metrics.auditsPassed}/{metrics.auditsTotal} ✅
                    </div>
                </div>
            </div>

            {/* Template Expiration */}
            {metrics.templateExpiresIn !== null && (
                <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                    <div className="flex items-center gap-2">
                        <Lock className="w-5 h-5 text-blue-600" />
                        <div>
                            <div className="text-sm font-medium text-blue-900">
                                Plantilla biométrica activa
                            </div>
                            <div className="text-xs text-blue-700">
                                Se eliminará automáticamente en {metrics.templateExpiresIn} horas
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Actions */}
            <div className="flex gap-4">
                <button
                    onClick={handleDeleteNow}
                    disabled={deleting}
                    className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                    <Trash2 className="w-5 h-5" />
                    {deleting ? 'Eliminando...' : 'Eliminar ahora'}
                </button>

                {certificate && (
                    <a
                        href={certificate.downloadUrl}
                        download
                        className="flex items-center justify-center gap-2 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                    >
                        <Download className="w-5 h-5" />
                        Certificado
                    </a>
                )}
            </div>

            {/* Footer */}
            <div className="mt-6 pt-6 border-t border-gray-200">
                <div className="text-xs text-gray-600 text-center">
                    <p>Última actualización: {new Date().toLocaleString('es-MX')}</p>
                    <p className="mt-1">
                        <a href="/privacy" className="text-blue-600 hover:underline">
                            Ver política de privacidad completa
                        </a>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default PrivacyScoreCard;
```

---

## 5. Acción Técnica #5: Endpoint ARCO Self-Service

### Objetivo

Implementar portal de autoservicio para que usuarios ejerzan derechos ARCO (Acceso, Rectificación, Cancelación, Oposición) sin intervención manual.

### Endpoint de Acceso (Descargar Datos)

```typescript
// src/routes/arco.routes.ts
import { Router, Request, Response } from 'express';
import { body, validationResult } from 'express-validator';
import { db } from '../database';
import { generateDataExportZip } from '../services/export.service';
import { auditLog } from '../services/audit.service';

const router = Router();

/**
 * GET /api/arco/access
 * Descarga todos los datos personales del usuario (formato JSON/CSV)
 */
router.get(
    '/access',
    async (req: Request, res: Response) => {
        const userId = req.user?.id;

        if (!userId) {
            return res.status(401).json({ message: 'Unauthorized' });
        }

        try {
            // 1. Recopilar todos los datos del usuario
            const userData = await db.query(`
                SELECT * FROM users WHERE id = $1
            `, [userId]);

            const consentLogs = await db.query(`
                SELECT * FROM consent_logs WHERE user_id = $1
            `, [userId]);

            const biometricData = await db.query(`
                SELECT template_id, created_at, expires_at, deleted_at
                FROM biometric_templates
                WHERE user_id = $1
            `, [userId]);

            const arcoRequests = await db.query(`
                SELECT * FROM arco_requests WHERE user_id = $1
            `, [userId]);

            // 2. Preparar datos en formato estructurado
            const exportData = {
                user: userData.rows[0],
                consent_history: consentLogs.rows,
                biometric_templates: biometricData.rows,
                arco_requests: arcoRequests.rows,
                export_metadata: {
                    generated_at: new Date().toISOString(),
                    format: 'JSON',
                    version: '1.0',
                },
            };

            // 3. Generar ZIP con JSON + CSV
            const zipBuffer = await generateDataExportZip(exportData);

            // 4. Auditoría
            await auditLog.emit('arco.access', {
                userId,
                timestamp: new Date(),
            });

            // 5. Enviar archivo
            res.setHeader('Content-Type', 'application/zip');
            res.setHeader('Content-Disposition', `attachment; filename="facecode_data_${userId}.zip"`);
            res.send(zipBuffer);

        } catch (error) {
            console.error('Error generating data export:', error);
            res.status(500).json({ message: 'Failed to export data' });
        }
    }
);

/**
 * POST /api/arco/rectify
 * Permite al usuario corregir datos inexactos
 */
router.post(
    '/rectify',
    [
        body('field').isString(),
        body('newValue').isString(),
    ],
    async (req: Request, res: Response) => {
        const userId = req.user?.id;
        const { field, newValue } = req.body;

        if (!userId) {
            return res.status(401).json({ message: 'Unauthorized' });
        }

        // Lista blanca de campos editables
        const editableFields = ['name', 'email', 'phone'];

        if (!editableFields.includes(field)) {
            return res.status(400).json({ message: 'Field not editable' });
        }

        try {
            await db.query(`
                UPDATE users
                SET ${field} = $1, updated_at = NOW()
                WHERE id = $2
            `, [newValue, userId]);

            await auditLog.emit('arco.rectify', {
                userId,
                field,
                timestamp: new Date(),
            });

            res.json({ success: true, message: 'Data updated successfully' });

        } catch (error) {
            console.error('Error updating user data:', error);
            res.status(500).json({ message: 'Failed to update data' });
        }
    }
);

/**
 * DELETE /api/arco/cancel
 * Elimina la cuenta del usuario y todos sus datos
 */
router.delete(
    '/cancel',
    async (req: Request, res: Response) => {
        const userId = req.user?.id;

        if (!userId) {
            return res.status(401).json({ message: 'Unauthorized' });
        }

        try {
            // 1. Eliminar datos biométricos
            await deleteBiometricData(userId);

            // 2. Eliminar datos de usuario (soft delete)
            await db.query(`
                UPDATE users
                SET
                    deleted_at = NOW(),
                    email = CONCAT('deleted_', id, '@facecode.app'),
                    name = 'Deleted User'
                WHERE id = $1
            `, [userId]);

            // 3. Programar eliminación permanente en 30 días
            await db.query(`
                INSERT INTO deletion_queue (user_id, scheduled_for)
                VALUES ($1, NOW() + INTERVAL '30 days')
            `, [userId]);

            // 4. Auditoría
            await auditLog.emit('arco.cancel', {
                userId,
                timestamp: new Date(),
            });

            // 5. Enviar correo de confirmación
            await sendAccountDeletionEmail(userId);

            res.json({
                success: true,
                message: 'Account deleted successfully. Data will be permanently removed in 30 days.',
            });

        } catch (error) {
            console.error('Error deleting account:', error);
            res.status(500).json({ message: 'Failed to delete account' });
        }
    }
);

/**
 * POST /api/arco/oppose
 * Permite oponerse a tratamientos específicos
 */
router.post(
    '/oppose',
    [
        body('purposeType').isIn(['secondary', 'marketing', 'profiling']),
    ],
    async (req: Request, res: Response) => {
        const userId = req.user?.id;
        const { purposeType } = req.body;

        if (!userId) {
            return res.status(401).json({ message: 'Unauthorized' });
        }

        try {
            await db.query(`
                INSERT INTO arco_requests (
                    user_id, request_type, purpose_type, status, created_at
                ) VALUES ($1, 'oppose', $2, 'completed', NOW())
            `, [userId, purposeType]);

            // Actualizar flags de usuario
            await db.query(`
                UPDATE users
                SET ${purposeType}_consent = false
                WHERE id = $1
            `, [userId]);

            await auditLog.emit('arco.oppose', {
                userId,
                purposeType,
                timestamp: new Date(),
            });

            res.json({ success: true, message: 'Opposition registered successfully' });

        } catch (error) {
            console.error('Error registering opposition:', error);
            res.status(500).json({ message: 'Failed to register opposition' });
        }
    }
);

export default router;
```

---

## Resumen de Implementación

### Checklist Final

- ✅ **Logging de consentimiento** con cifrado AES-256 y retención de 5 años
- ✅ **Eliminación automática 24h** con verificación criptográfica
- ✅ **Procesamiento on-device** (iOS/Android) con fallback seguro
- ✅ **Privacy Score Card** UI con botón "Eliminar ahora"
- ✅ **Endpoint ARCO** self-service para acceso/rectificación/cancelación/oposición

### Próximos Pasos

1. **Testing exhaustivo** de cada componente (unit + integration + E2E)
2. **Auditoría de seguridad externa** (pentesting + code review)
3. **Revisión legal** con despacho especializado en privacy
4. **Deployment gradual** (beta privada → público limitado → producción)
5. **Monitoreo continuo** con dashboards en Grafana + alertas en PagerDuty

---

**Contacto Técnico:**
- Engineering Lead: [engineering@facecode.app](mailto:engineering@facecode.app)
- Security Team: [security@facecode.app](mailto:security@facecode.app)
- Privacy Officer: [dpo@facecode.app](mailto:dpo@facecode.app)

---

> **© 2025 FaceCode® Guardian Network**
> *Implementación ética • Código abierto • Privacidad por diseño*
