upbuild: build up

up:
	docker-compose -f local1.yml up

build:
	docker-compose -f local1.yml build

run:
	docker-compose -f local1.yml run $(filter-out $@,$(MAKECMDGOALS))

restart:
	docker-compose -f local1.yml restart $(filter-out $@,$(MAKECMDGOALS))

shell:
	docker-compose -f local1.yml exec django /entrypoint python manage.py shell_plus

bash:
	docker-compose -f local1.yml exec django /entrypoint bash

down:
	docker-compose -f local1.yml down $(filter-out $@,$(MAKECMDGOALS))

destroy:
	docker-compose -f local1.yml down -v

createsuperuser:
	docker-compose -f local1.yml exec django /entrypoint python manage.py createsuperuser

makemigrations:
	docker-compose -f local1.yml run --rm django python manage.py makemigrations $(filter-out $@,$(MAKECMDGOALS))

migrate:
	docker-compose -f local1.yml run --rm django python manage.py migrate $(filter-out $@,$(MAKECMDGOALS))

urls:
	docker-compose -f local1.yml run django python manage.py show_urls

logs:
	docker-compose -f local1.yml logs -f $(filter-out $@,$(MAKECMDGOALS))

test:
	docker-compose -f local1.yml run --service-ports --rm django python manage.py test $(filter-out $@,$(MAKECMDGOALS))

debug:
	docker-compose -f local1.yml run --service-ports --rm $(filter-out $@,$(MAKECMDGOALS))

rm_pyc:
	find . -name '__pycache__' -name '*.pyc' | xargs rm -rf


test_local:
	docker-compose -f local1.yml exec django /entrypoint python manage.py test --settings=config.settings.test $(filter-out $@,$(MAKECMDGOALS))

stagingup:
	docker-compose -f staging.yml up -d --build
