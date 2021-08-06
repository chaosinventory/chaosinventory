#!/bin/bash
set -e
cd src
python manage.py migrate
python manage.py collectstatic --noinput

gunicorn chaosinventory.wsgi --name chaosinventory --bind="[::]:8000"

exit 0
