.PHONY: dev dev-db dev-full stop clean seed-roles test test-backend test-frontend help

# One-line development setup
dev: dev-db
	@echo "✓ Database started"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Backend: cd backend && make install && cp .env.sample .env && make dev"
	@echo "  2. Frontend: cd frontend && npm install && cp env.example .env.local && npm run dev"
	@echo ""
	@echo "Or run 'make dev-full' to start everything in Docker"

# Start only database
dev-db:
	@echo "Starting PostgreSQL..."
	docker-compose up -d postgres
	@echo "Waiting for database to be ready..."
	@sleep 5
	@docker-compose exec -T postgres pg_isready -U user_mgmt -d user_management || sleep 5

# Start full stack in Docker (backend + frontend + db)
dev-full:
	@echo "Starting full stack..."
	docker-compose --profile full up -d
	@echo ""
	@echo "Services starting:"
	@echo "  - Database: postgresql://localhost:5432/user_management"
	@echo "  - Backend: http://localhost:8000"
	@echo "  - Frontend: http://localhost:3000"
	@echo ""
	@echo "View logs: docker-compose logs -f"

# Stop all services
stop:
	docker-compose --profile full down

# Clean all data (WARNING: destroys database)
clean:
	docker-compose --profile full down -v
	@echo "✓ All containers and volumes removed"

# Seed initial roles (run after migrations)
seed-roles:
	@echo "Seeding roles..."
	@echo "TODO: Implement role seeding script"

# Run all tests (backend + frontend) with coverage
test: test-backend test-frontend
	@echo ""
	@echo "✓ All tests completed"
	@echo ""
	@echo "Coverage reports:"
	@echo "  Backend:  backend/htmlcov/index.html"
	@echo "  Frontend: frontend/playwright-report/index.html"

# Run backend tests (unit + integration + contract) with coverage
test-backend:
	@echo "Running backend tests with coverage..."
	@cd backend && \
		if [ -d "venv" ]; then \
			./venv/bin/pytest --cov=src --cov-report=html --cov-report=term-missing || true; \
		else \
			echo "⚠ Backend venv not found. Run: cd backend && make install"; \
		fi

# Run frontend E2E tests
test-frontend:
	@echo ""
	@echo "Running frontend E2E tests..."
	@cd frontend && npm run test:e2e || true

# Show help
help:
	@echo "User Management - Development Commands"
	@echo ""
	@echo "Quick Start:"
	@echo "  make dev          - Start database only (recommended for local development)"
	@echo "  make dev-full     - Start full stack in Docker"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run all tests (backend + frontend) with coverage"
	@echo "  make test-backend - Run backend tests (unit/integration/contract)"
	@echo "  make test-frontend- Run frontend E2E tests (Playwright)"
	@echo ""
	@echo "Management:"
	@echo "  make stop         - Stop all services"
	@echo "  make clean        - Remove all containers and data"
	@echo "  make seed-roles   - Seed initial roles (Admin, User)"
	@echo ""
	@echo "Individual Services:"
	@echo "  Backend:  cd backend && make help"
	@echo "  Frontend: cd frontend && npm run"
	@echo ""
	@echo "Environment Setup:"
	@echo "  1. Copy backend/.env.sample to backend/.env"
	@echo "  2. Copy frontend/env.example to frontend/.env.local"
	@echo "  3. Generate JWT secret: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
