#!/bin/sh
set -e
brew install binutils proj gdal
pip install -r requirements/local.txt
docker-compose -f deployments/docker-compose.yml up -d
python3 manage.py migrate --noinput
python manage.py runserver
exec "$@"
