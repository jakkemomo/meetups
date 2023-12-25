from django.core.files.storage import default_storage


def delete_image_if_exists(instance):
    image_url = instance.image_url
    if image_url:
        try:
            if default_storage.exists(image_url):
                default_storage.delete(image_url)

        except Exception as exc:
            return exc
