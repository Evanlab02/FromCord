.PHONY: del-data
del-data:
	rm -rf data/*

.PHONY: clean
clean:
	rm -rf build fromcord.spec data dist

.venv:
	uv venv

data:
	mkdir -p data

.PHONY: requirements
requirements:
	uv pip compile -o requirements.txt requirements.in
	uv pip compile -o requirements.dev.txt requirements.dev.in

.PHONY: pyinstall
pyinstall:
	pyinstaller src/main.py --onefile --name "fromcord" --add-data ".env:.env"
	chmod +x dist/fromcord

.PHONY: install
install: .venv data
	uv pip install -r requirements.dev.txt

.PHONY: refresh
refresh: headless
	docker compose cp fromcord:/app/fromcord.spec ./fromcord.spec
	docker compose cp fromcord:/app/build/ .

.PHONY: dev
dev: .venv data
	python -m src.main

.PHONY: compose
compose: .venv data
	docker compose build

.PHONY: run
run: .venv data
	docker compose up

.PHONY: headless
headless: .venv data
	docker compose up -d

.PHONY: stop
stop:
	docker compose down

.PHONY: format
format:
	@black .
	@isort . --profile black

.PHONY: lint
lint:
	@black --check .
	@isort . --check-only --profile black
	@flake8 src/ --max-line-length=100
	@mypy src/ --strict

.PHONY: test
test:
	@pytest . --cov=. --no-cov-on-fail --cov-report term-missing
	@coverage xml
	@coverage html
