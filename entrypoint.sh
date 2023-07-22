#!/bin/sh
set -e
sudo apt-get install binutils libproj-dev gdal-bin
pip install -r requirements/local.txt
docker-compose -f deployments/docker-compose.yml up -d
python3 manage.py migrate --noinput
echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete();User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
python manage.py runserver
exec "$@"
