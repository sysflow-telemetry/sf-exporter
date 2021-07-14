#!/usr/bin/env python3
#
# Copyright (C) 2019 IBM Corporation.
#
# Authors:
# Frederico Araujo <frederico.araujo@ibm.com>
# Teryl Taylor <terylt@ibm.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# Watches for new monitoring files and uploads them to cloud object store
#
# Instructions:
#      ./exporter -h for help and command line options
#

import logging, argparse, sys, os, time
import shutil
from time import strftime, gmtime
from executor import PeriodicExecutor
from pathlib import Path
from minio import Minio
from minio.error import InvalidResponseError, S3Error
from urllib3 import Timeout
from urllib3.exceptions import MaxRetryError

HEALTH = logging.CRITICAL + 10


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
            return secret_file.read().replace('\n', '')
    except FileNotFoundError:
        logging.error('Secret not found in %s/%s', secrets_dir, secret_name)
    except IOError:
        logging.error('Caught exception while reading secret \'%s\'', secret_name)


def cleanup(args):
    """cleanup exported traces from local tmpfs"""
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


def get_runner(exporttype):
    """
    Returns the main logic for main thread. Must be only invoked in starting
    thread and not reentrantable.
    """
    if exporttype == 'local':
        return local_export
    elif exporttype == 's3':
        return export_to_s3
    raise argparse.ArgumentTypeError('Unknown export type.')


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def local_export(args):
    """local file copy routine"""
    # List traces
    traces = [f for f in files(args.dir)]
    traces.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    # Upload complete traces, exclude most recent log
    for trace in traces[:-1]:
        epoch = os.path.basename(trace)
        dirStr = ""
        if is_int(epoch):
            dirStr = strftime('%Y/%m/%d', gmtime(int(epoch)))
        if len(args.nodeip) > 0:
            dirStr = os.path.join(args.nodeip, dirStr)
        if len(args.nodename) > 0:
            dirStr = os.path.join(args.nodename, dirStr)
        if len(args.clusterid) > 0:
            dirStr = os.path.join(args.clusterid, dirStr)
        if len(args.s3prefix) > 0:
            dirStr = os.path.join(args.s3prefix, dirStr)
        dirStr = os.path.join(args.todir, dirStr)
        to = os.path.join(dirStr, epoch)
        logging.info('Moving file %s to %s', trace, to)
        try:
            Path(dirStr).mkdir(parents=True, exist_ok=True)
            shutil.move(trace, to)
        except OSError:
            logging.exception('Unable to move file %s to %s', trace, to)
            cleanup(args)


def export_to_s3(args):
    """S3 export routine"""
    # Retrieve s3  access and secret keys
    access_key = get_secret('s3_access_key') if not args.s3accesskey else args.s3accesskey
    secret_key = get_secret('s3_secret_key') if not args.s3secretkey else args.s3secretkey

    # Initialize minioClient with an endpoint and access/secret keys.
    minioClient = Minio(
        '%s:%s' % (args.s3endpoint, args.s3port),
        access_key=access_key,
        secret_key=secret_key,
        secure=args.secure,
    )
    minioClient._http.connection_pool_kw['timeout'] = Timeout(connect=args.timeout, read=3 * args.timeout)

    # Make a bucket with the make_bucket API call
    try:
        if not minioClient.bucket_exists(args.s3bucket):
            minioClient.make_bucket(args.s3bucket, location=args.s3location)
    except MaxRetryError:
        logging.error('Connection timeout! Removing traces older than %d minutes', args.agemin)
        cleanup(args)
        pass
    except InvalidResponseError:
        logging.error('Caught exception while checking and creating object store bucket')
        raise
    except S3Error as exc:
        logging.error('Caught an S3 exception when trying to create bucket', exc)
    else:
        # Upload traces to the server
        try:
            traces = [f for f in files(args.dir)]
            traces.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
            # Upload complete traces, exclude most recent log
            for trace in traces[:-1]:
                minioClient.fput_object(
                    args.s3bucket,
                    '%s.%s.sf' % (os.path.basename(trace), args.nodeip),
                    trace,
                    metadata={
                        'x-amz-meta-nodename': args.nodename,
                        'x-amz-meta-nodeip': args.nodeip,
                        'x-amz-meta-podname': args.podname,
                        'x-amz-meta-podip': args.podip,
                        'x-amz-meta-podservice': args.podservice,
                        'x-amz-meta-podns': args.podns,
                        'x-amz-meta-poduuid': args.poduuid,
                    },
                )
                os.remove(trace)
                logging.info('Uploaded trace %s', trace)
            # Upload partial trace without removing it
            # minioClient.fput_object(args.s3bucket, os.path.basename(traces[-1]), traces[-1], metadata={'X-Amz-Meta-Trace': 'partial'})
            # logging.info('Uploaded trace %s', traces[-1])
        except InvalidResponseError:
            logging.error('Caught exception while uploading traces to object store')
        except S3Error as exc:
            logging.error('Caught an S3 exception uploading trace to bucket', exc)


def run_tests(args):
    if args.exporttype == 'local':
        logging.info(
            'Running local monitor copy task from %s to %s, scaninterval: %ss',
            args.dir,
            args.todir,
            args.scaninterval,
        )
        if not os.access(args.dir, os.W_OK):
            logging.error('Directory %s does not exist or is not writable', args.dir)
            return False
        if not os.access(args.todir, os.W_OK):
            logging.error('Directory %s does not exist or is not writable', args.todir)
            return False
        return True
    elif args.exporttype == 's3':
        logging.info(
            'Running monitor task with host: %s:%s, bucket: %s, scaninterval: %ss',
            args.s3endpoint,
            args.s3port,
            args.s3bucket,
            args.scaninterval,
        )
        access_key = get_secret('s3_access_key') if not args.s3accesskey else args.s3accesskey
        secret_key = get_secret('s3_secret_key') if not args.s3secretkey else args.s3secretkey
        minioClient = Minio(
            '%s:%s' % (args.s3endpoint, args.s3port),
            access_key=access_key,
            secret_key=secret_key,
            secure=args.secure,
        )
        minioClient._http.connection_pool_kw['timeout'] = Timeout(connect=args.timeout, read=3 * args.timeout)
        try:
            minioClient.bucket_exists("nonexistingbucket")
            return True
        except:
            logging.error('Object storage is not reachable')
            return False
    return False


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':

    # set command line args
    parser = argparse.ArgumentParser(description='sf-exporter: watches and uploads monitoring files to object store.')
    parser.add_argument('--exporttype', help='export type', default='s3', choices=['s3', 'local'])
    parser.add_argument('--s3endpoint', help='s3 server address', default='localhost')
    parser.add_argument('--s3port', help='s3 server port', default=443)
    parser.add_argument('--s3accesskey', help='s3 access key', default=None)
    parser.add_argument('--s3secretkey', help='s3 secret key', default=None)
    parser.add_argument('--s3bucket', help='target data bucket', default='telemetry')
    parser.add_argument('--s3location', help='target data bucket location', default='us-south')
    parser.add_argument('--s3prefix', help='s3 bucket prefix', default='')
    parser.add_argument('--secure', help='enables SSL connection', type=str2bool, nargs='?', const=True, default=True)
    parser.add_argument('--scaninterval', help='interval between scans', type=float, default=1)
    parser.add_argument('--timeout', help='connection timeout', type=float, default=5)
    parser.add_argument('--agemin', help='age in minutes to keep in case of repeated timeouts', type=float, default=60)
    parser.add_argument('--dir', help='data directory', default='/mnt/data')
    parser.add_argument('--todir', help='data directory', default='/mnt/s3')
    parser.add_argument('--nodename', help='exporter\'s node name', default='')
    parser.add_argument('--nodeip', help='exporter\'s node IP', default='')
    parser.add_argument('--podname', help='exporter\'s pod name', default='')
    parser.add_argument('--podip', help='exporter\'s pod IP', default='')
    parser.add_argument('--podservice', help='exporter\'s pod service', default='')
    parser.add_argument('--podns', help='exporter\'s pod namespace', default='')
    parser.add_argument('--poduuid', help='exporter\'s: pod UUID', default='')
    parser.add_argument('--clusterid', help='exporter\'s: cluster ID', default='')

    # parse args and configuration
    args = parser.parse_args()

    # setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]\t%(message)s')
    logging.addLevelName(level=HEALTH, levelName='HEALTH')
    logging.info('Read configuration from \'%s\'; logging to \'%s\'' % ('stdin', 'stdout'))

    try:
        if run_tests(args):
            logging.log(level=HEALTH, msg='Health checks: passed')
            exporter = PeriodicExecutor(args.scaninterval, get_runner(args.exporttype), [args])
            exporter.run()
        else:
            logging.log(level=HEALTH, msg='Health checks: failed')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        logging.exception('Error while executing exporter')
    else:
        sys.exit(0)
