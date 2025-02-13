poetry run python -m unittest discover

coverage erase
coverage run --source=app -m unittest discover
poetry run coverage report --fail-under=70
coverage html