# 参考 https://blog.csdn.net/wzw12315/article/details/105676529
# 基于直线探测的文本类图片矫正算法
import cv2
import numpy as np
import os

def text_img_rotation_adjust(img_path, save_path):
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
        print("图片{}不太行").format(img_path)
        return
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
    cv2.imwrite(save_path, cv_dst_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    # cv2.CV_IMWRITE_JPEG_QUALITY  设置图片格式为.jpeg或者.jpg的图片质量，其值为0---100（数值越大质量越高），默认95
    # cv2.CV_IMWRITE_WEBP_QUALITY  设置图片的格式为.webp格式的图片质量，值为0--100
    # cv2.CV_IMWRITE_PNG_COMPRESSION  设置.png格式的压缩比，其值为0--9（数值越大，压缩比越大），默认为3

if __name__=='__main__':

    input_path = r"D:\Documents\xpwszl14"
    output_path = r"D:\Documents\xpwszl14_temp_rot"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for filename in os.listdir(input_path):
        print(20*'*')
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            input_img_path = os.path.join(input_path, filename)
            output_img_path = os.path.join(output_path, filename)
            text_img_rotation_adjust(input_img_path, output_img_path)

    # 竖向排版暂不考虑