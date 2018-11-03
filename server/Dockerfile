FROM python:3.6

MAINTAINER David Karchmer <dkarchmer@gmail.com>

ENV C_FORCE_ROOT 1

# create unprivileged user
RUN adduser --disabled-password --gecos '' myuser

# Install PostgreSQL dependencies
RUN apt-get update && \
    apt-get install -y postgresql-client libpq-dev supervisor

# Step 1: Install any Python packages
# ----------------------------------------

ENV PYTHONUNBUFFERED 1
RUN mkdir /var/app
WORKDIR  /var/app
COPY requirements /var/app/requirements
RUN pip install -U pip
RUN pip install -r requirements/docker.txt
RUN pip install gunicorn

# Step 2: Copy Django Code
# ----------------------------------------

COPY apps /var/app/apps
COPY config /var/app/config
COPY manage.py /var/app/manage.py
ADD runserver.sh /var/app/runserver.sh
ADD runtest.sh /var/app/runtest.sh
RUN mkdir /var/app/logs
COPY locale /var/app/locale

EXPOSE 8080

CMD ["/var/app/runserver.sh"]
