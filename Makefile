test:
	pytest tests.py

format:
	black *.py

lint:
	mypy main.py

PHONY: format lint test
