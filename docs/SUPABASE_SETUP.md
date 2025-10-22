# 🔧 Configuración de Supabase

Esta guía explica cómo configurar Supabase para el **FaceCode Guardian Network**.

## 📋 Requisitos previos

1. Cuenta en [Supabase](https://supabase.com)
2. Node.js >= 18.0.0
3. npm, yarn o pnpm

## 🚀 Instalación

### 1. Instalar dependencias

```bash
npm install
```

### 2. Crear proyecto en Supabase

1. Ve a [app.supabase.com](https://app.supabase.com)
2. Crea un nuevo proyecto
3. Anota tu **Project URL** y **API Keys**

### 3. Configurar variables de entorno

Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

Edita `.env` y añade tus credenciales de Supabase:

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu_anon_key_aqui
SUPABASE_SERVICE_KEY=tu_service_role_key_aqui
```

**⚠️ IMPORTANTE:**
- **NUNCA** cometas el archivo `.env` al repositorio
- El `SERVICE_KEY` solo debe usarse en el servidor
- El `ANON_KEY` es seguro para el cliente/frontend

### 4. Obtener las credenciales

En tu proyecto de Supabase:

1. Ve a **Settings** > **API**
2. Copia:
   - **Project URL** → `SUPABASE_URL`
   - **anon/public key** → `SUPABASE_ANON_KEY`
   - **service_role key** → `SUPABASE_SERVICE_KEY`

## 📁 Estructura de archivos

```
src/
├── lib/
│   ├── config.ts              # Configuración centralizada
│   ├── supabase-client.ts     # Cliente para frontend (ANON_KEY)
│   └── supabase-server.ts     # Cliente para backend (SERVICE_KEY)
├── types/
│   └── supabase.ts            # Tipos de TypeScript para DB
└── server/
    └── index.ts               # Ejemplo de servidor
```

## 🔐 Uso seguro

### Frontend (Navegador)

```typescript
// ✅ Correcto - Usa el cliente público
import { supabaseClient } from './lib/supabase-client';

// Consulta segura que respeta RLS
const { data, error } = await supabaseClient
  .from('audit_events')
  .select('*');
```

### Backend (Servidor)

```typescript
// ✅ Correcto - Usa el cliente de servidor
import { supabaseServer } from './lib/supabase-server';

// Operación administrativa
const { data, error } = await supabaseServer
  .from('audit_events')
  .insert({ event_type: 'system_check' });
```

### ❌ Errores comunes

```typescript
// ❌ NUNCA hagas esto en frontend
import { supabaseServer } from './lib/supabase-server';
// Esto expondrá tu SERVICE_KEY
```

## 🗃️ Schema de base de datos

### Crear tabla de auditoría (ejemplo)

En el **SQL Editor** de Supabase, ejecuta:

```sql
-- Tabla de eventos de auditoría
CREATE TABLE audit_events (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  event_type TEXT NOT NULL,
  user_id UUID REFERENCES auth.users(id),
  metadata JSONB DEFAULT '{}',
  severity TEXT CHECK (severity IN ('info', 'warning', 'critical'))
);

-- Habilitar Row Level Security
ALTER TABLE audit_events ENABLE ROW LEVEL SECURITY;

-- Policy: Usuarios autenticados pueden leer sus propios eventos
CREATE POLICY "Users can view own events"
  ON audit_events FOR SELECT
  USING (auth.uid() = user_id);

-- Policy: Solo admins pueden insertar eventos
CREATE POLICY "Admins can insert events"
  ON audit_events FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM auth.users
      WHERE id = auth.uid()
      AND raw_user_meta_data->>'role' = 'admin'
    )
  );
```

### Generar tipos de TypeScript

Después de crear tus tablas:

```bash
npx supabase gen types typescript --project-id <tu-project-id> > src/types/supabase.ts
```

## 🧪 Probar la configuración

```bash
npm run dev
```

Deberías ver:

```
🚀 FaceCode Guardian Network - Iniciando...
📡 Verificando conexión a Supabase...
   URL: https://tu-proyecto.supabase.co
   Entorno: development

✅ Conexión a Supabase establecida correctamente
```

## 📚 Recursos adicionales

- [Documentación de Supabase](https://supabase.com/docs)
- [Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)
- [Auth en Supabase](https://supabase.com/docs/guides/auth)
- [Realtime](https://supabase.com/docs/guides/realtime)

## 🆘 Solución de problemas

### Error: "Variable de entorno requerida no encontrada"

Asegúrate de que:
1. El archivo `.env` existe en la raíz del proyecto
2. Todas las variables están correctamente configuradas
3. No hay espacios alrededor del `=`

### Error: "Invalid API key"

1. Verifica que copiaste las claves correctamente desde Supabase
2. Asegúrate de no tener espacios al inicio o final
3. Confirma que usas el proyecto correcto

### Error de conexión

1. Verifica tu conexión a internet
2. Confirma que la URL de Supabase es correcta
3. Revisa el estado de Supabase en [status.supabase.com](https://status.supabase.com)

---

**© 2025 Christian - FaceCode Founder**
*Protegiendo la dignidad digital*
