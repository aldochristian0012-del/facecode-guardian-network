# FaceCode Guardian Network - Makefile
# =====================================

.PHONY: help install test run docker-build docker-run clean

help: ## Muestra esta ayuda
	@echo "FaceCode Guardian Network - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependencias
	pip install -r requirements.txt

install-dev: ## Instala dependencias de desarrollo
	pip install -r requirements.txt
	pip install poetry
	poetry install

test: ## Ejecuta tests
	pytest tests/ -v --cov=facecode_guardian --cov-report=html

test-unit: ## Ejecuta solo tests unitarios
	pytest tests/unit/ -v

test-integration: ## Ejecuta solo tests de integración
	pytest tests/integration/ -v

lint: ## Ejecuta linters
	black src/ tests/ --check
	flake8 src/ tests/
	mypy src/

format: ## Formatea código
	black src/ tests/

run: ## Ejecuta el servidor en modo desarrollo
	python -m uvicorn src.facecode_guardian.main:app --reload --host 0.0.0.0 --port 8000

run-prod: ## Ejecuta el servidor en modo producción
	gunicorn src.facecode_guardian.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

docker-build: ## Construye imagen Docker
	docker build -t facecode-guardian:latest .

docker-run: ## Ejecuta contenedor Docker
	docker-compose up -d

docker-stop: ## Detiene contenedor Docker
	docker-compose down

docker-logs: ## Muestra logs del contenedor
	docker-compose logs -f

clean: ## Limpia archivos temporales
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true

audit-logs: ## Muestra logs de auditoría recientes
	tail -n 50 logs/audit/*.log 2>/dev/null || echo "No hay logs de auditoría aún"

health-check: ## Verifica salud del sistema
	curl -s http://localhost:8000/api/v1/health | python -m json.tool

api-docs: ## Abre documentación de la API
	@echo "Documentación disponible en:"
	@echo "  Swagger UI: http://localhost:8000/docs"
	@echo "  ReDoc:      http://localhost:8000/redoc"
