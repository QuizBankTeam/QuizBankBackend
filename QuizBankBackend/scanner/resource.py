import random
import string
from QuizBankBackend.scanner.form import *
from QuizBankBackend.db import db
from QuizBankBackend.utility import setResponse
from QuizBankBackend.scanner.api import *
from QuizBankBackend.scanner.hough import *
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from google.cloud import vision


class ScannerResource(Resource):
    @jwt_required()
    def post(self):
        formJson = request.get_json()
        form = OCRForm.from_json(formJson)

        if form.validate():
            try:
                client = vision.ImageAnnotatorClient()
                content = formJson['image']
                image = vision.Image(content=content)
                result = client.text_detection(image=image)
                text = result.text_annotations[0].description

            except Exception as e:
                response = setResponse(400, str(e))
                return response

            response = setResponse(200, 'Detect text Successfully.', 'text', text)
            return response

        response = setResponse(400, 'Failed to detect text.')
        return response

class DocumentScannerResource(Resource):
    @jwt_required()
    def post(self):
        formJson = request.get_json()
        form = DocumentOCRForm.from_json(formJson)

        if form.validate():
            try:
                name = ''.join(random.choice(string.ascii_letters) for x in range(random.randint(1,32)))
                fileName = f'{name}.pdf'
                uploadFileToBucket('quizbank', fileName, formJson['document'])
                text = asyncDetectDocument(f'gs://quizbank/{fileName}', f'gs://quizbank/{name}.json')
                deleteFileFromBucket('quizbank', fileName)

            except Exception as e:
                response = setResponse(400, str(e))
                return response

            response = setResponse(200, 'Detect text Successfully.', 'text', text)
            return response

        response = setResponse(400, 'Failed to detect text.')
        return response

class AllImgurPhotoResource(Resource):
    @jwt_required()
    def get(self):
        userId = get_jwt_identity()
        images = db.photos.find({'owner': userId})
        if images is not None:
            response = setResponse(200, 'Get all images successfully.', 'images', list(images))
            return response

        response = setResponse(404, 'Images not found.')
        return response

class ImgurPhotoResource(Resource):
    def get(self, imageId):
        image = db.photos.find_one({'_id': imageId})
        if image is None:
            response = setResponse(404, 'Image not found.')
            return response
        response = setResponse(200, 'Get image successfully', 'image', image)
        return response

    @jwt_required()
    def post(self):
        formJson = request.get_json()
        form = PostImgurPhotoForm.from_json(formJson)

        if form.validate():
            imgurRes = uploadImage(formJson['image'])
            if imgurRes['status'] == 200:
                image = imgurRes['data']
                ownerId = get_jwt_identity()
                imageId = image['id']
                db.photos.insert_one({
                    '_id': imageId,
                    'owner': ownerId,
                    'link': image['link'],
                    'deletehash': image['deletehash']
                })
                response = setResponse(201, 'Upload an image successfully.')
                return response
            response = setResponse(imgurRes['status'], 'Something wrong when you access imgur.')
            return response

        response = setResponse(400, 'Failed to upload image.')
        return response

    @jwt_required()
    def delete(self, imageId, deletehash):
        db.photos.delete_one({'deletehash': deletehash})
        deleteImage(deletehash)
        response = setResponse(200, 'Delete image successfully.')
        return response
    
class HoughRotateResource(Resource):
    @jwt_required()
    def post(self):
        formJson = request.get_json()
        form = HoughRotateForm.from_json(formJson)

        if form.validate():
            try:
                b64Image = formJson['image']
                image = houghRotate(b64Image)
            except Exception as e:
                response = setResponse(400, str(e))
                return response

            response = setResponse(200, 'Rotate image successfully.', 'image', image)
            return response

        response = setResponse(400, 'Failed to rotate image.')
        return response