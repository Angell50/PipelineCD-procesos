.PHONY: help install test coverage lint format clean all

help:
	@echo "Available commands:"
	@echo "  make install     - Install all dependencies"
	@echo "  make test        - Run tests with pytest"
	@echo "  make coverage    - Run tests with coverage report"
	@echo "  make lint        - Run all linting tools"
	@echo "  make format      - Format code with black and isort"
	@echo "  make clean       - Remove generated files"
	@echo "  make all         - Run format, lint, and test"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

test:
	pytest

coverage:
	pytest --cov=src --cov-report=html --cov-report=term-missing

lint:
	@echo "Running flake8..."
	flake8 src tests
	@echo "Running pylint..."
	pylint src
	@echo "Running mypy..."
	mypy src

format:
	@echo "Running black..."
	black src tests
	@echo "Running isort..."
	isort src tests

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

all: format lint test
	@echo "All checks passed!"

pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files
