DEVI_APIKEY             ?= ApiKey SU-XXX-XXX-XXX:XXXXXXXXX

DOCKER_PROJECT          := yssb-devi-reports
DOCKER_COMPOSE_PROJECT  := $(shell echo '$(DOCKER_PROJECT)' | sed -e 's/[^a-z0-9]//g')
DOCKER_COMPOSE_ENV      := 
DOCKER_COMPOSE          := $(DOCKER_COMPOSE_ENV) docker-compose -p '$(DOCKER_COMPOSE_PROJECT)'

# Shell settings
.POSIX: # Run in .POSIX conforming mode. Shell with -e flag (it fails immediately after the first error)
.ONESHELL:

define help
Usage: make <command>
  help:                    			Show this help information
  clean:                   			Clean the project
  test:                    			Pass unit tests
  develenv-up:             			Launch the development environment with a docker-compose
  develenv-sh:             			Open a shell in the development environment
  develenv-down:           			Stop the development environment
  devi-account:            			Add Devi account using the apikey with DEVI_APIKEY env var
  devi-reports:            			List the reports in Devi for this account
  devi-report-params:      			Execute the report fulfillment_params_requests
  devi-report-fulfillment:			Execute the report fulfillment_requests
  devi-report-fulfillment-taxid:	Execute the report fulfillment_requests_taxid
  devi-report-inquiring:   			Execute the report inquiring_requests
  devi-report-eufunds:     			Execute the report for european funds requests
  devi-report-changepkg:   			Execute the report for package change requests

endef
export help

check-%:
	@if [ -z '${${*}}' ]; then echo 'Environment variable $* not set' && exit 1; fi

.PHONY: help
help:
	@echo "$$help"

.PHONY: clean
clean:
	find . -name "*.pyc" -exec rm -f {} \;
	rm *.xlsx

.PHONY: test
test:
	$(info) 'Passing unit tests'
	python -m unittest discover

.PHONY: develenv-up
develenv-up:
	$(info) 'Launching the development environment'
	$(DOCKER_COMPOSE) up --build -d

.PHONY: develenv-sh
develenv-sh:
	$(DOCKER_COMPOSE) exec develenv bash

.PHONY: develenv-down
develenv-down:
	$(info) 'Shutting down the development environment'
	$(DOCKER_COMPOSE) down --remove-orphans

.PHONY: devi-account
devi-account: check-DEVI_APIKEY
	ccli account add "$(DEVI_APIKEY)"

.PHONY: devi-reports
devi-reports:
	ccli report list -d .

.PHONY: devi-report-params
devi-report-params:
	ccli report execute fulfillment_params_requests -d .

.PHONY: devi-report-fulfillment
devi-report-fulfillment:
	ccli report execute fulfillment_requests -d .

.PHONY: devi-report-fulfillment-taxid
devi-report-fulfillment-taxid:
	ccli report execute fulfillment_requests_taxid -d .

.PHONY: devi-report-inquiring
devi-report-inquiring:
	ccli report execute inquiring_requests -d .

.PHONY: devi-report-eufunds
devi-report-eufunds:
	ccli report execute european_funds_requests -d .

.PHONY: devi-report-changepkg
devi-report-changepkg:
	ccli report execute package_change_requests -d .

# Functions
info := @printf '\033[32;01m%s\033[0m\n'
