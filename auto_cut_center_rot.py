import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import datetime
import cv2
import numpy as np
import os

def text_img_rotation_adjust(image):
    copy = image.copy()

    # 开运算：先腐蚀，在膨胀
    kernel = np.ones((32, 32), dtype=np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, 2)

    canny = cv2.Canny(image,50,200,3)
    # canny = cv2.Canny(image,300,700,3)
    lines = cv2.HoughLines(canny,1,np.pi/180,220)
    sum = 0.0
    count = 0
    # print(lines)
    for i in range(0, len(lines)):
        rho, theta = lines[i][0][0], lines[i][0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 10000 * (-b))
        y1 = int(y0 + 10000 * (a))
        x2 = int(x0 - 10000 * (-b))
        y2 = int(y0 - 10000 * (a))
        tmp_theta = theta / np.pi * 180
        # 排除干扰直线
        if tmp_theta < 80 or tmp_theta > 100:
            continue
        count = count + 1
        sum += theta
        # print(f"{theta} : {theta / np.pi * 180}")
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 1)
    # 计算平均旋转角度
    average = sum / count
    print("average: {}".format(average))
    #度数转换
    angle = average / np.pi * 180
    print("angle: {}".format(angle))
    angle = angle-90
    center = (image.shape[1] // 2, image.shape[0] // 2)
    rotMat = cv2.getRotationMatrix2D(center, angle, 1.0)
    # 用白色填充旋转后的图片周围
    cv_dst_img = cv2.warpAffine(copy, rotMat, (image.shape[1],image.shape[0]), borderValue=(255, 255, 255))
    return cv_dst_img

input = '41.jpg'
output_dir = './'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

image = cv.imread(input)

start_time = datetime.datetime.now()  # 开始时间
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

x1 = y1 = x2 = y2 = 0
for i in range(0, len(lines)):
    rho, theta = lines[i][0][0], lines[i][0][1]
    print(f"角度为{theta}")
    if theta == 0:
        # 书缝线可能为垂直线 即theta=0.0
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
# 直线斜率 
k = 0
# 直线截距
b = 0
if theta != 0:
    k = (y2-y1)/(x2-x1)
    b = y1 - k * x1
    b2 = y2 - k * x2
print(f"斜率为{k}  b为{b} b2为{b}")

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

# 无论k值正负 统一down在左 up在右边
if k > 0 :
    tmp_img = new_down
    new_down = new_up
    new_up = tmp_img

cut_width_1 = 0
for i in range(origin_width):
    if not np.array_equal(new_down[0,i], [0, 0, 0]):
        cut_width_1 = max(i,cut_width_1)
        # print(cut_width)
tmp_high = new_down.shape[0] - 1
for i in range(origin_width):
    if not np.array_equal(new_down[tmp_high,i], [0, 0, 0]):
        cut_width_1 = max(i,cut_width_1)
print(f"左白右黑 切割宽度{cut_width_1}")

cut_width_2 = origin_width
for i in range(origin_width-1,0,-1):
    if not np.array_equal(new_up[0,i], [0, 0, 0]):
        cut_width_2 = min(i,cut_width_2)
tmp_high = origin_high - 1
for i in range(origin_width-1,0,-1):
    if not np.array_equal(new_up[tmp_high,i], [0, 0, 0]):
        cut_width_2 = min(i,cut_width_2)
print(f"左黑右白 切割宽度{cut_width_2}")

# 裁剪坐标为[y0:y1, x0:x1]
left_part = new_down[0:origin_high, 0:cut_width_1]
right_part = new_up[0:origin_high, cut_width_2:origin_width]
end_time = datetime.datetime.now()  # 结束时间
print(f"切割成功,耗时{(end_time - start_time).seconds}秒.")

left_part_rot = text_img_rotation_adjust(left_part)
right_part_rot = text_img_rotation_adjust(right_part)

# 构建输出文件名
count = 0
output_filename_right= f"img_{count}.jpg"
count = count + 1
output_filename_left = f"img_{count}.jpg"
count = count + 1
# 构建输出路径
output_left_path = os.path.join(output_dir, output_filename_left)
output_right_path = os.path.join(output_dir, output_filename_right)

cv2.imwrite(output_left_path, left_part_rot, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
cv2.imwrite(output_right_path, right_part_rot, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

plt.subplot(151), plt.imshow(copy), plt.title('opening')
plt.xticks([]), plt.yticks([])

plt.subplot(152), plt.imshow(left_part), plt.title('left_part')
plt.xticks([]), plt.yticks([])

plt.subplot(153), plt.imshow(left_part_rot), plt.title('left_part_rot')
plt.xticks([]), plt.yticks([])

plt.subplot(154), plt.imshow(right_part), plt.title('right_part')
plt.xticks([]), plt.yticks([])

plt.subplot(155), plt.imshow(right_part_rot), plt.title('right_part_rot')
plt.xticks([]), plt.yticks([])

plt.tight_layout()
plt.show()