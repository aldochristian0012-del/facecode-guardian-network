# AVISO DE PRIVACIDAD
## FaceCode Guardian Network

**Versión:** 1.0
**Fecha de última actualización:** [PENDIENTE - Insertar fecha de publicación]
**Vigencia:** A partir de su publicación

---

## TABLA DE CONTENIDOS

1. [Identidad y Domicilio del Responsable](#1-identidad-y-domicilio-del-responsable)
2. [Datos Personales que se Recaban](#2-datos-personales-que-se-recaban)
3. [Finalidades del Tratamiento](#3-finalidades-del-tratamiento)
4. [Datos Biométricos: Naturaleza Sensible y Consentimiento Expreso](#4-datos-biométricos-naturaleza-sensible-y-consentimiento-expreso)
5. [Fundamento Legal para el Tratamiento](#5-fundamento-legal-para-el-tratamiento)
6. [Mecanismos de Recabación](#6-mecanismos-de-recabación)
7. [Transferencias de Datos Personales](#7-transferencias-de-datos-personales)
8. [Periodo de Retención y Criterios de Conservación](#8-periodo-de-retención-y-criterios-de-conservación)
9. [Procesamiento On-Device y Minimización de Datos](#9-procesamiento-on-device-y-minimización-de-datos)
10. [Derechos ARCO y Mecanismos de Ejercicio](#10-derechos-arco-y-mecanismos-de-ejercicio)
11. [Revocación del Consentimiento](#11-revocación-del-consentimiento)
12. [Limitación de Uso y Divulgación](#12-limitación-de-uso-y-divulgación)
13. [Medidas de Seguridad Técnicas y Administrativas](#13-medidas-de-seguridad-técnicas-y-administrativas)
14. [Uso de Cookies y Tecnologías de Rastreo](#14-uso-de-cookies-y-tecnologías-de-rastreo)
15. [Cambios al Aviso de Privacidad](#15-cambios-al-aviso-de-privacidad)
16. [Autoridad de Protección de Datos](#16-autoridad-de-protección-de-datos)
17. [Consentimiento](#17-consentimiento)

---

## 1. IDENTIDAD Y DOMICILIO DEL RESPONSABLE

**[PENDIENTE - Nombre legal completo de la entidad responsable]**, en adelante "**el Responsable**", con domicilio en:

- **Calle y número:** [PENDIENTE]
- **Colonia:** [PENDIENTE]
- **Ciudad y Estado:** [PENDIENTE]
- **Código Postal:** [PENDIENTE]
- **País:** [PENDIENTE]

**Datos de contacto del Departamento de Protección de Datos Personales:**
- **Correo electrónico:** [PENDIENTE - Ejemplo: privacidad@facecode.com]
- **Teléfono:** [PENDIENTE]
- **Horario de atención:** [PENDIENTE - Ejemplo: Lunes a Viernes de 9:00 a 18:00 hrs]

Es responsable del tratamiento de sus datos personales conforme a la Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP) y su Reglamento.

---

## 2. DATOS PERSONALES QUE SE RECABAN

Para el funcionamiento de **FaceCode Guardian Network**, recabamos las siguientes categorías de datos personales:

### 2.1 Datos de Identificación
- Nombre completo
- Correo electrónico
- Número de teléfono (opcional)
- Dirección IP
- Identificador único de dispositivo (Device ID)

### 2.2 Datos Biométricos (Sensibles)
- **Vectores faciales (embeddings):** Representación matemática de características faciales únicas, extraída mediante algoritmos de deep learning
- **Metadatos de captura:** Timestamp, calidad de imagen, condiciones de iluminación
- **Parámetros de vivacidad (liveness detection):** Indicadores para prevención de ataques de presentación (spoofing)

**IMPORTANTE:** Los datos biométricos son clasificados como **datos personales sensibles** bajo el artículo 3, fracción VI de la LFPDPPP, y requieren su **consentimiento expreso y por escrito** para su tratamiento (artículo 9 LFPDPPP).

### 2.3 Datos Técnicos y de Uso
- Registros de autenticación (logs)
- Información del navegador y sistema operativo
- Datos de geolocalización aproximada (ciudad/país, derivados de IP)
- Estadísticas de uso agregadas y anonimizadas

---

## 3. FINALIDADES DEL TRATAMIENTO

Sus datos personales serán utilizados para las siguientes finalidades:

### 3.1 Finalidades Primarias (Necesarias para el servicio)
1. **Autenticación biométrica:** Verificación de identidad mediante reconocimiento facial
2. **Prevención de fraude:** Detección de intentos de suplantación y ataques de presentación
3. **Cumplimiento de obligaciones legales:** Atención a requerimientos de autoridades competentes
4. **Gestión de la relación contractual:** Administración de su cuenta y servicios contratados
5. **Seguridad del sistema:** Protección de infraestructura contra accesos no autorizados

### 3.2 Finalidades Secundarias (Opcionales, requieren consentimiento separado)
1. **Mejora de algoritmos:** Entrenamiento y optimización de modelos de machine learning (solo con datos anonimizados)
2. **Comunicaciones de marketing:** Envío de información sobre nuevos servicios y actualizaciones
3. **Estudios de mercado:** Análisis de patrones de uso para desarrollo de producto (datos agregados)

**Usted puede negarse al tratamiento de sus datos para finalidades secundarias** mediante el mecanismo descrito en la sección 12 (Limitación de Uso y Divulgación). La negativa no afectará la prestación del servicio principal.

---

## 4. DATOS BIOMÉTRICOS: NATURALEZA SENSIBLE Y CONSENTIMIENTO EXPRESO

### 4.1 Clasificación Legal
Los vectores faciales (embeddings) y demás datos biométricos procesados por FaceCode Guardian Network son **datos personales sensibles** conforme al artículo 3, fracción VI de la LFPDPPP, debido a que:

- Permiten la identificación única de personas
- Revelan características físicas particulares
- Su uso indebido puede generar discriminación o riesgo a la integridad física/patrimonial

### 4.2 Mecanismo de Consentimiento Expreso
El tratamiento de sus datos biométricos requiere su **consentimiento expreso, informado e inequívoco**, obtenido mediante:

1. **Firma electrónica avanzada** con certificado digital timestamped
2. **Registro inmutable** que incluye:
   - User ID único
   - Timestamp preciso (UTC con milisegundos)
   - Dirección IP de origen
   - Device ID del dispositivo utilizado
   - Versión exacta de este Aviso de Privacidad
   - Hash SHA-256 del consentimiento para verificación de integridad

3. **Doble opt-in con confirmación explícita:** Se requiere marcar una casilla específica que declara:

> "He leído, entiendo y acepto expresamente el tratamiento de mis datos biométricos (vectores faciales) conforme al Aviso de Privacidad de FaceCode Guardian Network. Estoy consciente de que estos datos son sensibles y que puedo revocar mi consentimiento en cualquier momento."

### 4.3 Información Previa al Consentimiento
Antes de solicitar su consentimiento, se le proporciona información clara y destacada sobre:

- Qué datos biométricos específicos se recaban
- Para qué finalidades se utilizarán
- Cuánto tiempo se conservarán (24 horas por defecto)
- Cómo puede ejercer sus derechos ARCO
- Cómo revocar su consentimiento
- Las medidas de seguridad implementadas

---

## 5. FUNDAMENTO LEGAL PARA EL TRATAMIENTO

El tratamiento de sus datos personales se fundamenta en:

### 5.1 Marco Normativo Nacional
- **Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP)** - Publicada en el DOF el 5 de julio de 2010
- **Reglamento de la LFPDPPP** - Publicado en el DOF el 21 de diciembre de 2011
- **Lineamientos del Aviso de Privacidad** (INAI/2015)

### 5.2 Bases Legales Específicas
- **Artículo 8 LFPDPPP:** Consentimiento del titular para tratamiento de datos personales
- **Artículo 9 LFPDPPP:** Consentimiento expreso para datos sensibles (biométricos)
- **Artículo 16 LFPDPPP:** Principios de licitud, consentimiento, información, calidad, finalidad, lealtad, proporcionalidad y responsabilidad

### 5.3 Interés Legítimo (cuando aplique)
En casos específicos previstos por el artículo 10 LFPDPPP, el tratamiento puede realizarse sin consentimiento cuando:
- Exista orden de autoridad competente
- Sea necesario para prevenir fraude en verificación de identidad
- Los datos figuren en fuentes de acceso público

---

## 6. MECANISMOS DE RECABACIÓN

Sus datos personales son recabados mediante:

### 6.1 Directamente del Titular
- **Formularios de registro:** Captura manual de datos de identificación
- **Aplicación móvil/web:** Captura biométrica mediante cámara del dispositivo
- **Cookies y tecnologías similares:** Registro automático de datos técnicos (ver sección 14)

### 6.2 Fuentes Indirectas (con su consentimiento previo)
- **APIs de terceros:** Integración con sistemas de partners tecnológicos (solo metadatos técnicos, nunca datos biométricos)
- **Proveedores de servicios cloud:** Logs de infraestructura para seguridad y auditoría

### 6.3 Procesamiento On-Device
**La captura y procesamiento inicial de datos biométricos se realiza LOCALMENTE en su dispositivo** (smartphone, tablet, computadora), sin transmisión inmediata a servidores externos. Solo se envían:
- Vectores faciales cifrados (no imágenes en crudo)
- Metadatos necesarios para autenticación
- Resultados de liveness detection

**Su rostro nunca sale de su dispositivo en forma de fotografía o video completo.** Solo se transmiten representaciones matemáticas irreversibles.

---

## 7. TRANSFERENCIAS DE DATOS PERSONALES

### 7.1 Transferencias Nacionales
Sus datos personales podrán ser transferidos dentro del territorio nacional a:

1. **Proveedores de servicios en la nube (Cloud Service Providers):**
   - [PENDIENTE - Ejemplo: AWS México, Google Cloud México]
   - Finalidad: Almacenamiento seguro de vectores faciales cifrados
   - Garantías: Contrato de procesamiento de datos (DPA) conforme LFPDPPP

2. **Proveedores de servicios de seguridad informática:**
   - [PENDIENTE - Nombre del proveedor]
   - Finalidad: Monitoreo de infraestructura, prevención de intrusiones
   - Garantías: Acuerdos de confidencialidad y obligaciones de protección equivalentes

### 7.2 Transferencias Internacionales
Sus datos personales podrán ser transferidos fuera de México a:

1. **Servidores de respaldo (backup) ubicados en:** [PENDIENTE - País, ejemplo: Estados Unidos - AWS US-East]
   - Garantías: Certificación Privacy Shield successor / Cláusulas Contractuales Estándar
   - Finalidad: Continuidad operativa y recuperación ante desastres

2. **Proveedores de análisis de seguridad:** [PENDIENTE - Si aplica]
   - Solo datos anonimizados y agregados
   - Finalidad: Detección de patrones de fraude global

### 7.3 Consentimiento para Transferencias
Al aceptar este Aviso de Privacidad, **usted consiente expresamente** las transferencias mencionadas, excepto para transferencias a terceros no relacionados con la prestación del servicio, las cuales requerirán su consentimiento adicional por separado.

### 7.4 Transferencias sin Consentimiento
Conforme al artículo 37 LFPDPPP, ciertos datos pueden transferirse sin su consentimiento cuando:
- Sea exigido por autoridad competente
- Sea necesario para atención médica de emergencia
- Esté previsto en ley o tratado internacional

---

## 8. PERIODO DE RETENCIÓN Y CRITERIOS DE CONSERVACIÓN

### 8.1 Retención de Datos Biométricos (Default)
**Los vectores faciales (embeddings) y datos de liveness detection se conservan por 24 HORAS** desde la última autenticación exitosa, después de las cuales son **eliminados automáticamente de forma irreversible** mediante:

1. Sobrescritura múltiple (patrón Gutmann o DoD 5220.22-M)
2. Eliminación de backups rotacionales
3. Generación de certificado de eliminación descargable (ver endpoint `/verify-deletion`)

### 8.2 Extensión de Retención (Opt-In)
Usted puede solicitar la extensión del periodo de retención mediante consentimiento adicional:

- **Hasta 30 días:** Para usuarios frecuentes que requieren autenticaciones recurrentes
- **Hasta 90 días:** Para integraciones enterprise con auditorías periódicas
- **Indefinido (hasta revocación):** Solo para casos contractuales específicos con justificación documentada

**La extensión requiere confirmación explícita** mediante checkbox separado y registro independiente del consentimiento original.

### 8.3 Retención de Datos No Biométricos
- **Logs de autenticación (sin datos biométricos):** 12 meses para auditoría de seguridad
- **Datos de contacto (email, teléfono):** Mientras subsista la relación contractual + 5 años (prescripción legal)
- **Datos de facturación:** 10 años (obligación fiscal conforme Código Fiscal de la Federación)

### 8.4 Criterios de Eliminación
La eliminación de datos se realiza cuando:
1. Transcurre el periodo de retención establecido
2. Usted revoca su consentimiento
3. Se ejerce el derecho de cancelación (ARCO)
4. Los datos dejan de ser necesarios para las finalidades que motivaron su tratamiento
5. Existe orden de autoridad competente

---

## 9. PROCESAMIENTO ON-DEVICE Y MINIMIZACIÓN DE DATOS

### 9.1 Arquitectura Privacy-by-Design
FaceCode Guardian Network implementa **procesamiento local primario** (on-device) para minimizar la exposición de datos biométricos:

1. **Captura y extracción de embeddings:** Se realiza en el dispositivo del usuario mediante SDK local
2. **Liveness detection:** Algoritmos anti-spoofing ejecutados localmente
3. **Cifrado antes de transmisión:** Los vectores se cifran con AES-256-GCM antes de salir del dispositivo
4. **Transmisión solo de datos necesarios:** Nunca se envían imágenes en crudo, solo vectores matemáticos

### 9.2 Minimización de Datos (Data Minimization)
Conforme al principio de proporcionalidad (artículo 6 LFPDPPP):
- Solo recabamos datos estrictamente necesarios para autenticación
- No almacenamos imágenes faciales completas
- No registramos datos contextuales innecesarios (ubicación GPS precisa, contactos, etc.)
- Los vectores faciales se reducen dimensionalmente para almacenamiento eficiente

### 9.3 Anonimización y Pseudonimización
Para finalidades secundarias (mejora de algoritmos), aplicamos:
- **Anonimización irreversible:** Desvinculación total de identidad
- **Pseudonimización:** Sustitución de identificadores directos por tokens
- **Agregación estadística:** Reportes solo con métricas grupales (nunca individuales)

---

## 10. DERECHOS ARCO Y MECANISMOS DE EJERCICIO

Conforme a los artículos 22 a 34 de la LFPDPPP, usted tiene derecho a:

### 10.1 Derechos ARCO
- **Acceso:** Conocer qué datos personales tenemos, para qué los usamos y las condiciones de tratamiento
- **Rectificación:** Solicitar corrección de datos inexactos o incompletos
- **Cancelación:** Solicitar eliminación de sus datos cuando considere que no están siendo tratados conforme a la ley
- **Oposición:** Oponerse al tratamiento de sus datos para finalidades específicas

### 10.2 Procedimiento de Ejercicio
Para ejercer sus derechos ARCO, debe:

1. **Enviar solicitud por escrito** a: [PENDIENTE - privacidad@facecode.com]
   - Incluir: Nombre completo, correo electrónico registrado, copia de identificación oficial
   - Especificar: Derecho(s) que desea ejercer y razones (para cancelación/oposición)

2. **Plazo de respuesta:** 20 días hábiles contados desde la recepción de la solicitud
3. **Plazo para hacer efectivos los derechos:** 15 días hábiles después de comunicar la procedencia

### 10.3 Formulario Simplificado
Puede utilizar el formulario digital disponible en: [PENDIENTE - URL del portal de privacidad]

### 10.4 Acceso Inmediato a Datos Biométricos
Para datos biométricos específicamente, ofrecemos acceso expedito mediante:
- **Dashboard de usuario:** Visualización de embeddings almacenados (representación hash, no vector completo)
- **API de consulta:** Endpoint `/api/my-biometric-data` con autenticación OAuth 2.0
- **Exportación en formato JSON:** Descarga de todos sus datos en formato portable

### 10.5 Cancelación Automática de Datos Biométricos
Puede solicitar eliminación inmediata (sin esperar 24 horas) mediante:
- Botón "Eliminar mis datos biométricos ahora" en la configuración de cuenta
- Confirmación mediante código OTP enviado a su email registrado
- Certificado de eliminación generado automáticamente al completar el proceso

---

## 11. REVOCACIÓN DEL CONSENTIMIENTO

### 11.1 Derecho de Revocación
Usted puede revocar su consentimiento para el tratamiento de sus datos personales **en cualquier momento**, sin necesidad de justificación, conforme al artículo 8 de la LFPDPPP.

### 11.2 Mecanismo de Revocación
Para revocar su consentimiento:

1. **Acceda a su cuenta** en FaceCode Guardian Network
2. **Navegue a:** Configuración > Privacidad > Gestión de Consentimientos
3. **Seleccione:** "Revocar consentimiento para uso de datos biométricos"
4. **Confirme mediante:** Código de verificación enviado a su email + autenticación de dos factores
5. **Efecto inmediato:** Los datos biométricos se eliminan en <15 minutos

### 11.3 Consecuencias de la Revocación
Al revocar su consentimiento:
- **Se eliminarán todos sus vectores faciales y datos biométricos asociados**
- **No podrá utilizar autenticación facial** (podrá usar métodos alternativos como contraseña + 2FA)
- **Se conservarán datos no biométricos** necesarios para la relación contractual (email, historial de transacciones)

### 11.4 Alternativas Post-Revocación
Si revoca el consentimiento biométrico, podrá:
- Migrar a autenticación tradicional (usuario/contraseña + OTP)
- Utilizar autenticación basada en tokens de hardware (FIDO2/WebAuthn)
- Cerrar completamente su cuenta (eliminación total de datos)

---

## 12. LIMITACIÓN DE USO Y DIVULGACIÓN

### 12.1 Derecho de Limitación
Usted puede limitar el uso y divulgación de sus datos personales mediante:

1. **Registro en listas de exclusión internas:**
   - Marketing: Desactivar comunicaciones promocionales
   - Perfilamiento: Oponerse a análisis de comportamiento

2. **Configuración granular de consentimientos:**
   - Dashboard de privacidad con toggles independientes para cada finalidad secundaria

### 12.2 Mecanismo de Ejercicio
Para limitar el uso de sus datos:
- **Email directo a:** [PENDIENTE - privacidad@facecode.com] con asunto "Limitación de Uso"
- **Configuración de cuenta:** Sección "Preferencias de Privacidad"
- **Formato estructurado:** Utilice el formulario disponible en [PENDIENTE - URL]

### 12.3 Excepciones
No podrá limitar el uso de datos cuando:
- Sea necesario para cumplir obligaciones legales
- Sea requerido por autoridad competente
- Sea indispensable para la prestación del servicio principal (autenticación)

---

## 13. MEDIDAS DE SEGURIDAD TÉCNICAS Y ADMINISTRATIVAS

Conforme al artículo 19 de la LFPDPPP, implementamos medidas de seguridad **físicas, técnicas y administrativas** para proteger sus datos personales:

### 13.1 Seguridad Técnica
- **Cifrado en tránsito:** TLS 1.3 con Perfect Forward Secrecy para todas las comunicaciones
- **Cifrado en reposo:** AES-256-GCM para almacenamiento de vectores faciales
- **Gestión de claves:** AWS KMS / Azure Key Vault con rotación automática cada 90 días
- **Hashing criptográfico:** SHA-256 para verificación de integridad de consentimientos
- **Aislamiento de datos:** Arquitectura multi-tenant con segregación por usuario
- **Monitoreo 24/7:** SIEM (Security Information and Event Management) con alertas en tiempo real

### 13.2 Seguridad Administrativa
- **Capacitación obligatoria:** Todo el personal con acceso a datos personales recibe entrenamiento anual en LFPDPPP
- **Políticas de acceso:** Principio de mínimo privilegio (least privilege)
- **Acuerdos de confidencialidad:** Todos los empleados y proveedores firman NDAs específicos
- **Auditorías internas:** Revisiones trimestrales de cumplimiento normativo
- **Designación formal:** Oficial de Protección de Datos (DPO) con reporte directo a dirección general

### 13.3 Seguridad Física
- **Datacenters certificados:** [PENDIENTE - ISO 27001, SOC 2 Type II, etc.]
- **Control de acceso biométrico:** A instalaciones críticas de procesamiento
- **Videovigilancia:** 24/7 en perímetros de seguridad
- **Respaldo geográficamente distribuido:** Backups en mínimo 2 ubicaciones físicas separadas

### 13.4 Respuesta a Incidentes
Contamos con un **Plan de Respuesta a Brechas de Seguridad** que incluye:
1. Detección y contención en <1 hora
2. Notificación a titulares afectados en <72 horas (conforme mejores prácticas GDPR)
3. Notificación al INAI cuando proceda
4. Remediación y análisis forense
5. Reporte público de transparencia (si la brecha afecta >1000 usuarios)

---

## 14. USO DE COOKIES Y TECNOLOGÍAS DE RASTREO

### 14.1 Tipos de Cookies Utilizadas
Nuestro sitio web y aplicaciones utilizan las siguientes tecnologías:

1. **Cookies esenciales (estrictamente necesarias):**
   - Gestión de sesiones (session_id)
   - Autenticación (auth_token)
   - No requieren consentimiento (necesarias para el servicio)

2. **Cookies de rendimiento:**
   - Google Analytics (para métricas de uso agregadas)
   - Requieren consentimiento

3. **Cookies de funcionalidad:**
   - Preferencias de idioma
   - Configuración de UI
   - Requieren consentimiento

### 14.2 Gestión de Cookies
Usted puede controlar cookies mediante:
- **Banner de consentimiento:** Al primera visita, puede aceptar/rechazar cookies no esenciales
- **Panel de preferencias:** Configuración > Privacidad > Gestión de Cookies
- **Configuración del navegador:** Puede bloquear cookies desde su navegador (puede afectar funcionalidad)

### 14.3 Cookies de Terceros
Solo utilizamos cookies de terceros con su consentimiento:
- **Google Analytics:** [Política de privacidad](https://policies.google.com/privacy)
- **[PENDIENTE - Otros proveedores si aplica]**

### 14.4 Almacenamiento Local (LocalStorage/IndexedDB)
Para procesamiento on-device almacenamos temporalmente:
- Modelos de ML para liveness detection (solo en su dispositivo)
- Caché de embeddings para autenticación offline
- Estos datos se eliminan al cerrar sesión o desinstalar la app

---

## 15. CAMBIOS AL AVISO DE PRIVACIDAD

### 15.1 Derecho de Modificación
Nos reservamos el derecho de modificar este Aviso de Privacidad para:
- Cumplir cambios legislativos o regulatorios
- Implementar nuevas medidas de seguridad
- Adaptar el aviso a nuevas funcionalidades del servicio

### 15.2 Mecanismo de Notificación
Cualquier cambio será notificado mediante:

1. **Publicación en sitio web:** [PENDIENTE - URL del aviso]
2. **Email a usuarios registrados:** Con 10 días hábiles de anticipación
3. **Notificación in-app:** Banner destacado al iniciar sesión
4. **Historial de versiones:** Disponible en [PENDIENTE - URL changelog]

### 15.3 Cambios Sustanciales
Si los cambios afectan significativamente:
- El tratamiento de datos biométricos
- Las finalidades del tratamiento
- Las transferencias internacionales
- Los derechos de los titulares

**Se solicitará NUEVO CONSENTIMIENTO EXPRESO** mediante el mecanismo descrito en la sección 4.2.

### 15.4 Control de Versiones
Cada versión del aviso incluye:
- Número de versión semántico (X.Y - mayor.menor)
- Fecha de publicación
- Resumen de cambios (changelog)
- Hash SHA-256 para verificación de autenticidad

**Versión actual:** 1.0 | **Hash:** [PENDIENTE - Se genera al publicar]

---

## 16. AUTORIDAD DE PROTECCIÓN DE DATOS

### 16.1 INAI - Instituto Nacional de Transparencia, Acceso a la Información y Protección de Datos Personales

Si considera que su derecho a la protección de datos personales ha sido vulnerado, puede acudir al INAI:

- **Sitio web:** [https://home.inai.org.mx](https://home.inai.org.mx)
- **Teléfono:** 800 835 43 24 (lada sin costo)
- **Email:** [email protected]
- **Domicilio:** Insurgentes Sur 3211, Col. Insurgentes Cuicuilco, Alcaldía Coyoacán, C.P. 04530, Ciudad de México

### 16.2 Procedimiento de Protección de Derechos
Conforme a los artículos 45 a 51 de la LFPDPPP, puede iniciar un procedimiento de protección de derechos ante el INAI cuando:
- El Responsable no responda su solicitud ARCO en plazo
- Se niegue injustificadamente a dar trámite a su solicitud
- La respuesta no satisfaga su solicitud

**Requisitos:** Presentar escrito libre o formato disponible en el sitio del INAI, anexando evidencia de la solicitud original.

---

## 17. CONSENTIMIENTO

### 17.1 Declaración de Consentimiento Informado

Al marcar la casilla de aceptación y/o firmar electrónicamente, **DECLARO QUE:**

1. ✓ He leído íntegramente el presente Aviso de Privacidad
2. ✓ Entiendo la naturaleza sensible de los datos biométricos que proporciono
3. ✓ Comprendo las finalidades para las cuales se tratarán mis datos personales
4. ✓ Conozco mis derechos ARCO y los mecanismos para ejercerlos
5. ✓ Entiendo que puedo revocar mi consentimiento en cualquier momento
6. ✓ Estoy consciente del periodo de retención de 24 horas (salvo extensión opt-in)
7. ✓ Acepto las transferencias de datos descritas en la sección 7

### 17.2 Consentimiento Expreso para Datos Biométricos

**OTORGO MI CONSENTIMIENTO EXPRESO, INFORMADO E INEQUÍVOCO** para que [PENDIENTE - Nombre del Responsable] trate mis datos biométricos (vectores faciales, parámetros de liveness detection) conforme a este Aviso de Privacidad.

### 17.3 Consentimientos Opcionales (Finalidades Secundarias)

☐ **Acepto recibir comunicaciones de marketing** sobre nuevos servicios y actualizaciones
☐ **Autorizo el uso de mis datos anonimizados** para mejora de algoritmos de ML
☐ **Consiento extender el periodo de retención** a [seleccionar: 30 días / 90 días / indefinido]

### 17.4 Registro de Consentimiento

Al completar el proceso de registro, se generará automáticamente un **Certificado de Consentimiento** con los siguientes datos:

```json
{
  "user_id": "UUID único",
  "timestamp": "2025-10-29T14:32:15.782Z",
  "ip_address": "192.0.2.1",
  "device_id": "hash del dispositivo",
  "privacy_notice_version": "1.0",
  "privacy_notice_hash": "SHA-256 del documento",
  "consent_signature": "firma electrónica ECDSA",
  "optional_consents": {
    "marketing": false,
    "ml_training": false,
    "extended_retention": null
  }
}
```

Este certificado está disponible para descarga en cualquier momento desde su panel de usuario.

---

## ANEXO A: DEFINICIONES TÉCNICAS

Para mayor claridad, se definen los siguientes términos técnicos:

- **Embedding / Vector facial:** Representación matemática de características faciales en un espacio vectorial de N dimensiones (típicamente 128-512 dimensiones), generada mediante redes neuronales convolucionales (CNN). No permite reconstruir la imagen original.

- **Liveness detection:** Técnica anti-spoofing que verifica que la captura biométrica proviene de una persona viva presente, no de fotografías, videos o máscaras 3D.

- **On-device processing:** Procesamiento realizado localmente en el dispositivo del usuario (smartphone/tablet/PC) sin transmisión inmediata de datos en crudo a servidores remotos.

- **Cifrado end-to-end:** Cifrado de datos desde el dispositivo de origen hasta el destino final, sin descifrado intermedio en servidores de tránsito.

- **Hash SHA-256:** Función criptográfica de una vía que genera una huella digital única de 256 bits. Cualquier cambio mínimo en el documento original produce un hash completamente diferente.

- **Anonimización irreversible:** Proceso mediante el cual los datos personales se transforman de tal manera que ya no pueden vincularse a una persona identificable, ni siquiera utilizando información adicional.

---

## ANEXO B: PLAZOS LEGALES (REFERENCIA RÁPIDA)

| Acción | Plazo Legal |
|--------|-------------|
| Respuesta a solicitud ARCO | 20 días hábiles |
| Implementación de ARCO procedente | 15 días hábiles tras notificación |
| Retención default de datos biométricos | 24 horas |
| Notificación de cambios sustanciales | 10 días hábiles previos |
| Conservación de logs de auditoría | 12 meses |
| Conservación de datos fiscales | 10 años (CFF) |

---

## ANEXO C: CONTACTOS CLAVE

| Departamento | Contacto | Horario |
|--------------|----------|---------|
| Protección de Datos | [PENDIENTE - privacidad@facecode.com] | L-V 9:00-18:00 |
| Soporte Técnico | [PENDIENTE - soporte@facecode.com] | 24/7 |
| Oficial de Seguridad | [PENDIENTE - security@facecode.com] | L-V 9:00-18:00 |
| Relaciones con Autoridades | [PENDIENTE - legal@facecode.com] | L-V 9:00-17:00 |

---

## CONTROL DE CAMBIOS

| Versión | Fecha | Cambios Realizados | Autor |
|---------|-------|-------------------|-------|
| 1.0 | [PENDIENTE] | Versión inicial conforme LFPDPPP 2025 | [PENDIENTE] |
|  |  |  |  |

---

**ÚLTIMA ACTUALIZACIÓN:** [PENDIENTE - Fecha de publicación]
**FECHA DE VIGENCIA:** [PENDIENTE - Fecha de entrada en vigor]

---

*Este documento ha sido elaborado conforme a la Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP), su Reglamento y los Lineamientos del Aviso de Privacidad emitidos por el INAI. Se recomienda validación final con asesor legal especializado en protección de datos antes de su publicación.*

**[PENDIENTE - FIRMA DIGITAL DEL REPRESENTANTE LEGAL]**
