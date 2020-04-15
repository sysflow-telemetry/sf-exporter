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
FROM registry.access.redhat.com/ubi8/ubi:8.1-406

ARG VERSION=dev
ARG RELEASE=dev

# Update Label
LABEL "name"="Sysflow Exporter"
LABEL "vendor"="IBM"
LABEL "version"="${VERSION}"
LABEL "release"="${RELEASE}"
LABEL "summary"="Sysflow Exporter exports SysFlow traces to S3-compliant object stores or rsyslog servers in several formats, including Avro, JSON, and CSV."
LABEL "description"="Sysflow Exporter exports SysFlow traces to S3-compliant object stores or rsyslog servers in several formats, including Avro, JSON, and CSV."
LABEL "io.k8s.display-name"="Sysflow Exporter"
LABEL "io.k8s.description"="Sysflow Exporter exports SysFlow traces to S3-compliant object stores or rsyslog servers in several formats, including Avro, JSON, and CSV."

# Update License
RUN mkdir /licenses
COPY ./LICENSE.md /licenses/

# Install Python environment
RUN dnf install -y --disableplugin=subscription-manager \
        python3 \
        python3-wheel && \
    mkdir -p /usr/local/lib/python3.6/site-packages && \
    ln -s /usr/bin/easy_install-3 /usr/bin/easy_install && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip && \
    dnf -y clean all && rm -rf /var/cache/dnf

# working directory
WORKDIR /usr/local/exporter

# sources
COPY src/executor.py .
COPY src/exporter.py .
COPY modules/sysflow/py3 sfmod

# dependencies
COPY src/requirements.txt .
RUN pip install -r requirements.txt && \
    cd sfmod && \ 
    easy_install . 

# environment variables
ENV TZ=UTC

ARG exporttype=s3
ENV EXPORT_TYPE=$exporttype

ARG exportfields=
ENV EXPORT_FIELDS=$exportfields

ARG sysloghost=localhost
ENV SYSLOG_HOST=$sysloghost

ARG syslogport=514
ENV SYSLOG_PORT=$syslogport

ARG syslogprotocol=TCP
ENV SYSLOG_PROTOCOL=$syslogprotocol

ARG syslogexpint=0.05
ENV SYSLOG_EXP_INT=$syslogexpint

ARG endpoint=localhost
ENV S3_ENDPOINT=$endpoint

ARG port=9000
ENV S3_PORT=$port

ARG interval=60
ENV INTERVAL=$interval

ARG bucket=sf-monitoring
ENV S3_BUCKET=$bucket

ARG dir=/mnt/data
ENV DIR=$dir

ARG location=us-south
ENV S3_LOCATION=$location

ARG secure=True
ENV SECURE=$secure

ARG exporterid=
ENV EXPORTER_ID=$exporterid

ARG nodeip=
ENV NODE_IP=$nodeip

ARG podname=
ENV POD_NAME=$podname

ARG podnamespace=
ENV POD_NAMESPACE=$podnamespace

ARG podip=
ENV POD_IP=$podip

ARG podserviceaccount=
ENV POD_SERVICE_ACCOUNT=$podserviceaccount

ARG poduuid=
ENV POD_UUID=$poduuid

# entrypoint
CMD python ./exporter.py --exporttype=$EXPORT_TYPE --exportfields=$EXPORT_FIELDS --sysloghost=$SYSLOG_HOST --syslogport=$SYSLOG_PORT --syslogprotocol=$SYSLOG_PROTOCOL --syslogexpint=$SYSLOG_EXP_INT --s3endpoint=$S3_ENDPOINT --s3port=$S3_PORT --secure=$SECURE --scaninterval=$INTERVAL --dir=$DIR --s3bucket=$S3_BUCKET --s3location=$S3_LOCATION --nodename=$EXPORTER_ID --nodeip=$NODE_IP --podname=$POD_NAME --podns=$POD_NAMESPACE --podip=$POD_IP --podservice=$POD_SERVICE_ACCOUNT --poduuid=$POD_UUID

