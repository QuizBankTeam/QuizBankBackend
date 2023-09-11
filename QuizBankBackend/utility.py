import logging, base64
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

def formFieldError(form):
    for field, error in form.errors.items():
        message = f'Field: {field}, Error: {error}'
        logging.error(message)
        response = setResponse(400, message)
        return response

def isBase64(s):
    try:
        return base64.b64encode(base64.b64decode(s)) == s
    except Exception:
        return False
