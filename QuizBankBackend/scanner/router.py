from QuizBankBackend import api
from QuizBankBackend.scanner.resource import *


api.add_resource(ScannerResource, '/scanner')
