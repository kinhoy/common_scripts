# 参考 https://blog.csdn.net/wzw12315/article/details/105676529
# 基于直线探测的文本类图片矫正算法
import cv2
import numpy as np
from matplotlib import pyplot as plt

img_path = 'xx.jpg'

print("working: {}".format(img_path))
image = cv2.imread(img_path, cv2.IMREAD_COLOR)
copy = image.copy()
# 开运算：先腐蚀，在膨胀
kernel = np.ones((32, 32), dtype=np.uint8)
image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, 2)
# cv2.namedWindow("opening",0)
# cv2.imshow('opening', opening)
canny = cv2.Canny(image,50,200,3)
# canny = cv2.Canny(image,300,700,3)
lines = cv2.HoughLines(canny,1,np.pi/180,220)
print(40*'#')
print(lines)
print(40*'#')
sum = 0.0
count = 0
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
if count == 0:
    print(40*'#')
    print("图片{}不太行，直接复制原图，无法自动处理".format(img_path))
    print(40*'#')
else:
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
    # cv2.imwrite(save_path, cv_dst_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    plt.subplot(121), plt.imshow(copy), plt.title('ori')
    plt.xticks([]), plt.yticks([])

    plt.subplot(122), plt.imshow(cv_dst_img), plt.title('rot')
    plt.xticks([]), plt.yticks([])

    plt.tight_layout()
    plt.show()