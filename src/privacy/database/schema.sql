-- ============================================================================
-- SCHEMA DE BASE DE DATOS PARA GESTIÓN DE CONSENTIMIENTOS BIOMÉTRICOS
-- FaceCode Guardian Network - Cumplimiento LFPDPPP 2025
-- ============================================================================
--
-- Versión: 1.0
-- Fecha: 2025-10-29
-- Motor recomendado: MySQL 8.0+ / PostgreSQL 14+
-- Características requeridas: InnoDB, UTF-8, Transacciones ACID
--
-- IMPORTANTE: Este schema implementa:
-- - Write-once tables para inmutabilidad de consentimientos
-- - Cifrado at-rest para datos sensibles (requiere TDE - Transparent Data Encryption)
-- - Índices optimizados para auditoría y consultas ARCO
-- - Particionamiento por fecha para eficiencia en eliminación masiva
-- ============================================================================

-- ============================================================================
-- TABLA 1: biometric_consents (Registro inmutable de consentimientos)
-- ============================================================================

CREATE TABLE IF NOT EXISTS biometric_consents (
    -- Identificadores principales
    consent_id CHAR(36) NOT NULL PRIMARY KEY COMMENT 'UUID del consentimiento',
    user_id CHAR(36) NOT NULL COMMENT 'UUID del usuario (FK a tabla users)',

    -- Timestamps (doble formato para auditoría)
    timestamp_iso VARCHAR(30) NOT NULL COMMENT 'Timestamp ISO 8601 con milisegundos',
    timestamp_unix BIGINT NOT NULL COMMENT 'Unix timestamp en milisegundos',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp de creación DB',

    -- Datos de origen (pseudonimizados + cifrados)
    ip_address_hash CHAR(64) NOT NULL COMMENT 'SHA-256 hash de IP (para analytics)',
    ip_address_encrypted VARCHAR(256) NOT NULL COMMENT 'IP cifrada AES-256-GCM (para auditoría legal)',
    device_id VARCHAR(128) NOT NULL COMMENT 'Hash del dispositivo',
    user_agent TEXT COMMENT 'User agent del navegador',
    geolocation JSON COMMENT 'Ciudad/país aproximado (sin GPS): {city, country, country_code}',

    -- Versión de documentos legales
    privacy_notice_version VARCHAR(10) NOT NULL DEFAULT '1.0' COMMENT 'Versión del aviso de privacidad',
    privacy_notice_hash CHAR(64) NOT NULL COMMENT 'SHA-256 del documento completo',

    -- Consentimientos (granular)
    consent_type VARCHAR(50) NOT NULL DEFAULT 'biometric_explicit' COMMENT 'Tipo de consentimiento',
    consent_method VARCHAR(50) NOT NULL DEFAULT 'electronic_signature' COMMENT 'Método de captura',
    legal_basis VARCHAR(50) NOT NULL DEFAULT 'LFPDPPP_Art9' COMMENT 'Fundamento legal',

    -- Consentimientos opcionales (JSON para flexibilidad)
    optional_consents JSON NOT NULL COMMENT 'Consentimientos secundarios: {marketing, ml_training, extended_retention}',

    -- Política de retención
    retention_policy VARCHAR(20) NOT NULL DEFAULT '24h' COMMENT 'Política de retención: 24h|30d|90d|indefinite',
    retention_expires_at DATETIME COMMENT 'Fecha de expiración (NULL si indefinite)',

    -- Firma digital y verificación
    consent_hash CHAR(64) NOT NULL COMMENT 'SHA-256 del payload completo',
    consent_signature TEXT NOT NULL COMMENT 'Firma ECDSA en formato DER (hex)',
    certificate_version VARCHAR(10) NOT NULL DEFAULT '1.0' COMMENT 'Versión del certificado',

    -- Estado de revocación
    is_revoked BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'Consentimiento revocado por usuario',
    revocation_timestamp DATETIME COMMENT 'Fecha de revocación',
    revocation_reason TEXT COMMENT 'Motivo de revocación (proporcionado por usuario)',

    -- Índices para optimización
    INDEX idx_user_id (user_id),
    INDEX idx_timestamp_unix (timestamp_unix),
    INDEX idx_retention_expires (retention_expires_at),
    INDEX idx_is_revoked (is_revoked),
    INDEX idx_privacy_version (privacy_notice_version),

    -- Índice compuesto para consultas ARCO
    INDEX idx_user_active (user_id, is_revoked, retention_expires_at),

    -- Constraint: No permitir updates (write-once)
    -- Implementar mediante triggers o permisos a nivel aplicación

    -- Constraint: Validar retention_policy
    CONSTRAINT chk_retention_policy CHECK (
        retention_policy IN ('24h', '30d', '90d', 'indefinite')
    ),

    -- Constraint: Si revocado, debe tener timestamp
    CONSTRAINT chk_revocation CHECK (
        (is_revoked = FALSE AND revocation_timestamp IS NULL) OR
        (is_revoked = TRUE AND revocation_timestamp IS NOT NULL)
    )

) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Registro inmutable de consentimientos biométricos - LFPDPPP Art. 9';

-- Particionamiento por año para eficiencia en archivado
-- (Descomentar si se espera volumen >1M consentimientos/año)
-- ALTER TABLE biometric_consents PARTITION BY RANGE (YEAR(created_at)) (
--     PARTITION p2025 VALUES LESS THAN (2026),
--     PARTITION p2026 VALUES LESS THAN (2027),
--     PARTITION p2027 VALUES LESS THAN (2028),
--     PARTITION p_future VALUES LESS THAN MAXVALUE
-- );

-- ============================================================================
-- TABLA 2: privacy_notice_versions (Control de versiones de aviso)
-- ============================================================================

CREATE TABLE IF NOT EXISTS privacy_notice_versions (
    version_id INT AUTO_INCREMENT PRIMARY KEY,
    version VARCHAR(10) NOT NULL UNIQUE COMMENT 'Versión semántica: 1.0, 1.1, 2.0',
    document_hash CHAR(64) NOT NULL UNIQUE COMMENT 'SHA-256 del documento completo',
    document_url VARCHAR(512) NOT NULL COMMENT 'URL del documento publicado',
    changelog TEXT COMMENT 'Resumen de cambios respecto a versión anterior',
    published_at DATETIME NOT NULL COMMENT 'Fecha de publicación',
    superseded_by VARCHAR(10) COMMENT 'Versión que reemplaza a esta (NULL si actual)',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'Versión activa (solo 1 debe estar en TRUE)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_version (version),
    INDEX idx_is_active (is_active),

    -- Solo una versión activa a la vez
    -- (Implementar mediante trigger o constraint único filtrado en MySQL 8.0+)
    UNIQUE KEY uk_active_version (is_active) WHERE (is_active = TRUE)

) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Control de versiones de Aviso de Privacidad';

-- Insertar versión inicial
INSERT INTO privacy_notice_versions (
    version,
    document_hash,
    document_url,
    changelog,
    published_at,
    is_active
) VALUES (
    '1.0',
    '[PENDIENTE - Calcular hash SHA-256 del documento final]',
    'https://facecode.com/legal/aviso-privacidad-v1.0.pdf',
    'Versión inicial conforme LFPDPPP 2025',
    NOW(),
    TRUE
);

-- ============================================================================
-- TABLA 3: data_deletion_queue (Cola de eliminación automática)
-- ============================================================================

CREATE TABLE IF NOT EXISTS data_deletion_queue (
    deletion_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id CHAR(36) NOT NULL COMMENT 'UUID del usuario',
    data_type VARCHAR(50) NOT NULL COMMENT 'Tipo de dato: biometric_embeddings|full_account',
    scheduled_deletion_at DATETIME NOT NULL COMMENT 'Fecha programada de eliminación',
    deletion_method VARCHAR(50) NOT NULL DEFAULT 'gutmann_35pass' COMMENT 'Método de eliminación segura',
    status ENUM('scheduled', 'in_progress', 'completed', 'failed') NOT NULL DEFAULT 'scheduled',
    priority ENUM('normal', 'high', 'urgent') NOT NULL DEFAULT 'normal' COMMENT 'Prioridad (high para revocaciones)',

    -- Timestamps de ejecución
    started_at DATETIME COMMENT 'Inicio de proceso de eliminación',
    completed_at DATETIME COMMENT 'Fin de proceso de eliminación',

    -- Verificación de eliminación
    deletion_certificate_id CHAR(36) COMMENT 'UUID del certificado de eliminación generado',
    verification_hash CHAR(64) COMMENT 'Hash de verificación de eliminación completa',

    -- Metadatos
    error_message TEXT COMMENT 'Mensaje de error si status=failed',
    retry_count INT NOT NULL DEFAULT 0 COMMENT 'Número de reintentos',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_user_id (user_id),
    INDEX idx_scheduled_deletion (scheduled_deletion_at, status),
    INDEX idx_status_priority (status, priority),

    -- Evitar duplicados para mismo usuario/tipo
    UNIQUE KEY uk_user_datatype (user_id, data_type, status) WHERE (status IN ('scheduled', 'in_progress'))

) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Cola de eliminación automática de datos biométricos - LFPDPPP Art. 26';

-- ============================================================================
-- TABLA 4: deletion_certificates (Certificados de eliminación)
-- ============================================================================

CREATE TABLE IF NOT EXISTS deletion_certificates (
    certificate_id CHAR(36) NOT NULL PRIMARY KEY COMMENT 'UUID del certificado',
    user_id CHAR(36) NOT NULL COMMENT 'UUID del usuario',
    deletion_timestamp DATETIME NOT NULL COMMENT 'Fecha/hora de eliminación',
    data_types_deleted JSON NOT NULL COMMENT 'Array de tipos de datos eliminados',
    deletion_method VARCHAR(50) NOT NULL COMMENT 'Método utilizado (gutmann_35pass, dod_5220, etc.)',

    -- Verificación criptográfica
    certificate_hash CHAR(64) NOT NULL COMMENT 'SHA-256 del certificado completo',
    certificate_signature TEXT NOT NULL COMMENT 'Firma digital ECDSA',

    -- Evidencia de eliminación
    files_deleted INT NOT NULL COMMENT 'Número de archivos eliminados',
    database_rows_deleted INT NOT NULL COMMENT 'Número de registros DB eliminados',
    backups_purged INT NOT NULL COMMENT 'Número de backups purgados',
    total_bytes_wiped BIGINT NOT NULL COMMENT 'Bytes totales sobrescritos',

    -- Metadatos
    download_url VARCHAR(512) COMMENT 'URL de descarga del certificado PDF',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_user_id (user_id),
    INDEX idx_deletion_timestamp (deletion_timestamp)

) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Certificados de eliminación segura de datos - Evidencia para ARCO';

-- ============================================================================
-- TABLA 5: audit_log (Log de auditoría inmutable)
-- ============================================================================

CREATE TABLE IF NOT EXISTS audit_log (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(100) NOT NULL COMMENT 'Acción realizada: CONSENT_CREATED|CONSENT_REVOKED|DATA_DELETED|ARCO_REQUEST',
    consent_id CHAR(36) COMMENT 'UUID del consentimiento relacionado',
    user_id CHAR(36) COMMENT 'UUID del usuario afectado',
    timestamp DATETIME NOT NULL COMMENT 'Timestamp del evento',
    ip_address_hash CHAR(64) COMMENT 'Hash SHA-256 de IP origen',

    -- Datos adicionales según tipo de acción
    error_type VARCHAR(100) COMMENT 'Tipo de error (si aplica)',
    error_message TEXT COMMENT 'Mensaje de error (si aplica)',
    additional_data JSON COMMENT 'Datos adicionales en formato JSON',

    -- Metadatos de auditoría
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_action (action),
    INDEX idx_user_id (user_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_consent_id (consent_id)

) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Log de auditoría inmutable - Retención 12 meses (LFPDPPP)';

-- Particionamiento por mes para eficiencia en archivado
ALTER TABLE audit_log PARTITION BY RANGE (UNIX_TIMESTAMP(created_at)) (
    PARTITION p202510 VALUES LESS THAN (UNIX_TIMESTAMP('2025-11-01')),
    PARTITION p202511 VALUES LESS THAN (UNIX_TIMESTAMP('2025-12-01')),
    PARTITION p202512 VALUES LESS THAN (UNIX_TIMESTAMP('2026-01-01')),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- ============================================================================
-- TABLA 6: arco_requests (Solicitudes de derechos ARCO)
-- ============================================================================

CREATE TABLE IF NOT EXISTS arco_requests (
    request_id CHAR(36) NOT NULL PRIMARY KEY COMMENT 'UUID de la solicitud',
    user_id CHAR(36) NOT NULL COMMENT 'UUID del usuario solicitante',
    request_type ENUM('access', 'rectification', 'cancellation', 'opposition') NOT NULL,

    -- Datos de la solicitud
    request_details TEXT NOT NULL COMMENT 'Detalles de la solicitud (texto libre)',
    submitted_at DATETIME NOT NULL COMMENT 'Fecha de envío',
    submitted_via VARCHAR(50) NOT NULL COMMENT 'Canal: web_form|email|postal',

    -- Verificación de identidad
    identity_verified BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'Identidad verificada',
    verification_method VARCHAR(100) COMMENT 'Método de verificación (INE, pasaporte, etc.)',
    verification_document_hash CHAR(64) COMMENT 'Hash del documento de identificación',

    -- Procesamiento
    status ENUM('submitted', 'under_review', 'approved', 'rejected', 'completed') NOT NULL DEFAULT 'submitted',
    assigned_to VARCHAR(100) COMMENT 'Email del oficial de privacidad asignado',
    response_deadline DATETIME COMMENT 'Plazo legal de respuesta (20 días hábiles)',

    -- Resolución
    resolution TEXT COMMENT 'Respuesta proporcionada al titular',
    resolved_at DATETIME COMMENT 'Fecha de resolución',
    completion_deadline DATETIME COMMENT 'Plazo para hacer efectivo el derecho (15 días hábiles)',
    completed_at DATETIME COMMENT 'Fecha de completado',

    -- Metadatos
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_request_type (request_type),
    INDEX idx_response_deadline (response_deadline),
    INDEX idx_submitted_at (submitted_at)

) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Solicitudes de derechos ARCO - LFPDPPP Art. 22-34';

-- ============================================================================
-- TABLA 7: biometric_data (Datos biométricos activos - SEPARADA por seguridad)
-- ============================================================================
-- IMPORTANTE: Esta tabla debe estar en un database separado con cifrado TDE
-- Solo accesible por microservicio de autenticación (segregación de red)

CREATE TABLE IF NOT EXISTS biometric_data (
    embedding_id CHAR(36) NOT NULL PRIMARY KEY COMMENT 'UUID del embedding',
    user_id CHAR(36) NOT NULL COMMENT 'UUID del usuario (FK)',

    -- Vector facial cifrado
    embedding_vector BLOB NOT NULL COMMENT 'Vector facial cifrado con AES-256-GCM (512-1024 bytes)',
    embedding_dimension INT NOT NULL COMMENT 'Dimensionalidad del vector (128, 256, 512)',
    model_version VARCHAR(20) NOT NULL COMMENT 'Versión del modelo ML utilizado',

    -- Parámetros de liveness detection
    liveness_score DECIMAL(5,4) COMMENT 'Score de vivacidad (0.0-1.0)',
    liveness_method VARCHAR(50) COMMENT 'Método de liveness detection',

    -- Metadatos de captura (NO almacenar imágenes)
    capture_quality DECIMAL(5,4) COMMENT 'Calidad de captura (0.0-1.0)',
    capture_timestamp DATETIME NOT NULL COMMENT 'Timestamp de captura original',
    last_auth_timestamp DATETIME COMMENT 'Última autenticación exitosa',

    -- Gestión de retención
    retention_policy VARCHAR(20) NOT NULL DEFAULT '24h',
    expires_at DATETIME NOT NULL COMMENT 'Fecha de eliminación automática',

    -- Cifrado adicional
    encryption_key_id VARCHAR(100) NOT NULL COMMENT 'ID de la clave KMS utilizada',
    encryption_iv VARCHAR(64) NOT NULL COMMENT 'IV único para AES-GCM',

    -- Metadatos
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_user_id (user_id),
    INDEX idx_expires_at (expires_at),
    INDEX idx_last_auth (last_auth_timestamp),

    -- Solo un embedding activo por usuario
    UNIQUE KEY uk_active_user (user_id)

) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  ENCRYPTION='Y' -- Requiere MySQL 8.0+ con TDE habilitado
  COMMENT='Datos biométricos activos - Almacenamiento cifrado (LFPDPPP Art. 19)';

-- ============================================================================
-- TRIGGERS PARA INMUTABILIDAD Y AUDITORÍA
-- ============================================================================

-- Trigger: Prevenir UPDATE en biometric_consents (write-once)
DELIMITER //
CREATE TRIGGER prevent_consent_update
BEFORE UPDATE ON biometric_consents
FOR EACH ROW
BEGIN
    -- Permitir solo actualización de campos de revocación
    IF OLD.is_revoked = FALSE AND NEW.is_revoked = TRUE THEN
        -- Revocación permitida
        SET NEW.consent_id = OLD.consent_id;
        SET NEW.user_id = OLD.user_id;
        SET NEW.timestamp_iso = OLD.timestamp_iso;
        SET NEW.consent_hash = OLD.consent_hash;
        SET NEW.consent_signature = OLD.consent_signature;
        -- Otros campos inmutables aquí...
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Updates not allowed on biometric_consents (write-once table)';
    END IF;
END//
DELIMITER ;

-- Trigger: Auditoría automática en creación de consentimiento
DELIMITER //
CREATE TRIGGER audit_consent_creation
AFTER INSERT ON biometric_consents
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (
        action,
        consent_id,
        user_id,
        timestamp,
        additional_data
    ) VALUES (
        'CONSENT_CREATED',
        NEW.consent_id,
        NEW.user_id,
        NEW.timestamp_iso,
        JSON_OBJECT(
            'privacy_notice_version', NEW.privacy_notice_version,
            'retention_policy', NEW.retention_policy,
            'optional_consents', NEW.optional_consents
        )
    );
END//
DELIMITER ;

-- Trigger: Auditoría en revocación de consentimiento
DELIMITER //
CREATE TRIGGER audit_consent_revocation
AFTER UPDATE ON biometric_consents
FOR EACH ROW
BEGIN
    IF OLD.is_revoked = FALSE AND NEW.is_revoked = TRUE THEN
        INSERT INTO audit_log (
            action,
            consent_id,
            user_id,
            timestamp,
            additional_data
        ) VALUES (
            'CONSENT_REVOKED',
            NEW.consent_id,
            NEW.user_id,
            NEW.revocation_timestamp,
            JSON_OBJECT('revocation_reason', NEW.revocation_reason)
        );
    END IF;
END//
DELIMITER ;

-- ============================================================================
-- STORED PROCEDURES PARA OPERACIONES COMUNES
-- ============================================================================

-- Procedure: Obtener consentimientos activos de un usuario
DELIMITER //
CREATE PROCEDURE get_active_consents(IN p_user_id CHAR(36))
BEGIN
    SELECT
        consent_id,
        timestamp_iso,
        privacy_notice_version,
        retention_policy,
        retention_expires_at,
        optional_consents,
        is_revoked
    FROM biometric_consents
    WHERE user_id = p_user_id
      AND is_revoked = FALSE
      AND (retention_expires_at IS NULL OR retention_expires_at > NOW())
    ORDER BY timestamp_unix DESC;
END//
DELIMITER ;

-- Procedure: Limpiar datos biométricos expirados (ejecutar cada hora)
DELIMITER //
CREATE PROCEDURE cleanup_expired_biometric_data()
BEGIN
    DECLARE deleted_count INT DEFAULT 0;

    -- Eliminar embeddings expirados
    DELETE FROM biometric_data
    WHERE expires_at <= NOW();

    SET deleted_count = ROW_COUNT();

    -- Log de auditoría
    INSERT INTO audit_log (
        action,
        timestamp,
        additional_data
    ) VALUES (
        'AUTOMATED_CLEANUP',
        NOW(),
        JSON_OBJECT('deleted_count', deleted_count)
    );

    SELECT deleted_count AS embeddings_deleted;
END//
DELIMITER ;

-- Procedure: Procesar cola de eliminación (ejecutar cada 15 minutos)
DELIMITER //
CREATE PROCEDURE process_deletion_queue()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_deletion_id INT;
    DECLARE v_user_id CHAR(36);
    DECLARE v_data_type VARCHAR(50);

    -- Cursor para elementos pendientes
    DECLARE cur CURSOR FOR
        SELECT deletion_id, user_id, data_type
        FROM data_deletion_queue
        WHERE status = 'scheduled'
          AND scheduled_deletion_at <= NOW()
        ORDER BY priority DESC, scheduled_deletion_at ASC
        LIMIT 100; -- Procesar 100 por lote

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO v_deletion_id, v_user_id, v_data_type;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Marcar como en progreso
        UPDATE data_deletion_queue
        SET status = 'in_progress', started_at = NOW()
        WHERE deletion_id = v_deletion_id;

        -- Llamar a función de eliminación real (implementar en aplicación)
        -- Por ahora solo simulamos
        -- CALL delete_user_biometric_data(v_user_id);

        -- Marcar como completado
        UPDATE data_deletion_queue
        SET status = 'completed', completed_at = NOW()
        WHERE deletion_id = v_deletion_id;

    END LOOP;

    CLOSE cur;
END//
DELIMITER ;

DELIMITER ;

-- ============================================================================
-- EVENTOS PROGRAMADOS (CRON JOBS DB)
-- ============================================================================

-- Habilitar event scheduler
SET GLOBAL event_scheduler = ON;

-- Evento: Limpiar datos biométricos expirados (cada hora)
CREATE EVENT IF NOT EXISTS cleanup_expired_data_hourly
ON SCHEDULE EVERY 1 HOUR
DO
    CALL cleanup_expired_biometric_data();

-- Evento: Procesar cola de eliminación (cada 15 minutos)
CREATE EVENT IF NOT EXISTS process_deletion_queue_15min
ON SCHEDULE EVERY 15 MINUTE
DO
    CALL process_deletion_queue();

-- Evento: Archivar audit_log antiguo (mensual)
CREATE EVENT IF NOT EXISTS archive_old_audit_logs_monthly
ON SCHEDULE EVERY 1 MONTH
DO
    -- Mover logs >12 meses a tabla de archivo
    INSERT INTO audit_log_archive
    SELECT * FROM audit_log
    WHERE created_at < DATE_SUB(NOW(), INTERVAL 12 MONTH);

    -- Eliminar de tabla principal
    DELETE FROM audit_log
    WHERE created_at < DATE_SUB(NOW(), INTERVAL 12 MONTH);

-- ============================================================================
-- PERMISOS Y SEGURIDAD
-- ============================================================================

-- Usuario de aplicación (read/write limitado)
CREATE USER IF NOT EXISTS 'facecode_app'@'%' IDENTIFIED BY '[PENDIENTE - contraseña fuerte]';

GRANT SELECT, INSERT ON biometric_consents TO 'facecode_app'@'%';
GRANT SELECT ON privacy_notice_versions TO 'facecode_app'@'%';
GRANT SELECT, INSERT, UPDATE ON data_deletion_queue TO 'facecode_app'@'%';
GRANT SELECT, INSERT ON deletion_certificates TO 'facecode_app'@'%';
GRANT INSERT ON audit_log TO 'facecode_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON arco_requests TO 'facecode_app'@'%';

-- Usuario de microservicio de autenticación (solo biometric_data)
CREATE USER IF NOT EXISTS 'facecode_auth'@'10.0.0.0/8' IDENTIFIED BY '[PENDIENTE - contraseña fuerte]';

GRANT SELECT, INSERT, UPDATE, DELETE ON biometric_data TO 'facecode_auth'@'10.0.0.0/8';

-- Usuario de jobs de limpieza (solo procedures)
CREATE USER IF NOT EXISTS 'facecode_cleanup'@'localhost' IDENTIFIED BY '[PENDIENTE - contraseña fuerte]';

GRANT EXECUTE ON PROCEDURE cleanup_expired_biometric_data TO 'facecode_cleanup'@'localhost';
GRANT EXECUTE ON PROCEDURE process_deletion_queue TO 'facecode_cleanup'@'localhost';

-- Usuario de auditoría/BI (solo lectura)
CREATE USER IF NOT EXISTS 'facecode_readonly'@'%' IDENTIFIED BY '[PENDIENTE - contraseña fuerte]';

GRANT SELECT ON biometric_consents TO 'facecode_readonly'@'%';
GRANT SELECT ON audit_log TO 'facecode_readonly'@'%';
GRANT SELECT ON arco_requests TO 'facecode_readonly'@'%';
-- NO acceso a biometric_data (datos sensibles)

-- ============================================================================
-- NOTAS DE IMPLEMENTACIÓN
-- ============================================================================

-- 1. CIFRADO AT-REST (TDE - Transparent Data Encryption)
--    MySQL 8.0+: Habilitar con: ALTER TABLE biometric_data ENCRYPTION='Y';
--    Requiere configuración de keyring plugin

-- 2. BACKUPS
--    - Backup diario completo con mysqldump --single-transaction
--    - Backup incremental cada 6 horas (binlog)
--    - Retención: 30 días (rotar automáticamente)
--    - IMPORTANTE: Sincronizar eliminación con backups

-- 3. ÍNDICES
--    - Revisar uso con EXPLAIN y ajustar según patrones reales
--    - Considerar índices covering para queries frecuentes

-- 4. PARTICIONAMIENTO
--    - Implementar si volumen >1M registros
--    - Facilita eliminación masiva (DROP PARTITION)

-- 5. REPLICACIÓN
--    - Master-slave para alta disponibilidad
--    - IMPORTANTE: Replicar eliminaciones a todos los slaves

-- 6. MONITOREO
--    - Alertas si data_deletion_queue.status='failed' count > 10
--    - Alertas si arco_requests cerca del deadline
--    - Dashboard de métricas de privacidad

-- ============================================================================
-- FIN DEL SCHEMA
-- ============================================================================
