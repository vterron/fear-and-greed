SHELL := /bin/bash

.PHONY: all

all: test

test:
	pytest --pyargs fear_and_greed -v
local:
	sam build && sam local invoke
deploy:
	sam deploy
