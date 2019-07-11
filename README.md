# sf-exporter
Sysflow exporter to export Sysflow traces to COS

## Container
```
./build
./export (to push to IBM Cloud docker registry)
```

## Development
```
cd src & pip3 install -r requirements.txr
cd sfmod & sudo python3 setup.py install
```

## Usage
```
usage: exporter.py [-h] [--exporttype {cos,syslog}] [--sysloghost SYSLOGHOST]
                   [--syslogport SYSLOGPORT] [--cosendpoint COSENDPOINT]
                   [--cosport COSPORT] [--cosaccesskey COSACCESSKEY]
                   [--cossecretkey COSSECRETKEY] [--secure [SECURE]]
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
  --exporttype {cos,syslog}
                        export type
  --sysloghost SYSLOGHOST
                        syslog host address
  --syslogport SYSLOGPORT
                        syslog UDP port
  --cosendpoint COSENDPOINT
                        cos server address
  --cosport COSPORT     cos server port
  --cosaccesskey COSACCESSKEY
                        cos access key
  --cossecretkey COSSECRETKEY
                        cos secret key
  --secure [SECURE]     indicates if SSL connection
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
