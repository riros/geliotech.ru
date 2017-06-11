#!/usr/bin/env bash

git pull
sudo python3 manage.py collectstatic --noinput
sudo python3 manage.py migrate

python manage.py thumbnail clear_delete_all

sudo systemctl restart uwsgi-app@geliotech
sudo systemctl restart nginx

chown nginx:nginx -R ../geliotech/