### DATABASE
# ¯¯¯¯¯¯¯¯


database.connect: ## Connect to database
	docker compose exec db psql -Upostgres

database.migrate: ## Create alembic migration file
	docker compose run --rm server python src/manage.py db migrate

database.create: ## Create alembic creation file
	docker compose run --rm server python src/manage.py initialize_table

database.upgrade: ## Upgrade to latest migration
	docker compose run --rm server python src/manage.py db upgrade

database.downgrade: ## Downgrade latest migration
	docker compose run --rm server python src/manage.py db downgrade
