import requests
import json
import re
from QuizBankBackend import config
from google.cloud import storage
from google.cloud import vision
from base64 import b64decode


imgurUrl = 'https://api.imgur.com/3/image'
authHeader = 'Authorization'
clientId = config['ImgurClientId']

def uploadImage(image: str):
    payload = {'image': image}
    files = []
    headers = {authHeader: f'Client-ID {clientId}'}

    response = requests.post(imgurUrl, headers=headers, data=payload, files=files)

    return json.loads(response.text)

def deleteImage(deletehash: str):
    payload = {}
    files = []
    headers = {authHeader: f'Client-ID {clientId}'}

    response = requests.delete(f'{imgurUrl}/{deletehash}', headers=headers, data=payload, files=files)

    return response.text

def uploadFileToBucket(bucket_name, file_name, base64):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    bytes = b64decode(base64, validate=True)
    blob.upload_from_string(bytes, content_type='application/pdf')

def deleteFileFromBucket(bucket_name, file_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.delete()
    print("File {} deleted from {}.".format(file_name, bucket_name))

def deleteBlobFromBucket(blob_list):
    for blob in blob_list:
        print(blob.name)
        blob.delete()

def asyncDetectDocument(gcs_source_uri, gcs_destination_uri):
    mime_type = "application/pdf"

    batch_size = 2

    client = vision.ImageAnnotatorClient()

    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source = vision.GcsSource(uri=gcs_source_uri)
    input_config = vision.InputConfig(gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size
    )

    async_request = vision.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config, output_config=output_config
    )

    operation = client.async_batch_annotate_files(requests=[async_request])

    print("Waiting for the operation to finish.")
    operation.result(timeout=420)

    storage_client = storage.Client()

    match = re.match(r"gs://([^/]+)/(.+)", gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    blob_list = [
        blob
        for blob in list(bucket.list_blobs(prefix=prefix))
        if not blob.name.endswith("/")
    ]
    # print("Output files:")

    result = ''
    for output in blob_list:
        json_string = output.download_as_bytes().decode("utf-8")
        response = json.loads(json_string)

        for page in response['responses']:
            result += page['fullTextAnnotation']['text']

    deleteBlobFromBucket(blob_list)
    # print("Full text:\n")
    # print(result)
    return result