#
# Copyright (C) 2021 IBM Corporation.
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

ARG UBI_VER
FROM registry.access.redhat.com/ubi8/ubi:${UBI_VER}

ARG VERSION=dev
ARG RELEASE=dev

# Update Labels
LABEL "name"="SysFlow Exporter"
LABEL "vendor"="SysFlow"
LABEL "maintainer"="The SysFlow team"
LABEL "documentation"="https://sysflow.readthedocs.io"
LABEL "version"="${VERSION}"
LABEL "release"="${RELEASE}"
LABEL "summary"="The SysFlow Exporter exports SysFlow traces to S3-compliant object stores."
LABEL "description"="The SysFlow Exporter exports SysFlow traces to S3-compliant object stores."
LABEL "io.k8s.display-name"="SysFlow Exporter"
LABEL "io.k8s.description"="The SysFlow Exporter exports SysFlow traces to S3-compliant object stores."

# Update License
RUN mkdir /licenses
COPY ./LICENSE.md /licenses/

# Install Python environment
RUN dnf install -y --disableplugin=subscription-manager \
        gcc \
        python38 \
        python38-devel \
        python38-wheel && \
    mkdir -p /usr/local/lib/python3.8/site-packages && \
    ln -s /usr/bin/python3 /usr/bin/python && \    
    dnf -y clean all && rm -rf /var/cache/dnf

# working directory
WORKDIR /usr/local/exporter

# sources
COPY src/executor.py .
COPY src/exporter.py .
COPY modules/sysflow/py3 /tmp/build/sfmod

# dependencies
COPY src/requirements.txt /tmp/build
RUN cd /tmp/build && python3 -m pip install -r requirements.txt && \
    cd sfmod && \ 
    python3 -m pip install . && \
    rm -r /tmp/build

# environment variables
ENV TZ=UTC

ARG exporttype=s3
ENV EXPORT_TYPE=$exporttype

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

ARG todir=/mnt/s3
ENV TO_DIR=$todir

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

ARG clusterid=
ENV CLUSTER_ID=$clusterid

ARG s3prefix=
ENV S3_PREFIX=$s3prefix

# entrypoint
CMD python3 ./exporter.py --exporttype=$EXPORT_TYPE --s3endpoint=$S3_ENDPOINT --s3port=$S3_PORT --secure=$SECURE --scaninterval=$INTERVAL --dir=$DIR --s3bucket=$S3_BUCKET --s3location=$S3_LOCATION --nodename=$EXPORTER_ID --nodeip=$NODE_IP --podname=$POD_NAME --podns=$POD_NAMESPACE --podip=$POD_IP --podservice=$POD_SERVICE_ACCOUNT --poduuid=$POD_UUID --todir=$TO_DIR --clusterid=$CLUSTER_ID --s3prefix=$S3_PREFIX
