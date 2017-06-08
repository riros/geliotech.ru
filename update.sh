#!/usr/bin/env bash

git pull
python3 manage.py makemigrations
python manage.py migrate
sudo python3 manage.py collectstatic