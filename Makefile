# Makefile for the Emission library
# 
#
.PHONY: doc

default:
	@echo "Use target: test, install, uninstall, upload or clean"


test:
	py.test tests


# Install in develop mode
# (require setuptools)
install:
	python setup.py develop --no-deps

# Uninstall develop mode
uninstall:
	python setup.py develop --no-deps --uninstall

upload:
	python setup.py publish


clean:
	rm -rf build
	rm -rf dist
	rm -rf emission/*.pyc

help: default
