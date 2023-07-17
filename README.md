# Django Project Structure
This is a template/project structure for developing django-based applications -
either strictly through the `django-rest-framework` or just `django`.

The project is meant to be easily clone-able, and used as the starter template for
the next big thing our team develops.

## First run
1. Create `.env` file in the root dir with fields from `.env.example`
2. Optionally (to use maps) [get and set](https://yandex.ru/dev/jsapi-v2-1/doc/ru/#get-api-key) yandex maps api key in the `.env` file
3. Install docker-compose
4. `chmod +x entrypoint.sh && ./entrypoint.sh`

This will install postgres db in docker, install geo dependencies, create superuser admin:admin, run migrations and run server.
5. After you have done this once you can just run `python manage.py runserver` next time


### Creating an App
1. Create a folder with the app name in `apps`. For example: `poll`
2. Run `python manage.py startapp poll apps/poll` from the root directory of the project


## Project Tree
```bash
.
├── apps
│   └── example_api # A django rest app
│       ├── api
│       │   ├── v1
│       │   │   ├── __init__.py
│       │   │   ├── serializers.py
│       │   │   ├── services.py
│       │   │   ├── tests.py
│       │   │   ├── urls.py
│       │   │   └── views.py
│       │   ├── v2
│       │   │   ├── __init__.py
│       │   │   ├── serializers.py
│       │   │   ├── services.py
│       │   │   ├── tests.py
│       │   │   ├── urls.py
│       │   │   └── views.py
│       │   └── __init__.py
│       ├── management
│       │   ├── commands
│       │   │   └── command.py
│       │   └── __init__.py
│       ├── migrations
│       │   └── __init__.py
│       ├── templates
│       ├── tests
│       ├── admin.py
│       ├── apps.py
│       ├── __init__.py
│       ├── models.py
│       ├── urls.py
│       ├── utils.py
│       └── views.py
├── common # An optional folder containing common "stuff" for the entire project
├── config
│   ├── settings.py
│   ├── asgi.py
│   ├── __init__.py
│   ├── urls.py
│   └── wsgi.py
├── deployments
│   ├── django-project
│   │   └── Dockerfile
│   ├── nginx
│   │   ├── default.conf
│   │   └── Dockerfile
│   └── docker-compose.yml
├── docs
│   ├── CHANGELOG.md
│   ├── CONTRIBUTING.md
│   ├── deployment.md
│   ├── local-development.md
│   └── swagger.yaml
├── requirements
│   ├── common.txt
│   ├── development.txt
│   ├── local.txt
│   └── production.txt
├── static
├── entrypoint.sh
├── manage.py
├── pytest.ini
└── README.md

```

## Rationale
Each `app` should be designed in way to be plug-able, that is, dragged and dropped
into any other project and it’ll work independently.

### `apps`
* A mother-folder containing all apps for our project. Congruent to any JS-framework's `src` folder.
* An app can be a django template project, or an API.

### `api`
* We like to place all our API components into a package within an app called
`api`. For example, in this repository it's the `example_api/api` folder. That allows us to isolate our API components in a consistent location. If
we were to put it in the root of our app, then we would end up with a huge list
of API-specific modules in the general area of the app.

For projects with a lot of small, interconnecting apps, it can be hard to hunt
down where a particular API view lives. In contrast to placing all API code
within each relevant app, sometimes it makes more sense to build an app
specifically for the API. This is where all the serializers, renderers, and views
are placed. Therefore, the name of the app should reflect its API version

### `api-versioning`
It might often be necessary to support multiple versions of an API throughout the lifetime of a project. Therefore, we're adding in support right from the start.

For different API versions, we're assuming the following will change:
- Serializers
- Views
- URLs
- Services

`model`s can be thought of as shared between versions. Therefore, migrating changes should be versioned carefully without breaking different versions of the API.


### What's Version 2?
Currently we're proposing that major changes to the following, constitutes a new API version:
1. Representation of data, either for submission or retrieval
1. Major optimizations
1. Major code reorganization and code refactor

### `config`
* Contains project configuration files, including the primary URL file
* ~~Contains settings split into `base`, `local`, `production` and `development`.~~. Update: As environment
specific variables will be handled using environment variables, we've deemed it unnecessary to have
separate settings files.


### `deployments`
* Contains Docker, Docker-Compose and nginx specific files for deploying in different
environments


### `documentation`
* We’ll have CHANGELOG.md
* We’ll have CONTRIBUTING.md
* We’ll have deployment instructions
* We’ll have local startup instructions


### `services`
* We’ll be writing business logic in services instead of anywhere else.


### `gitignore`
* https://github.com/github/gitignore/blob/main/Python.gitignore


## References
- [Two Scoops of Django by Daniel and Audrey Feldroy](https://www.feldroy.com/books/two-scoops-of-django-3-x)
- [Django Best Practices](https://django-best-practices.readthedocs.io/en/latest/index.html)
- [Cookiecutter Django](https://github.com/cookiecutter/cookiecutter-django)
- [HackSoft Django Style Guide](https://github.com/HackSoftware/Django-Styleguide)
- [Radoslav Georgiev - Django Structure for Scale and Longevity](https://www.youtube.com/watch?v=yG3ZdxBb1oo)
