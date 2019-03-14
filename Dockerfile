FROM python:2-slim

ENV BASEDIR=/app/ephemeral-exporter
ENV SCRIPT=ephemeral-export.py
RUN mkdir -p $BASEDIR

WORKDIR $BASEDIR

COPY requirements.txt $BASEDIR
RUN apt-get update && apt-get install -y gcc
RUN pip install --no-cache-dir -r requirements.txt

COPY $SCRIPT $BASEDIR

EXPOSE 8000

CMD python -u ./$SCRIPT