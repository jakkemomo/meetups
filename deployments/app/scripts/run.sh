#!/bin/bash

# Apply migrations to the first database from env variable called POSTGRES_DB
# Then apply migrations to the second database from env variable called WS_DB
python manage.py migrate --noinput --database=channels_postgres \
  && python manage.py migrate --noinput \
  && python manage.py collectstatic --noinput \
        && python manage.py runserver 0.0.0.0:8000
