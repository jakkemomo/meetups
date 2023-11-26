import logging
from functools import wraps
from django.core.files.storage import default_storage

logger = logging.getLogger("upload_app")


def task_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as exc:
            logger.error(f'error: {func.__name__}: {exc}')
        else:
            return result

    return wrapper


@task_logger
def upload_image(file):
    rel_url = f'images/{file.name}'
    default_storage.save(rel_url, file)
    return rel_url
