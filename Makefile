PROJECT_NAME = $(shell basename $(CURDIR))

.PHONY: install install-dev update freeze dev build run stop restart

install:
	@poetry install

install-dev:
	@poetry add --group dev -r .dev-requirements.txt

update:
	@poetry update

sync:
	@python bin/package_sync.py

freeze:
	@if [ -f requirements.txt ]; then rm -f requirements.txt; fi
	@poetry export --without dev --without-hashes -f requirements.txt --output requirements.txt
	@if [ -f requirements-dev.txt ]; then rm -f dev-requirements.txt; fi
	@poetry export --only dev --without-hashes -f requirements.txt --output requirements-dev.txt

clean:
	@if [ -f requirements.txt ]; then rm -f requirements.txt; fi
	@if [ -f requirements-dev.txt ]; then rm -f requirements-dev.txt; fi
	@find $(PROJECT_DIR) -name '__pycache__' -exec rm -rf {} \;

dev:
	PYTHONPATH=$(CURDIR) uvicorn $(PROJECT_NAME).main:app --host 0.0.0.0 --port 8000 --reload

run:
	@poetry run $(PROJECT_NAME)

# Docker targets (use PROJECT_NAME variable from .env)
docker-build:
	@poetry export -f requirements.txt --output requirements.txt
	./bin/env_utils.sh build

docker-run:
	./bin/env_utils.sh run

docker-stop:
	./bin/env_utils.sh stop

docker-restart:
	./bin/env_utils.sh restart

docker-remove:
	./bin/env_utils.sh remove

docker-delete:
	./bin/env_utils.sh delete

PROJECT_DIR := $(CURDIR)/axe_hack_city
PYTHON_FILES := $(shell find $(PROJECT_DIR) -name '*.py')

sort:
	isort $(PYTHON_FILES)

format:
	black $(PYTHON_FILES)

lint:
	pylint $(PYTHON_FILES)


add_imports:
	./bin/add_imports.sh $(PROJECT_DIR)

comment:
	./bin/add_filename_comment.sh $(PROJECT_DIR)


