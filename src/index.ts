/**
 * FaceCode Guardian Network
 * Punto de entrada principal
 */

import 'dotenv/config'
import { supabase, checkSupabaseConnection } from './lib/supabase.js'

/**
 * Función principal de inicialización
 */
async function main() {
  console.log('🛡️  FaceCode Guardian Network - Iniciando...')
  console.log('📍 Protegiendo la dignidad digital mediante IA ética\n')

  // Verificar conexión con Supabase
  console.log('🔍 Verificando conexión con Supabase...')
  const isConnected = await checkSupabaseConnection()

  if (isConnected) {
    console.log('✅ Conexión exitosa con Supabase')
    console.log('🔐 Cliente de Supabase configurado y listo\n')
  } else {
    console.error('❌ Error al conectar con Supabase')
    console.error('   Por favor, verifica tu configuración de variables de entorno\n')
    process.exit(1)
  }

  console.log('🌐 Guardian Network está en línea')
  console.log('⚖️  Cumpliendo con el Reglamento de IA de la UE y EAA')
}

// Ejecutar la aplicación
main().catch((error) => {
  console.error('❌ Error fatal:', error.message)
  process.exit(1)
})
