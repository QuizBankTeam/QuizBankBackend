from QuizBankBackend import api
from QuizBankBackend.user.resource import *


api.add_resource(UserProfileResource, '/profile')
api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(RefreshTokenResource, '/refresh')
api.add_resource(ResetPasswordResource, '/resetPassword', endpoint='api.resetPassword')
api.add_resource(ForgotPasswordResource, '/forgotPassword')
api.add_resource(VerifyTokenResource, '/verifyToken/<string:token>', endpoint='api.verifyToken')