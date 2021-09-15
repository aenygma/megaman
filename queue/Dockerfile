FROM alpine:latest
RUN apk update
RUN apk add sqlite python3 py3-pip
RUN pip install peewee huey

RUN rm -f /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python
