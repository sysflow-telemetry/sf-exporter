#
# Copyright (C) 2020 IBM Corporation.
#
# Authors:
# Frederico Araujo <frederico.araujo@ibm.com>
# Teryl Taylor <terylt@ibm.com>
#

# Build environment configuration
include ./makefile.manifest.inc

.PHONY: all
all: docker-build

.PHONY: docker-build
docker-build:
	docker build -t sf-exporter --build-arg UBI_VER=$(UBI_VERSION) -f Dockerfile .
