import cv2
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
def hough():
    img = cv2.imread("test.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    lines = cv2.HoughLinesP(thresh, 1, np.pi/180, 100, minLineLength=1, maxLineGap=100)
    # 創建一個空的字典來存儲每個 y 座標的直線數量
    line_density = {}

    # 準備一個空的圖片用於顯示偵測到的直線
    line_img = np.zeros(img.shape, dtype=np.uint8)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # 對每一條線，增加它覆蓋的 y 座標的直線數量
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if y not in line_density:
                line_density[y] = 0
            line_density[y] += 1
    cv2.imwrite('Detected dbscan Lines.jpg', line_img)

    # 將線的兩點座標換算成中心點的 y 座標
    centers = [(line[0][1] + line[0][3]) / 2 for line in lines]

    # 使用 DBSCAN 來分組這些中心點
    dbscan = DBSCAN(eps=11, min_samples=2) # 這裡的 eps 參數是兩條線被認為是一條線的最大距離
    labels = dbscan.fit_predict(np.array(centers).reshape(-1, 1))

    # 計算每一組的範圍
    ranges = []
    for label in set(labels):
        indices = np.where(labels == label)[0]
        ranges.append((min(centers[i] for i in indices), max(centers[i] for i in indices)))

    # 在原始圖片上畫出每一組的範圍
    for i, (y1, y2) in enumerate(ranges):
        roi = img[int(y1):int(y2), :]
        cv2.imwrite(f'dbscan_{i}.jpg', roi)

   

hough()
