#!/usr/bin/env bash

git pull
sudo python3 manage_prod.py collectstatic --noinput
sudo python3 manage_prod.py migrate
sudo systemctl restart uwsgi-app@geliotech
sudo systemctl restart nginx

