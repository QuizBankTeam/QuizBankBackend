from QuizBankBackend import app
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt


@app.after_request
def refreshExpireJWTs(response):
    print(response)
    print(type(response))
    return response
    # try:
    #     expTime = get_jwt()['exp']
    #     now = datetime.now(timezone.utc)
    #     if expTime - now <= timedelta(minutes=10):
             
