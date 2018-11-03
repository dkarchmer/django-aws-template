FROM node:5
# ==========================================================
# Docker Image used for Building Gulp based systems
# Usage:
# docker build -t webapp/builder webapp
# docker run --rm -v ${PWD}/webapp:/var/app/webapp -v ${PWD}/server:/var/app/server -v ${PWD}/staticfiles:/var/app/staticfiles -t webapp/builder bower install --allow-root
# docker run --rm -v ${PWD}/webapp:/var/app/webapp -v ${PWD}/server:/var/app/server -v ${PWD}/staticfiles:/var/app/staticfiles -t webapp/builder npm install
# docker run --rm -v ${PWD}/webapp:/var/app/webapp -v ${PWD}/server:/var/app/server -v ${PWD}/staticfiles:/var/app/staticfiles -t webapp/builder gulp
# ==========================================================

RUN mkdir -p /var/app/webapp
RUN mkdir -p /var/app/staticfiles
RUN mkdir -p /var/app/server
WORKDIR /var/app/webapp

# Install app dependencies
RUN npm install -g bower gulp-cli


