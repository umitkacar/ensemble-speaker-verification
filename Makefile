.PHONY: help install dev-install test lint format clean docs

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install the package
	pip install .

dev-install: ## Install development dependencies
	pip install -e ".[dev,viz,audio]"
	pre-commit install

test: ## Run tests
	hatch run test

test-cov: ## Run tests with coverage
	hatch run test-cov

lint: ## Run linters
	hatch run lint

format: ## Format code
	hatch run format

format-check: ## Check code formatting
	hatch run format-check

type-check: ## Run type checking
	hatch run type-check

all-checks: ## Run all checks (format, lint, type-check, test)
	hatch run all

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs: ## Build documentation
	hatch run docs:build

docs-serve: ## Serve documentation locally
	hatch run docs:serve

build: ## Build distribution packages
	hatch build

publish-test: ## Publish to TestPyPI
	hatch publish -r test

publish: ## Publish to PyPI
	hatch publish

pre-commit: ## Run pre-commit on all files
	pre-commit run --all-files

update-deps: ## Update dependencies
	pip install --upgrade pip hatch pre-commit
	pre-commit autoupdate

run-cli: ## Run CLI help
	hatch run speech-verify --help

example-verify: ## Run example verification
	hatch run speech-verify verify ./examples/speaker1.wav ./examples/speaker2.wav
