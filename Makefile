TAG=sha-$(shell git rev-parse --short HEAD)$(shell git diff --quiet || echo ".uncommitted")

.PHONY: default help lint format clean integration-test deploy generate-secrets

default: help

## display this help message
help:
	@awk '/^##.*$$/,/^[~\/\.a-zA-Z_-]+:/' $(MAKEFILE_LIST) | awk '!(NR%2){print $$0p}{p=$$0}' | awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' | sort

## lints the python files
lint:
	@black --check rli/ tests/

## formats the python files
format:
	@black api/ tests/

## runs all tests
test:
	@pytest --junitxml=./test_output/test-report.xml --cov=api --cov-report=xml:test_output/coverage.xml --cov-report=html:test_output/coverage tests

## cleans all temp files
clean:
	@rm -rf .pytest_cache test_output .coverage rli.egg-info .pytest_cache .scannerwork

## initializes the repo for development
init:
	@./scripts/init.sh

## runs the integration smoke test
integration-test:
	@./scripts/integration_test.sh

## deploys local version to aws dev env
deploy: generate-secrets
	@serverless deploy

## creates the secrets.json file
generate-secrets:
	@echo "{'JWT_SECRET': '${JWT_SECRET}', 'REFRESH_SECRET': '${REFRESH_SECRET}'}" | sed "s/'/\"/g" | jq . > secrets.json
