help:
	@echo Dealscan Make commands
	@echo `make format`             - format codebase
	@echo `make lint`               - check code
	@echo `make migrations`         - make migrations
	@echo `make migrate`            - migrate
	@echo `make tailwind-watcher`   - run tailwind watcher

# Database

migrations:
	@echo Making migrations...
	poetry run python manage.py makemigrations --noinput

migrate:
	@echo Migrating...
	poetry run python manage.py migrate --noinput

# Static

collectstatic:
	@echo Collecting static...
	poetry run python manage.py collectstatic

# Tailwind

tailwind-watcher:
	@echo Running watcher...
	npx tailwindcss -i ./accounts/static/src/input.css -o ./static/src/output.css --watch

# Lint

format:
	@echo Formatting codebase...
	poetry run black .
	poetry run isort .

lint:
	@echo Linting...
	poetry run flake8 . 
	poetry run black . --check 
	poetry run isort . --check-only 
	poetry run mypy .

.PHONY: help format lint migrations migrate