#!/usr/bin/env bash

git pull
sudo python3 manage_prod.py collectstatic --silent
sudo python3 manage_prod.py migrate
sudo systemctl restart uwsgi