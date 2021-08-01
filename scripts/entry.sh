#!/bin/bash
cd src
python manage.py migrate
python manage.py collectstatic --noinput

gunicorn chaosinventory.wsgi --name chaosinventory --bind="[::]:8000"
