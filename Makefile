MODULES  = llisp tests
VENV = venv
PYTHON = python3

test:
	pytest tests/*.py

format:
	isort -rc $(MODULES)
	black .

lint:
	flake8
	mypy llisp
	isort -rc --check-only $(MODULES)
	black --check .

venv:
	virtualenv -p $(PYTHON) $(VENV)

install_dev: venv
	$(VENV)/bin/pip install -r requirements.txt

PHONY: format lint test install_dev
