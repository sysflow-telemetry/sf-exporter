#!/bin/bash
# Usage: cleanup image
docker rmi $1
docker image prune -f