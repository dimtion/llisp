MODULES  = llisp tests
VENV = venv
PYTHON = python3

VENV_PYTHON ?= $(VENV)/bin/python

test:
	$(VENV_PYTHON) -m pytest --cov llisp tests/*.py

format:
	$(VENV_PYTHON) -m isort $(MODULES)
	$(VENV_PYTHON) -m black .

lint:
	$(VENV_PYTHON) -m flake8
	$(VENV_PYTHON) -m mypy llisp
	$(VENV_PYTHON) -m isort --check-only $(MODULES)
	$(VENV_PYTHON) -m black --check .

$(VENV):
	virtualenv -p $(PYTHON) $(VENV)

install_dev: $(VENV)
	$(VENV_PYTHON) -m pip install -r requirements.txt
	$(VENV_PYTHON) -m pre-commit install

PHONY: format lint test install_dev
