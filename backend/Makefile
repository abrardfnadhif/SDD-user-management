.PHONY: install dev lint format type-check test clean

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

# Clean build artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov dist build
