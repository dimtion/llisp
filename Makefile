MODULES  = llisp tests
VENV = venv
PYTHON = python3

test:
	pytest tests/*.py

format:
	isort -rc $(MODULES)
	black .

lint:
	isort -rc --check-only $(MODULES)
	flake8
	mypy llisp

venv:
	virtualenv -p $(PYTHON) $(VENV)

install_dev: venv
	$(VENV)/bin/pip install -r requirements.txt

PHONY: format lint test install_dev
