#!/bin/sh
set -eu
docker build -t powerline-shell .
docker run --rm --interactive --tty \
    --volume $PWD:/code \
    powerline-shell "$@"
