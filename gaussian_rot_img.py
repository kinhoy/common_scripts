# 参考 https://dream.blog.csdn.net/article/details/113670582

# 第一步 
# 先把图像的边缘直线检测出来 得到threshold1和threshold2
# import cv2 as cv
# import numpy as np

# src = cv.imread("aaaa.jpg")
# gray_img = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

# def nothing(): 
#     pass

# cv.namedWindow("bar")
# cv.createTrackbar("threshold1", "bar", 0, 255, nothing)
# cv.createTrackbar("threshold2", "bar", 0, 255, nothing)

# dst = cv.equalizeHist(gray_img)
# # 高斯滤波降噪
# gaussian = cv.GaussianBlur(dst, (9, 9), 0)
# cv.imshow("gaussian", gaussian)

# while True: 
#     threshold1 = cv.getTrackbarPos("threshold1", "bar") 
#     threshold2 = cv.getTrackbarPos("threshold2", "bar") 
#     # 边缘检测 
#     edges = cv.Canny(gaussian, threshold1, threshold2) 
#     cv.imshow("edges", edges) 
#     if cv.waitKey(1) & 0xFF == 27:
#         break
# cv.destroyAllWindows()

# 上面程序调参得到参数
# threshold1 = 201
# threshold2 = 255

# 第二步 
# 用上一步得到的threshold1和threshold2作为边缘检测Canny的参数
import cv2 as cv
import numpy as np

src = cv.imread("aaaa.jpg")
copy = src.copy()
gray_img = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
dst = cv.equalizeHist(gray_img)
# 高斯滤波降噪
gaussian = cv.GaussianBlur(dst, (9, 9), 0)
# cv.imshow("gaussian", gaussian)

# 边缘检测
edges = cv.Canny(gaussian, 201, 255)
cv.imshow("edges", edges)
# Hough 直线检测
# 重点注意第四个参数 阈值，只有累加后的值高于阈值时才被认为是一条直线，
# 也可以把它看成能检测到的直线的最短长度（以像素点为单位）
# 在霍夫空间理解为：至少有多少条正弦曲线交于一点才被认为是直线
lines = cv.HoughLines(edges, 1.0, np.pi/180, 150)

# 将检测到的直线通过极坐标的方式画出来
print(lines.ndim)
print(lines.shape)

sum = 0.0
for line in lines: 
    # line[0]存储的是点到直线的极径和极角，其中极角是弧度表示的，theta是弧度 
    rho, theta = line[0] 
    # 下述代码为获取 (x0,y0) 具体值 
    a = np.cos(theta) 
    b = np.sin(theta) 
    x0 = a*rho 
    y0 = b*rho 
    # 下图 1000 的目的是为了将线段延长 以 (x0,y0) 为基础，进行延长 
    x1 = int(x0+1000*(-b)) 
    y1 = int(y0+1000*a) 
    x2 = int(x0-1000*(-b)) 
    y2 = int(y0-1000*a) 
    cv.line(src, (x1, y1), (x2, y2), (0, 255, 0), 2)
    sum += theta

average = sum / len(lines)
print("average: {}".format(average))
#度数转换
angle = average / np.pi * 180
print("angle: {}".format(angle))
angle = angle-90
center = (src.shape[1] // 2, src.shape[0] // 2)
rotMat = cv.getRotationMatrix2D(center, angle, 1.0)
# 用白色填充旋转后的图片周围
cv_dst_img = cv.warpAffine(copy, rotMat, (src.shape[1],src.shape[0]), borderValue=(255, 255, 255))
cv.imshow("rot", cv_dst_img)
# cv2.imwrite('cv_dst_img2.jpg',cv_dst_img,[int(cv2.IMWRITE_JPEG_QUALITY),100])

cv.imshow("line", src)
cv.waitKey()
cv.destroyAllWindows()
