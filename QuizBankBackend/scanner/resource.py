import random
import string
from QuizBankBackend.scanner.form import *
from QuizBankBackend.db import db
from QuizBankBackend.utility import setResponse, formFieldError
from QuizBankBackend.scanner.api import *
from QuizBankBackend.scanner.hough import *
from QuizBankBackend.scanner.realesrgan import *
from QuizBankBackend.scanner.latexocr import imageToLatex
from QuizBankBackend import limiter
from flask import request, Response
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

        return formFieldError(form)

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

        return formFieldError(form)

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

        return formFieldError(form)

    @jwt_required()
    def delete(self, imageId, deletehash):
        result = db.photos.delete_one({'deletehash': deletehash})

        if result.deleted_count == 0:
            response = setResponse(404, 'Image not found.')
            return response

        deleteImage(deletehash)
        response = setResponse(200, 'Delete image successfully.')
        return response

class HoughRotateResource(Resource):
    @jwt_required()
    def post(self):
        form = HoughRotateForm()

        if form.validate():
            file = request.files['image']
            jpegContents = file.read()
            file.close()
            try:
                image = houghRotate(jpegContents)
            except Exception as e:
                response = setResponse(400, str(e))
                return response

            response = Response(image, content_type='image/jpeg')

            return response

        return formFieldError(form)

class RealESRGANResource(Resource):
    @jwt_required()
    # @limiter.limit('1/minute')
    def post(self):
        form = RealESRGANForm()

        if form.validate():
            file = request.files['image']
            jpegContents = file.read()
            file.close()
            try:
                image = imageEnhanceWrapper(jpegContents)
                if image == 'Image is too big.':
                    response = setResponse(413, image)
                    return response

                response = Response(image, content_type='image/jpeg')
            except Exception as e:
                response = setResponse(406, str(e))
                return response

            return response

        return formFieldError(form)
    
class LatexOCRResource(Resource):
    @jwt_required()
    def post(self):
        form = LatexOCRForm()

        if form.validate():
            file = request.files['image']
            jpegContents = file.read()
            file.close()
            try:
                latex = imageToLatex(jpegContents)
            except Exception as e:
                response = setResponse(406, str(e))
                return response

            response = setResponse(200, 'Convert image to latex successfully.', 'latex', latex)
            return response

        return formFieldError(form)