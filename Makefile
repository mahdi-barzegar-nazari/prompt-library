.PHONY: install lint format typecheck test check readme all

install:
	python -m pip install -e ".[dev]"

lint:
	ruff check .
	ruff format --check .

format:
	ruff check --fix .
	ruff format .

typecheck:
	mypy

test:
	python -m unittest discover -s tests -v

check:
	promptlint check

readme:
	promptlint sync-readme

all: lint typecheck test check
