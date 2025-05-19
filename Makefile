clean:
	sudo find . -name "*.pyc" -delete
	sudo find . -name "*.pyo" -delete

set-up: clean
	doppler run -- pip install -r requirements.txt

# DOPPLER COMMANDS
d-login:
	doppler login

d-setup:
	sudo doppler setup

update-requirements:
	pip freeze > requirements.txt

setup: clean
	pip install -r requirements.txt

server: clean
	doppler run -- python manage.py runserver

superuser: clean
	doppler run -- python manage.py createsuperuser2