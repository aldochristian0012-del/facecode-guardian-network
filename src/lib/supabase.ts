import { createClient, SupabaseClient } from '@supabase/supabase-js'
import type { Database } from '../types/database.types'

/**
 * Supabase Client Configuration
 *
 * Este cliente proporciona acceso seguro a la base de datos Supabase
 * para el FaceCode Guardian Network, asegurando la protección de datos
 * y el cumplimiento con las regulaciones de privacidad de la UE.
 */

// Validación de variables de entorno requeridas
const supabaseUrl = process.env.SUPABASE_URL
const supabaseAnonKey = process.env.SUPABASE_ANON_KEY

if (!supabaseUrl) {
  throw new Error(
    'SUPABASE_URL no está definida. Por favor, configura las variables de entorno necesarias.'
  )
}

if (!supabaseAnonKey) {
  throw new Error(
    'SUPABASE_ANON_KEY no está definida. Por favor, configura las variables de entorno necesarias.'
  )
}

/**
 * Cliente de Supabase singleton
 *
 * Configurado con:
 * - Autenticación automática de tokens
 * - Persistencia de sesión
 * - Opciones de seguridad para protección de datos
 */
export const supabase: SupabaseClient<Database> = createClient<Database>(
  supabaseUrl,
  supabaseAnonKey,
  {
    auth: {
      autoRefreshToken: true,
      persistSession: true,
      detectSessionInUrl: true
    }
  }
)

/**
 * Helper para verificar la conexión a Supabase
 * @returns Promise<boolean> - true si la conexión es exitosa
 */
export async function checkSupabaseConnection(): Promise<boolean> {
  try {
    const { error } = await supabase.from('_health_check').select('count').limit(1)

    // Si no existe la tabla _health_check, aún así consideramos que la conexión es válida
    if (error && !error.message.includes('does not exist')) {
      console.error('Error al conectar con Supabase:', error.message)
      return false
    }

    return true
  } catch (error) {
    console.error('Error al verificar conexión con Supabase:', error)
    return false
  }
}

export default supabase
