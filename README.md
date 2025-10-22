# FaceCode® Guardian Network

> **Protegiendo la dignidad digital mediante IA ética, transparencia radical y cumplimiento regulatorio.**  
> Alineado con el **Reglamento de IA de la UE** y la **Directiva de Accesibilidad Europea (EAA)**.

![FaceCode Guardian Network](diagrams/system_architecture.png)

Este repositorio contiene la arquitectura conceptual, principios éticos y especificaciones técnicas del **FaceCode Guardian Network** —una infraestructura de gobernanza para sistemas de reconocimiento facial orientada a la protección de derechos humanos y la rendición de cuentas algorítmica.

## 🌐 Visión

Garantizar que toda implementación de FaceCode® incluya:
- **Botón Ético Rojo** (veto humano en tiempo real)
- **Transparencia por diseño**
- **Anti-bias activo**
- **Auditoría continua**

## 🧭 Componentes clave

- **Guardian Nodes**: Instancias autónomas que monitorean el uso de FaceCode®
- **Ethical Dashboard**: Visualización en tiempo real de métricas técnicas y éticas (compatible con Grafana/Notion)
- **Open Test Case Protocol**: Plantillas estandarizadas para pruebas públicas y auditables
- **Compliance Layer**: Mapeo automático a requisitos del AI Act y EAA

## 🚀 Quick Start

### Requisitos previos

- Node.js >= 18.0.0
- Cuenta en [Supabase](https://supabase.com)

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/aldochristian0012-del/facecode-guardian-network.git
cd facecode-guardian-network

# 2. Instalar dependencias
npm install

# 3. Configurar variables de entorno
cp .env.example .env
# Edita .env con tus credenciales de Supabase

# 4. Iniciar en modo desarrollo
npm run dev
```

### Configuración de Supabase

1. Crea un proyecto en [Supabase](https://app.supabase.com)
2. Obtén tus credenciales desde **Settings > API**
3. Añádelas a tu archivo `.env`:

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu_anon_key_aqui
SUPABASE_SERVICE_KEY=tu_service_role_key_aqui
```

Ver guía completa: [📖 Configuración de Supabase](docs/SUPABASE_SETUP.md)

## 📂 Documentación

### Guías de configuración
- [🔧 Configuración de Supabase](docs/SUPABASE_SETUP.md)

### Principios y especificaciones
- [⚖️ Principios éticos](docs/ethical_principles.md)
- [📘 Guía para implementadores](docs/implementation_guide.md) *(próximamente)*
- [✅ Plantilla de Caso de Prueba Abierto](docs/open_test_case_template.md) *(próximamente)*

## 🖼 Diagrama de arquitectura

El diagrama fuente está en [`diagrams/system_architecture.mmd`](diagrams/system_architecture.mmd) (formato Mermaid).  
Puedes editarlo en [Mermaid Live Editor](https://mermaid.live).

![Arquitectura del Guardian Network](https://img.shields.io/badge/Mermaid-Compatible-brightgreen)

## 📜 Licencia

Este proyecto se distribuye bajo la **Licencia Ética FaceCode® v1.0**, que prioriza el uso humano, no discriminatorio y alineado con los derechos fundamentales.  
Ver [`LICENSE.md`](LICENSE.md).

---

> **© 2025 Christian — Fundador de FaceCode®**  
> *Amigo del Mundo • Derecho a la dignidad digital*

