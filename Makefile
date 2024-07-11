dev-up:
	docker-compose up -d

dev-build:
	docker-compose up --build

dev-down:
	docker-compose down

dev-down-v:
	docker-compose down -v

dev-logs:
	docker-compose logs -f

init-db:
	python3 init.py

makemigration:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

set-up:
	make makemigration
	make migrate
	make init-db