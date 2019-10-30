# SysFlow Exporter (sf-exporter repo)
SysFlow exporter to export SysFlow traces to S3-compliant object stores and rsyslog servers.

## Cloning source
The sf-exporter project has been tested primarily on Ubuntu 16.04 and 18.04. The project will be tested on other flavors of UNIX in the future. This document 
describes how to build and run the application both inside a docker container and on a Linux host. Building and running the application inside a docker container 
is the easiest way to start. For convenience, skip the build step and pull pre-built images directly from Docker Hub.

To build the project, first pull down the source code, with submodules:

```
git clone --recursive git@github.com:sysflow-telemetry/sf-exporter.git 
```

To checkout submodules on an already cloned repo:

```
git submodule update --init --recursive
```

## Container
```
docker build --pull --force-rm -t sf-exporter . 
```
For s3 export:
```
docker service create --name sf-exporter \
    -e NODE_IP=10.1.0.159 \
    -e INTERVAL=15 \
    --secret s3_access_key \
    --secret s3_secret_key \
    --mount type=bind,source=/mnt/data,destination=/mnt/data \
    sf-exporter:latest
```
For remote syslogging:
```
docker service create --name sf-exporter \
    -e SYSLOG_HOST=localhost \
    -e SYSLOG_PORT=514 \
    -e NODE_IP=10.1.0.159 \
    -e INTERVAL=15 \
    -e DIR=/mnt/data \
    --mount type=bind,source=/mnt/data,destination=/mnt/data \
    sf-exporter:latest
```

## Development
```
cd src & pip3 install -r requirements.txt
cd modules/sysflow/py3 & sudo python3 setup.py install
```
Example run with remote syslogging export:
```
./exporter.py --exporttype syslog --sysloghost 127.0.0.1 --syslogport 514 --dir /mnt/data --nodeip testnode --scaninterval 15
```
## Usage
```
usage: exporter.py [-h] [--exporttype {s3,syslog}] [--sysloghost SYSLOGHOST]
                   [--syslogport SYSLOGPORT] [--s3endpoint S3ENDPOINT]
                   [--s3port S3PORT] [--s3accesskey S3ACCESSKEY]
                   [--s3secretkey S3SECRETKEY] [--secure [SECURE]]
                   [--scaninterval SCANINTERVAL] [--timeout TIMEOUT]
                   [--agemin AGEMIN] [--dir DIR] [--s3bucket S3BUCKET]
                   [--s3location S3LOCATION] [--nodename NODENAME]
                   [--nodeip NODEIP] [--podname PODNAME] [--podip PODIP]
                   [--podservice PODSERVICE] [--podns PODNS]
                   [--poduuid PODUUID]

sf-exporter: service for watching and uploading monitoring files to object
store.

optional arguments:
  -h, --help            show this help message and exit
  --exporttype {s3,syslog}
                        export type
  --sysloghost SYSLOGHOST
                        syslog host address
  --syslogport SYSLOGPORT
                        syslog UDP port
  --s3endpoint S3ENDPOINT
                        s3 server address
  --s3port S3PORT     s3 server port
  --s3accesskey S3ACCESSKEY
                        s3 access key
  --s3secretkey S3SECRETKEY
                        s3 secret key
  --secure [SECURE]     indicates if SSL connection
  --scaninterval SCANINTERVAL
                        interval between scans
  --timeout TIMEOUT     connection timeout
  --agemin AGEMIN       number of minutes of traces to preserve in case of
                        repeated timeouts
  --dir DIR             data directory
  --s3bucket S3BUCKET
                        target data bucket
  --s3location S3LOCATION
                        target data bucket location
  --nodename NODENAME   exporter's node name
  --nodeip NODEIP       exporter's node IP
  --podname PODNAME     exporter's pod name
  --podip PODIP         exporter's pod IP
  --podservice PODSERVICE
                        exporter's pod service
  --podns PODNS         exporter's pod namespace
  --poduuid PODUUID     exporter's: pod UUID
```
