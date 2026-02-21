set_env_vars := USER_NAME=$(shell id -un) USER_ID=$(shell id -u) GROUP_ID=$(shell id -g) GROUP_NAME=$(shell id -gn)


init:
	$(set_env_vars) docker compose run --rm app uv sync
.PHONY: init
up:
	$(set_env_vars) docker compose up -d
.PHONY: up

logs:
	$(set_env_vars) docker compose logs -f
.PHONY: logs
ps:
	$(set_env_vars) docker compose ps
.PHONY: ps

down:
	$(set_env_vars) docker compose down --remove-orphans --rmi all
.PHONY: down
restart:
	$(set_env_vars) docker compose down && $(set_env_vars) docker compose up -d
.PHONY: restart

build:
	$(set_env_vars) docker compose build --no-cache
.PHONY: build

bash:
	$(set_env_vars) docker compose exec app bash
.PHONY: bash

shell:
	@echo "Running shell in app container"
	$(set_env_vars) docker compose run --rm app bash
.PHONY: run
permission:
	@echo "Setting permissions for app container"
	$(set_env_vars) docker compose run --rm app sudo chown ${USER_NAME} -R ~${USER_NAME}/.{local,cache,config}
.PHONY: permission

setup:
	$(set_env_vars) docker compose run --rm app npm install
.PHONY: setup

login:
	$(set_env_vars) docker compose exec app wrangler login --callback-host=0.0.0.0
.PHONY: login