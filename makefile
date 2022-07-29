lint:
	flake8 --ignore=E402,E501,E712,W503,E203
	black --check .

format:
	black .
	isort .

refresh:
	python main.py run renew

update:
	python main.py run latest

shell:
	python manage.py shell