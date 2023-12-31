from QuizBankBackend import api
from QuizBankBackend.scanner.resource import *


api.add_resource(ScannerResource, '/scanner')
api.add_resource(DocumentScannerResource, '/documentScanner')
api.add_resource(AllImgurPhotoResource, '/images')
api.add_resource(ImgurPhotoResource, '/image', '/image/<string:imageId>', '/image/<string:imageId>/<string:deletehash>')
api.add_resource(HoughRotateResource, '/imageRotate')
api.add_resource(RealESRGANResource, '/realesrgan')
api.add_resource(LatexOCRResource, '/latexocr')