
install:
	pip install -r requirements.pip

up: install
	python server.py

.PHONY: install up
