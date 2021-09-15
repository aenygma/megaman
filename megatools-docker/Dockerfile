# syntax=docker/dockerfile:1
FROM alpine:latest

# Deps
RUN apk add --update build-base libtool automake autoconf pkgconfig \
    glib glib-dev libcurl curl-dev asciidoc openssl-dev
RUN apk add git meson ninja 

# Build and Install
RUN git clone https://megous.com/git/megatools && cd megatools && meson b && \
    ninja -C b install
# for huey consumer
RUN apk add sqlite python3 py3-pip
RUN pip install peewee huey

# Purge
RUN apk del build-base libtool automake autoconf pkgconfig glib-dev curl-dev \
    asciidoc openssl-dev
RUN apk del git meson ninja 
