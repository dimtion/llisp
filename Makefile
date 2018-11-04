test:
	pytest tests.py

format:
	black *.py

lint:
	mypy main.py lbuiltins.py

PHONY: format lint test
