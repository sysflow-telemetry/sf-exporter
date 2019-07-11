FROM python:3-alpine

# working directory
WORKDIR /usr/local/exporter

# sources
COPY src/executor.py .
COPY src/exporter.py .
COPY src/sfmod sfmod

# dependencies
COPY src/requirements.txt .
RUN apk add --update \
  && pip install --upgrade pip   && pip install --upgrade pip \
  &&  pip install -r requirements.txt \
  && rm -rf /var/cache/apk/*

RUN cd sfmod && \
    python3 setup.py install 

# environment variables
ARG exporttype=cos
ENV EXPORT_TYPE=$exporttype

ARG sysloghost=localhost
ENV SYSLOG_HOST=$sysloghost

ARG syslogport=514
ENV SYSLOG_PORT=$syslogport

ARG endpoint=localhost
ENV COS_ENDPOINT=$endpoint

ARG port=9000
ENV COS_PORT=$port

ARG interval=60
ENV INTERVAL=$interval

ARG bucket=sf-monitoring
ENV COS_BUCKET=$bucket

ARG dir=/mnt/data
ENV DIR=$dir

ARG location=us-south
ENV COS_LOCATION=$location

ARG secure=True
ENV SECURE=$secure

ARG nodename=
ENV NODE_NAME=$nodename

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
CMD python ./exporter.py --exporttype=$EXPORT_TYPE --sysloghost=$SYSLOG_HOST --syslogport=$SYSLOG_PORT --cosendpoint=$COS_ENDPOINT --cosport=$COS_PORT --secure=$SECURE --scaninterval=$INTERVAL --dir=$DIR --cosbucket=$COS_BUCKET --coslocation=$COS_LOCATION --nodename=$NODE_NAME --nodeip=$NODE_IP --podname=$POD_NAME --podns=$POD_NAMESPACE --podip=$POD_IP --podservice=$POD_SERVICE_ACCOUNT --poduuid=$POD_UUID

