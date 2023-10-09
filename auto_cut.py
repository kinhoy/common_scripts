# 将扫描书籍获得的双页单图 按照书缝线切割成两个部分
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import datetime


start_time = datetime.datetime.now()  # 开始时间
image = cv.imread("44.jpg")
print(f'裁剪之前的图片尺寸{image.shape}')
# img.shape[0]：图像的垂直尺寸（高度）
# img.shape[1]：图像的水平尺寸（宽度）
cut_width_left = 300
cut_width_right = 100
origin_width = image.shape[1]
origin_high = image.shape[0]
# 裁剪坐标为[y0:y1, x0:x1]
central_line_part = image[0:origin_high, origin_width//2-cut_width_left:origin_width//2+cut_width_right]

offset_left = origin_width//2-cut_width_left

print(f'裁剪之后的图片尺寸{central_line_part.shape}')
copy = central_line_part.copy()
width = central_line_part.shape[1]
high = central_line_part.shape[0]
gray_img = cv.cvtColor(central_line_part, cv.COLOR_BGR2GRAY)
kernel = np.ones((32, 32), dtype=np.uint8)
opening = cv.morphologyEx(gray_img, cv.MORPH_OPEN, kernel, 2)
canny = cv.Canny(opening,50,200,3)
lines = cv.HoughLines(canny,1,np.pi/180,220)

x1 = 0
y1 = 0
x2 = 0
y2 = 0
for i in range(0, len(lines)):
    rho, theta = lines[i][0][0], lines[i][0][1]
    print(f"角度为{theta}")
    if theta == 0:
        continue
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 10000 * (-b))
    y1 = int(y0 + 10000 * (a))
    x2 = int(x0 - 10000 * (-b))
    y2 = int(y0 - 10000 * (a))
    print(f"{x1}:{y1} 切割直线的两点坐标 {x2}:{y2}")
    cv.line(copy, (x1, y1), (x2, y2), (0, 255, 0), 8)
    break
# 书缝线可能为垂直线 即theta=0.0
# 直线斜率 
k = 0
b = 0
if theta != 0:
    k = (y2-y1)/(x2-x1)
    b = y1 - k * x1
    b2 = y2 - k * x2

print(f"斜率为{k}  b为{b} b2为{b}")


# 待修改 需要考虑斜率正负问题


# mk = -1 / np.tan(theta)
# mb = rho * np.sin(theta)
# print(f"斜率为{mk}  b为{mb}")

up = np.zeros((high, width, 3), dtype='uint8')
down = np.zeros((high, width,3), dtype='uint8')   # 黑底, 一定要加uint8
# print(f"宽为{width}  高为{high}")

# 开始小图切割
for i in range(width):
    for j in range(high):
        # print(f"{i},{j}------{i * k + b}")
        if (i * k + b) <= j:
            up[j,i] = copy[j,i]
        else:
            down[j,i] = copy[j,i]
# cv.imwrite('up.jpg',up)
# cv.imwrite('down.jpg',down)

# 开始大图切割     
new_y1 = high
new_x1 = int((new_y1-b)/k) + offset_left
new_y2 = 0
new_x2 = int((new_y2 - b)/k) + offset_left
new_b =new_y1 - k * new_x1
print(f"{new_x1}:{new_y1} 新的两点坐标 {new_x2}:{new_y2}")
new_up = np.zeros((origin_high, origin_width, 3), dtype='uint8')
new_down = np.zeros((origin_high, origin_width,3), dtype='uint8')   # 黑底, 一定要加uint8
for i in range(origin_width):
    for j in range(origin_high):
        # print(f"{i},{j}------{i * k + b}")
        if (i * k + new_b) <= j:
            new_up[j,i] = image[j,i]
        else:
            new_down[j,i] = image[j,i]

cut_width = 0
for i in range(origin_width):
    if not np.array_equal(new_down[0,i], [0, 0, 0]):
        cut_width = max(i,cut_width)
        # print(cut_width)
tmp_high = new_down.shape[0] - 1
for i in range(origin_width):
    if not np.array_equal(new_down[tmp_high,i], [0, 0, 0]):
        cut_width = max(i,cut_width)
        # print(cut_width)
print(f"最大切割宽度{cut_width}")
# 裁剪坐标为[y0:y1, x0:x1]
left_part = image[0:origin_high, 0:cut_width]

cut_width = origin_width
for i in range(origin_width-1,0,-1):
    if not np.array_equal(new_up[0,i], [0, 0, 0]):
        cut_width = min(i,cut_width)
        # print(cut_width)
tmp_high = origin_high - 1
for i in range(origin_width-1,0,-1):
    if not np.array_equal(new_up[tmp_high,i], [0, 0, 0]):
        cut_width = min(i,cut_width)
        # print(cut_width)
print(f"最小切割宽度{cut_width}")
# 裁剪坐标为[y0:y1, x0:x1]
right_part = image[0:origin_high, cut_width:origin_width]

end_time = datetime.datetime.now()  # 结束时间
print(f"切割成功,耗时{(end_time - start_time).seconds}秒.")

plt.subplot(241), plt.imshow(central_line_part), plt.title('Original_central_line_part')
plt.xticks([]), plt.yticks([])

plt.subplot(242), plt.imshow(copy), plt.title('opening')
plt.xticks([]), plt.yticks([])

plt.subplot(243), plt.imshow(up), plt.title('up')
plt.xticks([]), plt.yticks([])

plt.subplot(244), plt.imshow(down), plt.title('down')
plt.xticks([]), plt.yticks([])


plt.subplot(245), plt.imshow(new_up), plt.title('left')
plt.xticks([]), plt.yticks([])

plt.subplot(246), plt.imshow(new_down), plt.title('right')
plt.xticks([]), plt.yticks([])

plt.subplot(247), plt.imshow(left_part), plt.title('left_part')
plt.xticks([]), plt.yticks([])

plt.subplot(248), plt.imshow(right_part), plt.title('right_part')
plt.xticks([]), plt.yticks([])

plt.tight_layout()
plt.show()