.PHONY: test

default: test

build:
	docker build -t python-build-cli-planner-app .

test: build
	docker run -t python-build-cli-planner-app python -m pytest /app/tests/tests.py

start: build
	docker run -it python-build-cli-planner-app