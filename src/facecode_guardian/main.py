"""
FaceCode Guardian Network - Servidor Principal
===============================================

API REST para reconocimiento facial ético con cumplimiento regulatorio.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

from .api import router
from .config import settings

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="""
    ## FaceCode Guardian Network API

    Sistema de reconocimiento facial ético con cumplimiento del **AI Act de la UE**.

    ### Características principales:
    - **Botón Ético Rojo**: Veto humano en tiempo real
    - **Detección de Bias**: Monitoreo activo de sesgos algorítmicos
    - **Auditoría Completa**: Registro de todas las operaciones
    - **Límites Éticos**: Anti-vigilancia masiva

    ### Cumplimiento regulatorio:
    - EU AI Act (Sistemas de Alto Riesgo)
    - GDPR (Datos Biométricos)
    - Directiva de Accesibilidad Europea (EAA)

    ### Endpoints principales:
    - `POST /api/v1/detect`: Detección facial con validación ética
    - `POST /api/v1/approve`: Botón Ético Rojo (aprobar/vetar)
    - `GET /api/v1/health`: Estado del sistema
    - `GET /api/v1/bias/report`: Reporte de equidad

    ---

    > © 2025 Christian - Fundador de FaceCode®
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "detection",
            "description": "Operaciones de detección facial"
        },
        {
            "name": "ethics",
            "description": "Botón Ético Rojo y controles humanos"
        },
        {
            "name": "monitoring",
            "description": "Monitoreo, auditoría y métricas"
        }
    ]
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(router, prefix=settings.API_PREFIX, tags=["facecode-guardian"])


@app.get("/", response_class=HTMLResponse)
async def root():
    """Página principal con información del sistema"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FaceCode Guardian Network</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }
            h1 { margin-top: 0; }
            .feature {
                background: rgba(255, 255, 255, 0.2);
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
            }
            .btn {
                display: inline-block;
                padding: 12px 24px;
                margin: 10px 5px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                text-decoration: none;
                color: white;
                font-weight: bold;
                transition: all 0.3s;
            }
            .btn:hover {
                background: rgba(255, 255, 255, 0.5);
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ FaceCode Guardian Network</h1>
            <p><strong>Protegiendo la dignidad digital mediante IA ética</strong></p>

            <div class="feature">
                <h3>✅ Sistema Activo</h3>
                <p>API de reconocimiento facial con cumplimiento del AI Act de la UE</p>
            </div>

            <div class="feature">
                <h3>🔴 Botón Ético Rojo</h3>
                <p>Veto humano en tiempo real - Control total sobre las decisiones algorítmicas</p>
            </div>

            <div class="feature">
                <h3>📊 Transparencia Total</h3>
                <p>Auditoría completa, detección de bias y métricas de equidad</p>
            </div>

            <div style="margin-top: 30px;">
                <a href="/docs" class="btn">📖 Documentación API</a>
                <a href="/api/v1/health" class="btn">💚 Estado del Sistema</a>
                <a href="/redoc" class="btn">📚 ReDoc</a>
            </div>

            <p style="margin-top: 30px; font-size: 0.9em; opacity: 0.8;">
                © 2025 Christian - Fundador de FaceCode®<br>
                Amigo del Mundo • Derecho a la dignidad digital
            </p>
        </div>
    </body>
    </html>
    """


@app.on_event("startup")
async def startup_event():
    """Evento al iniciar el servidor"""
    print("=" * 60)
    print("🛡️  FaceCode Guardian Network - Starting...")
    print("=" * 60)
    print(f"Version: {settings.API_VERSION}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"Red Button: {'ENABLED' if settings.REQUIRE_HUMAN_APPROVAL else 'DISABLED'}")
    print(f"Bias Detection: {'ENABLED' if settings.ENABLE_BIAS_DETECTION else 'DISABLED'}")
    print(f"Audit Logging: {'ENABLED' if settings.ENABLE_AUDIT_LOG else 'DISABLED'}")
    print("=" * 60)
    print(f"📖 Docs: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"💚 Health: http://{settings.HOST}:{settings.PORT}/api/v1/health")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Evento al detener el servidor"""
    print("\n🛑 FaceCode Guardian Network - Shutting down...")


def run_server():
    """Inicia el servidor uvicorn"""
    uvicorn.run(
        "facecode_guardian.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else settings.WORKERS
    )


if __name__ == "__main__":
    run_server()
