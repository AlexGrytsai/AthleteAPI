poetry run python -m unittest discover

coverage erase
coverage run --source=app -m unittest discover
coverage html