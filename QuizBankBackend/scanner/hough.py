import base64
import cv2
import numpy as np

def readb64(base64String):
    imageString = base64.b64decode(base64String)
    nparray = np.fromstring(imageString, np.uint8)
    image = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
    return image

def writeb64(image):
    base64String = cv2.imencode('.jpg', image)[1].tostring()
    base64String = base64.b64encode(base64String).decode('utf-8')
    return base64String

def houghRotate(base64_string):
    img = readb64(base64_string)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    lines = cv2.HoughLinesP(thresh, 1, np.pi/180, 100, minLineLength=1, maxLineGap=100)#為甚麼用HoughLineP因為它為Hough的優化 第二個參數為rho pi/180為了找出所有的角度
    slopes = []

    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (y2 - y1) / (x2 - x1)
        slopes.append(slope)

    median_slope = np.median(slopes)
    angle = np.arctan(median_slope) * 180 / np.pi
    height, width = img.shape[:2]
    center = (width / 2, height / 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (width, height), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return writeb64(rotated)