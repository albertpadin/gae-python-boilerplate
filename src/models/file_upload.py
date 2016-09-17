from google.appengine.ext import ndb
from utils import save_file_to_cloudstorage
from utils import save_base64_to_cloudstorage
from libraries.helpers.string_functions import find_between
from libraries.helpers.string_functions import find_between_r
from google.appengine.api import images
import base64


class File(ndb.Model):
    p_created = ndb.DateTimeProperty(auto_now_add=True, name='created')
    p_updated = ndb.DateTimeProperty(auto_now=True, name='updated')
    p_gcs_key = ndb.BlobKeyProperty(name='gcs_key')
    p_uploader = ndb.KeyProperty('User', name='uploader')
    p_serving_url = ndb.StringProperty(name='serving_url')
    p_file_path = ndb.StringProperty(name='file_path')
    p_file_name = ndb.StringProperty(name='file_name')


    @property
    def gcs_key(self):
        return self.p_gcs_key

    @gcs_key.setter
    def gcs_key(self, value):
        if value:
            self.p_gcs_key = value


    @property
    def uploader(self):
        return self.p_uploader

    @uploader.setter
    def uploader(self, value):
        if value:
            self.p_uploader = value


    @property
    def serving_url(self):
        return self.p_serving_url

    @serving_url.setter
    def serving_url(self, value):
        if value:
            self.p_serving_url = value


    @property
    def file_path(self):
        return self.p_file_path

    @file_path.setter
    def file_path(self, value):
        if value:
            self.p_file_path = value


    @property
    def file_name(self):
        return self.p_file_name

    @file_name.setter
    def file_name(self, value):
        if value:
            self.p_file_name = value.strip()


    @property
    def gcs_url(self):
        return "https://storage.googleapis.com" + self.file_path


    @property
    def gcs_path(self):
        return "gs:/" + self.file_path


    @classmethod
    def create_file(cls, uploader, file, base64_type=False):
        folder = 'files/' + str(uploader.key.id())

        if base64_type:
            serving_url, gcs_key, file_path, file_data = save_base64_to_cloudstorage(file, folder=folder)
        else:
            mime_type = file.type
            serving_url, gcs_key, file_path, file_data = save_file_to_cloudstorage(file.file.read(), folder=folder, mime_type=mime_type)

        file = cls()
        file.gcs_key = gcs_key
        file.uploader = uploader.key
        file.serving_url = serving_url
        file.file_path = file_path
        file.put()
        return file

