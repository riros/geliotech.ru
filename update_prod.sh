#!/usr/bin/env bash

git pull
sudo python3 manage_prod.py collectstatic --silent