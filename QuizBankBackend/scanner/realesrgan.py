from QuizBankBackend.scanner.Real_ESRGAN.inference_realesrgan import imageEnhance

def imageEnhanceWrapper(imageBytes):
    return imageEnhance(imageBytes)