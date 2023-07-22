# Meetups App

## First run
1. Create `.env` file in the root dir with fields from `.env.example`
2. Optionally (to use maps) [get and set](https://yandex.ru/dev/jsapi-v2-1/doc/ru/#get-api-key) yandex maps api key in the `.env` file
3. Install docker-compose
4. `chmod +x entrypoint.sh && ./entrypoint.sh` (You can also use entrypoint-mac.sh if you are using mac)

This will install postgres db in docker, install geo dependencies, create superuser admin:admin, run migrations and run server.
5. After you have done this once you can just run `python manage.py runserver` next time


### Creating an App
1. Create a folder with the app name in `apps`. For example: `poll`
2. Run `python manage.py startapp poll apps/poll` from the root directory of the project
