FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y postgis postgresql-15-postgis-3 postgresql-15-postgis-3-scripts
RUN pip install --no-cache-dir fastapi[all] psycopg2-binary geoalchemy2 uvicorn shapely sqlalchemy requests pydantic 

COPY . /app

COPY ./cronjob /etc/cron.d/ingest-job
RUN chmod 0644 /etc/cron.d/ingest-job && crontab /etc/cron.d/ingest-job

