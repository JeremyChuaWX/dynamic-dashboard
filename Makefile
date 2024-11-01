include .env
export

.PHONY: setup
setup:
	mkdir artifacts

.PHONY: migrate
migrate:
	docker compose up --build postgres.migrate -d
	docker compose wait postgres.migrate
	docker compose down --remove-orphans --volumes
	docker image prune -f

.PHONY: seed
seed:
	docker compose up --build postgres.seed -d
	docker compose wait postgres.seed
	docker compose down --remove-orphans --volumes
	docker image prune -f

.PHONY: ollama
ollama:
	ollama serve

.PHONY: start
start:
	docker compose up --build app

.PHONY: stop
stop:
	docker compose down --remove-orphans --volumes
	docker image prune -f
