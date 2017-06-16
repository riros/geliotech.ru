#!/usr/bin/env bash

git pull
python3 manage.py collectstatic --noinput
python3 manage.py migrate

#python manage.py thumbnail clear_delete_all
echo "start imoprt"
#python manage.py import
echo "import commplete... restart services"
systemctl restart uwsgi-app@geliotech
systemctl restart nginx
echo "done"
chown nginx:nginx -R ../geliotech.ru/
