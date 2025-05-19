clean:
	sudo find . -name "*.pyc" -delete
	sudo find . -name "*.pyo" -delete

set-up: clean
	pip install -r requirements.txt

update-requirements:
	pip freeze > requirements.txt

setup: clean
	pip install -r requirements.txt

start-server: clean
	python manage.py runserver

superuser: clean
	python manage.py createsuperuser2

start-db:
	sudo docker compose -f .docker/docker-compose.yml up -d --build

migrations: clean
	python manage.py makemigrations

migrate: clean
	python manage.py migrate



# Tests
coverage: clean
	pytest -v --disable-warnings --cov
	
pytest: clean
	pytest -v --disable-warnings

test: clean
	python manage.py test --settings=setup.django.test