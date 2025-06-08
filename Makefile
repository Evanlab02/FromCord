.venv:
	uv venv

.PHONY: requirements
requirements:
	uv pip compile -o requirements.txt requirements.in

.PHONY: install
install: .venv
	uv pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf build dist formcord.spec fromcord.spec

.PHONY: build
build: clean
	pyinstaller src/main.py --onefile --name "fromcord" --add-data ".env:.env"
	rm -rf formcord.spec fromcord.spec
	chmod +x dist/fromcord

.PHONY: run
run: build
	./dist/fromcord

.PHONY: dev
dev:
	python -m src.main
