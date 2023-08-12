#!/bin/sh
set -e
brew install binutils proj gdal
pip install -r requirements/local.txt
docker-compose -f deployments/docker-compose.yml up -d
python3 manage.py migrate --noinput
echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete();User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
python3 manage.py loaddata --app events category_fixture.json
python3 manage.py runserver
exec "$@"
