/**
 * Configuration Module
 *
 * Centraliza todas las variables de entorno y validaciones.
 * Asegura que las credenciales estén presentes antes de inicializar la app.
 */

import { config as loadEnv } from 'dotenv';

// Cargar variables de entorno desde .env
loadEnv();

interface Config {
  supabase: {
    url: string;
    anonKey: string;
    serviceKey: string;
  };
  nodeEnv: string;
  port: number;
  logLevel: string;
}

/**
 * Valida que una variable de entorno exista
 */
function getEnvVar(key: string, fallback?: string): string {
  const value = process.env[key] || fallback;

  if (!value) {
    throw new Error(
      `❌ Variable de entorno requerida no encontrada: ${key}\n` +
      `Por favor, crea un archivo .env basado en .env.example`
    );
  }

  return value;
}

/**
 * Configuración global de la aplicación
 */
export const config: Config = {
  supabase: {
    url: getEnvVar('SUPABASE_URL'),
    anonKey: getEnvVar('SUPABASE_ANON_KEY'),
    serviceKey: getEnvVar('SUPABASE_SERVICE_KEY'),
  },
  nodeEnv: getEnvVar('NODE_ENV', 'development'),
  port: parseInt(getEnvVar('PORT', '3000'), 10),
  logLevel: getEnvVar('LOG_LEVEL', 'info'),
};

/**
 * Validación de seguridad: asegurar que no se use SERVICE_KEY en cliente
 */
if (typeof window !== 'undefined') {
  throw new Error(
    '⚠️  ADVERTENCIA DE SEGURIDAD: ' +
    'Este módulo contiene SUPABASE_SERVICE_KEY y NO debe ser importado en código de cliente. ' +
    'Usa src/lib/supabase-client.ts para frontend.'
  );
}

export default config;
