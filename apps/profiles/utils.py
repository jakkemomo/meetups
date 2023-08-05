import hashlib


def users_image_upload_path(instance, filename):
    filename_hash = hashlib.sha1(
        f"{filename}_{instance.username}".encode(), usedforsecurity=False
    ).hexdigest()
    return f"users/image/{filename_hash}.jpeg"
