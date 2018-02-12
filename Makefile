
INVENV = $(shell python -c 'import sys; print ("1" if hasattr(sys, "real_prefix") else "0")')

virtualenv:
ifeq ($(INVENV), 0)
	@echo "must run under virtualenv: \033[92msource virtualenv.sh\033[0m"
	@exit 1
endif

install: virtualenv
	pip install -r requirements.pip

up: install
	python server.py

.PHONY: install up virtualenv
