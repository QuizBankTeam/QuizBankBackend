import base64
from QuizBankBackend.scanner.form import *
from QuizBankBackend.utility import setResponse
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required 
from google.cloud import vision


class ScannerResource(Resource):
    @jwt_required()
    def post(self):
        formJson = request.get_json()
        form = OCRForm.from_json(formJson)

        if form.validate():
            client = vision.ImageAnnotatorClient()
            content = formJson['image']
            image = vision.Image(content=content)
            result = client.text_detection(image=image)
            text = result.text_annotations[0].description

            response = setResponse(200, 'Detect text Successfully.', 'text', text)
            return response

        response = setResponse(400, 'Failed to detect text.')
        return response
