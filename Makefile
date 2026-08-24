.PHONY: help build up down restart logs shell-backend shell-frontend migrate makemigrations createsuperuser test clean

help:
	@echo "MatchMind AI - Development Commands"
	@echo "===================================="
	@echo ""
	@echo "Setup & Build:"
	@echo "  make setup          - Initial project setup"
	@echo "  make build          - Build Docker images"
	@echo ""
	@echo "Services:"
	@echo "  make up             - Start all services"
	@echo "  make down           - Stop all services"
	@echo "  make restart        - Restart all services"
	@echo "  make logs           - View all logs"
	@echo "  make logs-backend   - View backend logs"
	@echo "  make logs-frontend  - View frontend logs"
	@echo ""
	@echo "Database:"
	@echo "  make migrate        - Run migrations"
	@echo "  make makemigrations - Create new migrations"
	@echo "  make createsuperuser - Create Django superuser"
	@echo "  make db-shell       - Access PostgreSQL shell"
	@echo ""
	@echo "Development:"
	@echo "  make shell-backend  - Access backend shell"
	@echo "  make shell-frontend - Access frontend shell"
	@echo "  make test           - Run tests"
	@echo "  make test-backend   - Run backend tests"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Remove containers and volumes"
	@echo ""

setup:
	@bash scripts/setup.sh

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started!"
	@echo "Frontend: http://localhost:5173"
	@echo "Backend API: http://localhost:8000/api"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

shell-backend:
	docker-compose exec backend bash

shell-frontend:
	docker-compose exec frontend sh

migrate:
	docker-compose exec backend python manage.py migrate

makemigrations:
	docker-compose exec backend python manage.py makemigrations

createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

db-shell:
	docker-compose exec db psql -U matchmind -d matchmind_db

test:
	@echo "Running all tests..."
	@make test-backend

test-backend:
	docker-compose exec backend pytest

clean:
	docker-compose down -v
	@echo "⚠️  All containers and volumes removed!"
