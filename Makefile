.PHONY: setup
setup:
	mkdir artifacts

.PHONY: migrate
migrate:
	docker compose up --build database.migrate -d
	docker compose wait database.migrate
	docker compose down --remove-orphans --volumes
	docker image prune -f

.PHONY: seed
seed:
	docker compose up --build database.seed -d
	docker compose wait database.seed
	docker compose down --remove-orphans --volumes
	docker image prune -f
