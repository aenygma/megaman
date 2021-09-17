# syntax=docker/dockerfile:1
FROM alpine:latest

# Deps
RUN apk add --update build-base libtool automake autoconf pkgconfig \
    glib glib-dev libcurl curl-dev asciidoc openssl-dev git meson ninja && \
# Build and Install
git clone https://megous.com/git/megatools && cd megatools && meson b && \
    ninja -C b install && \
# for huey consumer
apk add sqlite python3 py3-pip && pip install peewee huey pymegatools && \
# Purge
apk del build-base libtool automake autoconf pkgconfig glib-dev curl-dev \
    asciidoc openssl-dev git meson ninja
