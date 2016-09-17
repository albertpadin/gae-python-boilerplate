from libraries import cloudstorage
from settings import CLOUDSTORAGE_BUCKET
from libraries.helpers.string_functions import generate_random_string
from google.appengine.api import images
from google.appengine.ext import blobstore
import datetime
from libraries.helpers.date_functions import datetime_to_timestamp
import base64
import logging


def save_file_to_cloudstorage(file_data, folder="files", filename=None, mime_type='application/octet-stream', feeling_lucky=False, append_key=False):
    bucket = "/" + CLOUDSTORAGE_BUCKET +"/" + folder + '/'
    if not filename:
        filename = generate_random_string(120) + str(datetime_to_timestamp(datetime.datetime.now())).replace(".", "")
    filename = (''.join(e for e in filename if e.isalnum())).decode('unicode_escape').encode('ascii','ignore')
    if append_key:
        filename += generate_random_string(100) + str(datetime_to_timestamp(datetime.datetime.now())).replace(".", "")
    file_path = bucket + filename
    with cloudstorage.open(file_path, mode="w", content_type=mime_type, options={'x-goog-acl': 'public-read'}) as f:
        if feeling_lucky:
            file_data = images.Image(file_data)
            file_data.im_feeling_lucky()
            file_data = file_data.execute_transforms(output_encoding=images.JPEG)
        f.write(file_data)
    gcs_serving_url = "https://storage.googleapis.com" + file_path

    blob_key = blobstore.create_gs_key("/gs" + file_path)

    try:
        gcs_key = blobstore.BlobKey(blob_key)
    except Exception, e:
        logging.exception(e)
        gcs_key = None

    try:
        serving_url = images.get_serving_url(blob_key, secure_url=True)
    except Exception, e:
        logging.exception(e)
        serving_url = gcs_serving_url
    return serving_url, gcs_key or None, file_path, file_data


def save_base64_to_cloudstorage(file_data, folder="files", filename=None, mime_type='application/octet-stream', feeling_lucky=False, append_key=False):
    file_data = base64.b64decode(file_data)

    bucket = "/" + CLOUDSTORAGE_BUCKET +"/" + folder + '/'
    if not filename:
        filename = generate_random_string(120) + str(datetime_to_timestamp(datetime.datetime.now())).replace(".", "")
    filename = (''.join(e for e in filename if e.isalnum())).decode('unicode_escape').encode('ascii','ignore')
    if append_key:
        filename += generate_random_string(100) + str(datetime_to_timestamp(datetime.datetime.now())).replace(".", "")
    file_path = bucket + filename
    with cloudstorage.open(file_path, mode="w", content_type=mime_type, options={'x-goog-acl': 'public-read'}) as f:
        if feeling_lucky:
            file_data = images.Image(file_data)
            file_data.im_feeling_lucky()
            file_data = file_data.execute_transforms(output_encoding=images.JPEG)
        f.write(file_data)
    gcs_serving_url = "https://storage.googleapis.com" + file_path

    blob_key = blobstore.create_gs_key("/gs" + file_path)

    try:
        gcs_key = blobstore.BlobKey(blob_key)
    except Exception, e:
        logging.exception(e)
        gcs_key = None

    try:
        serving_url = images.get_serving_url(blob_key, secure_url=True)
    except Exception, e:
        logging.exception(e)
        serving_url = gcs_serving_url
    return serving_url, gcs_key or None, file_path, file_data
