.PHONY:

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

lint:
	@python3.6 $(shell which pylint)  ./oauth2_client/ ./django_oauth2_client/ --rcfile=.pylintrc && flake8

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
