FROM node:10
# ==========================================================
# Docker Image used for Building Gulp based systems
# Usage:
#    docker build -t builder .
#    docker run --rm -v ${PWD}/webapp:/var/app/webapp -t builder
#    docker run --rm -v ${PWD}/webapp:/var/app/webapp --entrypoint npm -t builder install
#    docker run --rm -v ${PWD}/webapp:/var/app/webapp -t builder templates
# ==========================================================

RUN mkdir -p /var/app/webapp
RUN mkdir -p /var/app/staticfiles
RUN mkdir -p /var/app/server

# Install app dependencies
RUN npm install -g gulp-cli@2.3.0

WORKDIR /var/app/webapp

# Build Locally
WORKDIR /var/app/webapp
