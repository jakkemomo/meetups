# Meetups App

## Pre requirements
Install [docker](https://docs.docker.com/engine/install/) and [docker compose](https://docs.docker.com/compose/install/)

## Basic setup
1. Create `.env` file in the root dir with filled out fields from `.env.example`
2. Run `docker-compose -f deployments/docker-compose.yml up -d`
3. Go to `http://localhost:8000/swagger` and you should see the app running

## Local setup for easier debugging
1. Create `.env` file in the root dir with filled out fields from `.env.example`
2. Run your postgres db via `docker-compose -f deployments/docker-compose-db.yml up -d`
3. For linux: install geo dependencies via `sudo apt-get install binutils libproj-dev gdal-bin`
4. For mac: install geo dependencies via `brew install binutils proj gdal`
5. Setup your virtual environment and install requirements via `pip install -r requirements/local.txt`
6. Install pre-commit hooks via `pre-commit install` for code formatting and linting before commit
7. Run migrations via `python manage.py migrate`
8. Run server via `python manage.py runserver`
9. Go to `http://localhost:8000/swagger` and you should see the app running


### Creating an App
1. Create a folder with the app name in `apps`. For example: `poll`
2. Run `python manage.py startapp poll apps/poll` from the root directory of the project

### How to update from main branch
`git stash && git checkout main && git pull && pip install -r requirements/common.txt && python manage.py migrate && git stash pop
`
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
