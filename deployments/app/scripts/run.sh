#!/bin/bash

# Apply migrations to the first database from env variable called POSTGRES_DB
# Then apply migrations to the second database from env variable called WS_DB
python manage.py migrate --noinput --database=$POSTGRES_DB \
  && python manage.py migrate --noinput --database=$WS_DB \
  && python manage.py collectstatic --noinput \
        && python manage.py runserver 0.0.0.0:8000
