set_env_vars := USER_NAME=$(shell id -un) USER_ID=$(shell id -u) GROUP_ID=$(shell id -g) GROUP_NAME=$(shell id -gn)

default: help

help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  up - Start the services"
	@echo "  logs - Follow the logs"
	@echo "  ps - List the services"
	@echo "  down - Stop the services"
	@echo "  restart - Restart the services"
	@echo "  reload - Rebuild containers and restart the services"
	@echo "  build - Build the services"
	@echo "  bash - Run a bash shell in the app container"
	@echo "  shell - Run a shell in the app container"
	@echo "  permission - Set permissions for the app container"
	@echo "  setup - Install dependencies"
	@echo "  login - Login to the app container"
	@echo "  cf-token-url - Open Cloudflare token creation page (Zone list + DNS edit)"
.PHONY: help

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

reload:
	$(set_env_vars) docker compose down && $(set_env_vars) docker compose up -d --build
.PHONY: reload

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

# ゾーン一覧取得・レコード更新用トークン作成ページを開く（zone read + zone_dns edit）
CF_TOKEN_URL := https://dash.cloudflare.com/profile/api-tokens?permissionGroupKeys=%5B%7B%22key%22%3A%22zone%22%2C%22type%22%3A%22read%22%7D%2C%7B%22key%22%3A%22zone_dns%22%2C%22type%22%3A%22edit%22%7D%5D&accountId=%2A&zoneId=all&name=Wrangler%20DNS%20Token

cf-token-url:
	@echo "Open: $(CF_TOKEN_URL)"
	@command -v xdg-open >/dev/null 2>&1 && xdg-open "$(CF_TOKEN_URL)" || \
	command -v open >/dev/null 2>&1 && open "$(CF_TOKEN_URL)" || \
	echo "Please open the URL above in your browser"
.PHONY: cf-token-url