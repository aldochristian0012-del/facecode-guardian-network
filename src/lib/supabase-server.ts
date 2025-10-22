/**
 * Supabase Server Instance (Backend Only)
 *
 * ⚠️  PELIGRO: Esta instancia usa SUPABASE_SERVICE_KEY
 * ⚠️  NUNCA importes este módulo en código de cliente/frontend
 * ⚠️  Bypasea todas las Row Level Security (RLS) policies
 *
 * Usa este cliente SOLO para:
 * - Operaciones administrativas en el servidor
 * - Migración de datos
 * - Tareas de mantenimiento
 * - APIs internas
 *
 * Para operaciones de usuario, prefiere supabase-client.ts
 */

import { createClient } from '@supabase/supabase-js';
import type { Database } from '../types/supabase.js';
import { config } from './config.js';

/**
 * Cliente de Supabase con privilegios de servicio
 * ⚠️  Solo para uso en servidor - NUNCA en cliente
 */
export const supabaseServer = createClient<Database>(
  config.supabase.url,
  config.supabase.serviceKey,
  {
    auth: {
      autoRefreshToken: false,
      persistSession: false,
    },
  }
);

/**
 * Verificación de seguridad runtime
 */
if (typeof window !== 'undefined') {
  throw new Error(
    '🚨 VIOLACIÓN DE SEGURIDAD CRÍTICA 🚨\n\n' +
    'El módulo supabase-server.ts fue importado en código de cliente.\n' +
    'Este módulo contiene SUPABASE_SERVICE_KEY y debe ser usado SOLO en servidor.\n\n' +
    'Para frontend, usa: src/lib/supabase-client.ts'
  );
}

export default supabaseServer;
