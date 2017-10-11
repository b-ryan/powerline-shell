FROM aa8y/core:python2

MAINTAINER github.com/banga/powerline-shell

USER root
RUN apk add --no-cache --update \
      bzr \
      fossil \
      git \
      mercurial \
      php5 \
      subversion && \
    rm -rf /var/cache/apk/*

# Cache the dev requirements. Directory is set in the base image.
WORKDIR $APP_DIR
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt && \
    rm -rf requirements-dev.txt

# 'USER' is set in the base image. It points to a non-root user called 'docker'.
USER $USER
RUN bzr whoami "$USERNAME <$USER@example.com>" && \
    git config --global user.email "$USER@example.com" && \
    git config --global user.name "$USERNAME"

COPY . ./
USER root
RUN ./setup.py install && \
    chown -R $USER:$USER .

USER $USER
ENTRYPOINT ["/bin/bash"]
