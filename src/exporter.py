#!/usr/bin/env python
#-------------------------------------------------------------------------------
#
# Watches for new monitoring files and uploads them to cloud object store
#
# Instructions:
#      ./exporter -h for help and command line options
#
# F. Araujo (frederico.araujo@ibm.com)
#
#-------------------------------------------------------------------------------
#
import logging, argparse, codecs, sys, os, json, time, socket
from executor import PeriodicExecutor
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists)
from urllib3 import Timeout
from urllib3.exceptions import MaxRetryError

def files(path):  
    """list files in dir path"""
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield os.path.join(path, file)

def get_secret(secret_name):
    """extract secret from vault, if using a vault"""    
    try:
        secrets_dir = '/run/secrets' if not (os.path.isdir('/run/secrets/k8s')) else '/run/secrets/k8s'
        with open('%s/%s' % (secrets_dir, secret_name), 'r') as secret_file:
            return secret_file.read()
    except IOError:
        logging.exception('Caught exception while reading secret \'%s\'', secret_name)

def cleanup(args):
    """cleaup exported traces from local tmpfs""" 
    now = time.time()
    cutoff = now - (args.agemin * 60)

    files = os.listdir(args.dir)
    for xfile in files:
        f = os.path.join(args.dir, xfile)
        if os.path.isfile(f):
            t = os.stat(f)
            c = t.st_ctime
            # delete file if older than agemin
            if c < cutoff:
	        logging.warn('Trace \'%s\' removed before being uploaded to object store', f)
                os.remove(f)

def run(args):
    """main thread"""
    # Retrieve cos  access and secret keys
    access_key = get_secret('cos_access_key') if not args.accesskey else args.accesskey
    secret_key = get_secret('cos_secret_key') if not args.secretkey else args.secretkey

    # Initialize minioClient with an endpoint and access/secret keys.
    minioClient = Minio('%s:%s' % (args.host, args.port),
			access_key=access_key,
			secret_key=secret_key,
			secure=True)
    minioClient._http.connection_pool_kw['timeout'] = Timeout(connect=args.timeout, read=3*args.timeout)

    # Make a bucket with the make_bucket API call.
    try:
    	if not minioClient.bucket_exists(args.bucket):
            minioClient.make_bucket(args.bucket, location=args.location)        
    except MaxRetryError:
        logging.error('Connection timeout! Removing traces older than %d minutes', args.agemin)
	cleanup(args)
        pass
    except BucketAlreadyOwnedByYou:
        pass
    except BucketAlreadyExists:
        pass
    except ResponseError:
        raise
    else:
        # Upload traces to the server
        try:
            traces = [f for f in files(args.dir)]
            traces.sort(key=lambda f: int(filter(str.isdigit, f)))
            # Upload complete traces, exclude most recent log
            for trace in traces[:-1]:
                hostname = socket.gethostname()
                ip = socket.gethostbyname(hostname)
                minioClient.fput_object(args.bucket, os.path.basename(trace), '%s.%s' % (ip, trace), metadata={'x-amz-meta-host': hostname})
                os.remove(trace)
                logging.info('Uploaded trace %s', trace)
            # Upload partial trace without removing it
	    #minioClient.fput_object(args.bucket, os.path.basename(traces[-1]), traces[-1], metadata={'X-Amz-Meta-Trace': 'partial'})
	    #logging.info('Uploaded trace %s', traces[-1])
        except ResponseError:
            logging.exception('Caught exception while uploading traces to object store')

if __name__ == '__main__':
    
    # set command line args
    parser = argparse.ArgumentParser(
        description='sf-exporter: service for watching and uploading monitoring files to object store.'
    )
    parser.add_argument('--host', help='cos server address', default='localhost') 
    parser.add_argument('--port', help='cos server port', default=9000)
    parser.add_argument('--accesskey', help='cos access key', default=None)
    parser.add_argument('--secretkey', help='cos secret key', default=None)
    parser.add_argument('--scaninterval', help='interval between scans', type=float, default=1)
    parser.add_argument('--timeout', help='connection timeout', type=float, default=5)
    parser.add_argument('--agemin', help='number of minutes of traces to preserve in case of repeated timeouts', type=float, default=60)
    parser.add_argument('--dir', help='data directory', default='/mnt/data')
    parser.add_argument('--bucket', help='target data bucket', default='sf-monitoring')
    parser.add_argument('--location', help='target data bucket location', default='us-south')
   
    # parse args and configuration
    args = parser.parse_args()

    # setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]\t%(message)s')
    logging.info('Read configuration from \'%s\'; logging to \'%s\'' % ('stdin', 'stdout'))

    try:
        logging.info('Running monitor task with host: %s:%s, bucket: %s, scaninterval: %ss', args.host, args.port, args.bucket, args.scaninterval)
        exporter = PeriodicExecutor(args.scaninterval, run, [args])
	exporter.run()
    except:
        logging.exception('Error while executing exporter')

    sys.exit(0)
