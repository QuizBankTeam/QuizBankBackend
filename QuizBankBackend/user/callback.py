from QuizBankBackend import mail, app
from QuizBankBackend.db import db
from datetime import (
    datetime,
    timedelta,
    timezone
)
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    set_access_cookies
)
from flask import url_for
from flask_mail import Message
from itsdangerous import TimedSerializer as Serializer


@app.after_request
def refreshExpireJWTs(response):
    try:
        expTime = get_jwt()['exp']
        now = datetime.now(timezone.utc)
        targetTimestamp = datetime.timestamp(now + timedelta(minutes=20))
        if targetTimestamp > expTime:
            userId = get_jwt_identity()
            token = create_access_token(identity=userId)
            set_access_cookies(response, token)
        return response
    except (RuntimeError, KeyError):
        return response

def getUserJWSToken(user: dict):
    serializer = Serializer(app.config['SECRET_KEY'])
    # print(type(serializer.dumps({'userId': user['_id']})))
    return serializer.dumps({'userId': user['_id']})

def verifyUserJWSToken(token: str):
    serializer = Serializer(app.config['SECRET_KEY'])
    try:
        userId = serializer.loads(token, max_age=300)['userId']
    except Exception as err:
        return err
    return db.users.find_one({'_id': userId})

def sendEmail(user: dict):
    token = getUserJWSToken(user)
    msg = Message('Confirm your email', recipients=[user['email']], sender='noreply@quizbank.com')
    msg.body = f'''To reset your password, visit the following link:
        {url_for('api.verifyToken', token=token, _external=True)}
        If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)
