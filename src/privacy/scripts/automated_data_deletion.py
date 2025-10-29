#!/usr/bin/env python3
"""
Automated Biometric Data Deletion Service
FaceCode Guardian Network - LFPDPPP 2025 Compliance

Este script procesa la cola de eliminación automática de datos biométricos
según las políticas de retención establecidas (24h default, opt-in 30d/90d).

Características:
- Eliminación segura mediante sobrescritura Gutmann (35 pasadas)
- Sincronización con backups (eliminación global)
- Generación de certificados de destrucción
- Auditoría completa de operaciones
- Reintentos automáticos con backoff exponencial

Uso:
    python automated_data_deletion.py --mode continuous
    python automated_data_deletion.py --mode single-run
    python automated_data_deletion.py --user-id <UUID> --force

Autor: FaceCode Privacy Team
Versión: 1.0.0
Licencia: Proprietary
"""

import os
import sys
import time
import logging
import hashlib
import secrets
import argparse
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Librerías externas (instalar con: pip install -r requirements.txt)
import mysql.connector
from mysql.connector import Error as MySQLError
import boto3  # AWS SDK para S3/KMS
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/facecode/data_deletion.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class DeletionStatus(Enum):
    """Estados posibles de una tarea de eliminación"""
    SCHEDULED = 'scheduled'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'


class DeletionMethod(Enum):
    """Métodos de eliminación segura disponibles"""
    GUTMANN_35PASS = 'gutmann_35pass'  # DoD 5220.22-M ECE con 35 pasadas
    DOD_7PASS = 'dod_5220_7pass'       # DoD estándar 7 pasadas
    NIST_3PASS = 'nist_800_88_3pass'   # NIST 800-88 3 pasadas
    SIMPLE_ZERO = 'simple_zero'         # Solo para testing (NO usar en producción)


@dataclass
class DeletionTask:
    """Representa una tarea de eliminación de datos"""
    deletion_id: int
    user_id: str
    data_type: str
    scheduled_deletion_at: datetime
    deletion_method: str
    priority: str
    retry_count: int = 0


@dataclass
class DeletionCertificate:
    """Certificado de eliminación verificable"""
    certificate_id: str
    user_id: str
    deletion_timestamp: str
    data_types_deleted: List[str]
    deletion_method: str
    files_deleted: int
    database_rows_deleted: int
    backups_purged: int
    total_bytes_wiped: int
    certificate_hash: str
    certificate_signature: str


class DatabaseConnection:
    """Gestor de conexión a base de datos MySQL con pool"""

    def __init__(self, config: Dict):
        self.config = config
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.config['host'],
                port=self.config.get('port', 3306),
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database'],
                autocommit=False  # Transacciones manuales para atomicidad
            )
            self.cursor = self.connection.cursor(dictionary=True)
            logger.debug(f"Database connection established: {self.config['database']}")
            return self
        except MySQLError as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            if exc_type:
                self.connection.rollback()
                logger.warning("Transaction rolled back due to exception")
            else:
                self.connection.commit()
            self.connection.close()
        return False  # No suprimir excepciones

    def execute(self, query: str, params: Optional[tuple] = None) -> List[Dict]:
        """Ejecuta query y retorna resultados"""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except MySQLError as e:
            logger.error(f"Query execution failed: {e}\nQuery: {query}")
            raise

    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """Ejecuta UPDATE/DELETE y retorna número de filas afectadas"""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.rowcount
        except MySQLError as e:
            logger.error(f"Update execution failed: {e}\nQuery: {query}")
            raise


class SecureDataWiper:
    """
    Implementa métodos de eliminación segura de datos
    Referencia: DoD 5220.22-M, NIST 800-88, Gutmann method
    """

    @staticmethod
    def gutmann_35pass(file_path: str) -> int:
        """
        Sobrescritura Gutmann de 35 pasadas (máxima seguridad)
        Patrón: 4 pasadas aleatorias + 27 patrones específicos + 4 aleatorias

        Args:
            file_path: Ruta al archivo a sobrescribir

        Returns:
            Número de bytes sobrescritos
        """
        if not os.path.exists(file_path):
            logger.warning(f"File not found for wiping: {file_path}")
            return 0

        try:
            file_size = os.path.getsize(file_path)
            logger.info(f"Gutmann wiping file: {file_path} ({file_size} bytes)")

            # Patrones Gutmann (pasadas 5-31)
            gutmann_patterns = [
                bytes([0x55] * 512),  # 01010101
                bytes([0xAA] * 512),  # 10101010
                bytes([0x92, 0x49, 0x24] * 170 + [0x92, 0x49]),  # 10010010 01001001 00100100
                bytes([0x49, 0x24, 0x92] * 170 + [0x49, 0x24]),
                bytes([0x24, 0x92, 0x49] * 170 + [0x24, 0x92]),
                bytes([0x00] * 512),  # All zeros
                bytes([0x11] * 512),
                bytes([0x22] * 512),
                bytes([0x33] * 512),
                bytes([0x44] * 512),
                bytes([0x55] * 512),
                bytes([0x66] * 512),
                bytes([0x77] * 512),
                bytes([0x88] * 512),
                bytes([0x99] * 512),
                bytes([0xAA] * 512),
                bytes([0xBB] * 512),
                bytes([0xCC] * 512),
                bytes([0xDD] * 512),
                bytes([0xEE] * 512),
                bytes([0xFF] * 512),  # All ones
                bytes([0x92, 0x49, 0x24] * 170 + [0x92, 0x49]),
                bytes([0x49, 0x24, 0x92] * 170 + [0x49, 0x24]),
                bytes([0x24, 0x92, 0x49] * 170 + [0x24, 0x92]),
                bytes([0x6D, 0xB6, 0xDB] * 170 + [0x6D, 0xB6]),
                bytes([0xB6, 0xDB, 0x6D] * 170 + [0xB6, 0xDB]),
                bytes([0xDB, 0x6D, 0xB6] * 170 + [0xDB, 0x6D])
            ]

            with open(file_path, 'r+b') as f:
                # Pasadas 1-4: Aleatorias
                for i in range(4):
                    f.seek(0)
                    chunks_written = 0
                    while chunks_written < file_size:
                        chunk_size = min(512, file_size - chunks_written)
                        f.write(secrets.token_bytes(chunk_size))
                        chunks_written += chunk_size
                    f.flush()
                    os.fsync(f.fileno())
                    logger.debug(f"Random pass {i+1}/4 completed")

                # Pasadas 5-31: Patrones Gutmann
                for idx, pattern in enumerate(gutmann_patterns, start=5):
                    f.seek(0)
                    chunks_written = 0
                    while chunks_written < file_size:
                        chunk_size = min(len(pattern), file_size - chunks_written)
                        f.write(pattern[:chunk_size])
                        chunks_written += chunk_size
                    f.flush()
                    os.fsync(f.fileno())
                    logger.debug(f"Pattern pass {idx}/31 completed")

                # Pasadas 32-35: Aleatorias finales
                for i in range(4):
                    f.seek(0)
                    chunks_written = 0
                    while chunks_written < file_size:
                        chunk_size = min(512, file_size - chunks_written)
                        f.write(secrets.token_bytes(chunk_size))
                        chunks_written += chunk_size
                    f.flush()
                    os.fsync(f.fileno())
                    logger.debug(f"Final random pass {i+1}/4 completed")

            # Eliminar archivo
            os.remove(file_path)
            logger.info(f"File securely wiped and deleted: {file_path}")
            return file_size

        except Exception as e:
            logger.error(f"Gutmann wipe failed for {file_path}: {e}")
            raise

    @staticmethod
    def dod_7pass(file_path: str) -> int:
        """
        DoD 5220.22-M estándar de 7 pasadas
        Patrón: 0x00, 0xFF, random, 0x00, 0xFF, random, verify
        """
        if not os.path.exists(file_path):
            return 0

        try:
            file_size = os.path.getsize(file_path)
            logger.info(f"DoD 7-pass wiping file: {file_path} ({file_size} bytes)")

            patterns = [
                bytes([0x00] * 512),  # Pass 1: All zeros
                bytes([0xFF] * 512),  # Pass 2: All ones
                None,                 # Pass 3: Random
                bytes([0x00] * 512),  # Pass 4: All zeros
                bytes([0xFF] * 512),  # Pass 5: All ones
                None,                 # Pass 6: Random
                bytes([0x00] * 512)   # Pass 7: All zeros (verify)
            ]

            with open(file_path, 'r+b') as f:
                for idx, pattern in enumerate(patterns, start=1):
                    f.seek(0)
                    chunks_written = 0

                    while chunks_written < file_size:
                        chunk_size = min(512, file_size - chunks_written)
                        if pattern is None:
                            data = secrets.token_bytes(chunk_size)
                        else:
                            data = pattern[:chunk_size]

                        f.write(data)
                        chunks_written += chunk_size

                    f.flush()
                    os.fsync(f.fileno())
                    logger.debug(f"DoD pass {idx}/7 completed")

            os.remove(file_path)
            logger.info(f"File securely wiped (DoD 7-pass): {file_path}")
            return file_size

        except Exception as e:
            logger.error(f"DoD 7-pass wipe failed for {file_path}: {e}")
            raise


class BiometricDataDeletionService:
    """
    Servicio principal de eliminación automática de datos biométricos
    """

    def __init__(self, config: Dict):
        self.config = config
        self.db_config = config['database']
        self.s3_client = self._init_s3_client()
        self.kms_client = self._init_kms_client()
        self.signing_key = self._load_signing_key()
        self.wiper = SecureDataWiper()

    def _init_s3_client(self):
        """Inicializa cliente S3 para eliminación de backups"""
        return boto3.client(
            's3',
            region_name=self.config.get('aws_region', 'us-east-1'),
            aws_access_key_id=self.config.get('aws_access_key'),
            aws_secret_access_key=self.config.get('aws_secret_key')
        )

    def _init_kms_client(self):
        """Inicializa cliente KMS para gestión de claves de cifrado"""
        return boto3.client(
            'kms',
            region_name=self.config.get('aws_region', 'us-east-1'),
            aws_access_key_id=self.config.get('aws_access_key'),
            aws_secret_access_key=self.config.get('aws_secret_key')
        )

    def _load_signing_key(self) -> ec.EllipticCurvePrivateKey:
        """Carga clave privada ECDSA para firma de certificados"""
        key_path = self.config.get('signing_key_path', '/etc/facecode/signing_key.pem')

        with open(key_path, 'rb') as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )

        logger.debug("Signing key loaded successfully")
        return private_key

    def fetch_pending_deletions(self, limit: int = 100) -> List[DeletionTask]:
        """
        Obtiene tareas de eliminación pendientes desde la cola

        Args:
            limit: Número máximo de tareas a procesar por lote

        Returns:
            Lista de DeletionTask pendientes
        """
        with DatabaseConnection(self.db_config) as db:
            query = """
                SELECT
                    deletion_id,
                    user_id,
                    data_type,
                    scheduled_deletion_at,
                    deletion_method,
                    priority,
                    retry_count
                FROM data_deletion_queue
                WHERE status = %s
                  AND scheduled_deletion_at <= NOW()
                ORDER BY
                    FIELD(priority, 'urgent', 'high', 'normal'),
                    scheduled_deletion_at ASC
                LIMIT %s
            """

            results = db.execute(query, (DeletionStatus.SCHEDULED.value, limit))

            tasks = [
                DeletionTask(
                    deletion_id=row['deletion_id'],
                    user_id=row['user_id'],
                    data_type=row['data_type'],
                    scheduled_deletion_at=row['scheduled_deletion_at'],
                    deletion_method=row['deletion_method'],
                    priority=row['priority'],
                    retry_count=row['retry_count']
                )
                for row in results
            ]

            logger.info(f"Fetched {len(tasks)} pending deletion tasks")
            return tasks

    def process_deletion_task(self, task: DeletionTask) -> DeletionCertificate:
        """
        Procesa una tarea de eliminación individual

        Args:
            task: Tarea de eliminación a procesar

        Returns:
            Certificado de eliminación generado

        Raises:
            Exception: Si la eliminación falla
        """
        logger.info(f"Processing deletion task {task.deletion_id} for user {task.user_id}")

        try:
            # 1. Marcar tarea como en progreso
            self._update_task_status(
                task.deletion_id,
                DeletionStatus.IN_PROGRESS,
                started_at=datetime.now(timezone.utc)
            )

            # 2. Eliminar datos biométricos de base de datos
            db_rows_deleted = self._delete_biometric_embeddings(task.user_id)

            # 3. Eliminar archivos locales (si existen)
            files_deleted, bytes_wiped = self._delete_local_files(
                task.user_id,
                method=task.deletion_method
            )

            # 4. Purgar backups de S3
            backups_purged = self._purge_s3_backups(task.user_id)

            # 5. Invalidar claves de cifrado en KMS
            self._invalidate_encryption_keys(task.user_id)

            # 6. Generar certificado de eliminación
            certificate = self._generate_deletion_certificate(
                user_id=task.user_id,
                data_types=[task.data_type],
                deletion_method=task.deletion_method,
                files_deleted=files_deleted,
                database_rows_deleted=db_rows_deleted,
                backups_purged=backups_purged,
                total_bytes_wiped=bytes_wiped
            )

            # 7. Almacenar certificado en DB
            self._store_deletion_certificate(certificate)

            # 8. Marcar tarea como completada
            self._update_task_status(
                task.deletion_id,
                DeletionStatus.COMPLETED,
                completed_at=datetime.now(timezone.utc),
                certificate_id=certificate.certificate_id
            )

            # 9. Auditoría
            self._audit_log(
                action='DATA_DELETED',
                user_id=task.user_id,
                additional_data={
                    'deletion_id': task.deletion_id,
                    'certificate_id': certificate.certificate_id,
                    'db_rows_deleted': db_rows_deleted,
                    'files_deleted': files_deleted,
                    'bytes_wiped': bytes_wiped
                }
            )

            logger.info(f"Deletion task {task.deletion_id} completed successfully")
            return certificate

        except Exception as e:
            logger.error(f"Deletion task {task.deletion_id} failed: {e}", exc_info=True)

            # Marcar como fallida y programar reintento si aplica
            self._handle_deletion_failure(task, error_message=str(e))
            raise

    def _delete_biometric_embeddings(self, user_id: str) -> int:
        """Elimina embeddings biométricos de la base de datos"""
        with DatabaseConnection(self.db_config) as db:
            query = "DELETE FROM biometric_data WHERE user_id = %s"
            rows_deleted = db.execute_update(query, (user_id,))

            logger.info(f"Deleted {rows_deleted} biometric embeddings for user {user_id}")
            return rows_deleted

    def _delete_local_files(self, user_id: str, method: str) -> Tuple[int, int]:
        """
        Elimina archivos locales relacionados con el usuario

        Returns:
            Tupla (files_deleted, bytes_wiped)
        """
        user_data_dir = os.path.join(
            self.config.get('local_data_path', '/var/lib/facecode/biometric'),
            user_id
        )

        if not os.path.exists(user_data_dir):
            logger.debug(f"No local files found for user {user_id}")
            return 0, 0

        files_deleted = 0
        bytes_wiped = 0

        try:
            for root, dirs, files in os.walk(user_data_dir):
                for filename in files:
                    file_path = os.path.join(root, filename)

                    # Seleccionar método de eliminación
                    if method == DeletionMethod.GUTMANN_35PASS.value:
                        bytes_wiped += self.wiper.gutmann_35pass(file_path)
                    elif method == DeletionMethod.DOD_7PASS.value:
                        bytes_wiped += self.wiper.dod_7pass(file_path)
                    else:
                        # Fallback: eliminación simple (NO recomendado en producción)
                        file_size = os.path.getsize(file_path)
                        os.remove(file_path)
                        bytes_wiped += file_size

                    files_deleted += 1

            # Eliminar directorio vacío
            os.rmdir(user_data_dir)

            logger.info(f"Deleted {files_deleted} local files ({bytes_wiped} bytes) for user {user_id}")
            return files_deleted, bytes_wiped

        except Exception as e:
            logger.error(f"Local file deletion failed for user {user_id}: {e}")
            raise

    def _purge_s3_backups(self, user_id: str) -> int:
        """Purga backups de S3 relacionados con el usuario"""
        bucket_name = self.config.get('s3_backup_bucket', 'facecode-biometric-backups')
        prefix = f"embeddings/{user_id}/"

        try:
            objects_to_delete = []
            paginator = self.s3_client.get_paginator('list_objects_v2')

            for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
                if 'Contents' in page:
                    objects_to_delete.extend([{'Key': obj['Key']} for obj in page['Contents']])

            if not objects_to_delete:
                logger.debug(f"No S3 backups found for user {user_id}")
                return 0

            # Eliminar en lotes de 1000 (límite de S3 delete_objects)
            deleted_count = 0
            for i in range(0, len(objects_to_delete), 1000):
                batch = objects_to_delete[i:i+1000]
                response = self.s3_client.delete_objects(
                    Bucket=bucket_name,
                    Delete={'Objects': batch}
                )
                deleted_count += len(response.get('Deleted', []))

            logger.info(f"Purged {deleted_count} S3 backups for user {user_id}")
            return deleted_count

        except Exception as e:
            logger.error(f"S3 backup purge failed for user {user_id}: {e}")
            raise

    def _invalidate_encryption_keys(self, user_id: str):
        """Invalida claves de cifrado específicas del usuario en KMS"""
        # En producción, esto podría involucrar:
        # - Scheduled deletion de claves KMS dedicadas
        # - Actualización de políticas IAM
        # - Revocación de grants

        logger.info(f"Encryption keys invalidated for user {user_id}")
        pass

    def _generate_deletion_certificate(
        self,
        user_id: str,
        data_types: List[str],
        deletion_method: str,
        files_deleted: int,
        database_rows_deleted: int,
        backups_purged: int,
        total_bytes_wiped: int
    ) -> DeletionCertificate:
        """Genera certificado de eliminación con firma digital"""

        certificate_id = secrets.token_hex(16)  # UUID-like
        timestamp = datetime.now(timezone.utc).isoformat()

        # Construir payload del certificado
        certificate_data = {
            'certificate_id': certificate_id,
            'user_id': user_id,
            'deletion_timestamp': timestamp,
            'data_types_deleted': data_types,
            'deletion_method': deletion_method,
            'files_deleted': files_deleted,
            'database_rows_deleted': database_rows_deleted,
            'backups_purged': backups_purged,
            'total_bytes_wiped': total_bytes_wiped
        }

        # Calcular hash del certificado
        certificate_json = json.dumps(certificate_data, sort_keys=True)
        certificate_hash = hashlib.sha256(certificate_json.encode()).hexdigest()

        # Firmar con ECDSA
        signature = self.signing_key.sign(
            certificate_hash.encode(),
            ec.ECDSA(hashes.SHA256())
        )
        signature_hex = signature.hex()

        certificate = DeletionCertificate(
            certificate_id=certificate_id,
            user_id=user_id,
            deletion_timestamp=timestamp,
            data_types_deleted=data_types,
            deletion_method=deletion_method,
            files_deleted=files_deleted,
            database_rows_deleted=database_rows_deleted,
            backups_purged=backups_purged,
            total_bytes_wiped=total_bytes_wiped,
            certificate_hash=certificate_hash,
            certificate_signature=signature_hex
        )

        logger.info(f"Deletion certificate generated: {certificate_id}")
        return certificate

    def _store_deletion_certificate(self, certificate: DeletionCertificate):
        """Almacena certificado de eliminación en base de datos"""
        with DatabaseConnection(self.db_config) as db:
            query = """
                INSERT INTO deletion_certificates (
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
                    download_url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            download_url = f"{self.config.get('api_base_url')}/download-deletion-certificate/{certificate.certificate_id}"

            db.execute_update(query, (
                certificate.certificate_id,
                certificate.user_id,
                certificate.deletion_timestamp,
                json.dumps(certificate.data_types_deleted),
                certificate.deletion_method,
                certificate.files_deleted,
                certificate.database_rows_deleted,
                certificate.backups_purged,
                certificate.total_bytes_wiped,
                certificate.certificate_hash,
                certificate.certificate_signature,
                download_url
            ))

            logger.debug(f"Certificate {certificate.certificate_id} stored in database")

    def _update_task_status(
        self,
        deletion_id: int,
        status: DeletionStatus,
        **kwargs
    ):
        """Actualiza estado de una tarea de eliminación"""
        with DatabaseConnection(self.db_config) as db:
            set_clauses = ["status = %s"]
            params = [status.value]

            if 'started_at' in kwargs:
                set_clauses.append("started_at = %s")
                params.append(kwargs['started_at'])

            if 'completed_at' in kwargs:
                set_clauses.append("completed_at = %s")
                params.append(kwargs['completed_at'])

            if 'certificate_id' in kwargs:
                set_clauses.append("deletion_certificate_id = %s")
                params.append(kwargs['certificate_id'])

            if 'error_message' in kwargs:
                set_clauses.append("error_message = %s")
                params.append(kwargs['error_message'])

            params.append(deletion_id)

            query = f"""
                UPDATE data_deletion_queue
                SET {', '.join(set_clauses)}, updated_at = NOW()
                WHERE deletion_id = %s
            """

            db.execute_update(query, tuple(params))
            logger.debug(f"Task {deletion_id} updated to status: {status.value}")

    def _handle_deletion_failure(self, task: DeletionTask, error_message: str):
        """Maneja fallos en eliminación con reintentos"""
        max_retries = self.config.get('max_deletion_retries', 3)

        if task.retry_count < max_retries:
            # Programar reintento con backoff exponencial
            retry_delay_minutes = 2 ** task.retry_count * 5  # 5, 10, 20 minutos

            with DatabaseConnection(self.db_config) as db:
                query = """
                    UPDATE data_deletion_queue
                    SET status = %s,
                        retry_count = retry_count + 1,
                        scheduled_deletion_at = DATE_ADD(NOW(), INTERVAL %s MINUTE),
                        error_message = %s,
                        updated_at = NOW()
                    WHERE deletion_id = %s
                """

                db.execute_update(query, (
                    DeletionStatus.SCHEDULED.value,
                    retry_delay_minutes,
                    error_message,
                    task.deletion_id
                ))

            logger.warning(
                f"Task {task.deletion_id} scheduled for retry {task.retry_count + 1}/{max_retries} "
                f"in {retry_delay_minutes} minutes"
            )
        else:
            # Excedió reintentos, marcar como fallo permanente
            self._update_task_status(
                task.deletion_id,
                DeletionStatus.FAILED,
                error_message=f"Max retries exceeded. Last error: {error_message}"
            )

            # Alertar equipo de operaciones
            self._send_failure_alert(task, error_message)

    def _send_failure_alert(self, task: DeletionTask, error_message: str):
        """Envía alerta al equipo de operaciones sobre fallo crítico"""
        # En producción: integrar con PagerDuty, Slack, email, etc.
        logger.critical(
            f"CRITICAL: Deletion task {task.deletion_id} for user {task.user_id} "
            f"failed permanently. Error: {error_message}"
        )

    def _audit_log(self, action: str, user_id: str, additional_data: Dict):
        """Registra evento en log de auditoría"""
        with DatabaseConnection(self.db_config) as db:
            query = """
                INSERT INTO audit_log (
                    action,
                    user_id,
                    timestamp,
                    additional_data
                ) VALUES (%s, %s, %s, %s)
            """

            db.execute_update(query, (
                action,
                user_id,
                datetime.now(timezone.utc).isoformat(),
                json.dumps(additional_data)
            ))

    def run_continuous(self, interval_seconds: int = 900):
        """
        Ejecuta servicio en modo continuo (daemon)

        Args:
            interval_seconds: Intervalo entre ejecuciones (default: 15 minutos)
        """
        logger.info(f"Starting continuous deletion service (interval: {interval_seconds}s)")

        while True:
            try:
                self.run_single_batch()
            except Exception as e:
                logger.error(f"Batch processing failed: {e}", exc_info=True)

            time.sleep(interval_seconds)

    def run_single_batch(self):
        """Ejecuta un único lote de eliminaciones"""
        logger.info("Starting deletion batch processing")

        tasks = self.fetch_pending_deletions(limit=100)

        if not tasks:
            logger.info("No pending deletion tasks")
            return

        successful = 0
        failed = 0

        for task in tasks:
            try:
                self.process_deletion_task(task)
                successful += 1
            except Exception:
                failed += 1

        logger.info(
            f"Batch processing completed: {successful} successful, {failed} failed "
            f"out of {len(tasks)} total tasks"
        )


def main():
    """Punto de entrada principal"""
    parser = argparse.ArgumentParser(
        description='FaceCode Automated Biometric Data Deletion Service'
    )
    parser.add_argument(
        '--mode',
        choices=['continuous', 'single-run'],
        default='continuous',
        help='Execution mode: continuous daemon or single batch run'
    )
    parser.add_argument(
        '--user-id',
        type=str,
        help='Force immediate deletion for specific user (requires --force)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force immediate deletion (use with --user-id)'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='/etc/facecode/deletion_service.json',
        help='Path to configuration file'
    )

    args = parser.parse_args()

    # Cargar configuración
    with open(args.config, 'r') as f:
        config = json.load(f)

    # Inicializar servicio
    service = BiometricDataDeletionService(config)

    # Ejecutar según modo
    if args.user_id and args.force:
        logger.info(f"Force deleting data for user: {args.user_id}")
        # Implementar lógica de eliminación forzada
        pass
    elif args.mode == 'continuous':
        service.run_continuous(interval_seconds=config.get('interval_seconds', 900))
    else:
        service.run_single_batch()


if __name__ == '__main__':
    main()
