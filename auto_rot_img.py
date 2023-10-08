# 参考 https://blog.csdn.net/wzw12315/article/details/105676529
# 基于直线探测的文本类图片矫正算法
import cv2
import numpy as np

def text_img_rotation_adjust_(img_path):
    image = cv2.imread(img_path, cv2.IMREAD_COLOR)
    copy = image.copy()
    canny = cv2.Canny(image,50,200,3)
    lines = cv2.HoughLines(canny,1,np.pi/180,220)
    # print(lines[0])
    # print(lines.shape)
    # for x1, y1, x2, y2 in lines[0]:
    #     cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 100)
 
    sum = 0.0
    for i in range(0, len(lines)):
        rho, theta = lines[i][0][0], lines[i][0][1]
 
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
 
        sum += theta
 
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 1)
 
    average = sum/len(lines)
 
    print("average: {}".format(average))
    #度数转换
    angle = average / np.pi * 180
    print("angle: {}".format(angle))
    angle = angle-90
 
    # M = cv2.getRotationMatrix2D((image.shape[0]/2,image.shape[1]/2),angle,1)
    # result = cv2.warpAffine(copy,M,(image.shape[1],image.shape[0]))
    # cv2.imshow("warp image", result)
    # cv2.imshow("canny",canny)
    # cv2.imshow("lines", image)

    center = (image.shape[1] // 2, image.shape[0] // 2)
    rotMat = cv2.getRotationMatrix2D(center, angle, 1.0)
    # 用白色填充旋转后的图片周围
    cv_dst_img = cv2.warpAffine(copy, rotMat, (image.shape[1],image.shape[0]), borderValue=(255, 255, 255))
    # cv2.imshow("cv_dst_img", cv_dst_img)
    # cv2.imwrite('cv_dst_img.jpg',cv_dst_img)
    cv2.imwrite('cv_dst_img2.jpg',cv_dst_img,[int(cv2.IMWRITE_JPEG_QUALITY),100])
    # cv2.CV_IMWRITE_JPEG_QUALITY  设置图片格式为.jpeg或者.jpg的图片质量，其值为0---100（数值越大质量越高），默认95
    # cv2.CV_IMWRITE_WEBP_QUALITY  设置图片的格式为.webp格式的图片质量，值为0--100
    # cv2.CV_IMWRITE_PNG_COMPRESSION  设置.png格式的压缩比，其值为0--9（数值越大，压缩比越大），默认为3


if __name__=='__main__':
    # image = cv2.imread("aaaa.jpg",cv2.IMREAD_COLOR)
    input = "source.jpg"
    # input = "shuti.png" 竖向排版暂不考虑
    text_img_rotation_adjust_(input)
    cv2.waitKey(0)