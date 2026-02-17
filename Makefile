PROJECT_NAME = $(shell basename $(CURDIR))
PROJECT_DIR := $(CURDIR)/axe_hack_city
PYTHON_FILES := $(shell find $(PROJECT_DIR) -name '*.py')
POETRY ?= $(HOME)/.local/bin/poetry

ifeq ($(wildcard $(POETRY)),)
POETRY := poetry
endif

.PHONY: install install-dev update sync freeze export-requirements clean dev run \
	docker-build docker-run docker-stop docker-restart docker-remove docker-delete \
	sort format lint add_imports comment

install:
	@$(POETRY) install

install-dev:
	@$(POETRY) add --group dev -r .dev-requirements.txt

update:
	@$(POETRY) update

sync:
	@$(POETRY) run python bin/package_sync.py

freeze:
	@$(POETRY) lock

# Optional compatibility export for tooling that still requires pip-style requirements files.
export-requirements:
	@$(POETRY) export --without dev --without-hashes -f requirements.txt --output requirements.txt
	@$(POETRY) export --only dev --without-hashes -f requirements.txt --output requirements-dev.txt

clean:
	@find $(PROJECT_DIR) -name '__pycache__' -exec rm -rf {} \;

dev:
	@$(POETRY) run uvicorn $(PROJECT_NAME).main:app --host 0.0.0.0 --port 8000 --reload

run:
	@$(POETRY) run $(PROJECT_NAME)

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
	@$(POETRY) run isort $(PYTHON_FILES)

format:
	@$(POETRY) run black $(PYTHON_FILES)

lint:
	@$(POETRY) run pylint $(PYTHON_FILES)

add_imports:
	./bin/add_imports.sh $(PROJECT_DIR)

comment:
	./bin/add_filename_comment.sh $(PROJECT_DIR)
