# sf-exporter
Sysflow exporter to export Sysflow traces to COS

## Container
```
./build
./export (to push to IBM Cloud docker registry)
```

## Usage
```
usage: exporter.py [-h] [--cosendpoint COSENDPOINT] [--cosport COSPORT]
                   [--cosaccesskey COSACCESSKEY] [--cossecretkey COSSECRETKEY]
                   [--scaninterval SCANINTERVAL] [--timeout TIMEOUT]
                   [--agemin AGEMIN] [--dir DIR] [--cosbucket COSBUCKET]
                   [--coslocation COSLOCATION] [--nodename NODENAME]
                   [--nodeip NODEIP] [--podname PODNAME] [--podip PODIP]
                   [--podservice PODSERVICE] [--podns PODNS]
                   [--poduuid PODUUID]

sf-exporter: service for watching and uploading monitoring files to object
store.

optional arguments:
  -h, --help            show this help message and exit
  --cosendpoint COSENDPOINT
                        cos server address
  --cosport COSPORT     cos server port
  --cosaccesskey COSACCESSKEY
                        cos access key
  --cossecretkey COSSECRETKEY
                        cos secret key
  --scaninterval SCANINTERVAL
                        interval between scans
  --timeout TIMEOUT     connection timeout
  --agemin AGEMIN       number of minutes of traces to preserve in case of
                        repeated timeouts
  --dir DIR             data directory
  --cosbucket COSBUCKET
                        target data bucket
  --coslocation COSLOCATION
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
