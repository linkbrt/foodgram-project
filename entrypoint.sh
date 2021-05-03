#!/bin/sh

cd server
python manage.py makemigrations --no-input
python manage.py migrate --no-input

sudo python manage.py collectstatic --no-input

gunicorn config.wsgi:application --bind 0.0.0.0:8000
