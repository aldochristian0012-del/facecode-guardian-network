# Aviso de Privacidad Integral — FaceCode® Guardian Network

**Última actualización:** 29 de octubre de 2025
**Versión:** 1.0
**Responsable:** FaceCode® Guardian Network

---

## Introducción

En FaceCode® Guardian Network, la privacidad y la protección de datos personales son pilares fundamentales de nuestra misión ética. Este Aviso de Privacidad describe de manera clara, transparente y accesible cómo recopilamos, procesamos, almacenamos, compartimos y protegemos sus datos personales, con especial énfasis en **datos biométricos** derivados del reconocimiento facial.

Este documento cumple con:

- **Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP)** de México
- **Reglamento General de Protección de Datos (GDPR)** de la Unión Europea
- **Reglamento de Inteligencia Artificial (AI Act)** de la UE
- **California Consumer Privacy Act (CCPA)** y **California Privacy Rights Act (CPRA)**
- **Directiva de Accesibilidad Europea (EAA)**
- Mejores prácticas internacionales de privacidad por diseño y por defecto

---

## 1. Identidad y Contacto del Responsable

**Responsable del Tratamiento:**
FaceCode® Guardian Network
Christian (Fundador)
Contacto de Privacidad: [privacy@facecode.app](mailto:privacy@facecode.app)
Sitio web: [facecode.app](https://facecode.app) *(pendiente de publicación)*

**Oficial de Protección de Datos (DPO):**
Para consultas específicas sobre privacidad y derechos ARCO, contacte a nuestro Oficial de Protección de Datos en [dpo@facecode.app](mailto:dpo@facecode.app).

---

## 2. Tipos de Datos Personales Recopilados

### 2.1. Datos Biométricos (Categoría Especial)

Los datos biométricos son **datos sensibles** bajo todas las legislaciones aplicables y reciben protección especial:

- **Características faciales:** Geometría facial, distancias entre puntos clave (ojos, nariz, boca), contornos, patrones de textura
- **Plantillas biométricas:** Representaciones matemáticas irreversibles generadas a partir de imágenes faciales mediante algoritmos de deep learning
- **Vectores de embeddings:** Representaciones numéricas de alta dimensión (512–2048 dimensiones) que codifican rasgos únicos del rostro

**Importante:**
- **NO almacenamos fotografías ni videos** de su rostro, salvo cuando usted lo autorice explícitamente para fines específicos (por ejemplo, verificación manual de identidad).
- Las plantillas biométricas son **irreversibles**: no se puede reconstruir una imagen facial a partir de ellas.
- Todo procesamiento de datos biométricos requiere su **consentimiento explícito, libre, específico, informado e inequívoco**.

### 2.2. Datos de Identificación

- Nombre completo
- Correo electrónico
- Número de teléfono (opcional)
- Nombre de usuario (alias)
- Fotografía de perfil (opcional, no utilizada para reconocimiento facial sin consentimiento separado)

### 2.3. Datos de Dispositivo y Técnicos

- Dirección IP
- Identificador único de dispositivo (UUID)
- Tipo de dispositivo, sistema operativo y versión
- Navegador web y versión
- Configuración regional e idioma
- Información de sensores (cámara, acelerómetro, giroscopio) — solo con permiso explícito del dispositivo

### 2.4. Datos de Uso y Comportamiento

- Historial de interacciones con la aplicación
- Fecha y hora de acceso
- Funcionalidades utilizadas
- Preferencias de configuración
- Logs de errores y eventos técnicos (anonimizados)

### 2.5. Datos de Análisis Emocional (Opcional)

Con su consentimiento explícito adicional, podemos procesar:

- Estimaciones de estado emocional (alegría, tristeza, sorpresa, etc.) derivadas de expresiones faciales
- Nivel de atención o fatiga (estimado)
- Datos de contexto de la sesión (iluminación, distancia a cámara)

**Estos datos son siempre agregados y anonimizados. Nunca identificamos emociones de individuos específicos sin consentimiento explícito y justificación legítima.**

---

## 3. Finalidades del Tratamiento de Datos

### 3.1. Finalidades Principales (Requieren Consentimiento)

1. **Autenticación biométrica:** Verificar su identidad mediante reconocimiento facial para acceso seguro a servicios.
2. **Análisis de experiencia de usuario:** Evaluar usabilidad, accesibilidad y calidad de la interacción con la aplicación.
3. **Mejora del servicio:** Optimizar algoritmos, corregir errores y desarrollar nuevas funcionalidades.
4. **Cumplimiento de obligaciones legales:** Responder a solicitudes de autoridades competentes (solo cuando sea legalmente obligatorio).

### 3.2. Finalidades Secundarias (Requieren Consentimiento Adicional)

5. **Entrenamiento de modelos de IA:** Utilizar datos biométricos anonimizados y agregados para mejorar modelos de reconocimiento facial y reducir sesgos algorítmicos.
6. **Investigación académica y científica:** Colaborar con instituciones de investigación en proyectos de ética en IA, detección de sesgos y privacidad (siempre con anonimización completa).
7. **Análisis de mercado y preferencias:** Entender tendencias de uso para desarrollar productos más inclusivos y accesibles.

**Usted puede rechazar las finalidades secundarias sin que esto afecte su acceso a las finalidades principales.**

---

## 4. Fundamento Legal del Tratamiento

El tratamiento de sus datos se basa en:

1. **Consentimiento explícito:** Para datos biométricos y finalidades secundarias.
2. **Ejecución de contrato:** Para proporcionar servicios de autenticación solicitados por usted.
3. **Interés legítimo:** Para mejorar la seguridad, prevenir fraudes y garantizar el correcto funcionamiento técnico.
4. **Cumplimiento de obligaciones legales:** Cuando la ley exija retención de ciertos datos (por ejemplo, para auditorías fiscales o respuestas a autoridades).

---

## 5. Principios de Privacidad por Diseño

### 5.1. Procesamiento Preferente en Dispositivo (On-Device Processing)

**La mayoría del procesamiento biométrico ocurre localmente en su dispositivo**, sin envío de datos a servidores externos. Esto incluye:

- Generación de plantillas biométricas
- Verificación de identidad (matching 1:1)
- Análisis de calidad de imagen
- Estimación de vivacidad (liveness detection)

**Solo se envían datos al servidor cuando:**
- Usted autoriza explícitamente el almacenamiento en la nube (por ejemplo, para sincronización entre dispositivos)
- Es técnicamente imposible procesar en el dispositivo (hardware insuficiente)
- Usted solicita funcionalidades específicas que requieren procesamiento en servidor (identificación 1:N en grandes bases de datos)

### 5.2. Minimización de Datos

Recopilamos **únicamente los datos estrictamente necesarios** para cumplir con las finalidades descritas. No recopilamos datos "por si acaso" ni datos superfluos.

### 5.3. Retención Mínima

- **Plantillas biométricas:** Eliminadas automáticamente después de **24 horas** si no hay autenticación activa, salvo que usted autorice un período mayor.
- **Logs de consentimiento:** Retenidos por **5 años** para cumplimiento legal y auditoría.
- **Datos de uso anonimizados:** Retenidos indefinidamente (no son datos personales tras la anonimización).
- **Datos de cuenta activa:** Retenidos mientras su cuenta esté activa. Tras eliminación de cuenta, borrados en **7 días** con verificación criptográfica.

### 5.4. Cifrado de Extremo a Extremo

Todos los datos biométricos en tránsito y en reposo están cifrados con:

- **En tránsito:** TLS 1.3 con Perfect Forward Secrecy (PFS)
- **En reposo:** AES-256-GCM con claves gestionadas mediante HSM (Hardware Security Module) o servicios de gestión de claves en la nube con certificación FIPS 140-2 nivel 3.

### 5.5. Anonimización y Seudonimización

- Los datos utilizados para entrenamiento de modelos son **totalmente anonimizados** mediante técnicas de privacidad diferencial (differential privacy).
- Los datos de análisis están **seudonimizados** con identificadores aleatorios, sin vínculo directo a su identidad.

---

## 6. Compartición de Datos

### 6.1. No Vendemos sus Datos

**FaceCode® nunca vende ni alquila datos personales a terceros, anunciantes o brokers de datos.**

### 6.2. Compartición con Terceros (Solo Cuando Sea Necesario)

Podemos compartir datos con:

1. **Proveedores de servicios técnicos:**
   - Hosting en la nube (AWS, Google Cloud, Azure) con contratos de procesamiento de datos (DPA) conforme a GDPR/LFPDPPP
   - Servicios de análisis de seguridad y prevención de fraudes
   - Proveedores de CDN (Content Delivery Network) para optimizar rendimiento

2. **Autoridades legales:**
   - Solo cuando sea legalmente obligatorio mediante orden judicial válida
   - Publicamos un **Informe de Transparencia anual** con estadísticas agregadas de solicitudes gubernamentales

3. **Investigadores académicos:**
   - Solo con datos anonimizados y bajo acuerdos de confidencialidad y uso ético

**Todos los terceros firman acuerdos contractuales que garantizan el mismo nivel de protección que este Aviso.**

---

## 7. Transferencias Internacionales de Datos

Si sus datos se transfieren fuera de su país de residencia, garantizamos protecciones equivalentes mediante:

- **Cláusulas Contractuales Estándar (SCC)** aprobadas por la Comisión Europea
- **Binding Corporate Rules (BCR)** cuando sea aplicable
- **Certificaciones Privacy Shield 2.0** (si disponible)
- **Evaluaciones de impacto de transferencia** conforme a sentencias Schrems II (UE)

**Usted tiene derecho a solicitar información detallada sobre transferencias internacionales en cualquier momento.**

---

## 8. Derechos ARCO y Otros Derechos de Privacidad

### 8.1. Derechos ARCO (México/LFPDPPP)

Usted tiene derecho a:

- **Acceso:** Conocer qué datos personales tenemos sobre usted
- **Rectificación:** Corregir datos inexactos o incompletos
- **Cancelación:** Solicitar la eliminación de sus datos
- **Oposición:** Oponerse al tratamiento de sus datos para finalidades específicas

### 8.2. Derechos GDPR (Unión Europea)

Además de ARCO, tiene derecho a:

- **Portabilidad de datos:** Recibir sus datos en formato estructurado, de uso común e interoperable (JSON, CSV)
- **Limitación del tratamiento:** Suspender temporalmente el procesamiento de sus datos
- **Derecho al olvido:** Solicitar eliminación inmediata en circunstancias específicas
- **Derecho a no ser objeto de decisiones automatizadas:** Solicitar intervención humana en decisiones que le afecten significativamente

### 8.3. Derechos CCPA/CPRA (California, EE.UU.)

- **Conocer qué información se recopila, vende o comparte**
- **Solicitar eliminación** de información personal
- **Optar por no participar** en la venta de datos (aunque FaceCode® no vende datos)
- **No discriminación** por ejercer sus derechos de privacidad
- **Corrección de datos inexactos**

### 8.4. Ejercicio de Derechos

Puede ejercer sus derechos mediante:

1. **Portal de privacidad self-service:** [facecode.app/privacy](https://facecode.app/privacy) → Sección ARCO
2. **Correo electrónico:** [privacy@facecode.app](mailto:privacy@facecode.app)
3. **Desde la aplicación:** Ajustes → Privacidad → Solicitud ARCO

**Plazo de respuesta:** 20 días hábiles (México/LFPDPPP), 30 días naturales (GDPR), 45 días (CCPA).

**Documentación requerida:**
- Nombre completo
- Correo electrónico registrado
- Descripción clara del derecho a ejercer
- Copia de identificación oficial (para proteger su identidad) — tratada de manera confidencial

---

## 9. Revocación del Consentimiento

Puede **revocar su consentimiento en cualquier momento** sin necesidad de justificación mediante:

1. **Aplicación móvil/web:** Ajustes → Privacidad → Revocar consentimiento biométrico
2. **Correo electrónico:** [privacy@facecode.app](mailto:privacy@facecode.app)
3. **Portal web:** Sección de gestión de consentimientos

**Efectos de la revocación:**
- Eliminación inmediata de plantillas biométricas (verificable mediante certificado criptográfico)
- Desactivación de funciones de autenticación facial
- Sus datos de cuenta permanecen activos (puede seguir usando servicios no biométricos)

---

## 10. Seguridad de los Datos

### 10.1. Medidas Técnicas

- **Cifrado AES-256** en reposo y TLS 1.3 en tránsito
- **Autenticación multifactor (MFA)** para acceso administrativo
- **Firewalls de aplicación web (WAF)** y sistemas de detección de intrusiones (IDS/IPS)
- **Auditorías de seguridad** trimestrales realizadas por terceros independientes
- **Pruebas de penetración (pentesting)** semestrales
- **Bug bounty program** para investigadores de seguridad

### 10.2. Medidas Organizativas

- **Formación obligatoria** en privacidad y seguridad para todo el personal
- **Acceso basado en principio de mínimo privilegio** (least privilege)
- **Registros de auditoría** inmutables de todos los accesos a datos personales
- **Plan de respuesta a incidentes** con notificación en menos de 72 horas (GDPR)

### 10.3. Notificación de Brechas de Seguridad

En caso de brecha de seguridad que afecte sus datos personales:

- **Le notificaremos sin dilación indebida** (máximo 72 horas tras detección)
- **Información incluida:** Naturaleza de la brecha, datos afectados, medidas adoptadas, recomendaciones para protegerse
- **Evidencias de mitigación:** Reportes de auditoría y certificados de remediación

---

## 11. Modo Ultra Privado (Ultra Private Mode)

Ofrecemos una modalidad opcional para usuarios con requisitos extremos de privacidad:

**Características:**
- **Procesamiento 100% local** sin conexión a servidores
- **Cero telemetría** (ni siquiera datos anonimizados)
- **Cifrado end-to-end** para backups locales
- **Auditoría independiente** con código fuente abierto para inspección

**Disponibilidad:** Suscripción premium o pago único (consulte planes en [facecode.app/pricing](https://facecode.app/pricing)).

---

## 12. Privacidad de Menores

FaceCode® **no está diseñado para menores de 16 años** (UE) o 13 años (EE.UU.). Si tiene menos de 16 años, necesita el consentimiento verificable de sus padres o tutores legales.

Si descubrimos que hemos recopilado datos de menores sin consentimiento parental, **eliminaremos esos datos inmediatamente**.

---

## 13. Cookies y Tecnologías de Rastreo

Utilizamos cookies y tecnologías similares para:

1. **Cookies esenciales:** Autenticación de sesión, seguridad (no requieren consentimiento)
2. **Cookies de análisis:** Google Analytics (anonimizado), con consentimiento
3. **Cookies de preferencias:** Idioma, tema visual (no requieren consentimiento)

**Gestión de cookies:** [facecode.app/cookies](https://facecode.app/cookies) o mediante configuración del navegador.

**No utilizamos cookies de publicidad ni rastreo para marketing.**

---

## 14. Actualizaciones del Aviso de Privacidad

Podemos actualizar este Aviso para reflejar cambios legales, técnicos o de servicio. Cuando hagamos cambios materiales:

- **Le notificaremos por correo electrónico** y mediante aviso destacado en la aplicación
- **Solicitaremos su consentimiento renovado** si los cambios afectan el tratamiento de datos biométricos
- **Mantendremos versiones históricas** disponibles en [facecode.app/privacy/archive](https://facecode.app/privacy/archive)

**Su uso continuado tras la notificación constituye aceptación de los cambios (excepto para datos biométricos, donde se requiere consentimiento explícito).**

---

## 15. Marco Legal y Jurisdicción

Este Aviso se rige por:

- Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP) de México
- Reglamento General de Protección de Datos (GDPR) de la UE
- Leyes locales aplicables según su ubicación

**Para disputas:**
- **México:** Instituto Nacional de Transparencia, Acceso a la Información y Protección de Datos Personales (INAI)
- **UE:** Autoridad de protección de datos de su país
- **California:** Oficina del Fiscal General de California

---

## 16. Transparencia Radical y Auditoría Pública

En línea con nuestros **Principios Éticos**, publicamos:

- **Informe de Transparencia anual:** Estadísticas de solicitudes de datos, brechas de seguridad, auditorías
- **Auditorías independientes:** Reportes técnicos de seguridad y privacidad (publicados en [facecode.app/audits](https://facecode.app/audits))
- **Código fuente abierto:** Componentes críticos de privacidad disponibles en GitHub para revisión pública

---

## 17. Contacto y Más Información

**Consultas generales de privacidad:**
[privacy@facecode.app](mailto:privacy@facecode.app)

**Oficial de Protección de Datos (DPO):**
[dpo@facecode.app](mailto:dpo@facecode.app)

**Solicitudes ARCO y ejercicio de derechos:**
[facecode.app/privacy/arco](https://facecode.app/privacy/arco)

**Soporte técnico:**
[support@facecode.app](mailto:support@facecode.app)

**Dirección postal:**
FaceCode® Guardian Network
[Dirección física pendiente]
México

---

## Resumen Ejecutivo (Para Referencia Rápida)

| **Aspecto** | **Descripción** |
|-------------|-----------------|
| **Datos recopilados** | Plantillas biométricas faciales, datos de cuenta, datos de dispositivo, datos de uso |
| **Finalidad principal** | Autenticación biométrica y mejora del servicio |
| **Base legal** | Consentimiento explícito (biométricos), ejecución de contrato, interés legítimo |
| **Almacenamiento** | Procesamiento preferente en dispositivo; retención de plantillas 24h salvo autorización |
| **Cifrado** | AES-256 (reposo), TLS 1.3 (tránsito) |
| **Compartición** | No vendemos datos; solo compartimos con proveedores de servicios bajo DPA estrictos |
| **Derechos** | ARCO, portabilidad, olvido, oposición, limitación |
| **Revocación** | En cualquier momento desde la app o por correo |
| **Contacto** | privacy@facecode.app |

---

**Fecha de entrada en vigor:** 29 de octubre de 2025
**Versión:** 1.0

---

> **© 2025 FaceCode® Guardian Network**
> *Protegiendo la dignidad digital • Transparencia radical • IA ética*
