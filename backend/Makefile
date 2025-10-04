.PHONY: install dev lint format type-check test clean setup help

# Install dependencies
install:
	pip install -r requirements-dev.txt

# Run development server
dev:
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Creating one..."; \
		python3.11 -m venv venv; \
		echo "Installing dependencies..."; \
		./venv/bin/pip install -r requirements-dev.txt; \
	fi
	@if [ ! -f ".env" ]; then \
		echo "Creating .env file from .env.sample..."; \
		cp .env.sample .env; \
		echo "✓ .env file created. Please update with your configuration."; \
	fi
	@echo "Starting FastAPI server on http://localhost:8000"
	./venv/bin/uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Run linter (zero-error policy)
lint:
	ruff check .

# Auto-fix linting issues
lint-fix:
	ruff check --fix .

# Format code
format:
	black .

# Check formatting
format-check:
	black --check .

# Type checking
type-check:
	mypy src/

# Run all quality checks
validate: type-check lint format-check
	@echo "✓ All quality checks passed"

# Run tests
test:
	pytest

# Run tests with coverage
test-cov:
	pytest --cov=src --cov-report=html --cov-report=term

# Setup environment (one-time)
setup:
	@echo "Setting up backend environment..."
	@if [ ! -d "venv" ]; then \
		echo "Creating virtual environment..."; \
		python3.11 -m venv venv; \
	fi
	@echo "Installing dependencies..."
	./venv/bin/pip install -r requirements-dev.txt
	@if [ ! -f ".env" ]; then \
		echo "Creating .env file..."; \
		cp .env.sample .env; \
		echo "✓ .env file created"; \
	fi
	@echo ""
	@echo "✓ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Update .env with your configuration"
	@echo "  2. Run 'make dev' to start the server"

# Clean build artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov dist build

# Show help
help:
	@echo "Backend Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup       - One-time setup (venv + dependencies + .env)"
	@echo "  make install     - Install/update dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make dev         - Start development server (auto-creates .env)"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint        - Run linter (ruff)"
	@echo "  make lint-fix    - Auto-fix linting issues"
	@echo "  make format      - Format code (black)"
	@echo "  make format-check- Check code formatting"
	@echo "  make type-check  - Run type checker (mypy)"
	@echo "  make validate    - Run all quality checks"
	@echo ""
	@echo "Testing:"
	@echo "  make test        - Run tests"
	@echo "  make test-cov    - Run tests with coverage"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean       - Remove build artifacts"
