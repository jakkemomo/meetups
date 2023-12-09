# Meetups App

Meetups is an initiative of a group of young and energetic people who want to change the world.  
And even if they don't succeed, the project leaders will know that their work has taught the participants the right approach to project development and management.

## First run
1. Create `.env` file in the root dir with fields from `.env.example`
2. Optionally (to use maps) [get and set](https://yandex.ru/dev/jsapi-v2-1/doc/ru/#get-api-key) yandex maps api key or, even better, [google maps api key](https://developers.google.com/maps/documentation/javascript/get-api-key) in the `.env` file
3. Install docker-compose
4. `chmod +x entrypoint.sh && ./entrypoint.sh` (You can also use entrypoint-mac.sh if you are using mac, but be sure to install psycopg lib before that)

This will install postgres db in docker, install geo dependencies, create superuser admin:admin, run migrations and run server.
5. After you have done this once you can just run `python manage.py runserver` next time


### Creating an App
1. Create a folder with the app name in `apps`. For example: `poll`
2. Run `python manage.py startapp poll apps/poll` from the root directory of the project

### How to update from main branch
1. git stash && git checkout main && git pull && pip install -r requirements/common.txt && python manage.py migrate && git stash pop

### How to make pull request on a new branch:
1. git checkout -b new_branch
2. git add name_of_changed_file
3. git commit -m "change log_description"
4. git push -u origin new_branch
5. Go to the Github page for the repository (e.g., https://github.com/jakkemomo/meetups)
6. Click on 'Pull requests' tab
7. Click on 'New pull request'
8. Choose your branch (new_branch) to compare with the main branch
9. Click on 'Create pull request' button

## Reporting Issues
To report a problem, you can open an [issue](https://github.com/jakkemomo/meetups/issues) in repository against a specific workflow. If the issue is sensitive in nature or a security related issue, please do not report in the issue tracker but instead text to [Alexander](https://t.me/jaqombo).

## Licensing
Meetups and its subprojects are licensed under the Apache License, Version 2.0. See [LICENSE](https://github.com/jakkemomo/meetups/blob/main/LICENSE) for the full license text.

## Contributing

Anyone can contribute to the Matuups project - learn more at [CONTRIBUTING.md](https://github.com/jakkemomo/meetups/blob/main/docs/CONTRIBUTING.md). All project management related documents can be found here.

## List of participants

[COMMITTERS.csv](https://github.com/jakkemomo/meetups/blob/main/docs/COMMITTERS.csv)
