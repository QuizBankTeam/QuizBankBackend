from QuizBankBackend.scanner.Real_ESRGAN.inference_realesrgan import imageEnhance

def imageEnhanceWrapper(base64String):
    result = imageEnhance(base64String)
    return result