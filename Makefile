all: clean deps

deps:
	pip install -Ur requirements_dev.txt

clean:
	find . -name "*.py[co]" -delete

test: clean integrations

unit:
	nosetests

integrations:
	nosetests --logging-level=ERROR -a slow --with-coverage --cover-package=flow --with-xunit
