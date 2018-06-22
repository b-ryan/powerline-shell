#!/bin/sh
set -eu
docker build -t powerline-shell .
docker run --rm -it powerline-shell nosetests "$@"
