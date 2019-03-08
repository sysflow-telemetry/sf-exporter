FROM python:3-alpine

# working directory
WORKDIR /usr/local/exporter

# sources
COPY src/executor.py .
COPY src/exporter.py .

# dependencies
COPY src/requirements.txt .
RUN apk add --update \
  && pip install --upgrade pip   && pip install --upgrade pip \
  &&  pip install -r requirements.txt \
  && rm -rf /var/cache/apk/*

# environment variables
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
CMD python ./exporter.py --cosendpoint=$COS_ENDPOINT --cosport=$COS_PORT --scaninterval=$INTERVAL --dir=$DIR --cosbucket=$COS_BUCKET --coslocation=$COS_LOCATION --nodename=$NODE_NAME --nodeip=$NODE_IP --podname=$POD_NAME --podns=$POD_NAMESPACE --podip=$POD_IP --podservice=$POD_SERVICE_ACCOUNT --poduuid=$POD_UUID

