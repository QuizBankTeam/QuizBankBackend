import uuid
from QuizBankBackend.db import db
from QuizBankBackend.questionSet.form import *
from QuizBankBackend.utility import setResponse, formFieldError
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity


class QuestionSetResource(Resource):
    def get(self, questionSetId):
        questionSet = db.questionSets.find_one({'_id': questionSetId})

        if questionSet is None:
            response = setResponse(404, 'Question set not found.')
            return response

        response = setResponse(
            200, 'Get question set successfully.', 'questionSet', questionSet)
        return response


    @jwt_required()
    def post(self):
        formJson = request.get_json()
        form = PostQuestionSetForm.from_json(formJson)

        if form.validate():
            bank = db.questionBanks.find_one({'_id': formJson['questionBank']})
            originateFrom = db.users.find_one({'_id': formJson['originateFrom']})

            if bank is None:
                response = setResponse(400, 'Question bank of set does not existed.')
                return response
            elif originateFrom is None:
                response = setResponse(400, 'Original user of set does not existed.')
                return response

            questionSetId = str(uuid.uuid4())
            formJson['_id'] = questionSetId
            formJson['provider'] = get_jwt_identity()

            for question in formJson['questions']:
                bank = db.questionBanks.find_one({'_id': formJson['questionBank']})
                originateFrom = db.users.find_one({'_id': formJson['originateFrom']})

                if bank is None:
                    response = setResponse(400, 'Question bank of quesiton does not existed.')
                    return response
                elif originateFrom is None:
                    response = setResponse(400, 'Original user of question does not existed.')
                    return response

                question['_id'] = str(uuid.uuid4())
                question['provider'] = get_jwt_identity()

            db.questionSets.insert_one(formJson)
            response = setResponse(201,
                                   'Add question set successfully!',
                                   'questionSet',
                                   formJson)
            return response

        return formFieldError(form)

    @jwt_required()
    def put(self):
        formJson = request.get_json()
        form = PutQuestionSetForm.from_json(formJson)

        if form.validate():
            filter = {'_id': formJson['questionSetId']}
            newQuestionSet = {'$set': formJson}
            db.questionSets.update_one(filter, newQuestionSet)
            questionSet = db.questionSets.find_one(filter)
            response = setResponse(200,
                                   'Update question set successfully.',
                                   'questionSet',
                                   questionSet)
            return response

        return formFieldError(form)

    @jwt_required()
    def delete(self, questionSetId):

        result = db.questionSets.delete_one({'_id': questionSetId})

        if result.deleted_count == 0:
            response = setResponse(400, 'Question set does not existed.')
            return response

        response = setResponse(200, 'Delete question set successfully.')
        return response
