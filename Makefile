.PHONY: help dist

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Install
install-dev:
	@pip3.6 install -U pip pipenv && pipenv install --dev

# Test
lint:
	@python3.6 $(shell which pylint)  ./ridi_oauth2/ ./ridi_django_oauth2/ --rcfile=.pylintrc && flake8

test:
	@python3.6 runtests.py

# Release
dist:
	rm -rf ./dist
	python setup.py sdist

pypi-upload:
	twine upload dist/*

pypi-test-upload:
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*

release: dist pypi-upload
