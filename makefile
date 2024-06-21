SHELL=/bin/bash
export LAMBDA?=card_transactions
export REPO=lambda-${LAMBDA}
export ENV?=dev
export ECR_URL=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

VENV_NAME?=venv
VENV_ACTIVATE=$(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3
DOCKER_COMPOSE = docker-compose
COMPOSE_FILE_BACKEND = ./infraestructure/backend/docker-compose.yml
COMPOSE_FILE_FRONTEND = ./infraestructure/frontend/docker-compose.yml

.PHONY: build-frontend build-backend setup-backend setup-frontend docker-build docker-up terraform-init terraform-apply terraform-destroy
#docker-compose -f infraestructure/backend/docker-compose.yml run web sh

build-frontend:
	@echo "Building frontend...."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE_FRONTEND) build frontend

start-frontend:
	@echo "Running frontend...."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE_FRONTEND) up -d

stop-frontend:
	@echo "Stopping frontend...."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE_FRONTEND) down --rmi all --volumes --remove-orphans

build-backend:
	@echo "Building backend...."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE_BACKEND) build

start-backend:
	@echo "Running backend...."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE_BACKEND) up -d

stop-backend:
	@echo "Stopping backend...."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE_BACKEND) down --rmi all --volumes --remove-orphans

makemigrations-backend:
	@echo "Making migrations...."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE_BACKEND) run web python manage.py makemigrations

migrate-backend:
	@echo "Applying migrations...."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE_BACKEND) run web python manage.py migrate

create-superuser-backend:
	@echo "Creating superuser...."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE_BACKEND) run web python manage.py create_superuser

setup-backend: build-backend start-backend makemigrations-backend migrate-backend create-superuser-backend
	@echo "Backend setup complete."

collectstatic-backend:
	@echo "Collecting static files...."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE_BACKEND) run web python manage.py collectstatic --noinput

show-env-backend:
	@echo "Showing DJANGO_SETTINGS_MODULE environment variable..."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE_BACKEND) run web sh -c 'echo $$DJANGO_SETTINGS_MODULE'

test:
	@echo "Testing...."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE_BACKEND) run web sh -c 'PYTHONPATH=/app pytest --cov=core --cov-report=term-missing'

fast-lint:
	@bash ./scripts/fast-lint.sh

fast-lint-fix:
	@bash ./scripts/fast-lint.sh --fix

lint-fix:
	@( \
		black . --exclude=env; \
		isort --force-single-line-imports --quiet --apply -l=250 .; \
		autoflake --recursive --exclude venv --in-place --expand-star-imports --remove-all-unused-imports ./; \
		isort --quiet --apply .; \
	)
