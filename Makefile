.PHONY: help install install-dev clean lint format test coverage docs build publish

help:  ## Show this help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install:  ## Install package and dependencies
	pip install -e .

install-dev:  ## Install package and development dependencies
	pip install -e ".[dev]"
	pre-commit install

clean:  ## Clean up build and temporary files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf .mypy_cache
	rm -rf .tox
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:  ## Run code linting
	pylint src/youtube_processor tests
	mypy src/youtube_processor tests
	black --check src/youtube_processor tests
	isort --check-only src/youtube_processor tests

format:  ## Format code
	black src/youtube_processor tests
	isort src/youtube_processor tests

test:  ## Run tests
	pytest -v tests/

coverage:  ## Run tests with coverage report
	pytest --cov=youtube_processor --cov-report=term-missing --cov-report=html tests/

test-watch:  ## Run tests in watch mode
	ptw --nobeep

check: clean lint test  ## Run all checks (clean, lint, test)

run:  ## Run the CLI application
	python -m youtube_processor.cli

build: clean  ## Build package
	python -m build

publish: build  ## Publish package to PyPI
	twine upload dist/*

setup-dev: install-dev  ## Set up development environment
	@echo "Creating config directory..."
	mkdir -p config
	@echo "Setting up pre-commit hooks..."
	pre-commit install
	@echo "Development environment setup complete!"

update-deps:  ## Update dependencies
	pip-compile --upgrade
	pip-compile --upgrade requirements-dev.in

# Directory creation
init:  ## Initialize project directories
	@echo "Creating project directories..."
	mkdir -p config
	mkdir -p docs
	mkdir -p src/youtube_processor/core
	mkdir -p tests
	@echo "Project structure created!"

# Credential management
setup-credentials:  ## Set up YouTube API credentials
	@echo "Setting up YouTube API credentials..."
	python -m youtube_processor.cli configure

# Working directory management
clean-work:  ## Clean working directories
	@echo "Cleaning work directories..."
	rm -rf work/*
	rm -rf downloads/*

# Docker support (if needed)
docker-build:  ## Build Docker image
	docker build -t youtube-processor .

docker-run:  ## Run Docker container
	docker run -it --rm youtube-processor

# Documentation
docs:  ## Generate documentation
	@echo "Generating documentation..."
	pdoc --html --output-dir docs/ src/youtube_processor
	@echo "Documentation generated in docs/"

docs-serve:  ## Serve documentation locally
	pdoc --http : src/youtube_processor

# Version management
bump-version:  ## Bump version number
	@echo "Current version: $$(grep -E '^version = ' pyproject.toml | cut -d'"' -f2)"
	@read -p "New version: " version; \
	sed -i "s/^version = .*/version = \"$$version\"/" pyproject.toml

# Git helpers
tag-release:  ## Create and push a new tag
	@echo "Current version: $$(grep -E '^version = ' pyproject.toml | cut -d'"' -f2)"
	@read -p "Tag name (e.g., v1.0.0): " tag; \
	git tag -a $$tag -m "Release $$tag" && \
	git push origin $$tag
