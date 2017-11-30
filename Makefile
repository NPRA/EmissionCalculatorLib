# Makefile for the Emission library
# 
#
.PHONY: doc

default:
	@echo "Targets:"
	@echo " all:		test, bdist"
	@echo " bdist:		make .whl file for distribution"
	@echo " test:		run test suite"
	@echo " publish:	publish / distribute wheel package to PyPI"
	@echo " clean:		remove .pyc files, build, dist dirs"
	@echo " install:	install develop build of this module (development)"
	@echo " uninstall:	uninstall develop build of this module (development)"


test:
	py.test tests


# Install in develop mode
# (require setuptools)
install:
	python setup.py develop --no-deps

# Uninstall develop mode
uninstall:
	python setup.py develop --no-deps --uninstall

publish:
	python setup.py publish

bdist: build
	python setup.py bdist_wheel

build:
	python setup.py build

clean:
	rm -rf build
	rm -rf dist
	rm -rf emission/*.pyc

help: default
