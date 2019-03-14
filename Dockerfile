FROM python:2-slim

ENV PORT=9230
ENV BASEDIR=/app/ephemeral-exporter
ENV SCRIPT=ephemeral-export.py

RUN mkdir -p $BASEDIR
WORKDIR $BASEDIR
COPY requirements.txt .
COPY $SCRIPT .
COPY stats.json .
COPY VERSION .

RUN apt-get update && apt-get install -y gcc
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE $PORT

CMD python -u ./$SCRIPT $PORT endpoint