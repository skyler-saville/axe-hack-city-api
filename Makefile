PROJECT_NAME = $(shell basename $(CURDIR))
PROJECT_DIR := $(CURDIR)/axe_hack_city
PYTHON_FILES := $(shell find $(PROJECT_DIR) -name '*.py')

.PHONY: install install-dev update sync freeze export-requirements clean dev run \
	docker-build docker-run docker-stop docker-restart docker-remove docker-delete \
	sort format lint add_imports comment

install:
	@poetry install

install-dev:
	@poetry add --group dev -r .dev-requirements.txt

update:
	@poetry update

sync:
	@poetry run python bin/package_sync.py

freeze:
	@poetry lock

# Optional compatibility export for tooling that still requires pip-style requirements files.
export-requirements:
	@poetry export --without dev --without-hashes -f requirements.txt --output requirements.txt
	@poetry export --only dev --without-hashes -f requirements.txt --output requirements-dev.txt

clean:
	@find $(PROJECT_DIR) -name '__pycache__' -exec rm -rf {} \;

dev:
	@poetry run uvicorn $(PROJECT_NAME).main:app --host 0.0.0.0 --port 8000 --reload

run:
	@poetry run $(PROJECT_NAME)

# Docker targets (use PROJECT_NAME variable from .env)
docker-build:
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

sort:
	@poetry run isort $(PYTHON_FILES)

format:
	@poetry run black $(PYTHON_FILES)

lint:
	@poetry run pylint $(PYTHON_FILES)

add_imports:
	./bin/add_imports.sh $(PROJECT_DIR)

comment:
	./bin/add_filename_comment.sh $(PROJECT_DIR)
