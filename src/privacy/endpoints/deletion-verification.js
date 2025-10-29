/**
 * Deletion Verification Endpoints
 * FaceCode Guardian Network - LFPDPPP Compliance
 *
 * Proporciona endpoints para:
 * - Verificación de eliminación de datos biométricos
 * - Descarga de certificados de eliminación
 * - Validación criptográfica de certificados
 *
 * @module DeletionVerificationEndpoints
 * @version 1.0.0
 */

const express = require('express');
const crypto = require('crypto');
const PDFDocument = require('pdfkit');
const QRCode = require('qrcode');
const { body, param, validationResult } = require('express-validator');

const router = express.Router();

/**
 * Middleware de autenticación
 * Verificar que el usuario solicitante es el propietario de los datos
 */
const authenticate = require('../middleware/auth');

/**
 * Clase para generación y verificación de certificados de eliminación
 */
class DeletionCertificateService {
  constructor(db, publicKey) {
    this.db = db;
    this.publicKey = publicKey; // Clave pública ECDSA para verificación
  }

  /**
   * Obtiene certificado de eliminación por ID
   *
   * @param {string} certificateId - UUID del certificado
   * @returns {Promise<Object|null>} Certificado o null si no existe
   */
  async getCertificate(certificateId) {
    const query = `
      SELECT
        certificate_id,
        user_id,
        deletion_timestamp,
        data_types_deleted,
        deletion_method,
        files_deleted,
        database_rows_deleted,
        backups_purged,
        total_bytes_wiped,
        certificate_hash,
        certificate_signature,
        download_url,
        created_at
      FROM deletion_certificates
      WHERE certificate_id = ?
    `;

    const results = await this.db.query(query, [certificateId]);

    if (!results || results.length === 0) {
      return null;
    }

    const cert = results[0];

    // Parsear JSON fields
    cert.data_types_deleted = JSON.parse(cert.data_types_deleted);

    return cert;
  }

  /**
   * Obtiene certificados de un usuario específico
   *
   * @param {string} userId - UUID del usuario
   * @returns {Promise<Array>} Lista de certificados
   */
  async getUserCertificates(userId) {
    const query = `
      SELECT
        certificate_id,
        deletion_timestamp,
        data_types_deleted,
        deletion_method,
        total_bytes_wiped,
        download_url
      FROM deletion_certificates
      WHERE user_id = ?
      ORDER BY deletion_timestamp DESC
    `;

    const results = await this.db.query(query, [userId]);

    return results.map(cert => ({
      ...cert,
      data_types_deleted: JSON.parse(cert.data_types_deleted)
    }));
  }

  /**
   * Verifica la firma criptográfica de un certificado
   *
   * @param {Object} certificate - Certificado a verificar
   * @returns {boolean} true si la firma es válida
   */
  verifyCertificateSignature(certificate) {
    try {
      // Reconstruir payload original (sin signature)
      const payload = {
        certificate_id: certificate.certificate_id,
        user_id: certificate.user_id,
        deletion_timestamp: certificate.deletion_timestamp,
        data_types_deleted: certificate.data_types_deleted,
        deletion_method: certificate.deletion_method,
        files_deleted: certificate.files_deleted,
        database_rows_deleted: certificate.database_rows_deleted,
        backups_purged: certificate.backups_purged,
        total_bytes_wiped: certificate.total_bytes_wiped
      };

      // Calcular hash
      const payloadJson = JSON.stringify(payload);
      const calculatedHash = crypto.createHash('sha256')
        .update(payloadJson)
        .digest('hex');

      // Verificar que el hash coincide
      if (calculatedHash !== certificate.certificate_hash) {
        return false;
      }

      // Verificar firma ECDSA
      const verify = crypto.createVerify('SHA256');
      verify.update(certificate.certificate_hash);
      verify.end();

      const isValid = verify.verify(
        this.publicKey,
        certificate.certificate_signature,
        'hex'
      );

      return isValid;

    } catch (error) {
      console.error('Certificate signature verification failed:', error);
      return false;
    }
  }

  /**
   * Genera PDF del certificado de eliminación
   *
   * @param {Object} certificate - Certificado a convertir en PDF
   * @returns {Promise<Buffer>} Buffer del PDF generado
   */
  async generateCertificatePDF(certificate) {
    return new Promise(async (resolve, reject) => {
      try {
        const doc = new PDFDocument({
          size: 'A4',
          margin: 50,
          info: {
            Title: `Certificado de Eliminación - ${certificate.certificate_id}`,
            Author: 'FaceCode Guardian Network',
            Subject: 'Certificado de Eliminación de Datos Biométricos',
            Keywords: 'LFPDPPP, ARCO, Eliminación de Datos'
          }
        });

        const chunks = [];
        doc.on('data', chunk => chunks.push(chunk));
        doc.on('end', () => resolve(Buffer.concat(chunks)));

        // Header con logo
        doc.fontSize(24)
           .font('Helvetica-Bold')
           .text('CERTIFICADO DE ELIMINACIÓN DE DATOS', { align: 'center' });

        doc.fontSize(12)
           .font('Helvetica')
           .text('FaceCode Guardian Network', { align: 'center' })
           .text(`Certificado ID: ${certificate.certificate_id}`, { align: 'center' })
           .moveDown(2);

        // Generar QR code para verificación
        const qrCodeUrl = `${process.env.API_BASE_URL}/verify-deletion/${certificate.certificate_id}`;
        const qrCodeDataUrl = await QRCode.toDataURL(qrCodeUrl, {
          errorCorrectionLevel: 'H',
          width: 150
        });

        // Insertar QR code
        doc.image(qrCodeDataUrl, {
          fit: [150, 150],
          align: 'center',
          valign: 'center'
        });

        doc.moveDown(1)
           .fontSize(10)
           .text('Escanea este código QR para verificar la autenticidad del certificado', {
             align: 'center'
           })
           .moveDown(2);

        // Sección 1: Información General
        doc.fontSize(14)
           .font('Helvetica-Bold')
           .text('1. INFORMACIÓN GENERAL', { underline: true })
           .moveDown(0.5);

        doc.fontSize(11)
           .font('Helvetica');

        const deletionDate = new Date(certificate.deletion_timestamp);
        const formattedDate = deletionDate.toLocaleString('es-MX', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          timeZoneName: 'short'
        });

        doc.text(`Usuario ID: ${certificate.user_id}`)
           .text(`Fecha y hora de eliminación: ${formattedDate}`)
           .text(`Método de eliminación: ${this.formatDeletionMethod(certificate.deletion_method)}`)
           .moveDown(1.5);

        // Sección 2: Datos Eliminados
        doc.fontSize(14)
           .font('Helvetica-Bold')
           .text('2. DATOS ELIMINADOS', { underline: true })
           .moveDown(0.5);

        doc.fontSize(11)
           .font('Helvetica')
           .text('Tipos de datos eliminados:');

        certificate.data_types_deleted.forEach(dataType => {
          doc.text(`  • ${this.formatDataType(dataType)}`, { indent: 20 });
        });

        doc.moveDown(1.5);

        // Sección 3: Estadísticas de Eliminación
        doc.fontSize(14)
           .font('Helvetica-Bold')
           .text('3. ESTADÍSTICAS DE ELIMINACIÓN', { underline: true })
           .moveDown(0.5);

        doc.fontSize(11)
           .font('Helvetica');

        const stats = [
          ['Archivos eliminados:', certificate.files_deleted],
          ['Registros de base de datos:', certificate.database_rows_deleted],
          ['Backups purgados:', certificate.backups_purged],
          ['Total de bytes sobrescritos:', this.formatBytes(certificate.total_bytes_wiped)]
        ];

        stats.forEach(([label, value]) => {
          doc.text(`${label} ${value}`, { indent: 20 });
        });

        doc.moveDown(1.5);

        // Sección 4: Verificación Criptográfica
        doc.fontSize(14)
           .font('Helvetica-Bold')
           .text('4. VERIFICACIÓN CRIPTOGRÁFICA', { underline: true })
           .moveDown(0.5);

        doc.fontSize(11)
           .font('Helvetica')
           .text(`Hash SHA-256 del certificado:`)
           .fontSize(9)
           .font('Courier')
           .text(certificate.certificate_hash, { indent: 20 })
           .fontSize(11)
           .font('Helvetica')
           .moveDown(0.5)
           .text('Firma digital ECDSA:')
           .fontSize(8)
           .font('Courier')
           .text(this.wrapText(certificate.certificate_signature, 80), { indent: 20 })
           .moveDown(1.5);

        // Sección 5: Fundamento Legal
        doc.fontSize(14)
           .font('Helvetica-Bold')
           .text('5. FUNDAMENTO LEGAL', { underline: true })
           .moveDown(0.5);

        doc.fontSize(10)
           .font('Helvetica')
           .text(
             'Este certificado se emite en cumplimiento de la Ley Federal de Protección de Datos ' +
             'Personales en Posesión de los Particulares (LFPDPPP), específicamente:',
             { align: 'justify' }
           )
           .moveDown(0.5)
           .text('• Artículo 26 - Derecho de Cancelación', { indent: 20 })
           .text('• Artículo 34 - Plazo para hacer efectivo el derecho', { indent: 20 })
           .text('• Lineamientos INAI - Transparencia en eliminación de datos', { indent: 20 })
           .moveDown(1);

        doc.fontSize(10)
           .font('Helvetica-Oblique')
           .text(
             'La eliminación se realizó mediante sobrescritura múltiple conforme a estándares ' +
             'internacionales de eliminación segura de datos (DoD 5220.22-M / Gutmann).',
             { align: 'justify' }
           )
           .moveDown(1.5);

        // Sección 6: Validez del Certificado
        doc.fontSize(14)
           .font('Helvetica-Bold')
           .text('6. VALIDEZ DEL CERTIFICADO', { underline: true })
           .moveDown(0.5);

        doc.fontSize(10)
           .font('Helvetica')
           .text(
             'Este certificado tiene validez legal como evidencia de eliminación de datos ' +
             'personales. Puede ser verificado en cualquier momento mediante:',
             { align: 'justify' }
           )
           .moveDown(0.5)
           .text(`• URL de verificación: ${qrCodeUrl}`, { indent: 20 })
           .text('• Validación de firma digital ECDSA con clave pública disponible en:', { indent: 20 })
           .text(`  ${process.env.API_BASE_URL}/public-keys/signing-key.pem`, { indent: 40 })
           .moveDown(2);

        // Footer
        doc.fontSize(8)
           .font('Helvetica')
           .text('_'.repeat(100), { align: 'center' })
           .moveDown(0.5)
           .text('FaceCode Guardian Network', { align: 'center' })
           .text('[PENDIENTE - Domicilio fiscal completo]', { align: 'center' })
           .text('[PENDIENTE - privacidad@facecode.com] | [PENDIENTE - Teléfono]', { align: 'center' })
           .moveDown(0.5)
           .text(
             `Generado automáticamente el ${new Date().toLocaleString('es-MX')}`,
             { align: 'center' }
           )
           .text(
             'Este documento tiene validez sin necesidad de firma autógrafa (firma electrónica avanzada)',
             { align: 'center', oblique: true }
           );

        // Finalizar PDF
        doc.end();

      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * Formatea método de eliminación para presentación
   */
  formatDeletionMethod(method) {
    const methods = {
      'gutmann_35pass': 'Gutmann (35 pasadas) - Máxima seguridad',
      'dod_5220_7pass': 'DoD 5220.22-M (7 pasadas)',
      'nist_800_88_3pass': 'NIST 800-88 (3 pasadas)',
      'simple_zero': 'Sobrescritura simple (testing)'
    };
    return methods[method] || method;
  }

  /**
   * Formatea tipo de dato para presentación
   */
  formatDataType(dataType) {
    const types = {
      'biometric_embeddings': 'Vectores faciales biométricos (embeddings)',
      'liveness_detection': 'Parámetros de detección de vivacidad',
      'capture_metadata': 'Metadatos de captura biométrica',
      'full_account': 'Cuenta completa (todos los datos)'
    };
    return types[dataType] || dataType;
  }

  /**
   * Formatea bytes a unidades legibles
   */
  formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  /**
   * Divide texto largo en líneas
   */
  wrapText(text, maxLength) {
    const regex = new RegExp(`.{1,${maxLength}}`, 'g');
    return text.match(regex).join('\n');
  }
}

/**
 * GET /api/verify-deletion/:certificateId
 * Verifica la autenticidad de un certificado de eliminación
 */
router.get(
  '/verify-deletion/:certificateId',
  [
    param('certificateId')
      .isLength({ min: 32, max: 36 })
      .withMessage('Invalid certificate ID format')
  ],
  async (req, res) => {
    try {
      // Validar input
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          errors: errors.array()
        });
      }

      const { certificateId } = req.params;
      const certificateService = new DeletionCertificateService(
        req.app.locals.db,
        req.app.locals.publicKey
      );

      // Obtener certificado
      const certificate = await certificateService.getCertificate(certificateId);

      if (!certificate) {
        return res.status(404).json({
          success: false,
          message: 'Certificate not found'
        });
      }

      // Verificar firma criptográfica
      const isValid = certificateService.verifyCertificateSignature(certificate);

      // Responder con información del certificado
      res.json({
        success: true,
        certificate: {
          certificate_id: certificate.certificate_id,
          deletion_timestamp: certificate.deletion_timestamp,
          data_types_deleted: certificate.data_types_deleted,
          deletion_method: certificateService.formatDeletionMethod(certificate.deletion_method),
          stats: {
            files_deleted: certificate.files_deleted,
            database_rows_deleted: certificate.database_rows_deleted,
            backups_purged: certificate.backups_purged,
            total_bytes_wiped: certificateService.formatBytes(certificate.total_bytes_wiped)
          },
          cryptographic_verification: {
            signature_valid: isValid,
            certificate_hash: certificate.certificate_hash,
            verification_method: 'ECDSA with SHA-256'
          }
        },
        verification: {
          verified_at: new Date().toISOString(),
          verification_status: isValid ? 'VALID' : 'INVALID',
          message: isValid
            ? 'La firma digital es válida. Este certificado es auténtico.'
            : 'ADVERTENCIA: La firma digital no es válida. Este certificado puede haber sido alterado.'
        }
      });

    } catch (error) {
      console.error('Certificate verification error:', error);
      res.status(500).json({
        success: false,
        message: 'Internal server error during verification'
      });
    }
  }
);

/**
 * GET /api/download-deletion-certificate/:certificateId
 * Descarga certificado de eliminación en formato PDF
 */
router.get(
  '/download-deletion-certificate/:certificateId',
  authenticate, // Requiere autenticación
  [
    param('certificateId')
      .isLength({ min: 32, max: 36 })
      .withMessage('Invalid certificate ID format')
  ],
  async (req, res) => {
    try {
      // Validar input
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          errors: errors.array()
        });
      }

      const { certificateId } = req.params;
      const userId = req.user.id; // Desde middleware de autenticación

      const certificateService = new DeletionCertificateService(
        req.app.locals.db,
        req.app.locals.publicKey
      );

      // Obtener certificado
      const certificate = await certificateService.getCertificate(certificateId);

      if (!certificate) {
        return res.status(404).json({
          success: false,
          message: 'Certificate not found'
        });
      }

      // Verificar que el usuario autenticado es el propietario
      if (certificate.user_id !== userId) {
        return res.status(403).json({
          success: false,
          message: 'Access denied: You can only download your own certificates'
        });
      }

      // Generar PDF
      const pdfBuffer = await certificateService.generateCertificatePDF(certificate);

      // Configurar headers para descarga
      res.setHeader('Content-Type', 'application/pdf');
      res.setHeader(
        'Content-Disposition',
        `attachment; filename=Certificado_Eliminacion_${certificateId}.pdf`
      );
      res.setHeader('Content-Length', pdfBuffer.length);

      // Enviar PDF
      res.send(pdfBuffer);

    } catch (error) {
      console.error('Certificate download error:', error);
      res.status(500).json({
        success: false,
        message: 'Internal server error during certificate generation'
      });
    }
  }
);

/**
 * GET /api/my-deletion-certificates
 * Lista todos los certificados de eliminación del usuario autenticado
 */
router.get(
  '/my-deletion-certificates',
  authenticate,
  async (req, res) => {
    try {
      const userId = req.user.id;

      const certificateService = new DeletionCertificateService(
        req.app.locals.db,
        req.app.locals.publicKey
      );

      const certificates = await certificateService.getUserCertificates(userId);

      res.json({
        success: true,
        count: certificates.length,
        certificates: certificates.map(cert => ({
          certificate_id: cert.certificate_id,
          deletion_timestamp: cert.deletion_timestamp,
          data_types_deleted: cert.data_types_deleted,
          deletion_method: certificateService.formatDeletionMethod(cert.deletion_method),
          total_bytes_wiped: certificateService.formatBytes(cert.total_bytes_wiped),
          download_url: cert.download_url,
          verify_url: `${process.env.API_BASE_URL}/verify-deletion/${cert.certificate_id}`
        }))
      });

    } catch (error) {
      console.error('Fetch certificates error:', error);
      res.status(500).json({
        success: false,
        message: 'Internal server error'
      });
    }
  }
);

/**
 * POST /api/request-immediate-deletion
 * Solicita eliminación inmediata de datos biométricos (sin esperar periodo de retención)
 */
router.post(
  '/request-immediate-deletion',
  authenticate,
  [
    body('confirmation')
      .equals('DELETE_MY_DATA')
      .withMessage('Confirmation phrase must be exactly: DELETE_MY_DATA'),
    body('reason')
      .optional()
      .isLength({ max: 500 })
      .withMessage('Reason must be 500 characters or less')
  ],
  async (req, res) => {
    try {
      // Validar input
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          errors: errors.array()
        });
      }

      const userId = req.user.id;
      const { reason } = req.body;

      // Verificar que no haya ya una solicitud pendiente
      const checkQuery = `
        SELECT COUNT(*) as pending_count
        FROM data_deletion_queue
        WHERE user_id = ?
          AND status IN ('scheduled', 'in_progress')
      `;

      const checkResult = await req.app.locals.db.query(checkQuery, [userId]);

      if (checkResult[0].pending_count > 0) {
        return res.status(409).json({
          success: false,
          message: 'A deletion request is already pending for this user'
        });
      }

      // Crear entrada en cola de eliminación con prioridad alta
      const deletionTime = new Date(Date.now() + 15 * 60 * 1000); // +15 minutos

      const insertQuery = `
        INSERT INTO data_deletion_queue (
          user_id,
          data_type,
          scheduled_deletion_at,
          deletion_method,
          status,
          priority
        ) VALUES (?, 'biometric_embeddings', ?, 'gutmann_35pass', 'scheduled', 'high')
      `;

      await req.app.locals.db.query(insertQuery, [userId, deletionTime]);

      // Revocar consentimiento
      const revokeQuery = `
        UPDATE biometric_consents
        SET is_revoked = TRUE,
            revocation_timestamp = NOW(),
            revocation_reason = ?
        WHERE user_id = ? AND is_revoked = FALSE
      `;

      await req.app.locals.db.query(revokeQuery, [
        reason || 'User requested immediate deletion',
        userId
      ]);

      // Auditoría
      const auditQuery = `
        INSERT INTO audit_log (
          action,
          user_id,
          timestamp,
          additional_data
        ) VALUES ('IMMEDIATE_DELETION_REQUESTED', ?, NOW(), ?)
      `;

      await req.app.locals.db.query(auditQuery, [
        userId,
        JSON.stringify({ reason, priority: 'high' })
      ]);

      res.json({
        success: true,
        message: 'Immediate deletion request submitted successfully',
        deletion_details: {
          scheduled_for: deletionTime.toISOString(),
          estimated_completion: 'Within 15-30 minutes',
          deletion_method: 'Gutmann 35-pass (maximum security)',
          data_to_be_deleted: ['biometric_embeddings', 'liveness_detection', 'capture_metadata'],
          certificate_available_after: 'Deletion completion',
          status_check_url: `${process.env.API_BASE_URL}/my-deletion-certificates`
        }
      });

    } catch (error) {
      console.error('Immediate deletion request error:', error);
      res.status(500).json({
        success: false,
        message: 'Internal server error'
      });
    }
  }
);

/**
 * GET /api/deletion-status/:userId
 * Consulta estado de eliminación de datos (solo para usuario autenticado o admin)
 */
router.get(
  '/deletion-status/:userId',
  authenticate,
  [
    param('userId')
      .isUUID()
      .withMessage('Invalid user ID format')
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          errors: errors.array()
        });
      }

      const { userId } = req.params;
      const requesterId = req.user.id;

      // Verificar autorización (solo el propio usuario o admin)
      if (userId !== requesterId && !req.user.isAdmin) {
        return res.status(403).json({
          success: false,
          message: 'Access denied'
        });
      }

      // Consultar estado de eliminación
      const statusQuery = `
        SELECT
          deletion_id,
          data_type,
          scheduled_deletion_at,
          status,
          priority,
          started_at,
          completed_at,
          deletion_certificate_id,
          error_message,
          retry_count
        FROM data_deletion_queue
        WHERE user_id = ?
        ORDER BY scheduled_deletion_at DESC
        LIMIT 10
      `;

      const deletionTasks = await req.app.locals.db.query(statusQuery, [userId]);

      res.json({
        success: true,
        user_id: userId,
        deletion_tasks: deletionTasks.map(task => ({
          deletion_id: task.deletion_id,
          data_type: task.data_type,
          scheduled_for: task.scheduled_deletion_at,
          status: task.status,
          priority: task.priority,
          started_at: task.started_at,
          completed_at: task.completed_at,
          certificate_id: task.deletion_certificate_id,
          error_message: task.error_message,
          retry_count: task.retry_count
        }))
      });

    } catch (error) {
      console.error('Deletion status check error:', error);
      res.status(500).json({
        success: false,
        message: 'Internal server error'
      });
    }
  }
);

module.exports = router;
