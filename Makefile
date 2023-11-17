help:
	@echo Dealscan Make commands
	@echo `make format` - format codebase
	@echo `make lint`   - check code
	@echo `make migrations`   - make migrations
	@echo `make migrate`   - migrate

# Database

migrations:
	@echo Making migrations...
	poetry run python manage.py makemigrations --noinput

migrate:
	@echo Migrating...
	poetry run python manage.py migrate --noinput

format:
	@echo Formatting codebase...
	poetry run black .
	poetry run isort .

lint:
	@echo Linting...
	poetry run flake8 . && black8 . --check && isort . --check-only && mypy .

.PHONY: help format lint migrations migrate