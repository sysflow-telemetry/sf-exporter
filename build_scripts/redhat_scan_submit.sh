#!/bin/bash
# Submit an image to RedHat Sysfow Exporter Jobs for certification
# Usage: redhat_scan_submit.sh [login secret] [image_to_be_scanned] [RedHat project ID] [container label]
set -e

docker build --build-arg VERSION=test --build-arg RELEASE=$(git rev-parse --short HEAD) -t sf-exporter-runtime .
docker login -u unused -p $1 scan.connect.redhat.com

docker tag $(docker images sf-exporter-runtime -q) scan.connect.redhat.com/ospid-0597582f-0fe8-4fdc-b141-d20cc8a67f41/test:$1
docker push scan.connect.redhat.com/ospid-0597582f-0fe8-4fdc-b141-d20cc8a67f41/test:$1

docker rmi scan.connect.redhat.com/ospid-0597582f-0fe8-4fdc-b141-d20cc8a67f41/test:$1
docker rmi sf-exporter-runtime
docker image prune -f


