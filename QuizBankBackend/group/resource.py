import uuid, logging
from QuizBankBackend.db import db
from QuizBankBackend.group.form import *
from QuizBankBackend.utility import setResponse, formFieldError, isBase64
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

            if isBase64(formJson['avatar']) is False and formJson['avatar'] is not None and formJson['avatar'] != "":
                response = setResponse(400, 'Avatar is not base64.')
                return response

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
            return formFieldError(form)

    @jwt_required()
    def put(self):
        formJson = request.get_json()
        form = PutGroupForm.from_json(formJson)

        if form.validate():
            group = db.groups.find_one({'_id': formJson['groupId']})

            if group is None:
                response = setResponse(404, 'Group does not existed.')
                return response
            else:
                if isBase64(formJson['avatar']) is False and formJson['avatar'] is not None and formJson['avatar'] != "":
                    response = setResponse(400, 'Avatar is not base64.')
                    return response

                if get_jwt_identity() == group['creator']:
                    formJson['_id'] = formJson['groupId']
                    del formJson['groupId']
                    db.groups.update_one(
                        {'_id': formJson['_id']},
                        {'$set': formJson}
                    )

                    response = setResponse(
                        200,
                        'Update group successfully.',
                        'group',
                        formJson
                    )
                    return response
                else:
                    response = setResponse(403, 'Permission denied.')
                    return response
        else:
            return formFieldError(form)

    @jwt_required()
    def delete(self, groupId):
        db.groups.delete_one({'_id': groupId})

        response = setResponse(200, 'Delete group successfully.')
        return response
