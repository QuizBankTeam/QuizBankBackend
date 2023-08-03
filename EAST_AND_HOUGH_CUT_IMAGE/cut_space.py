import numpy as np
import cv2

def hough():
    img = cv2.imread("test.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    lines = cv2.HoughLinesP(thresh, 1, np.pi/180, 100, minLineLength=1, maxLineGap=100)

    line_img = np.zeros(img.shape, dtype=np.uint8)
    line_density = {}

    # 每條線的平均 y 座標
    avg_y = [(line[0][1] + line[0][3]) / 2 for line in lines]

   
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # 對每一條線，增加它覆蓋的 y 座標的直線數量
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if y not in line_density:
                line_density[y] = 0
            line_density[y] += 1
    cv2.imwrite('Detected space Lines.jpg', line_img)
     # 按照平均 y 座標排序
    lines = [tuple(line[0]) for line in lines] 
    lines_sorted = [x for _,x in sorted(zip(avg_y, lines))]

    # 切割圖片
    split_positions = [0] # 從頂部開始切割

    i = 0
    while i < len(lines_sorted) - 1:
        _, curr_y1, _, curr_y2 = lines_sorted[i]
        curr_y_avg = (curr_y1 + curr_y2) / 2

        j = i + 1
        _, next_y1, _, next_y2 = lines_sorted[j]
        next_y_avg = (next_y1 + next_y2) / 2

        while j < len(lines_sorted) - 1 and abs(curr_y_avg - next_y_avg) < 60:
            j += 1
            _, next_y1, _, next_y2 = lines_sorted[j]
            next_y_avg = (next_y1 + next_y2) / 2

        if j < len(lines_sorted):  # Ensure we're not at the end
            split_positions.append(int(next_y_avg))
        i = j

    split_positions.append(img.shape[0]) # 到底部結束切割

    for i in range(len(split_positions) - 1):
        split_img = img[split_positions[i]:split_positions[i+1], :]
        cv2.imwrite(f'split_{i}.png', split_img)


hough()
