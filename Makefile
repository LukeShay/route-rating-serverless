TAG=sha-$(shell git rev-parse --short HEAD)$(shell git diff --quiet || echo ".uncommitted")
IMAGE_NAME=route-rating-serverless

.PHONY: default help lint format clean integration-tests deploy generate-secrets unit-tests integration-tests-remote smoke-test update-workflow

default: help

## display this help message
help:
	@awk '/^##.*$$/,/^[~\/\.a-zA-Z_-]+:/' $(MAKEFILE_LIST) | awk '!(NR%2){print $$0p}{p=$$0}' | awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' | sort

## cleans all temp files
clean:
	@rm -rf .pytest_cache test_output .coverage rli.egg-info .pytest_cache .scannerwork .serverless route-rating.log || exit 0

## lints the python files
lint: clean
	@black --check api/ tests/

## formats the python files
format: clean
	@black api/ tests/

## runs all unit tests
ut: clean
	@pytest --junitxml=./test_output/test-report.xml --cov=api --cov-report=xml:test_output/coverage.xml --cov-report=html:test_output/coverage tests

## runs the integration tests using yarn serverless local
it: clean
	@./tests/integration/test.sh test-local dev

## runs unit and integration tests
test: clean ut it

## runs the integration tests using yarn serverless on dev
itr: clean
	@./tests/integration/test.sh test-remote dev

## runs the integration tests using yarn serverless on prod
smoke-test: clean
	@./tests/integration/test.sh test-remote prod

## deploys local version to aws dev env
deploy: clean
	 @yarn serverless deploy -s dev --force

## updates the gh action workflow from the template
update-workflow: clean
	@./.github/convert.sh


