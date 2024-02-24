#!/bin/sh
set -e
sudo apt-get install binutils libproj-dev gdal-bin
pip install -r requirements/local.txt
docker-compose -f deployments/docker-compose.yml up -d
python3 manage.py migrate --noinput
python3 manage.py loaddata category_fixture.json city_fixture.json
python3 manage.py runserver
exec "$@"
