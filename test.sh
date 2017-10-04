#!/bin/sh

docker build -t powerline-shell .
docker run --rm -it powerline-shell -c nosetests
