# SysFlow Exporter (sf-exporter repo)

SysFlow exporter to export SysFlow traces to S3-compliant object stores.

> Note: For remote syslogging and other export formats and connectors, check the [SysFlow processor](https://github.com/sysflow-telemetry/sf-processor) project.

## Build

This document describes how to build and run the application both inside a docker container and on a Linux host. Building and running the application inside a docker container 
is the easiest way to start. For convenience, skip the build step and pull pre-built images directly from Docker Hub.

To build the project, first clone the source code, with submodules:

```bash
git clone --recursive git@github.com:sysflow-telemetry/sf-exporter.git 
```

To checkout submodules on an already cloned repo:

```bash
git submodule update --init --recursive
```

To build the docker image for the exporter locally, run:

```bash
docker build -t sf-exporter . 
```

## Docker usage

The easiest way to run the SysFlow exporter is from a Docker container, with host mount for the trace files to export. The following command shows how to run sf-exporter with trace files located in `/mnt/data` on the host.

```bash
docker run -d --rm --name sf-exporter \
    -e S3_ENDPOINT=<ip_address> \
    -e S3_BUCKET=<bucket_name> \
    -e S3_ACCESS_KEY=<access_key> \
    -e S3_SECRET_KEY=<secret_key> \
    -e NODE_IP=$HOSTNAME \
    -e INTERVAL=150 \ 
    -v /mnt/data:/mnt/data \
    sysflowtelemetry/sf-exporter
```

It's also possible to read S3's keys as docker secrets `s3_access_key` and `s3_secret_key`. Instructions for `docker compose` and `helm` deployments are available in [here](https://sysflow.readthedocs.io/en/latest/deploy.html).

```bash
docker service create --name sf-exporter \
    -e NODE_IP=10.1.0.159 \
    -e INTERVAL=15 \
    --secret s3_access_key \
    --secret s3_secret_key \
    --mount type=bind,source=/mnt/data,destination=/mnt/data \
    sf-exporter:latest
```

The exporter is usually executed as a pod or docker-compose service together with the SysFlow collector. The exporter automatically removes exported files from the local filesystem it monitors. See the [SysFlow deployments](https://github.com/sysflow-telemetry/sf-deployments) packages for more information.

## Development

To build the exporter locally, run:

```bash
cd src & pip3 install -r requirements.txt
cd modules/sysflow/py3 & sudo python3 setup.py install
```

To run the exporter from the command line:

```bash
./exporter.py -h
usage: exporter.py [-h] [--exporttype {s3,local}] [--s3endpoint S3ENDPOINT]
                   [--s3port S3PORT] [--s3accesskey S3ACCESSKEY]
                   [--s3secretkey S3SECRETKEY] [--s3bucket S3BUCKET]
                   [--s3location S3LOCATION] [--s3prefix S3PREFIX]
                   [--secure [SECURE]] [--scaninterval SCANINTERVAL]
                   [--timeout TIMEOUT] [--agemin AGEMIN] [--dir DIR]
                   [--todir TODIR] [--nodename NODENAME] [--nodeip NODEIP]
                   [--podname PODNAME] [--podip PODIP]
                   [--podservice PODSERVICE] [--podns PODNS]
                   [--poduuid PODUUID] [--clusterid CLUSTERID]

sf-exporter: service for watching and uploading monitoring files to object
store.

optional arguments:
  -h, --help            show this help message and exit
  --exporttype {s3,local}
                        export type
  --s3endpoint S3ENDPOINT
                        s3 server address
  --s3port S3PORT       s3 server port
  --s3accesskey S3ACCESSKEY
                        s3 access key
  --s3secretkey S3SECRETKEY
                        s3 secret key
  --s3bucket S3BUCKET   target data bucket
  --s3location S3LOCATION
                        target data bucket location
  --s3prefix S3PREFIX   exporter's: static prefix directory for s3 bucket
  --secure [SECURE]     indicates if SSL connection
  --scaninterval SCANINTERVAL
                        interval between scans
  --timeout TIMEOUT     connection timeout
  --agemin AGEMIN       number of minutes of traces to preserve in case of
                        repeated timeouts
  --dir DIR             data directory
  --todir TODIR         data directory
  --nodename NODENAME   exporter's node name
  --nodeip NODEIP       exporter's node IP
  --podname PODNAME     exporter's pod name
  --podip PODIP         exporter's pod IP
  --podservice PODSERVICE
                        exporter's pod service
  --podns PODNS         exporter's pod namespace
  --poduuid PODUUID     exporter's: pod UUID
  --clusterid CLUSTERID
                        exporter's: cluster ID
```
