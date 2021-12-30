#!/bin/bash
# Parse arguments in form of --ignore hostname
waitfor=([db]=1)

# Then we will not wait for hostnames that we ignore
if ((${waitfor[db]} == 1))
then
    while ! nc -zw1 $RDS_HOSTNAME $RDS_PORT; do
    echo "Database not found on network."
    sleep 1
    done
fi

python manage.py migrate --noinput
python manage.py init-basic-data

# Run a security check
python manage.py check --deploy

echo "========= DONE ============"
