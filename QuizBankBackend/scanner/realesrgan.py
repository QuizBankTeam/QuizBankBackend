from QuizBankBackend.scanner.RealESRGAN.inference_realesrgan import imageEnhance

def imageEnhanceWrapper(base64String):
    result = imageEnhance(base64String)
    return result