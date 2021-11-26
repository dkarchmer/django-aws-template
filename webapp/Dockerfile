FROM node:6
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
RUN npm install -g gulp-cli@1.4.0

WORKDIR /var/app/webapp

# COPY package.json /var/app/webapp
# RUN npm install

# Build Locally
WORKDIR /var/app/webapp
# ENTRYPOINT ["gulp"]
