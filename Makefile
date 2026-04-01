.PHONY: help up down logs migrate shell test

help:
	@echo "Доступные команды:"
	@echo "  make up        - Запустить все сервисы"
	@echo "  make down      - Остановить все сервисы"
	@echo "  make logs      - Показать логи"
	@echo "  make migrate   - Применить миграции"
	@echo "  make shell     - Открыть shell в контейнере"
	@echo "  make test      - Запустить тесты"

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

migrate:
	docker-compose exec app alembic upgrade head

shell:
	docker-compose exec app bash

test:
	docker-compose exec app pytest
