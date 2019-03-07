FROM python:2.7-alpine

# working directory
WORKDIR /usr/local/monitor

# sources
COPY executor.py .
COPY monitor.py .

# dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# environment variables
ARG host=localhost
ENV HOST=$host

ARG port=9000
ENV PORT=$port

ARG interval=1
ENV INTERVAL=$interval

ARG bucket=monitoringdata
ENV BUCKET=$bucket

ARG dir=/mnt/data
ENV DIR=$dir

ARG location=appliance_monitoring_data
ENV LOCATION=$location

# entrypoint
CMD python ./monitor.py --host=$HOST --port=$PORT --scaninterval=$INTERVAL --dir=$DIR --bucket=$BUCKET --location=$LOCATION
