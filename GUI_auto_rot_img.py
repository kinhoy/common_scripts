import cv2
import numpy as np
import datetime
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import shutil

wrong_file_list = []

def auto_rot_img(img_path, save_path):
    print(f"working: {img_path} to: {save_path}")
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
    if lines is None or len(lines) == 0:
        print(80*'#')
        print("图片{}不太行，直接复制原图，无法自动处理".format(img_path))
        print(80*'#')
        shutil.copy(img_path, save_path)
        global wrong_file_list
        wrong_file_list.append(save_path)
        return
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


def batch_rot_img():
    input_dir = input_dir_entry.get()
    output_dir = output_cut_dir_entry.get()
    files= os.listdir(input_dir)
    files.sort(key = lambda x: int(x[0:-4]))
    for filename in files:
        if filename.endswith(".jpg") or filename.endswith(".png"):
            print(filename)
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            # 执行切割操作
            auto_rot_img(input_path, output_path)
    print(80*"#")
    print("自动方向矫正完成!")
    print(80*"#")
    print("本次异常处理图片文件：")
    global wrong_file_list
    for i in wrong_file_list:
        print(i)
    messagebox.showinfo("成功", "批量文本图片自动方向矫正完成!")

app = tk.Tk()
app.title("自动文本图片方向矫正")

tk.Label(app, text="原图路径:").pack()
input_dir_entry = tk.Entry(app, width=70)
input_dir_entry.pack()
tk.Button(app, text="浏览", command=lambda: browse_directory(input_dir_entry)).pack()

tk.Label(app, text="裁剪保存路径:").pack()
output_cut_dir_entry = tk.Entry(app, width=70)
output_cut_dir_entry.pack()
tk.Button(app, text="浏览", command=lambda: browse_directory(output_cut_dir_entry)).pack()


tk.Button(app, text="自动矫正", command=batch_rot_img).pack()
def browse_directory(entry_field):
    directory = filedialog.askdirectory()
    entry_field.delete(0, tk.END)
    entry_field.insert(0, directory)

app.mainloop()
