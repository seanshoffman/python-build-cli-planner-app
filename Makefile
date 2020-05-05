.DEFAULT_GOAL := start

build:
	docker build -t python-build-cli-planner-app .

test: build
	docker run -t python-build-cli-planner-app pytest --verbose /app/tests/tests.py

start: build
	docker run -it python-build-cli-planner-app
