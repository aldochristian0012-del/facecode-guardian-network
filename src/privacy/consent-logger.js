/**
 * Consent Logger - Sistema de logging cifrado para consentimientos biométricos
 * Cumple con LFPDPPP Art. 9 - Consentimiento expreso para datos sensibles
 *
 * @module ConsentLogger
 * @version 1.0.0
 * @license Proprietary - FaceCode Guardian Network
 */

const crypto = require('crypto');
const { v4: uuidv4 } = require('uuid');

/**
 * Clase para registro y verificación de consentimientos biométricos
 * Implementa firma digital, timestamping y almacenamiento inmutable
 */
class ConsentLogger {
  /**
   * @param {Object} config - Configuración del logger
   * @param {string} config.encryptionKey - Clave AES-256 para cifrado (32 bytes hex)
   * @param {string} config.signingKey - Clave privada ECDSA para firma digital
   * @param {Object} config.database - Instancia de conexión a base de datos
   */
  constructor(config) {
    this.encryptionKey = Buffer.from(config.encryptionKey, 'hex');
    this.signingKey = config.signingKey;
    this.db = config.database;

    // Validar longitud de clave de cifrado
    if (this.encryptionKey.length !== 32) {
      throw new Error('Encryption key must be 32 bytes (256 bits)');
    }
  }

  /**
   * Registra un nuevo consentimiento biométrico con firma digital
   *
   * @param {Object} consentData - Datos del consentimiento
   * @param {string} consentData.userId - UUID del usuario
   * @param {string} consentData.ipAddress - Dirección IP de origen
   * @param {string} consentData.deviceId - Hash del dispositivo utilizado
   * @param {string} consentData.userAgent - User agent del navegador
   * @param {string} consentData.privacyNoticeVersion - Versión del aviso de privacidad
   * @param {Object} consentData.optionalConsents - Consentimientos opcionales
   * @param {boolean} consentData.optionalConsents.marketing - Comunicaciones de marketing
   * @param {boolean} consentData.optionalConsents.mlTraining - Uso para ML training
   * @param {string|null} consentData.optionalConsents.extendedRetention - Período extendido (30d/90d/indefinite)
   *
   * @returns {Promise<Object>} Certificado de consentimiento con firma digital
   */
  async logConsent(consentData) {
    try {
      // 1. Generar datos de auditoría
      const consentId = uuidv4();
      const timestamp = new Date().toISOString();
      const timestampUnix = Date.now();

      // 2. Obtener hash del documento de privacidad
      const privacyNoticeHash = await this.getPrivacyNoticeHash(
        consentData.privacyNoticeVersion
      );

      // 3. Construir payload del consentimiento
      const consentPayload = {
        consent_id: consentId,
        user_id: consentData.userId,
        timestamp_iso: timestamp,
        timestamp_unix: timestampUnix,
        ip_address: this.hashPII(consentData.ipAddress), // Hash para privacidad
        ip_original: this.encrypt(consentData.ipAddress), // Cifrado para auditoría
        device_id: consentData.deviceId,
        user_agent: consentData.userAgent,
        privacy_notice_version: consentData.privacyNoticeVersion,
        privacy_notice_hash: privacyNoticeHash,
        optional_consents: {
          marketing: consentData.optionalConsents.marketing || false,
          ml_training: consentData.optionalConsents.mlTraining || false,
          extended_retention: consentData.optionalConsents.extendedRetention || null
        },
        consent_type: 'biometric_explicit', // LFPDPPP Art. 9
        consent_method: 'electronic_signature', // Firma electrónica avanzada
        legal_basis: 'LFPDPPP_Art9', // Fundamento legal
        retention_policy: this.calculateRetentionPolicy(consentData.optionalConsents),
        geolocation: await this.getApproximateLocation(consentData.ipAddress)
      };

      // 4. Calcular hash del consentimiento completo
      const consentHash = this.calculateHash(JSON.stringify(consentPayload));

      // 5. Generar firma digital ECDSA
      const signature = this.signConsent(consentHash);

      // 6. Construir certificado de consentimiento
      const consentCertificate = {
        ...consentPayload,
        consent_hash: consentHash,
        consent_signature: signature,
        verification_url: `${process.env.API_BASE_URL}/verify-consent/${consentId}`,
        certificate_version: '1.0'
      };

      // 7. Almacenar en base de datos (write-once, no modificable)
      await this.storeConsent(consentCertificate);

      // 8. Registrar en log de auditoría
      await this.auditLog({
        action: 'CONSENT_CREATED',
        consent_id: consentId,
        user_id: consentData.userId,
        timestamp: timestamp,
        ip_address: this.hashPII(consentData.ipAddress)
      });

      // 9. Programar job de eliminación automática
      await this.scheduleDataDeletion(
        consentData.userId,
        this.calculateRetentionPolicy(consentData.optionalConsents)
      );

      // 10. Retornar certificado sin datos sensibles para cliente
      return {
        consent_id: consentId,
        timestamp: timestamp,
        consent_hash: consentHash,
        signature: signature,
        privacy_notice_version: consentData.privacyNoticeVersion,
        retention_expires_at: this.calculateExpirationDate(
          consentData.optionalConsents
        ),
        download_certificate_url: `${process.env.API_BASE_URL}/download-consent/${consentId}`,
        verify_url: `${process.env.API_BASE_URL}/verify-consent/${consentId}`
      };

    } catch (error) {
      // Log de error sin exponer datos sensibles
      await this.auditLog({
        action: 'CONSENT_ERROR',
        error_type: error.name,
        error_message: error.message,
        user_id: consentData.userId,
        timestamp: new Date().toISOString()
      });

      throw new Error(`Failed to log consent: ${error.message}`);
    }
  }

  /**
   * Cifra datos sensibles con AES-256-GCM
   *
   * @param {string} plaintext - Texto plano a cifrar
   * @returns {string} Texto cifrado en formato: iv:encrypted:authTag (hex)
   */
  encrypt(plaintext) {
    const iv = crypto.randomBytes(16); // IV único por operación
    const cipher = crypto.createCipheriv('aes-256-gcm', this.encryptionKey, iv);

    let encrypted = cipher.update(plaintext, 'utf8', 'hex');
    encrypted += cipher.final('hex');

    const authTag = cipher.getAuthTag().toString('hex');

    // Formato: iv:encrypted:authTag (permite verificación de integridad)
    return `${iv.toString('hex')}:${encrypted}:${authTag}`;
  }

  /**
   * Descifra datos previamente cifrados con AES-256-GCM
   *
   * @param {string} ciphertext - Texto cifrado en formato iv:encrypted:authTag
   * @returns {string} Texto plano descifrado
   */
  decrypt(ciphertext) {
    const [ivHex, encryptedHex, authTagHex] = ciphertext.split(':');

    const iv = Buffer.from(ivHex, 'hex');
    const encrypted = Buffer.from(encryptedHex, 'hex');
    const authTag = Buffer.from(authTagHex, 'hex');

    const decipher = crypto.createDecipheriv('aes-256-gcm', this.encryptionKey, iv);
    decipher.setAuthTag(authTag);

    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');

    return decrypted;
  }

  /**
   * Hash SHA-256 para datos de identificación personal (pseudonimización)
   *
   * @param {string} data - Dato a hashear (ej. IP, email)
   * @returns {string} Hash SHA-256 en hexadecimal
   */
  hashPII(data) {
    return crypto.createHash('sha256')
      .update(data + process.env.HASH_SALT) // Salt para evitar rainbow tables
      .digest('hex');
  }

  /**
   * Calcula hash SHA-256 del contenido del consentimiento
   *
   * @param {string} content - Contenido a hashear (JSON stringificado)
   * @returns {string} Hash SHA-256 en hexadecimal
   */
  calculateHash(content) {
    return crypto.createHash('sha256')
      .update(content)
      .digest('hex');
  }

  /**
   * Firma digitalmente el hash del consentimiento con ECDSA
   *
   * @param {string} contentHash - Hash del consentimiento a firmar
   * @returns {string} Firma digital en formato DER (hex)
   */
  signConsent(contentHash) {
    const sign = crypto.createSign('SHA256');
    sign.update(contentHash);
    sign.end();

    const signature = sign.sign(this.signingKey, 'hex');
    return signature;
  }

  /**
   * Verifica la firma digital de un consentimiento
   *
   * @param {string} contentHash - Hash del consentimiento
   * @param {string} signature - Firma digital a verificar
   * @param {string} publicKey - Clave pública ECDSA para verificación
   * @returns {boolean} true si la firma es válida
   */
  verifySignature(contentHash, signature, publicKey) {
    const verify = crypto.createVerify('SHA256');
    verify.update(contentHash);
    verify.end();

    return verify.verify(publicKey, signature, 'hex');
  }

  /**
   * Calcula política de retención según consentimientos opcionales
   *
   * @param {Object} optionalConsents - Consentimientos opcionales del usuario
   * @returns {string} Política de retención (24h/30d/90d/indefinite)
   */
  calculateRetentionPolicy(optionalConsents) {
    const extended = optionalConsents.extendedRetention;

    if (!extended || extended === null) {
      return '24h'; // Default LFPDPPP - minimización de datos
    }

    // Validar valores permitidos
    const allowedPolicies = ['30d', '90d', 'indefinite'];
    if (!allowedPolicies.includes(extended)) {
      throw new Error(`Invalid retention policy: ${extended}`);
    }

    return extended;
  }

  /**
   * Calcula fecha de expiración del consentimiento
   *
   * @param {Object} optionalConsents - Consentimientos opcionales
   * @returns {string|null} Fecha ISO de expiración o null si indefinido
   */
  calculateExpirationDate(optionalConsents) {
    const policy = this.calculateRetentionPolicy(optionalConsents);
    const now = new Date();

    switch (policy) {
      case '24h':
        return new Date(now.getTime() + 24 * 60 * 60 * 1000).toISOString();
      case '30d':
        return new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000).toISOString();
      case '90d':
        return new Date(now.getTime() + 90 * 24 * 60 * 60 * 1000).toISOString();
      case 'indefinite':
        return null; // Hasta revocación explícita
      default:
        return new Date(now.getTime() + 24 * 60 * 60 * 1000).toISOString();
    }
  }

  /**
   * Obtiene hash del documento de aviso de privacidad
   *
   * @param {string} version - Versión del aviso (ej. "1.0")
   * @returns {Promise<string>} Hash SHA-256 del documento
   */
  async getPrivacyNoticeHash(version) {
    // En producción, esto debería consultar un registro de documentos versionados
    // Por ahora retornamos un hash de ejemplo

    const query = `
      SELECT document_hash
      FROM privacy_notice_versions
      WHERE version = ?
    `;

    const result = await this.db.query(query, [version]);

    if (!result || result.length === 0) {
      throw new Error(`Privacy notice version ${version} not found`);
    }

    return result[0].document_hash;
  }

  /**
   * Obtiene ubicación aproximada (ciudad/país) desde IP sin almacenar GPS
   * Cumple con minimización de datos (LFPDPPP Art. 6)
   *
   * @param {string} ipAddress - Dirección IP
   * @returns {Promise<Object>} {city, country, country_code}
   */
  async getApproximateLocation(ipAddress) {
    try {
      // Integración con servicio de geolocalización (ej. MaxMind GeoLite2)
      // Solo ciudad/país, NO coordenadas GPS precisas

      // Simulación para ejemplo
      return {
        city: 'Ciudad de México',
        country: 'México',
        country_code: 'MX'
      };

      // Implementación real:
      // const geoip = require('geoip-lite');
      // const geo = geoip.lookup(ipAddress);
      // return {
      //   city: geo?.city || 'Unknown',
      //   country: geo?.country || 'Unknown',
      //   country_code: geo?.country || 'XX'
      // };

    } catch (error) {
      // Si falla geolocalización, no bloquear consentimiento
      return { city: 'Unknown', country: 'Unknown', country_code: 'XX' };
    }
  }

  /**
   * Almacena certificado de consentimiento en base de datos (write-once)
   *
   * @param {Object} certificate - Certificado de consentimiento completo
   * @returns {Promise<void>}
   */
  async storeConsent(certificate) {
    const query = `
      INSERT INTO biometric_consents (
        consent_id,
        user_id,
        timestamp_iso,
        timestamp_unix,
        ip_address_hash,
        ip_address_encrypted,
        device_id,
        user_agent,
        privacy_notice_version,
        privacy_notice_hash,
        optional_consents,
        consent_type,
        consent_method,
        legal_basis,
        retention_policy,
        geolocation,
        consent_hash,
        consent_signature,
        certificate_version,
        created_at,
        is_revoked
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW(), FALSE)
    `;

    const params = [
      certificate.consent_id,
      certificate.user_id,
      certificate.timestamp_iso,
      certificate.timestamp_unix,
      certificate.ip_address,
      certificate.ip_original,
      certificate.device_id,
      certificate.user_agent,
      certificate.privacy_notice_version,
      certificate.privacy_notice_hash,
      JSON.stringify(certificate.optional_consents),
      certificate.consent_type,
      certificate.consent_method,
      certificate.legal_basis,
      certificate.retention_policy,
      JSON.stringify(certificate.geolocation),
      certificate.consent_hash,
      certificate.consent_signature,
      certificate.certificate_version
    ];

    await this.db.query(query, params);
  }

  /**
   * Programa job de eliminación automática según política de retención
   *
   * @param {string} userId - UUID del usuario
   * @param {string} retentionPolicy - Política de retención (24h/30d/90d/indefinite)
   * @returns {Promise<void>}
   */
  async scheduleDataDeletion(userId, retentionPolicy) {
    if (retentionPolicy === 'indefinite') {
      return; // No programar eliminación automática
    }

    const expirationDate = this.calculateExpirationDate({ extendedRetention: retentionPolicy });

    const query = `
      INSERT INTO data_deletion_queue (
        user_id,
        data_type,
        scheduled_deletion_at,
        deletion_method,
        status,
        created_at
      ) VALUES (?, 'biometric_embeddings', ?, 'gutmann_35pass', 'scheduled', NOW())
    `;

    await this.db.query(query, [userId, expirationDate]);
  }

  /**
   * Registra evento en log de auditoría inmutable
   *
   * @param {Object} auditEntry - Entrada de auditoría
   * @returns {Promise<void>}
   */
  async auditLog(auditEntry) {
    const query = `
      INSERT INTO audit_log (
        action,
        consent_id,
        user_id,
        timestamp,
        ip_address_hash,
        error_type,
        error_message,
        created_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?, NOW())
    `;

    const params = [
      auditEntry.action,
      auditEntry.consent_id || null,
      auditEntry.user_id || null,
      auditEntry.timestamp,
      auditEntry.ip_address || null,
      auditEntry.error_type || null,
      auditEntry.error_message || null
    ];

    await this.db.query(query, params);
  }

  /**
   * Revoca un consentimiento existente (marca como revocado, no elimina registro)
   * Cumple con LFPDPPP Art. 8 - Derecho de revocación
   *
   * @param {string} userId - UUID del usuario
   * @param {string} reason - Motivo de revocación (opcional)
   * @returns {Promise<Object>} Certificado de revocación
   */
  async revokeConsent(userId, reason = null) {
    const timestamp = new Date().toISOString();

    // 1. Marcar consentimiento como revocado
    const updateQuery = `
      UPDATE biometric_consents
      SET is_revoked = TRUE,
          revocation_timestamp = ?,
          revocation_reason = ?
      WHERE user_id = ? AND is_revoked = FALSE
    `;

    await this.db.query(updateQuery, [timestamp, reason, userId]);

    // 2. Programar eliminación inmediata de datos biométricos
    await this.scheduleImmediateDeletion(userId);

    // 3. Generar certificado de revocación
    const revocationCertificate = {
      user_id: userId,
      revocation_timestamp: timestamp,
      revocation_reason: reason,
      data_deletion_scheduled: true,
      deletion_eta: '15 minutes',
      certificate_url: `${process.env.API_BASE_URL}/download-revocation/${userId}`
    };

    // 4. Log de auditoría
    await this.auditLog({
      action: 'CONSENT_REVOKED',
      user_id: userId,
      timestamp: timestamp
    });

    return revocationCertificate;
  }

  /**
   * Programa eliminación inmediata (dentro de 15 minutos)
   *
   * @param {string} userId - UUID del usuario
   * @returns {Promise<void>}
   */
  async scheduleImmediateDeletion(userId) {
    const deletionTime = new Date(Date.now() + 15 * 60 * 1000).toISOString(); // +15 min

    const query = `
      INSERT INTO data_deletion_queue (
        user_id,
        data_type,
        scheduled_deletion_at,
        deletion_method,
        status,
        priority,
        created_at
      ) VALUES (?, 'biometric_embeddings', ?, 'gutmann_35pass', 'scheduled', 'high', NOW())
      ON DUPLICATE KEY UPDATE scheduled_deletion_at = VALUES(scheduled_deletion_at), priority = 'high'
    `;

    await this.db.query(query, [userId, deletionTime]);
  }
}

/**
 * Ejemplo de uso
 */
async function example() {
  // Configuración (en producción, usar variables de entorno)
  const config = {
    encryptionKey: process.env.CONSENT_ENCRYPTION_KEY, // 32 bytes hex (64 caracteres)
    signingKey: process.env.CONSENT_SIGNING_PRIVATE_KEY, // PEM private key
    database: require('./db-connection') // Instancia de conexión a DB
  };

  const consentLogger = new ConsentLogger(config);

  // Registrar consentimiento
  const newConsent = await consentLogger.logConsent({
    userId: 'user-uuid-12345',
    ipAddress: '192.0.2.1',
    deviceId: 'device-hash-abc123',
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)...',
    privacyNoticeVersion: '1.0',
    optionalConsents: {
      marketing: false,
      mlTraining: true,
      extendedRetention: null // 24h default
    }
  });

  console.log('Consent Certificate:', newConsent);
  // {
  //   consent_id: 'uuid-...',
  //   timestamp: '2025-10-29T14:32:15.782Z',
  //   consent_hash: 'sha256-...',
  //   signature: 'ecdsa-signature-...',
  //   privacy_notice_version: '1.0',
  //   retention_expires_at: '2025-10-30T14:32:15.782Z',
  //   download_certificate_url: 'https://api.facecode.com/download-consent/uuid-...',
  //   verify_url: 'https://api.facecode.com/verify-consent/uuid-...'
  // }
}

module.exports = ConsentLogger;
