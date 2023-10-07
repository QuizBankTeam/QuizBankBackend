from QuizBankBackend import config
from datetime import timedelta


DEBUG = True
WTF_CSRF_TIME_LIMIT = 86400
# SECRET_KEY = os.urandom(24)
SECRET_KEY = config['SecretKey']
# SESSION_COOKIE_SECURE = True
JWT_SECRET_KEY = config['SecretKey']
# JWT_COOKIE_SECURE = True
JWT_TOKEN_LOCATION = ['cookies']
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
JWT_COOKIE_CSRF_PROTECT = False

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'quizbank401@gmail.com'
MAIL_PASSWORD = config['GmailAppPassword']
MAIL_USE_TLS = True
