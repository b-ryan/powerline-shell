FROM python:2-alpine

MAINTAINER github.com/b-ryan/powerline-shell

USER root
RUN apk add --no-cache --update \
      bzr \
      fossil \
      git \
      mercurial \
      php5 \
      subversion \
      && \
    rm -rf /var/cache/apk/*

RUN mkdir /code
WORKDIR /code
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt && \
    rm requirements-dev.txt

RUN bzr whoami "root <root@example.com>" && \
    git config --global user.email "root@example.com" && \
    git config --global user.name "root"

# COPY . ./
# RUN ./setup.py install

ENV USER root

CMD ["nosetests"]
