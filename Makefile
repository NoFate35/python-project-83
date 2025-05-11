install:
	uv sync
	
dev:
	./build_dev.sh
	uv run flask --debug --app page_analyzer:app run --port 8000

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:8000 page_analyzer:app

build:
	./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app


test-coverage:
	uv run pytest --cov=page_analyzer --cov-report xml

lint:
	uv run flake8 page_analyzer

save:
	git add --all
	git commit
	git push


test:
	uv run pytest

