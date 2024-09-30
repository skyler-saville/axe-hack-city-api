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
	@poetry export -f requirements.txt --output requirements.txt
	@poetry export -f requirements.txt --output .dev-requirements.txt --with-dev-dependencies

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
