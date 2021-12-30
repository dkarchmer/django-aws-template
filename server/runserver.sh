#!/bin/bash

cd /var/app
export PYTHONPATH=/var/app;$PYTHONPATH

/usr/local/bin/gunicorn --log-level info --log-file=- --workers 4 --name project_gunicorn -b 0.0.0.0:8000 --reload config.wsgi:application