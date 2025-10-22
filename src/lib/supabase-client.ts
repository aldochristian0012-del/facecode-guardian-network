/**
 * Supabase Client Instance (Frontend-Safe)
 *
 * ✅ SEGURO para usar en navegadores y aplicaciones cliente
 * ✅ Usa SUPABASE_ANON_KEY (respeta Row Level Security)
 * ✅ Los permisos están limitados por RLS policies
 *
 * Usa este cliente para:
 * - Autenticación de usuarios
 * - Consultas desde el frontend
 * - Suscripciones en tiempo real
 */

import { createClient } from '@supabase/supabase-js';
import type { Database } from '../types/supabase.js';

// Validar variables requeridas
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseAnonKey = process.env.SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error(
    '❌ Faltan variables de entorno para Supabase Client.\n' +
    'Asegúrate de tener SUPABASE_URL y SUPABASE_ANON_KEY en tu archivo .env'
  );
}

/**
 * Cliente público de Supabase
 * Seguro para exponer en frontend
 */
export const supabaseClient = createClient<Database>(
  supabaseUrl,
  supabaseAnonKey,
  {
    auth: {
      autoRefreshToken: true,
      persistSession: true,
      detectSessionInUrl: true,
    },
  }
);

export default supabaseClient;
