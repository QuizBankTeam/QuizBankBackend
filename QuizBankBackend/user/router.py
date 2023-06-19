from QuizBankBackend import api
from QuizBankBackend.user.resource import *

api.add_resource(UserProfileResource, '/profile')
api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')