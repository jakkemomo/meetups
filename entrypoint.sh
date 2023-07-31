#!/bin/sh
set -e
sudo apt-get install binutils libproj-dev gdal-bin
pip install -r requirements/local.txt
docker-compose -f deployments/docker-compose.yml up -d
python3 manage.py migrate --noinput
python manage.py runserver
exec "$@"
