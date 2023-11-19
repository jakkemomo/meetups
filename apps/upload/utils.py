from storages.backends.gcloud import GoogleCloudStorage

storage = GoogleCloudStorage()


def upload_image(file):
    try:
        content_type = file.content_type
        target_path = f'images/{file.name}'
        path = storage.save(target_path, file)
        return storage.url(path)

    except Exception as exc:
        print("Failed to upload!")
