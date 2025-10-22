/**
 * Database Type Definitions
 *
 * Este archivo contiene las definiciones de tipos para la base de datos Supabase.
 *
 * NOTA: Este archivo debe ser generado automáticamente desde tu esquema de Supabase.
 * Para generar los tipos, ejecuta:
 *
 *   npx supabase gen types typescript --project-id <tu-project-id> > src/types/database.types.ts
 *
 * O usando la CLI de Supabase:
 *
 *   supabase gen types typescript --linked > src/types/database.types.ts
 */

export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

/**
 * Database Schema
 *
 * TODO: Reemplazar con los tipos generados desde tu esquema de Supabase
 */
export interface Database {
  public: {
    Tables: {
      // Define tus tablas aquí
      // Ejemplo:
      // guardian_nodes: {
      //   Row: {
      //     id: string
      //     name: string
      //     status: string
      //     created_at: string
      //   }
      //   Insert: {
      //     id?: string
      //     name: string
      //     status: string
      //     created_at?: string
      //   }
      //   Update: {
      //     id?: string
      //     name?: string
      //     status?: string
      //     created_at?: string
      //   }
      // }
      [key: string]: {
        Row: Record<string, unknown>
        Insert: Record<string, unknown>
        Update: Record<string, unknown>
      }
    }
    Views: {
      [key: string]: {
        Row: Record<string, unknown>
      }
    }
    Functions: {
      [key: string]: {
        Args: Record<string, unknown>
        Returns: unknown
      }
    }
    Enums: {
      [key: string]: string
    }
  }
}
