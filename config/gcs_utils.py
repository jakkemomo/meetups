from google.cloud.storage import Client
from storages.backends.gcloud import GoogleCloudStorage

from config import settings


class ExtendedGoogleCloudStorage(GoogleCloudStorage):

    @property
    def client(self):
        if self._client is None:
            if settings.SERVICE_ACCOUNT:
                self._client = Client(project=self.project_id, credentials=self.credentials)
            else:
                self._client = Client.create_anonymous_client()
        return self._client


static = lambda: ExtendedGoogleCloudStorage(location="static")
media = lambda: ExtendedGoogleCloudStorage(location="media")
