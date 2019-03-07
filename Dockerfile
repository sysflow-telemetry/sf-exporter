FROM python:2.7-alpine

# working directory
WORKDIR /usr/local/exporter

# sources
COPY src/executor.py .
COPY src/exporter.py .

# dependencies
COPY src/requirements.txt .
RUN pip install -r requirements.txt

# environment variables
ARG host=localhost
ENV HOST=$host

ARG port=9000
ENV PORT=$port

ARG interval=1
ENV INTERVAL=$interval

ARG bucket=sf-monitoring
ENV BUCKET=$bucket

ARG dir=/mnt/data
ENV DIR=$dir

ARG location=us-south
ENV LOCATION=$location

# entrypoint
CMD python ./exporter.py --host=$HOST --port=$PORT --scaninterval=$INTERVAL --dir=$DIR --bucket=$BUCKET --location=$LOCATION
