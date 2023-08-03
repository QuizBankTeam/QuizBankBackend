from importlib.resources import path
import os,io
from google.cloud import vision
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import pandas as pd
import layoutparser as lp
import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import time
import cv2
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="your path"
client = vision.ImageAnnotatorClient()


# 發送 OCR 請求，並指定文字檢測參數
import argparse
from enum import Enum

from PIL import Image, ImageDraw, ExifTags

class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

def hough():
    img = cv2.imread("outputResize.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    lines = cv2.HoughLinesP(thresh, 1, np.pi/180, 100, minLineLength=1, maxLineGap=100)#為甚麼用HoughLineP因為它為Hough的優化 第二個參數為rho pi/180為了找出所有的角度
    slopes = []
    # 創建一個空的字典來存儲每個 y 座標的直線數量
    line_density = {}

    # 準備一個空的圖片用於顯示偵測到的直線
    line_img = np.zeros(img.shape, dtype=np.uint8)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (y2 - y1) / (x2 - x1)
        slopes.append(slope)
        cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # 對每一條線，增加它覆蓋的 y 座標的直線數量
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if y not in line_density:
                line_density[y] = 0
            line_density[y] += 1
    cv2.imwrite('Detected Lines.jpg', line_img)
    # Calculate the median slope
    median_slope = np.median(slopes) #找最大透過中位數
    angle = np.arctan(median_slope) * 180 / np.pi
    height, width = img.shape[:2]
    center = (width / 2, height / 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (width, height), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    cv2.imshow('Original Image', img)
    cv2.imshow('Rotated Image', rotated)
    return rotated

def resize_image(input_image_path, output_image_path, size):
    img = Image.open(input_image_path)

    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break

    try :
        exif = dict(img._getexif().items())

        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)
    except:
        print("no rotate")
    

    w, h = img.size
    new_height = h * size // w
    img = img.resize((size, new_height))

    img.save(output_image_path)




def detectBoundByEastWithHighWidth():
    image = cv2.imread("outputResize.png")
    orig = image.copy()
    (H, W) = image.shape[:2]
    ratio = int(W/H)
   #要320的倍數
    (newW, newH) = (320*ratio, 320) 
    rW = W / float(newW)
    rH = H / float(newH)

   
    image = cv2.resize(image, (newW, newH))

    (H, W) = image.shape[:2]
    layerNames = [
	"feature_fusion/Conv_7/Sigmoid",
	"feature_fusion/concat_3"]
    print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet("frozen_east_text_detection.pb")
    
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
        (123.68, 116.78, 103.94), swapRB=True, crop=False)
    start = time.time()
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    end = time.time()
   
    print("[INFO] text detection took {:.6f} seconds".format(end - start))
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    # 跑一個loop迴圈
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the geometrical
        # data used to derive potential bounding box coordinates that
        # surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]
        for x in range(0, numCols):
		# if our score does not have sufficient probability, ignore it
            if scoresData[x] < 0.6:
                continue
            # compute the offset factor as our resulting feature maps will
            # be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            # extract the rotation angle for the prediction and then
            # compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)
            # use the geometry volume to derive the width and height of
            # the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]
            # compute both the starting and ending (x, y)-coordinates for
            # the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)
            # add the bounding box coordinates and probability score to
            # our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)
        # draw the bounding box on the image
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)
    # show the output image
    cv2.imshow("Text Detection", orig)
    cv2.waitKey(0)

def detectBoundByEast():
    image = cv2.imread("outputResize.png")
   
    orig = image.copy()
    (H, W) = image.shape[:2]
   
   #要320的倍數
    (newW, newH) = (960, 640) 
    rW = W / float(newW)
    rH = H / float(newH)

   
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]
    layerNames = [
	"feature_fusion/Conv_7/Sigmoid",
	"feature_fusion/concat_3"]
    print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet("frozen_east_text_detection.pb")
    
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
        (123.68, 116.78, 103.94), swapRB=True, crop=False)
    start = time.time()
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    end = time.time()
   
    print("[INFO] text detection took {:.6f} seconds".format(end - start))
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    # 跑一個loop迴圈
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the geometrical
        # data used to derive potential bounding box coordinates that
        # surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]
        for x in range(0, numCols):
		# if our score does not have sufficient probability, ignore it
            if scoresData[x] < 0.5:
                continue
            # compute the offset factor as our resulting feature maps will
            # be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            # extract the rotation angle for the prediction and then
            # compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)
            # use the geometry volume to derive the width and height of
            # the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]
            # compute both the starting and ending (x, y)-coordinates for
            # the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)
            # add the bounding box coordinates and probability score to
            # our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)
        # draw the bounding box on the image
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)
    # show the output image
    cv2.imshow("Text Detection", orig)
    cv2.waitKey(0)


def draw_boxes(image, bounds, color):
    """Draws a border around the image using the hints in the vector list.

    Args:
        image: the input image object.
        bounds: list of coordinates for the boxes.
        color: the color of the box.

    Returns:
        An image with colored bounds added.
    """
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        draw.polygon(
            [
                bound.vertices[0].x,
                bound.vertices[0].y,
                bound.vertices[1].x,
                bound.vertices[1].y,
                bound.vertices[2].x,
                bound.vertices[2].y,
                bound.vertices[3].x,
                bound.vertices[3].y,
            ],
            None,
            color,
        )
    return image
def detectText(img, feature):
    with io.open(img,'rb') as image_file:
        content = image_file.read()
    image=vision_v1.types.Image(content=content)
    response = client.text_detection(image=image)
    document = response.full_text_annotation
    bounds = []
    texts=response.text_annotations
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if feature == FeatureType.SYMBOL:
                            bounds.append(symbol.bounding_box)

                    if feature == FeatureType.WORD:
                        bounds.append(word.bounding_box)

                if feature == FeatureType.PARA:
                    bounds.append(paragraph.bounding_box)

            if feature == FeatureType.BLOCK:
                bounds.append(block.bounding_box)
    return bounds  




    

def render_doc_text(filein, fileout):
    """Outlines document features (blocks, paragraphs and words) given an image.

    Args:
        filein: path to the input image.
        fileout: path to the output image.
    """
    image = Image.open(filein)
    # bounds = detectText(filein, FeatureType.BLOCK)
    # draw_boxes(image, bounds, "blue")
    bounds = detectText(filein, FeatureType.PARA)
    draw_boxes(image, bounds, "red")
   
    # bounds = detectText(filein, FeatureType.WORD)
    # draw_boxes(image, bounds, "yellow")

    if fileout != 0:
        image.save(fileout)
        
    else:
        image.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
   
    parser.add_argument("-c", "--min-confidence", type=float, default=0.5,
        help="minimum probability required to inspect a region")
    
    parser.add_argument("-out_file", help="Optional output file", default=0)
    args = parser.parse_args()
    # render_doc_text(os.path.abspath('C:\\Users\\0524e\\Desktop\\anaconda\\visonAPI\\question.png'), args.out_file)
    resize_image(os.path.abspath('C:\\Users\\0524e\\Desktop\\anaconda\\visonAPI\\question.png'),"outputResize.png",960)
   
    detectBoundByEast()
    detectBoundByEastWithHighWidth()
    hough()
    render_doc_text(os.path.abspath('C:\\Users\\0524e\\Desktop\\anaconda\\visonAPI\\outputResize.png'), args.out_file)

    