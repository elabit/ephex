# FROM python:2-slim
FROM centos:7

ENV PORT=9230
ENV BASEDIR=/app/ephemeral-exporter
ENV SCRIPT=ephemeral-export.py

# RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum update -y && yum install -y screen python36u \
    python36u-libs python36u-devel python36u-pip && \
    yum clean all -y
RUN ln -sf /usr/bin/python3.6 /usr/bin/python && ln -s /usr/bin/pip3.6 /usr/bin/pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


RUN chmod ug+x $BASEDIR/* 





RUN apt-get update && apt-get install -y gcc screen vim python-pip



RUN mkdir -p $BASEDIR
WORKDIR $BASEDIR
COPY $SCRIPT .
COPY stats.json .
COPY VERSION .
RUN chmod a+w $SCRIPT

EXPOSE $PORT

CMD python -u ./$SCRIPT $PORT endpoint