import hashlib


def events_image_upload_path(instance, filename):
    # collision
    filename_hash = hashlib.sha1(f'{filename}_{instance.name}'.encode()).hexdigest()
    return f'events/image/{filename_hash}'
