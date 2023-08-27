import uuid
from QuizBankBackend.db import db
from QuizBankBackend.quizRecord.form import *
from QuizBankBackend.utility import setResponse
from QuizBankBackend.constant import *
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity


class AllQuizRecordResource(Resource):
    @jwt_required()
    def get(self):
        quizRecordType = request.args.get('quizRecordType')
        if quizRecordType in QUIZ_RECORD_TYPE:
            userId = get_jwt_identity()
            recordFilter = {'type': quizRecordType, 'members': {"$in" : [userId]}}
            quizRecords = list(db.quizRecords.find(recordFilter))

            if quizRecords is None:
                response = setResponse(404, 'quiz Record not found.')
                return response

            response = setResponse(
                200,
                'Get all quiz records successfully.',
                'quizRecordList',
                quizRecords
            )
            return response
        else:
            response = setResponse(400, 'Failed to get all quiz records.')
            return response
        
class QuizRecordResource(Resource):
    def get(self): 
        quizRecordId = request.args.get('quizRecordId')
        quizRecordFilter = {'_id': quizRecordId}
        quizRecord = db.quizRecords.find_one(quizRecordFilter)
        questionIds = []
        questions = []
        if quizRecordId is None:
            response = setResponse(400, 'Failed to get quizRecord.')
            return response
        if quizRecord is None:
            response = setResponse(404, 'Quiz Record not found.')
            return response
        
        questionRecordFilter = {'_id': {"$in" :  quizRecord['questionRecords']}}
        questionRecords = list(db.questionRecords.find(questionRecordFilter))

        del quizRecord['questionRecords']
        quizRecord['questionRecords'] = questionRecords

        response = setResponse(
            200,
            'Get quiz record successfully.',
            'quizRecord',
            quizRecord
        )
        return response

    @jwt_required()
    def post(self):
        formJson = request.get_json()
        form = PostQuizRecordForm.from_json(formJson)
        questionRecordIDs = []
        if form.validate():
            quizRecordId = str(uuid.uuid4())
            formJson['_id'] = quizRecordId
            
            for questionRecord in formJson['questionRecords']:
                questionRecord['quizRecord'] = quizRecordId
                questionRecord['_id'] = str(uuid.uuid4())
                questionRecord['question']['_id'] = str(uuid.uuid4())
                questionRecordIDs.append(questionRecord['_id'])

            db.questionRecords.insert_many(formJson['questionRecords'])
            del formJson['questionRecords']
            formJson['questionRecords'] = questionRecordIDs
            db.quizRecords.insert_one(formJson)
            response = setResponse(200, 'Add quizRecord successfully')
            return response
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field: {field}, Error: {error}")
            response = setResponse(
                400, 'Failed to add quizRecord.')
            return response

    @jwt_required()
    def delete(self): 
        quizRecordId = request.args.get('quizRecordId')
        
        if quizRecordId is None:
            response = setResponse(
            400, 'Failed to delete quizRecord.')
            return response

        quizRecordFilter = {'_id': quizRecordId}
        questionRecordFilter = {'quizRecord': quizRecordId}
        result = db.quizRecords.delete_one(quizRecordFilter)
        deleteNumbers = db.questionRecords.delete_many(questionRecordFilter)
        if result.deleted_count==0:
            response = setResponse(
            404, 'the quiz record that request to delete was not found.')
            return response
        else:
            print(f'delete question record numbers is{deleteNumbers}')
            response = setResponse(
                200, 'delete quiz record successfully.')
            return response