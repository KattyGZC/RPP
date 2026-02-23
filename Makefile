.PHONY: help dev prod build migrate seed test lint clean logs

# Default target
help:
	@echo "Read Praxis Project - Available commands:"
	@echo ""
	@echo "  make dev          Start development environment"
	@echo "  make prod         Start production environment"
	@echo "  make build        Build all Docker images"
	@echo "  make migrate      Run database migrations"
	@echo "  make seed         Populate database with sample data"
	@echo "  make test         Run all tests"
	@echo "  make lint         Run code linters"
	@echo "  make logs         Tail logs from all services"
	@echo "  make clean        Remove all containers, volumes and images"
	@echo "  make shell        Open Django shell"
	@echo "  make psql         Open PostgreSQL shell"

# Development
dev:
	@cp -n .env.example .env.dev 2>/dev/null || true
	docker compose -f docker-compose.dev.yml up

dev-detached:
	docker compose -f docker-compose.dev.yml up -d

# Production
prod:
	@cp -n .env.example .env 2>/dev/null || true
	docker compose up -d

# Build images
build:
	docker compose build
	docker compose -f docker-compose.dev.yml build

# Database
migrate:
	docker compose -f docker-compose.dev.yml exec backend python manage.py migrate

makemigrations:
	docker compose -f docker-compose.dev.yml exec backend python manage.py makemigrations

seed:
	docker compose -f docker-compose.dev.yml exec backend python manage.py seed_data

# Testing
test:
	docker compose -f docker-compose.dev.yml exec backend python manage.py test apps --verbosity=2

test-coverage:
	docker compose -f docker-compose.dev.yml exec backend coverage run manage.py test apps
	docker compose -f docker-compose.dev.yml exec backend coverage report

# Code quality
lint:
	docker compose -f docker-compose.dev.yml exec backend flake8 apps core config
	docker compose -f docker-compose.dev.yml exec backend isort --check-only apps core config

format:
	docker compose -f docker-compose.dev.yml exec backend isort apps core config
	docker compose -f docker-compose.dev.yml exec backend black apps core config

# Utilities
logs:
	docker compose -f docker-compose.dev.yml logs -f

shell:
	docker compose -f docker-compose.dev.yml exec backend python manage.py shell

psql:
	docker compose -f docker-compose.dev.yml exec postgres psql -U rpp_user -d rpp_db_dev

# Cleanup
clean:
	docker compose down -v --rmi local
	docker compose -f docker-compose.dev.yml down -v --rmi local
