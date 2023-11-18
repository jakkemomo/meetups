from storages.backends.gcloud import GoogleCloudStorage

Static = lambda: GoogleCloudStorage(location='static')
Media = lambda: GoogleCloudStorage(location='media')
