/**
 * Supabase Database Type Definitions
 *
 * Este archivo define los tipos de TypeScript para las tablas de Supabase.
 * Actualiza estos tipos cuando modifiques el schema de la base de datos.
 *
 * Para auto-generar estos tipos desde tu schema de Supabase:
 * npx supabase gen types typescript --project-id <tu-project-id> > src/types/supabase.ts
 */

export interface Database {
  public: {
    Tables: {
      // Ejemplo: Tabla de auditoría de eventos
      audit_events: {
        Row: {
          id: string;
          created_at: string;
          event_type: string;
          user_id: string | null;
          metadata: Record<string, unknown>;
          severity: 'info' | 'warning' | 'critical';
        };
        Insert: {
          id?: string;
          created_at?: string;
          event_type: string;
          user_id?: string | null;
          metadata?: Record<string, unknown>;
          severity?: 'info' | 'warning' | 'critical';
        };
        Update: {
          id?: string;
          created_at?: string;
          event_type?: string;
          user_id?: string | null;
          metadata?: Record<string, unknown>;
          severity?: 'info' | 'warning' | 'critical';
        };
      };
      // Agrega más tablas según tu schema
    };
    Views: {
      // Define tus vistas aquí si las tienes
    };
    Functions: {
      // Define tus funciones de base de datos aquí
    };
  };
}
