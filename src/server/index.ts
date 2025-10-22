/**
 * FaceCode Guardian Network - Server Entry Point
 *
 * Este es un ejemplo básico de cómo usar Supabase en el servidor.
 * Demuestra el uso seguro de los clientes de Supabase.
 */

import { config } from '../lib/config.js';
import { supabaseServer } from '../lib/supabase-server.js';

async function main() {
  console.log('🚀 FaceCode Guardian Network - Iniciando...\n');

  // Validar conexión a Supabase
  console.log('📡 Verificando conexión a Supabase...');
  console.log(`   URL: ${config.supabase.url}`);
  console.log(`   Entorno: ${config.nodeEnv}\n`);

  try {
    // Ejemplo: Verificar conexión con una consulta simple
    const { error } = await supabaseServer.from('audit_events').select('count');

    if (error) {
      // Si la tabla no existe, es normal en un setup inicial
      if (error.code === '42P01') {
        console.log('⚠️  Tabla "audit_events" no existe aún.');
        console.log('   Esto es normal en un setup inicial.');
        console.log('   Crea tus tablas en el Supabase Dashboard.\n');
      } else {
        throw error;
      }
    } else {
      console.log('✅ Conexión a Supabase establecida correctamente\n');
    }

    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('✅ Guardian Network iniciado correctamente');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

    console.log('📋 Próximos pasos:');
    console.log('   1. Configura tu schema en Supabase Dashboard');
    console.log('   2. Actualiza src/types/supabase.ts con tus tipos');
    console.log('   3. Implementa los Guardian Nodes');
    console.log('   4. Configura el Ethical Dashboard\n');

  } catch (error) {
    console.error('❌ Error al conectar con Supabase:');
    console.error(error);
    process.exit(1);
  }
}

// Iniciar servidor
main().catch((error) => {
  console.error('❌ Error fatal:', error);
  process.exit(1);
});
