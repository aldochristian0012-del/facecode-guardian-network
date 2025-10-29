# Plantillas de Consentimiento Explícito — FaceCode®

**Versión:** 1.0
**Fecha:** 29 de octubre de 2025
**Cumplimiento:** LFPDPPP (México), GDPR (UE), CCPA/CPRA (California)

---

## Introducción

Este documento contiene plantillas legales de consentimiento explícito para el procesamiento de datos biométricos en FaceCode® Guardian Network. Estas plantillas están diseñadas para:

1. **Cumplir con legislación internacional** de protección de datos
2. **Ser comprensibles** para usuarios no técnicos
3. **Facilitar la integración** en interfaces de usuario (UI)
4. **Generar registros auditables** con valor legal

---

## 1. Plantilla de Consentimiento Principal (Español)

### Versión Completa (Para mostrar antes del primer uso)

```
═══════════════════════════════════════════════════════════════
         CONSENTIMIENTO PARA TRATAMIENTO DE DATOS BIOMÉTRICOS
═══════════════════════════════════════════════════════════════

Yo, [NOMBRE COMPLETO DEL USUARIO], manifiesto mi consentimiento
expreso, libre, específico, informado e inequívoco para que
FACECODE GUARDIAN NETWORK (en adelante, "FaceCode") lleve a cabo
el tratamiento de mis datos biométricos, consistentes en
características faciales y plantillas biométricas derivadas,
para las siguientes finalidades:

───────────────────────────────────────────────────────────────
1. FINALIDAD PRINCIPAL
───────────────────────────────────────────────────────────────

• Autenticación de identidad mediante reconocimiento facial
• Análisis de experiencia de usuario y accesibilidad
• Mejora técnica del servicio (corrección de errores, optimización)
• Cumplimiento de obligaciones legales aplicables

───────────────────────────────────────────────────────────────
2. FINALIDAD SECUNDARIA (OPCIONAL - Requiere autorización adicional)
───────────────────────────────────────────────────────────────

☐ Autorizo el uso de mis datos biométricos ANONIMIZADOS para:
  • Entrenamiento agregado de modelos de inteligencia artificial
  • Investigación académica sobre ética en IA y reducción de sesgos
  • Mejora de funcionalidades mediante análisis estadístico

Nota: Puedes rechazar esta finalidad sin afectar el servicio principal.

───────────────────────────────────────────────────────────────
3. DECLARACIONES DEL USUARIO
───────────────────────────────────────────────────────────────

Declaro que:

(a) He leído y comprendido el Aviso de Privacidad Integral de FaceCode,
    disponible en https://facecode.app/privacy

(b) Entiendo que mis datos biométricos serán procesados preferentemente
    en mi dispositivo (on-device processing) y NO se almacenarán
    fotografías ni videos de mi rostro

(c) Mis plantillas biométricas serán retenidas por un máximo de 24 HORAS,
    salvo que yo autorice expresamente un período mayor

(d) Puedo REVOCAR este consentimiento en cualquier momento desde:
    • Ajustes → Privacidad → Revocar consentimiento
    • Correo electrónico: privacy@facecode.app
    • Portal web: https://facecode.app/privacy/arco

(e) Tengo derecho a ejercer mis derechos ARCO (Acceso, Rectificación,
    Cancelación, Oposición) en los términos de la Ley Federal de
    Protección de Datos Personales en Posesión de los Particulares
    (LFPDPPP) y normativa aplicable (GDPR, CCPA, etc.)

(f) En caso de revocación, mis datos biométricos serán ELIMINADOS
    INMEDIATAMENTE de forma verificable mediante certificado criptográfico

───────────────────────────────────────────────────────────────
4. CONSENTIMIENTO EXPLÍCITO
───────────────────────────────────────────────────────────────

☑ DOY MI CONSENTIMIENTO EXPRESO Y POR ESCRITO para el tratamiento
  de mis datos biométricos faciales conforme a lo establecido en
  este documento y el Aviso de Privacidad de FaceCode.

───────────────────────────────────────────────────────────────
5. REGISTRO DE CONSENTIMIENTO (Llenado automático por el sistema)
───────────────────────────────────────────────────────────────

Fecha y hora:        [YYYY-MM-DD HH:MM:SS UTC]
Dispositivo:         [Marca, modelo, OS versión]
Dirección IP:        [XXX.XXX.XXX.XXX] (anonimizada tras 30 días)
Versión de Términos: [v1.0-2025-10-29]
Hash de documento:   [SHA-256 del texto de consentimiento]
ID de consentimiento: [UUID único]

Firma electrónica:   [Basada en biometría del dispositivo o PIN]

───────────────────────────────────────────────────────────────
IMPORTANTE: Este consentimiento se almacena de forma CIFRADA (AES-256)
y se conserva durante 5 AÑOS para cumplimiento de auditorías legales.
═══════════════════════════════════════════════════════════════
```

---

## 2. Plantilla de Consentimiento Simplificada (UI/UX)

### Para implementar en aplicaciones móviles y web

```
┌──────────────────────────────────────────────────────────────┐
│  🔐 Autorización de Reconocimiento Facial                    │
└──────────────────────────────────────────────────────────────┘

Para usar esta función, necesitamos tu permiso explícito.

📋 ¿Qué procesamos?
→ Geometría de tu rostro (distancias entre ojos, nariz, boca)
→ Plantillas matemáticas cifradas (NO guardamos fotos)

📍 ¿Dónde?
→ En tu dispositivo (no enviamos datos a servidores)

⏱ ¿Cuánto tiempo?
→ Máximo 24 horas, luego se eliminan automáticamente

🔓 Tus derechos:
→ Revocar en cualquier momento
→ Solicitar eliminación inmediata
→ Acceder a tus datos cuando quieras

☐ He leído el [Aviso de Privacidad] y doy mi consentimiento
  explícito para el procesamiento de mis datos biométricos

[Rechazar]  [Aceptar y continuar]
```

---

## 3. Plantilla de Consentimiento para Menores (Con Autorización Parental)

### Requiere verificación de identidad del padre/tutor

```
═══════════════════════════════════════════════════════════════
    CONSENTIMIENTO PARENTAL PARA DATOS BIOMÉTRICOS DE MENORES
═══════════════════════════════════════════════════════════════

DATOS DEL MENOR:
Nombre completo:     [________________________]
Fecha de nacimiento: [YYYY-MM-DD]
Edad:                [__ años] (menor de 16 años)

DATOS DEL PADRE/MADRE O TUTOR LEGAL:
Nombre completo:     [________________________]
Relación con menor:  [Padre/Madre/Tutor legal]
Identificación:      [Tipo: ______ Número: __________]
Correo electrónico:  [________________________]
Teléfono:            [________________________]

───────────────────────────────────────────────────────────────
DECLARACIÓN DE CONSENTIMIENTO PARENTAL
───────────────────────────────────────────────────────────────

Yo, [NOMBRE DEL PADRE/TUTOR], en mi calidad de [padre/madre/tutor
legal] de [NOMBRE DEL MENOR], declaro que:

(a) He leído y comprendido el Aviso de Privacidad de FaceCode
(b) Autorizo EXPRESAMENTE el procesamiento de datos biométricos
    faciales de mi hijo/a para las finalidades descritas
(c) Comprendo que puedo revocar esta autorización en cualquier momento
(d) Confirmo mi identidad mediante [documento de identidad oficial]

☑ DOY MI CONSENTIMIENTO PARENTAL para el tratamiento de datos
  biométricos de mi hijo/a [NOMBRE DEL MENOR]

Fecha de autorización: [YYYY-MM-DD HH:MM:SS]
Firma electrónica:     [_________________________]

Verificación de identidad: [Video-selfie + ID oficial]
═══════════════════════════════════════════════════════════════

NOTA LEGAL: FaceCode verificará la identidad del padre/tutor mediante
videollamada o documentación oficial antes de procesar datos del menor.
```

---

## 4. Plantilla de Renovación de Consentimiento (Anual)

### Para renovación periódica del consentimiento

```
┌──────────────────────────────────────────────────────────────┐
│  🔄 Renovación Anual de Consentimiento Biométrico            │
└──────────────────────────────────────────────────────────────┘

Hola [NOMBRE],

Ha pasado 1 año desde que autorizaste el uso de reconocimiento
facial en FaceCode. Como parte de nuestro compromiso con la
transparencia, te pedimos renovar tu consentimiento.

📊 Resumen de tu actividad en el último año:
→ Autenticaciones exitosas: [XXX]
→ Datos compartidos con terceros: Ninguno
→ Incidentes de seguridad: Ninguno
→ Solicitudes de acceso a tus datos: 0

¿Qué ha cambiado desde el último año?
→ [Lista de cambios en la política de privacidad, si los hay]
→ [Nuevas funcionalidades que afecten privacidad]

☐ RENUEVO mi consentimiento para el tratamiento de datos biométricos
  bajo los mismos términos del Aviso de Privacidad actualizado

[No renovar (eliminar datos)] [Renovar consentimiento]

───────────────────────────────────────────────────────────────
Si no respondes en 30 días, tus datos biométricos serán eliminados
automáticamente por precaución.
═══════════════════════════════════════════════════════════════
```

---

## 5. Plantilla de Revocación de Consentimiento

### Para que los usuarios revoquen su consentimiento fácilmente

```
┌──────────────────────────────────────────────────────────────┐
│  🚫 Revocar Consentimiento Biométrico                        │
└──────────────────────────────────────────────────────────────┘

Estás a punto de revocar tu consentimiento para el procesamiento
de datos biométricos en FaceCode.

⚠️ Consecuencias de la revocación:
→ Tus plantillas biométricas serán ELIMINADAS INMEDIATAMENTE
→ No podrás usar autenticación facial (puedes usar contraseña/PIN)
→ Recibirás un certificado criptográfico de eliminación verificable
→ Tus otros datos de cuenta permanecen activos

Razón de revocación (opcional):
☐ Preocupaciones de privacidad
☐ No uso la función
☐ Preferencia por otros métodos de autenticación
☐ Otro: [_________________________]

☑ Confirmo que deseo REVOCAR mi consentimiento y ELIMINAR
  mis datos biométricos de forma permanente

[Cancelar] [Confirmar revocación]

───────────────────────────────────────────────────────────────
Recibirás un correo de confirmación en los próximos 5 minutos.
═══════════════════════════════════════════════════════════════
```

---

## 6. Registro Técnico de Consentimiento (Backend)

### Estructura de base de datos para logging de consentimientos

```sql
-- Tabla: consent_logs
CREATE TABLE consent_logs (
    -- Identificadores
    consent_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Metadatos de consentimiento
    consent_timestamp   TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    consent_version     VARCHAR(50) NOT NULL, -- Ejemplo: "v1.0-2025-10-29"
    consent_type        VARCHAR(50) NOT NULL, -- "initial", "renewal", "revocation"
    consent_granted     BOOLEAN NOT NULL,      -- true = granted, false = revoked

    -- Finalidades aceptadas
    primary_purpose     BOOLEAN NOT NULL DEFAULT false,
    secondary_purpose   BOOLEAN NOT NULL DEFAULT false,

    -- Información del dispositivo
    device_id           VARCHAR(255),
    device_type         VARCHAR(100), -- "iOS", "Android", "Web"
    device_os           VARCHAR(100),
    device_model        VARCHAR(100),
    ip_address          INET,         -- Anonimizado tras 30 días
    user_agent          TEXT,

    -- Integridad y auditoría
    consent_text_hash   VARCHAR(64) NOT NULL, -- SHA-256 del texto exacto mostrado
    privacy_policy_url  VARCHAR(500),
    signature_method    VARCHAR(50), -- "biometric", "pin", "manual"
    signature_data      TEXT,        -- Firma electrónica cifrada

    -- Revocación (si aplica)
    revoked_at          TIMESTAMP WITH TIME ZONE,
    revocation_reason   TEXT,

    -- Cumplimiento legal
    legal_basis         VARCHAR(100), -- "consent", "contract", "legal_obligation"
    jurisdiction        VARCHAR(50),  -- "MX", "EU", "US-CA", etc.

    -- Cifrado
    encrypted_payload   TEXT,         -- Datos completos cifrados con AES-256
    encryption_key_id   VARCHAR(100), -- ID de la clave en KMS

    -- Índices para auditoría
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

    -- Índices
    INDEX idx_user_consent (user_id, consent_timestamp DESC),
    INDEX idx_consent_type (consent_type, consent_timestamp),
    INDEX idx_revocation (revoked_at) WHERE revoked_at IS NOT NULL
);

-- Política de retención: 5 años según LFPDPPP
-- Trigger para anonimizar IP tras 30 días
CREATE OR REPLACE FUNCTION anonymize_ip_after_30_days()
RETURNS void AS $$
BEGIN
    UPDATE consent_logs
    SET ip_address = '0.0.0.0'::inet
    WHERE consent_timestamp < NOW() - INTERVAL '30 days'
      AND ip_address != '0.0.0.0'::inet;
END;
$$ LANGUAGE plpgsql;

-- Job programado (pg_cron)
SELECT cron.schedule('anonymize-ips-daily', '0 2 * * *',
    'SELECT anonymize_ip_after_30_days();');
```

---

## 7. Ejemplo de Implementación en Código (JavaScript/TypeScript)

### Función para registrar consentimiento con cifrado

```typescript
import crypto from 'crypto';
import { v4 as uuidv4 } from 'uuid';

interface ConsentData {
    userId: string;
    consentGranted: boolean;
    primaryPurpose: boolean;
    secondaryPurpose: boolean;
    deviceInfo: {
        deviceId: string;
        deviceType: string;
        os: string;
        model: string;
        ipAddress: string;
        userAgent: string;
    };
    signatureMethod: 'biometric' | 'pin' | 'manual';
    signatureData?: string;
}

async function logConsent(data: ConsentData): Promise<string> {
    const consentId = uuidv4();
    const timestamp = new Date().toISOString();
    const consentVersion = 'v1.0-2025-10-29';

    // Hash del texto de consentimiento (debe coincidir con el mostrado al usuario)
    const consentText = await getConsentText(consentVersion);
    const consentTextHash = crypto
        .createHash('sha256')
        .update(consentText)
        .digest('hex');

    // Cifrado del payload completo con AES-256-GCM
    const encryptionKey = await getEncryptionKey(); // Desde KMS
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-gcm', encryptionKey, iv);

    const payload = JSON.stringify({
        ...data,
        consentId,
        timestamp,
        consentVersion,
        consentTextHash,
    });

    let encrypted = cipher.update(payload, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    const authTag = cipher.getAuthTag();

    // Guardar en base de datos
    await db.query(`
        INSERT INTO consent_logs (
            consent_id, user_id, consent_timestamp, consent_version,
            consent_type, consent_granted, primary_purpose, secondary_purpose,
            device_id, device_type, device_os, device_model,
            ip_address, user_agent, consent_text_hash,
            signature_method, signature_data, encrypted_payload,
            encryption_key_id, legal_basis, jurisdiction
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10,
            $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21
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
        data.deviceInfo.ipAddress,
        data.deviceInfo.userAgent,
        consentTextHash,
        data.signatureMethod,
        data.signatureData || null,
        JSON.stringify({ encrypted, authTag: authTag.toString('hex'), iv: iv.toString('hex') }),
        'kms-key-id-2025',
        'consent',
        'MX', // o detectar automáticamente
    ]);

    // Emitir evento de auditoría
    await auditLog.emit('consent.granted', {
        consentId,
        userId: data.userId,
        timestamp,
    });

    // Enviar correo de confirmación
    await sendConsentConfirmationEmail(data.userId, consentId);

    return consentId;
}
```

---

## 8. Plantilla de Correo de Confirmación de Consentimiento

### Email HTML para confirmar consentimiento otorgado

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Confirmación de Consentimiento - FaceCode®</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">

    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
        <h1 style="color: white; margin: 0;">🔐 FaceCode® Guardian Network</h1>
        <p style="color: white; margin: 10px 0 0 0;">Confirmación de Consentimiento</p>
    </div>

    <div style="background: #f9f9f9; padding: 30px; border: 1px solid #ddd; border-top: none; border-radius: 0 0 10px 10px;">

        <p>Hola <strong>[NOMBRE_USUARIO]</strong>,</p>

        <p>Has autorizado el procesamiento de tus datos biométricos en FaceCode®. Este correo confirma que tu consentimiento ha sido registrado correctamente.</p>

        <div style="background: white; padding: 20px; border-left: 4px solid #667eea; margin: 20px 0;">
            <h3 style="margin-top: 0;">📋 Detalles del consentimiento:</h3>
            <ul style="list-style: none; padding: 0;">
                <li><strong>ID de consentimiento:</strong> [CONSENT_ID]</li>
                <li><strong>Fecha y hora:</strong> [TIMESTAMP_FORMATTED]</li>
                <li><strong>Versión de términos:</strong> v1.0-2025-10-29</li>
                <li><strong>Dispositivo:</strong> [DEVICE_TYPE] - [DEVICE_MODEL]</li>
            </ul>
        </div>

        <h3>🔒 ¿Qué significa esto?</h3>
        <ul>
            <li>FaceCode procesará tus características faciales para autenticación</li>
            <li>El procesamiento ocurre en tu dispositivo (no en servidores)</li>
            <li>Tus plantillas biométricas se eliminan en 24 horas automáticamente</li>
            <li>Nunca vendemos ni compartimos tus datos con anunciantes</li>
        </ul>

        <h3>🔓 Tus derechos:</h3>
        <ul>
            <li><strong>Revocar:</strong> Puedes retirar tu consentimiento en cualquier momento desde Ajustes → Privacidad</li>
            <li><strong>Acceder:</strong> Solicita una copia de tus datos en <a href="mailto:privacy@facecode.app">privacy@facecode.app</a></li>
            <li><strong>Eliminar:</strong> Borra tus datos con un clic desde la aplicación</li>
        </ul>

        <div style="background: #fff3cd; border: 1px solid #ffc107; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p style="margin: 0;"><strong>⚠️ ¿No autorizaste esto?</strong></p>
            <p style="margin: 5px 0 0 0;">Si no reconoces esta actividad, contacta inmediatamente a <a href="mailto:security@facecode.app">security@facecode.app</a></p>
        </div>

        <div style="text-align: center; margin-top: 30px;">
            <a href="https://facecode.app/privacy" style="background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">Ver Política de Privacidad Completa</a>
        </div>

    </div>

    <div style="text-align: center; margin-top: 20px; font-size: 12px; color: #666;">
        <p>FaceCode® Guardian Network | Protegiendo la dignidad digital</p>
        <p>
            <a href="https://facecode.app/privacy" style="color: #667eea; text-decoration: none;">Privacidad</a> |
            <a href="https://facecode.app/terms" style="color: #667eea; text-decoration: none;">Términos</a> |
            <a href="mailto:privacy@facecode.app" style="color: #667eea; text-decoration: none;">Contacto</a>
        </p>
        <p style="margin-top: 10px;">© 2025 FaceCode® Guardian Network. Todos los derechos reservados.</p>
    </div>

</body>
</html>
```

---

## 9. Certificado de Eliminación de Datos Biométricos

### Documento generado tras revocación o eliminación

```
═══════════════════════════════════════════════════════════════
    CERTIFICADO DE ELIMINACIÓN DE DATOS BIOMÉTRICOS
    FaceCode® Guardian Network
═══════════════════════════════════════════════════════════════

ID de Certificado:   FCG-DEL-[YEAR]-[MONTH]-[DAY]-[RANDOM_ID]
Fecha de emisión:    [YYYY-MM-DD HH:MM:SS UTC]

Usuario:             [NOMBRE_USUARIO]
ID de usuario:       [USER_UUID]

───────────────────────────────────────────────────────────────
DATOS ELIMINADOS
───────────────────────────────────────────────────────────────

✓ Plantillas biométricas faciales (512 dimensiones)
✓ Embeddings de reconocimiento facial
✓ Historial de autenticaciones biométricas
✓ Metadatos asociados (timestamps, dispositivos)
✓ Backups en sistemas de respaldo

Total de registros eliminados: [XX]

───────────────────────────────────────────────────────────────
VERIFICACIÓN CRIPTOGRÁFICA
───────────────────────────────────────────────────────────────

Hash SHA-256 de registros eliminados:
[HASH_HEX_STRING_64_CARACTERES]

Firma digital del certificado (Ed25519):
[SIGNATURE_HEX_STRING]

Clave pública de verificación:
[PUBLIC_KEY_HEX_STRING]

Verificar firma en: https://facecode.app/verify-deletion

───────────────────────────────────────────────────────────────
AUDITORÍA
───────────────────────────────────────────────────────────────

Autorizado por:      Sistema automatizado de FaceCode®
Razón de eliminación: Revocación de consentimiento por usuario
Método de eliminación: Sobrescritura segura (3 pases + verificación)
Cumplimiento:        LFPDPPP, GDPR Art. 17, CCPA §1798.105

───────────────────────────────────────────────────────────────
GARANTÍAS
───────────────────────────────────────────────────────────────

FaceCode® CERTIFICA que:

1. Los datos biométricos han sido ELIMINADOS DE FORMA PERMANENTE
   de todos los sistemas de producción, staging y backups

2. La eliminación fue verificada mediante checksums criptográficos

3. No se conservan copias en servidores, cachés ni sistemas de terceros

4. Los logs de consentimiento se conservan 5 años para cumplimiento
   legal (no contienen datos biométricos)

───────────────────────────────────────────────────────────────
CONTACTO
───────────────────────────────────────────────────────────────

Para consultas sobre este certificado:
Email: dpo@facecode.app
Web:   https://facecode.app/verify-deletion/[CERTIFICATE_ID]

═══════════════════════════════════════════════════════════════
    Este certificado tiene validez legal y puede ser presentado
    ante autoridades de protección de datos si es requerido.
═══════════════════════════════════════════════════════════════

Generado automáticamente por FaceCode® Guardian Network
© 2025 FaceCode® | Privacidad garantizada
```

---

## 10. Checklist de Implementación para Desarrolladores

### Verificación de cumplimiento antes de deployment

```markdown
## ✅ Checklist de Implementación de Consentimientos

### Backend

- [ ] Tabla `consent_logs` creada en base de datos
- [ ] Cifrado AES-256-GCM implementado para payloads
- [ ] Integración con KMS (Key Management Service)
- [ ] Hash SHA-256 de textos de consentimiento implementado
- [ ] Job de anonimización de IPs configurado (30 días)
- [ ] Endpoint `/api/consent/grant` implementado
- [ ] Endpoint `/api/consent/revoke` implementado
- [ ] Endpoint `/api/consent/history` implementado (para el usuario)
- [ ] Sistema de logs de auditoría configurado
- [ ] Generación de certificados de eliminación implementada
- [ ] Firma digital Ed25519 para certificados configurada
- [ ] Webhook para notificación de revocaciones activado
- [ ] Política de retención de 5 años configurada

### Frontend (Web/Móvil)

- [ ] Pantalla de consentimiento inicial diseñada (UX/UI)
- [ ] Checkbox de consentimiento explícito implementado
- [ ] Validación de lectura de Aviso de Privacidad (scroll tracking)
- [ ] Modal de consentimiento secundario implementado
- [ ] Botón "Rechazar" funcional (no bloquea acceso a app, solo a biometría)
- [ ] Botón "Aceptar" registra consentimiento en backend
- [ ] Firma electrónica (biométrica/PIN) capturada
- [ ] Pantalla de gestión de privacidad en Ajustes
- [ ] Botón "Revocar consentimiento" funcional
- [ ] Botón "Eliminar ahora" con confirmación doble
- [ ] Pantalla de Privacy Score Card implementada
- [ ] Historial de consentimientos visible para el usuario
- [ ] Descarga de certificado de eliminación habilitada

### Emails y Notificaciones

- [ ] Template de confirmación de consentimiento diseñado (HTML)
- [ ] Email de confirmación enviado tras consentimiento
- [ ] Email de revocación enviado tras revocación
- [ ] Email de renovación anual configurado (recordatorio)
- [ ] Email con certificado de eliminación adjunto

### Legal y Documentación

- [ ] Aviso de Privacidad completo publicado en sitio web
- [ ] Versión corta para UI integrada
- [ ] Textos de consentimiento revisados por abogado especializado
- [ ] Traducciones a inglés/otros idiomas completadas
- [ ] Enlaces a políticas funcionando correctamente
- [ ] Información de contacto (privacy@facecode.app) activa

### Testing

- [ ] Flujo completo de consentimiento testeado (E2E)
- [ ] Revocación y eliminación verificadas manualmente
- [ ] Generación de certificados probada
- [ ] Firma digital validada
- [ ] Cifrado/descifrado de payloads verificado
- [ ] Testing con usuarios reales (A/B testing de comprensión)
- [ ] Pruebas de accesibilidad (WCAG 2.1 AA) pasadas
- [ ] Testing en múltiples dispositivos (iOS, Android, Web)

### Cumplimiento Legal

- [ ] Revisión legal con despacho especializado completada
- [ ] DPA (Data Processing Agreement) con proveedores firmados
- [ ] SCC (Standard Contractual Clauses) para transferencias internacionales
- [ ] Registro ante INAI (México) completado si aplica
- [ ] Evaluación de impacto (DPIA) realizada para procesamiento biométrico
- [ ] Documentación de "interés legítimo" preparada (si aplica)

### Seguridad

- [ ] Penetration testing de endpoints de consentimiento realizado
- [ ] Auditoría de seguridad externa completada
- [ ] Sistema de detección de intrusiones (IDS) configurado
- [ ] WAF (Web Application Firewall) activo
- [ ] Rate limiting en endpoints de consentimiento configurado
- [ ] Logs de auditoría inmutables configurados

### Monitoreo y Alertas

- [ ] Dashboard de métricas de consentimientos en Grafana/similar
- [ ] Alertas para revocaciones masivas configuradas
- [ ] Alertas para fallos en eliminación de datos configuradas
- [ ] Monitoreo de compliance score en tiempo real
- [ ] Reporte semanal de consentimientos activos/revocados
```

---

## Notas Finales

Estas plantillas son **versiones base** que deben ser **revisadas por un abogado especializado** en privacidad y protección de datos antes del deployment en producción, especialmente si operan en múltiples jurisdicciones.

**Recomendación:** Contratar consulta inicial con despacho especializado (Hogan Lovells Mexico, White & Case Mexico, o boutique tech privacy) para validación legal (presupuesto: $3k–$8k USD).

---

> **© 2025 FaceCode® Guardian Network**
> *Consentimiento ético • Transparencia legal • Implementación técnica*
