import cv2
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
def hough():
    img = cv2.imread("outputResize.png")
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
    cv2.imwrite('Detected kmeans Lines.jpg', line_img)
    # 當前的線中心點
    centers = np.array([(line[0][1] + line[0][3]) / 2 for line in lines]).reshape(-1, 1)

    # 預設問題數量
    n_clusters = 4

    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(centers)

    # 每一個問題的範圍
    ranges = []
    for i in range(n_clusters):
        indices = np.where(kmeans.labels_ == i)[0]
        ranges.append((min(centers[i] for i in indices), max(centers[i] for i in indices)))

    # 分割每一個問題
    for i, (y1, y2) in enumerate(ranges):
        roi = img[int(y1):int(y2), :]
        cv2.imwrite(f'kmean_{i}.jpg', roi)

hough()
