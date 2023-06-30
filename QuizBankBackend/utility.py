from flask import jsonify, make_response 


def setResponse(code: int, message: str, data_str: str = None, data: dict = None):
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
        data_str: data
    }))
    response.status_code = code
    return response
