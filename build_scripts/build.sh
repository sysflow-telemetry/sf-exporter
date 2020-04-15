#!/bin/bash
# Usage: build.sh version release target-image[:tag]
docker build --build-arg VERSION=$1 --build-arg RELEASE=$2 -t $3 .