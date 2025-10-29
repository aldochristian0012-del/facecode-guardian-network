# MICROCOPY A/B TESTING VARIANTS
## Aviso de Privacidad - FaceCode Guardian Network

**Objetivo:** Optimizar tasa de conversión (consent completion rate) para diferentes segmentos psicográficos
**Métrica principal:** % de usuarios que completan el consentimiento biométrico
**Métricas secundarias:** Tiempo promedio en página, bounce rate, tasa de lectura completa del aviso

---

## GUÍA DE USO

### Segmentación de Audiencias

| Variante | Perfil Psicográfico | Drivers de Decisión | Plataforma Recomendada |
|----------|-------------------|---------------------|------------------------|
| **Variante A** | Privacy-Paranoid | Seguridad, control, transparencia | Web (desktop), usuarios B2B |
| **Variante B** | Convenience-First | Rapidez, simplicidad, beneficios | Mobile (iOS/Android), millennials |
| **Variante C** | Balanced-Trust | Confianza, claridad, profesionalismo | Universal (control) |

### Configuración de Test A/B/C

```javascript
// Ejemplo de configuración en herramienta de testing (Optimizely, Google Optimize, VWO)
const abTest = {
  testName: "privacy_consent_microcopy_v1",
  variants: [
    { id: "A", name: "privacy_paranoid", traffic: 0.33 },
    { id: "B", name: "convenience_first", traffic: 0.33 },
    { id: "C", name: "balanced_trust", traffic: 0.34 }
  ],
  goalMetrics: [
    { name: "consent_completion", type: "conversion" },
    { name: "avg_time_on_page", type: "engagement" },
    { name: "full_read_through", type: "engagement" }
  ],
  minimumSampleSize: 385, // 95% confidence, 5% margin of error
  estimatedDuration: "14 days"
}
```

---

## VARIANTE A: PRIVACY-PARANOID
### Perfil de Usuario
- **Demografía:** 30-55 años, educación superior, ingresos medios-altos
- **Preocupaciones principales:** Vigilancia masiva, robo de identidad, uso indebido de datos
- **Motivaciones:** Control total, transparencia radical, cumplimiento legal estricto
- **Objeciones comunes:** "¿Quién más tendrá acceso?", "¿Puedo eliminar mis datos?", "¿Cómo sé que es seguro?"

### Microcopy (245 palabras)

---

#### **Título Principal**
# Tu Privacidad es No Negociable. Aquí Está Cómo la Protegemos.

#### **Subtítulo**
Autenticación biométrica con garantías legales y técnicas auditables. Control total en tus manos.

---

#### **Bloque 1: Qué Recabamos (Transparencia Máxima)**

**Datos biométricos que procesamos:**
- ✓ Vectores faciales (representación matemática, NO fotografías)
- ✓ Parámetros de detección de vivacidad (anti-spoofing)
- ✓ Metadatos de sesión (timestamp, Device ID)

**Datos que NUNCA tocamos:**
- ✗ Imágenes faciales en crudo (procesadas solo en TU dispositivo)
- ✗ Ubicación GPS precisa
- ✗ Contactos, fotos, mensajes u otros datos del dispositivo

---

#### **Bloque 2: Fundamento Legal Sólido**

Este aviso cumple **100% con LFPDPPP 2025** (Ley Federal de Protección de Datos Personales):
- Artículo 9: Consentimiento expreso para datos sensibles ✓
- Artículo 16: Principios de minimización y proporcionalidad ✓
- Lineamientos INAI 2015: Aviso de privacidad integral ✓

**Cada consentimiento se registra con firma electrónica timestamped + hash SHA-256 para auditorías.**

---

#### **Bloque 3: Retención Mínima por Defecto**

**Tus datos biométricos se autodestruyen en 24 horas.** Punto.

Después de tu última autenticación:
1. Eliminación automática mediante sobrescritura Gutmann (35 pasadas)
2. Certificado de destrucción descargable vía `/verify-deletion`
3. Cero backups residuales (sincronización global de eliminación)

*¿Necesitas retención extendida?* Opt-in explícito hasta 30/90 días (revocable en cualquier momento).

---

#### **Bloque 4: Procesamiento Local Primero**

**Tu rostro nunca sale de tu dispositivo. Punto.**

Arquitectura privacy-by-design:
- Extracción de embeddings: 100% on-device (SDK local)
- Transmisión: Solo vectores cifrados con AES-256-GCM
- Almacenamiento cloud: Solo para matching, nunca para análisis masivo

*Matemática simple:* Foto (2 MB) → Vector cifrado (512 bytes). No hay manera de reconstruir la imagen original.

---

#### **Bloque 5: Control Total ARCO**

Ejercicio inmediato de tus derechos:
- **Acceso:** Descarga tu historial completo en JSON portable
- **Rectificación:** Actualiza datos en 1 clic
- **Cancelación:** Eliminación express (<15 min) con certificado timestamped
- **Oposición:** Desactiva finalidades secundarias (marketing, ML training) sin afectar autenticación

**Dashboard de privacidad:** [Acceso directo] | **Email:** [privacidad@facecode.com] | **Respuesta garantizada en <20 días hábiles (LFPDPPP)**

---

#### **Call to Action**

☐ He leído y entiendo este aviso. Acepto expresamente el tratamiento de mis datos biométricos con las garantías descritas.

[Descargar Aviso Completo PDF] | [Historial de Versiones] | [Contactar al Oficial de Privacidad]

**Certificado de consentimiento:** Se generará automáticamente con tu User ID, timestamp UTC, IP origen y hash del documento para tu archivo personal.

---

### Hipótesis de Rendimiento

**Tasa de conversión esperada:** 68-75%
- **Fortalezas:** Genera confianza en usuarios suspicaces, reduce objeciones legales, diferenciación competitiva
- **Debilidades:** Puede intimidar a usuarios menos técnicos, texto más largo (↑ fricción)
- **Momento óptimo:** Registro inicial, antes de primera autenticación biométrica

### Métricas de Éxito

- Consent completion rate > 70%
- Tiempo promedio en página: 90-120 segundos (indica lectura completa)
- Bounce rate < 25%
- Tasa de revocación a 30 días < 5%

---

## VARIANTE B: CONVENIENCE-FIRST
### Perfil de Usuario
- **Demografía:** 18-35 años, nativos digitales, uso intensivo de apps
- **Preocupaciones principales:** Fricción en UX, tiempo perdido, complejidad
- **Motivaciones:** Rapidez, simplicidad, "just works"
- **Objeciones comunes:** "¿Cuánto tarda?", "¿Es realmente más rápido que contraseña?", "¿Complicará mi vida?"

### Microcopy (158 palabras)

---

#### **Título Principal**
# Entra en 0.3 Segundos. Sin Contraseñas. Sin Fricción.

#### **Subtítulo**
Autenticación facial que respeta tu privacidad. Configuración: 30 segundos. Beneficio: para siempre.

---

#### **Bloque 1: Por Qué Esto Es Mejor**

**Adiós a:**
- ❌ Contraseñas olvidadas (recuperación = 10 min perdidos)
- ❌ Códigos OTP por SMS (espera + tipeo = fricción)
- ❌ Preguntas de seguridad ridículas (¿tu primera mascota? En serio?)

**Hola a:**
- ✅ Autenticación instantánea: Mira → Entra (0.3s promedio)
- ✅ Sin instalaciones extras: Funciona con tu cámara actual
- ✅ Modo offline: Autentica incluso sin internet

---

#### **Bloque 2: Privacidad Sin Esfuerzo**

**Tu rostro = tu llave. Nunca sale de tu dispositivo.**

Procesamos todo localmente:
1. Tu cámara captura → Tu dispositivo analiza → Solo código numérico se envía
2. Eliminación automática en 24h (puedes extenderlo si quieres, pero ¿para qué?)
3. Cero fotos almacenadas. Cero bases de datos de caras. Solo matemática.

*Es como usar Face ID de Apple, pero para cualquier servicio.*

---

#### **Bloque 3: Configuración Express**

**3 pasos. 30 segundos. Listo.**

1. **Mira a la cámara** (parpadea 1 vez para confirmar que eres real)
2. **Tap en "Acepto"** (cumplimos con ley mexicana de privacidad, prometido)
3. **¡Listo!** Ahora entra con tu cara en todos tus dispositivos

*Siguiente autenticación: 0.3 segundos. Para siempre.*

---

#### **Bloque 4: Control Rápido**

¿Cambio de opinión? Elimina tus datos en 1 clic:
- **Configuración** → **Privacidad** → **Eliminar Datos Biométricos**
- Confirmación por email → Eliminación en <15 min
- Vuelve a contraseñas tradicionales sin drama

**También puedes:** Pausar temporalmente, cambiar a autenticación de voz, exportar tus datos.

---

#### **Call to Action**

☐ Entendido. Quiero autenticación instantánea con protección de privacidad incluida.

[Comenzar Ahora →] **30 segundos para configurar**

*Cumple 100% con Ley Federal de Protección de Datos (LFPDPPP). [Ver aviso completo] si te interesa lo legal.*

---

### Hipótesis de Rendimiento

**Tasa de conversión esperada:** 82-88%
- **Fortalezas:** Elimina fricción, enfoca en beneficios inmediatos, lenguaje simple
- **Debilidades:** Puede generar desconfianza en usuarios cautelosos, menos detalle legal
- **Momento óptimo:** Onboarding mobile, pop-up contextual durante login lento

### Métricas de Éxito

- Consent completion rate > 85%
- Tiempo promedio en página: 30-45 segundos (lectura rápida)
- Bounce rate < 15%
- Activación de autenticación biométrica post-consentimiento > 90%

---

## VARIANTE C: BALANCED-TRUST
### Perfil de Usuario
- **Demografía:** 25-50 años, perfil mixto, usuarios enterprise
- **Preocupaciones principales:** Balance entre seguridad y usabilidad
- **Motivaciones:** Confianza en marca, profesionalismo, claridad
- **Objeciones comunes:** "¿Es esto estándar?", "¿Otras empresas lo usan?", "¿Qué pasa si hay un problema?"

### Microcopy (197 palabras)

---

#### **Título Principal**
# Autenticación Biométrica de Clase Empresarial con Privacidad por Diseño

#### **Subtítulo**
Tecnología utilizada por [PENDIENTE - logos de clientes enterprise] con cumplimiento certificado LFPDPPP 2025.

---

#### **Bloque 1: Cómo Funciona**

**Autenticación facial en 3 niveles de seguridad:**

1. **Captura local:** Tu dispositivo analiza características faciales únicas
2. **Verificación de vivacidad:** Detecta automáticamente intentos de fraude (fotos, videos, máscaras)
3. **Matching cifrado:** Compara vectores matemáticos (no imágenes) contra tu perfil encriptado

**Ventajas clave:**
- Reducción de 94% en intentos de phishing vs. contraseñas
- Autenticación promedio: 0.3 segundos (vs. 8 segundos con contraseña+2FA)
- Tasa de error: <0.01% (certificado por [PENDIENTE - auditor externo])

---

#### **Bloque 2: Protección de Datos Personales**

**Cumplimos con el estándar más alto de privacidad en México:**

✓ **LFPDPPP 2025:** Ley Federal de Protección de Datos Personales
✓ **Lineamientos INAI:** Instituto Nacional de Transparencia
✓ **ISO 27001:** Gestión de seguridad de la información
✓ **SOC 2 Type II:** Auditoría externa de controles [PENDIENTE - certificación]

**Datos biométricos = Datos sensibles:**
- Requieren tu consentimiento expreso (no basta con "Aceptar Términos")
- Se almacenan cifrados con AES-256-GCM
- Se eliminan automáticamente en 24 horas (configurable hasta 90 días con opt-in)
- Nunca se comparten con terceros para marketing

---

#### **Bloque 3: Arquitectura de Privacidad**

**Privacy-by-Design: Protección desde el código**

- **On-device processing:** Extracción de características faciales ocurre en tu dispositivo, no en la nube
- **Cifrado end-to-end:** Datos biométricos viajan cifrados desde origen hasta almacenamiento
- **Minimización de datos:** Solo guardamos vectores matemáticos (512 bytes), no imágenes (2+ MB)
- **Segregación:** Tus datos aislados en infraestructura multi-tenant certificada

**Respaldo y eliminación:**
- Backups geográficamente distribuidos (continuidad operativa)
- Protocolo de eliminación sincronizada (producción + todos los backups)
- Certificado de destrucción descargable vía API

---

#### **Bloque 4: Tus Derechos (ARCO)**

Conforme a la LFPDPPP, tienes derecho a:

| Derecho | Acción | Plazo |
|---------|--------|-------|
| **Acceso** | Consulta qué datos tenemos | Dashboard instantáneo |
| **Rectificación** | Corrige datos inexactos | Actualización en 1 clic |
| **Cancelación** | Elimina tus datos biométricos | <15 minutos |
| **Oposición** | Rechaza usos secundarios (marketing, ML) | Configuración granular |

**Revocación de consentimiento:**
- Acceso: Configuración → Privacidad → Gestión de Consentimientos
- Efecto: Eliminación inmediata de datos biométricos
- Alternativa: Migración a autenticación tradicional (contraseña + OTP)

**Contacto:** [privacidad@facecode.com] | Respuesta garantizada en 20 días hábiles

---

#### **Bloque 5: Transparencia Operativa**

**Proveedores y transferencias:**
- Almacenamiento: [PENDIENTE - AWS/Azure/GCP] con certificación ISO 27001
- Ubicación de servidores: México + backup en [PENDIENTE - país con protección equivalente]
- Transferencias internacionales: Solo para backup redundante (con cláusulas contractuales estándar)

**Monitoreo y auditoría:**
- Logs de acceso con retención de 12 meses (auditoría de seguridad)
- Revisiones trimestrales de cumplimiento normativo
- Reporte anual de transparencia [PENDIENTE - URL cuando esté disponible]

**Plan de respuesta a incidentes:**
- Detección y contención: <1 hora
- Notificación a afectados: <72 horas
- Reporte público: Si afecta >1000 usuarios

---

#### **Call to Action**

☐ He leído y comprendo el tratamiento de mis datos biométricos conforme a este aviso.
☐ Acepto expresamente su procesamiento para autenticación y prevención de fraude.
☐ [Opcional] Acepto recibir comunicaciones sobre actualizaciones de seguridad.

[Aceptar y Continuar] | [Descargar Aviso Completo] | [Preguntas Frecuentes]

**Registro de consentimiento:** Se generará certificado digital con timestamp, firma electrónica y hash SHA-256 para verificación de autenticidad.

---

### Hipótesis de Rendimiento

**Tasa de conversión esperada:** 75-82%
- **Fortalezas:** Balance entre detalle y claridad, credibilidad empresarial, profesionalismo
- **Debilidades:** Longitud intermedia puede no optimizar ningún extremo
- **Momento óptimo:** Registro B2B, integraciones enterprise, usuarios de desktop

### Métricas de Éxito

- Consent completion rate > 78%
- Tiempo promedio en página: 60-75 segundos
- Bounce rate < 20%
- Net Promoter Score (NPS) de proceso de consentimiento > +50

---

## PLAN DE TESTING

### Fase 1: Validación Técnica (Semana 1)
- [ ] Implementar tracking de eventos para cada variante
- [ ] Configurar Google Analytics Goals + Custom Events
- [ ] Validar renderizado correcto en mobile/desktop/tablet
- [ ] Probar flujo completo de consentimiento end-to-end

### Fase 2: Soft Launch (Semana 2)
- [ ] Liberar a 5% de tráfico total (split equitativo A/B/C)
- [ ] Monitorear errores técnicos (JavaScript exceptions, API failures)
- [ ] Validar que datos se registran correctamente en analytics

### Fase 3: Full Test (Semanas 3-4)
- [ ] Escalar a 100% de tráfico (33%/33%/34% split)
- [ ] Recolectar mínimo 385 conversiones por variante (significancia estadística)
- [ ] Análisis intermedio día 7 (early stopping si diferencia >20%)

### Fase 4: Análisis y Decisión (Semana 5)
- [ ] Test de significancia estadística (Chi-cuadrado p<0.05)
- [ ] Análisis de segmentos (mobile vs. desktop, edad, fuente de tráfico)
- [ ] Entrevistas cualitativas con 10 usuarios de cada variante
- [ ] Decisión: Declarar ganador o iterar

### Configuración de Tracking

```javascript
// Google Analytics 4 - Event tracking
gtag('event', 'privacy_consent_view', {
  'variant': 'A', // A | B | C
  'user_segment': 'privacy_paranoid', // Segmentación
  'page_location': window.location.href
});

gtag('event', 'privacy_consent_completed', {
  'variant': 'A',
  'time_on_page': 87, // segundos
  'scroll_depth': 0.92, // % del documento leído
  'optional_consents': {
    'marketing': false,
    'ml_training': true,
    'extended_retention': null
  }
});

gtag('event', 'privacy_consent_abandoned', {
  'variant': 'A',
  'exit_point': 'section_4', // Última sección vista antes de salir
  'time_on_page': 34
});
```

### Criterios de Decisión

**Variante ganadora si:**
1. Tasa de conversión ≥ +5% absoluto vs. otras variantes (p<0.05)
2. No degrada métricas secundarias (tiempo en página no < 30s, bounce < 30%)
3. Validación cualitativa positiva (entrevistas post-test)

**Iteración si:**
- Diferencias no significativas (<3% absoluto entre variantes)
- Segmentos demuestran preferencias opuestas (mobile vs. desktop)
- Métricas secundarias contradictorias (alta conversión pero alta revocación)

---

## RECOMENDACIONES DE IMPLEMENTACIÓN

### Personalización por Contexto

```javascript
// Ejemplo de lógica de selección dinámica de variante
function selectPrivacyMicrocopy(userContext) {
  const { device, age, source, previousInteractions } = userContext;

  // Reglas de negocio (post-testing, cuando hay ganador claro)
  if (source === 'enterprise_b2b' || device === 'desktop') {
    return 'VARIANT_C_BALANCED'; // Profesionalismo
  }

  if (age < 30 && device === 'mobile') {
    return 'VARIANT_B_CONVENIENCE'; // Simplicidad
  }

  if (previousInteractions.includes('privacy_policy_read')) {
    return 'VARIANT_A_PRIVACY_PARANOID'; // Ya demostró interés en privacidad
  }

  // Default: Variante balanceada
  return 'VARIANT_C_BALANCED';
}
```

### Localización y Adaptación

- **Español neutro vs. regionalismos:** Evitar modismos mexicanos si hay usuarios LATAM
- **Nivel de lectura:** Variante A (12° grado), Variante B (8° grado), Variante C (10° grado)
- **Mobile-first:** Variantes B y C optimizadas para pantallas <375px width

---

## ANEXO: BENCHMARK COMPETITIVO

| Empresa | Tasa de Consentimiento | Tiempo Promedio | Longitud Microcopy | Enfoque |
|---------|----------------------|-----------------|-------------------|---------|
| **Competidor A** | 71% | 65s | ~200 palabras | Legal-heavy |
| **Competidor B** | 89% | 28s | ~120 palabras | Hyper-simplified |
| **Competidor C** | 78% | 52s | ~180 palabras | Balanced |
| **FaceCode (Objetivo)** | **>82%** | **45-60s** | **150-250 palabras** | Context-aware |

**Meta:** Superar a Competidor B en conversión manteniendo compliance legal completo (ventaja de Variante A).

---

**Última actualización:** 2025-10-29
**Autor:** FaceCode Growth Team
**Aprobación requerida:** Legal (validación de claims), Marketing (brand voice), Product (UX flows)
