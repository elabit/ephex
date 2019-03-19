FROM python:2-slim

ENV PORT=9230
ENV BASEDIR=/app/ephemeral-exporter
ENV SCRIPT=ephemeral-export.py

RUN apt-get update && apt-get install -y gcc screen vim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p $BASEDIR
WORKDIR $BASEDIR
COPY $SCRIPT .
COPY stats.json .
COPY VERSION .

EXPOSE $PORT

CMD python -u ./$SCRIPT $PORT endpoint