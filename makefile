# Set more sensible defaults
SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
.DEFAULT_GOAL := help

ifeq ($(origin .RECIPEPREFIX), undefined)
  $(error This Make does not support .RECIPEPREFIX. Please use GNU Make 4.0 or later)
endif
.RECIPEPREFIX = >

init: ## crea la imagen de docker y corre el docker-compose
> @bash ./scripts/init.sh

run: ## Corre el proyecto
> @bash ./scripts/run.sh

stop: ## Para el docker-compose
> docker-compose down