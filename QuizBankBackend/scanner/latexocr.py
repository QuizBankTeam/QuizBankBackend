import io
from PIL import Image
from pix2tex.cli import LatexOCR


def imageToLatex(image):
    image = Image.open(io.BytesIO(image))
    model = LatexOCR()
    # print(model(image))
    return model(image)