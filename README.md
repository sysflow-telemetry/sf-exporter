# sf-exporter
Sysflow Exporte

## Container
```
./build
./export (to push to IBM Cloud docker registry)
```

## Usage
```
usage: exporter.py [-h] [--host HOST] [--port PORT] [--accesskey ACCESSKEY]
                   [--secretkey SECRETKEY] [--scaninterval SCANINTERVAL]
                   [--timeout TIMEOUT] [--agemin AGEMIN] [--dir DIR]
                   [--bucket BUCKET] [--location LOCATION]

sf-exporter: service for watching and uploading monitoring files to object
store.

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           cos server address
  --port PORT           cos server port
  --accesskey ACCESSKEY
                        cos access key
  --secretkey SECRETKEY
                        cos secret key
  --scaninterval SCANINTERVAL
                        interval between scans
  --timeout TIMEOUT     connection timeout
  --agemin AGEMIN       number of minutes of traces to preserve in case of
                        repeated timeouts
  --dir DIR             data directory
  --bucket BUCKET       target data bucket
  --location LOCATION   target data bucket locationr
```
