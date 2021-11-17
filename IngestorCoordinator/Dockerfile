FROM python:3.8-alpine

ENV POSTGRES_DB_HOST=""
ENV POSTGRES_DB_USER="jobsity"
ENV POSTGRES_DB_PWD=""
ENV POSTGRES_TABLE_NAME="trips"
ENV INGESTION_FILE_PATH="/data/landing"
ENV INGESTION_PROCESSED_PATH="/data/processed"

RUN mkdir -p /data/landing && mkdir -p /data/processed
COPY . /opt/jobsity

WORKDIR /opt/jobsity
RUN apk update && apk add --no-cache --no-cache bash\
                       pkgconfig \
                       gcc \
                       libcurl \
                       python2-dev \
                       gpgme-dev \
                       libc-dev \
                       postgresql-dev  && rm -rf /var/cache/apk/*

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python","run.py"]