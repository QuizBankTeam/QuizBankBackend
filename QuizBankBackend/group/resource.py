import uuid, logging
from QuizBankBackend.db import db
from QuizBankBackend.group.form import *
from QuizBankBackend.utility import setResponse
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity


class GroupResource(Resource):
    def get(self, groupId):
        group = db.groups.find_one({'_id': groupId})

        if group is None:
            response = setResponse(404, 'Group does not existed.')
            return response
        else:
            response = setResponse(
                200,
               'Get group successfully',
               'group',
               group
            )
            return response

    @jwt_required()
    def post(self):
        formJson = request.get_json()
        form = PostGroupForm.from_json(formJson)

        if form.validate():
            formJson['creator'] = get_jwt_identity()
            formJson['_id'] = str(uuid.uuid4())
            formJson['members'].append(formJson['creator'])

            db.groups.insert_one(formJson)

            response = setResponse(
                201,
                'Create group successfully.',
                'group',
                formJson
            )
            return response
        else:
            for field, error in form.errors.items():
                message = f'Field: {field}, Error: {error}'
                logging.error(message)
                response = setResponse(400, message)
                return response
