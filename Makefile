install:
	uv sync
	
deva:
	./build_deva.sh
	uv run flask --debug --app page_analyzer:app run --port 8000
	

dev:
	./build_dev.sh
	uv run flask --debug --app page_analyzer:app run --port 8000
	

PORT ?= 8000
start:
	uv run gunicorn -t 180 -w 5 -b 0.0.0.0:8000 page_analyzer:app


build:
	./build.sh


test-coverage:
	uv run pytest --cov=page_analyzer --cov-report xml

lintf:
	uv run flake8 page_analyzer

lintr:
	uv run ruff check page_analyzer

save:
	git add --all
	git commit
	git push


test:
	uv run pytest

