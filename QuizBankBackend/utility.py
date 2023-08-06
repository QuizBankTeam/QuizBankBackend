from flask import jsonify, make_response 


def setResponse(code: int, message: str, name: str = None, data = None):
    if data is None:
        response = make_response(jsonify({
            'status': code,
            'message': message,
        }))
        response.status_code = code
        return response

    response = make_response(jsonify({
        'status': code,
        'message': message,
        name: data
    }))
    response.status_code = code
    return response
