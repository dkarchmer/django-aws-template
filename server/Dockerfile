FROM python:3.9-slim-buster

ENV C_FORCE_ROOT 1

# create unprivileged user
RUN adduser --disabled-password --gecos '' myuser

# Install PostgreSQL dependencies
RUN apt-get update && \
    apt-get install -y postgresql-client libpq-dev supervisor netcat gcc

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
ADD server-init.sh /var/app/server-init.sh
ADD runtest.sh /var/app/runtest.sh
RUN mkdir /var/app/logs
COPY locale /var/app/locale

CMD ["/var/app/runserver.sh"]
