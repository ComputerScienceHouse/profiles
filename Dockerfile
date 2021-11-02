FROM python:3.9-slim-buster
MAINTAINER Galen Guyer <galen@galenguyer.com>

RUN ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime

RUN apt-get -yq update && \
    apt-get -yq --no-install-recommends install gcc libsasl2-dev libldap2-dev libssl-dev git && \
    apt-get -yq clean all

RUN mkdir /opt/profiles

WORKDIR /opt/profiles

COPY requirements.txt /opt/profiles

RUN pip install -r requirements.txt

COPY . /opt/profiles

ENTRYPOINT ["gunicorn", "profiles:app",  "--bind=0.0.0.0:8080", "--access-logfile=-", "--timeout=600"]
