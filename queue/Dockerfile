FROM alpine:latest
RUN apk update && \
# add deps
apk add sqlite python3 py3-pip && \
# install libs
pip install peewee huey && \
# make python3 default
rm -f /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python
