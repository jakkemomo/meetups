import logging
import os.path
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-3hot3eg$sr1avw4o6avilt+&bz@qve)+oklbgp)70dkmz3-xdv"
)
DEBUG = True
DOCKERIZED = os.environ.get("DOCKERIZED", False)

GS_BUCKET_NAME = os.getenv("GS_BUCKET_NAME", "meetups-dev")
GS_BUCKET_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}'
GS_QUERYSTRING_AUTH = False

SERVICE_URL = os.environ.get("CLOUDRUN_SERVICE_URL")
SERVICE_ACCOUNT = False

if SERVICE_URL:
    from urllib.parse import urlparse

    ALLOWED_HOSTS = [str(urlparse(SERVICE_URL).netloc)]
    DEBUG = False
    DEBUG_PROPAGATE_EXCEPTIONS = True
    CSRF_TRUSTED_ORIGINS = [SERVICE_URL]
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SERVICE_ACCOUNT = True
else:
    SERVICE_URL = "http://localhost:8000/"
    ALLOWED_HOSTS = ['*']

if DOCKERIZED:
    # Settings for docker startup
    STATIC_ROOT = "/home/app/staticfiles"
    STATIC_URL = "/static/"
    MEDIA_ROOT = "/home/app/mediafiles"
    MEDIA_URL = "/media/"
else:
    # Settings for local/prod startup to use GCS
    from google.oauth2 import service_account

    # Set "static" folder
    STATICFILES_STORAGE = 'config.gcs_utils.static'

    # Set "media" folder
    DEFAULT_FILE_STORAGE = 'config.gcs_utils.media'

    # Add an unique ID to a file name if same file name exists
    GS_FILE_OVERWRITE = False

    try:
        GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
            os.path.join(BASE_DIR, 'gcpCredentials.json'),
        )
        SERVICE_ACCOUNT = True
    except FileNotFoundError:
        logging.warning(
            'No gcpCredentials.json file found. Using default credentials.')

    STATIC_URL = f'{GS_BUCKET_URL}/static/'

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://meetups-ui-6vuzexfx2q-lm.a.run.app',
]

# Geo libraries path
GDAL_LIBRARY_PATH = os.environ.get("GDAL_LIBRARY_PATH")
GEOS_LIBRARY_PATH = os.environ.get("GEOS_LIBRARY_PATH")

# Application definition
INSTALLED_APPS = [
    "daphne",
    "channels",
    "channels_postgres",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "apps.core.apps.CoreConfig",
    "apps.events.apps.EventsConfig",
    "apps.permissions.apps.PermissionsConfig",
    "apps.profiles.apps.ProfilesConfig",
    "apps.upload.apps.UploadConfig",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
    'django_filters',
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
            ]
        },
    }
]

ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5555"),
    },
    'channels_postgres': {
        'ENGINE': "django.contrib.gis.db.backends.postgis",
        "NAME": os.getenv("WS_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5555"),
    }
}

DATABASE_ROUTERS = ["config.db_routers.WSRouter", "config.db_routers.MainRouter"]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
password_validation = "django.contrib.auth.password_validation"
AUTH_PASSWORD_VALIDATORS: list[dict] = []

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

AUTH_USER_MODEL = "profiles.User"
LOGIN_URL = os.getenv("LOGIN_URL", "/api/v1/login")
VERIFY_EMAIL_URL = os.getenv(
    "VERIFY_EMAIL_URL",
    f"{SERVICE_URL}api/v1/verify/email/"
)
CONFIRM_PASSWORD_RESET_URL = os.getenv(
    "CONFIRM_FORGOT_PASSWORD_URL",
    f"{SERVICE_URL}api/v1/password/reset/confirm/"
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        'rest_framework_simplejwt.authentication.JWTAuthentication', ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 24,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend']
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=60),
    "TOKEN_OBTAIN_SERIALIZER": "apps.core.serializers.TokenPairSerializer",
    "UPDATE_LAST_LOGIN": True,
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}}
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'loggers': {
        'upload_app': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'core_app': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'profiles_app': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'events_app': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}

# Email
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND",
                          "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "information.mevent@gmail.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# Websockets
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_postgres.core.PostgresChannelLayer',
        'CONFIG': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            "NAME": os.getenv("WS_DB"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5555"),
        },
    },
}

WS_ALLOWED_ORIGINS = [
            "localhost",
            "127.0.0.1",
            "[::1]",
            "https://meetups-ui-6vuzexfx2q-lm.a.run.app",
        ]