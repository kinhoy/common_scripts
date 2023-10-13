import cv2
import numpy as np
from matplotlib import pyplot as plt

# img = cv2.imread('84.jpg')
img = cv2.imread('img_0.jpg')
# img.shape[0]：图像的垂直尺寸（高度）
# img.shape[1]：图像的水平尺寸（宽度）
copy = img.copy()
kernel = np.ones((48, 48), dtype=np.uint8)
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, 4)

img2 = cv2.pyrDown(opening)
print(f"原图宽度:{img.shape[1]}-新图宽度:{img2.shape[1]}")
print(f"原图高度:{img.shape[0]}-新图高度:{img2.shape[0]}")

k = img.shape[1] /img2.shape[1]
main_s = img2.shape[0]*img2.shape[1]
print(f"原图面积为 {main_s}")
ret, thresh = cv2.threshold(cv2.cvtColor(img2.copy(), cv2.COLOR_BGR2GRAY) , 127, 255, cv2.THRESH_BINARY)
contours,_ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
max_cut_rect_width = 0
max_rect_center = 0
for c in contours:
    rect = cv2.minAreaRect(c)
    # rect[1][0] 宽
    # rect[1][1] 高
    if rect[2] >= 45:
        continue
    hal_width = img2.shape[1]/2
    if rect[1][0] < hal_width:
        continue
    if rect[1][0]*rect[1][1]>0.9*main_s:
        continue
    print(20*"*")
    print(f"矩形宽度{int(rect[1][0])}--{img2.shape[1]}")
    print(f"矩形角度{int(rect[2])}")
    print(f"矩形中心 X:{rect[0][0]} Y:{rect[0][1]}")
    tmp = max(max_cut_rect_width,int(rect[1][0]))
    if max_cut_rect_width != tmp:
        # 更新最大矩形中心位置
        max_rect_center = int(rect[0][0])
        max_cut_rect_width = tmp
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img2, [box], 0, (0,0, 255), 3)
    cv2.putText(img2, str(int(rect[1][0])), (int(rect[0][0]),int(rect[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 10)
print(20*"#")
print(f"最大矩形宽度{max_cut_rect_width}")
print(f"图片中心X:{img2.shape[1]//2}")
print(f"最小裁剪矩形中心X:{max_rect_center}")

# 设置字体内容离边缘的宽度
white_side_width = 60
x_tmp = max_rect_center-max_cut_rect_width//2
# 左上角横坐标
x0 = x_tmp-white_side_width if x_tmp-white_side_width>0 else x_tmp
x_tmp = max_rect_center+max_cut_rect_width//2
# 右上角横坐标
x1 = x_tmp+white_side_width if x_tmp+white_side_width>0 else x_tmp
# 换算成原图比例坐标
x0 = int(k*x0)
x1 = int(k*x1)
print(f"x0为{x0}--x1为{x1}")
# 开始裁剪图片
cut_part = copy[0:copy.shape[0],x0:x1]

plt.subplot(141), plt.imshow(copy), plt.title('Original')
plt.xticks([]), plt.yticks([])

plt.subplot(142), plt.imshow(opening), plt.title('opening')
plt.xticks([]), plt.yticks([])

plt.subplot(143), plt.imshow(img2), plt.title('rect')
plt.xticks([]), plt.yticks([])

plt.subplot(144), plt.imshow(cut_part), plt.title('cut_side')
plt.xticks([]), plt.yticks([])
plt.tight_layout()
plt.show()