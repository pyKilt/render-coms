
INVENV = $(shell python -c 'import sys; print ("1" if hasattr(sys, "real_prefix") else "0")')

virtualenv:
# ifeq ($(INVENV), 0)
# 	$(shell source ./bin/activate)
# endif
ifeq ($(INVENV), 1)
	@echo "virtualenv already active"
endif

install:
	pip install -r requirements.pip

up: install
	python server.py
