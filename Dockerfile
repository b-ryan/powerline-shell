FROM python:2.7-alpine

MAINTAINER github.com/banga/powerline-shell

ENV USER docker
ENV USERNAME "Docker User"

# Create a 'docker' user because we do not want to run everything as 'root'. Use 9999 as the ID
# to keep it specific and away from the IDs in the host system.
RUN addgroup -g 9999 $USER && \
    adduser -u 9999 -G $USER -g "$USERNAME" -s /bin/bash -D $USER

RUN apk add --no-cache --update \
      bzr \
      fossil \
      git \
      mercurial \
      php5 \
      subversion && \
    rm -rf /var/cache/apk/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Cache the dev requirements.
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

USER docker
RUN bzr whoami "$USERNAME <$USER@example.com>" && \
    git config --global user.email "$USER@example.com" && \
    git config --global user.name "$USERNAME"

COPY . ./
USER root
RUN ./setup.py install && \
    chown -R docker:docker .

USER docker
ENTRYPOINT ["/bin/sh"]
