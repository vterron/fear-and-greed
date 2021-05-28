SHELL := /bin/bash

.PHONY: all test build clean push

all: test

test:
	tox
build:
	python3 -m build

clean:
	rm dist/ build/ -rfv

push:
	python3 -m twine upload --repository fear-and-greed --repository-url=https://upload.pypi.org/legacy/ --skip-existing dist/*
