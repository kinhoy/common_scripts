import paddlehub as hub
from matplotlib import pyplot as plt
import cv2
import numpy as np
import datetime
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

count = 0
text_detector = hub.Module(name="chinese_text_detection_db_server", enable_mkldnn=True)       # mkldnn加速仅在CPU下有效

def real_auto_center_cut(img_path, save_path, count_num):
    start_time = datetime.datetime.now()  # 开始时间
    img = cv2.imread(img_path)
    copy = img.copy()
    result = text_detector.detect_text(images=[img])
    data = result[0]['data']
    center = img.shape[1]//2
    min_left = img.shape[1]
    max_right = 0
    center_left = 0
    center_right = img.shape[1]

    for re in data:
        # 0左下、1右下、2右上、3左上
        # box = [re[1],re[0],re[3],re[2]]
        # box = np.intp(box)
        # boxPoints返回四个点顺序：右下→左下→左上→右上
        # cv2.drawContours(copy, [box], 0, (0,0, 255), 3)
        tmp1 = (re[3][0]+re[2][0])//2
        tmp2 = (re[0][0]+re[1][0])//2
        if tmp1 < center or tmp2 < center:
            # 框在左
            min_left = min(re[0][0],re[3][0],min_left)
            center_left = max(re[1][0],re[2][0],center_left)
        else:
            # 框在右
            center_right = min(re[0][0],re[3][0],center_right)
            max_right = max(re[1][0],re[2][0],max_right)

    print(f"左侧 {min_left} {center_left}, 右侧 {center_right}  {max_right}")

    # 两侧留白宽度
    offset  = 80 if (min_left-80) > 0 else 0
    # 裁剪
    left_part = img[0:img.shape[0], min_left-offset:center_left+offset]
    right_part = img[0:img.shape[0], center_right-offset:max_right+offset]

    height = img.shape[0]
    width = left_part.shape[1]
    # 创建新的白色背景图像
    new_left_image = np.ones((height, center, 3), dtype=np.uint8) * 255
    new_right_image = new_left_image.copy()
    
    if left_part.shape[1] >= new_left_image.shape[1]:
        new_left_image = left_part
    else:
        x_offset = (center - width) // 2
        y_offset = (height - left_part.shape[0]) // 2
        print(f"x_offset:{x_offset} , y_offset:{y_offset}")
        new_left_image[y_offset:y_offset + left_part.shape[0], x_offset:x_offset + width] = left_part
    if right_part.shape[1] >= new_right_image.shape[1]:
        new_right_image = right_part
    else:
        width = right_part.shape[1]
        x_offset = (center - width) // 2
        y_offset = (height - right_part.shape[0]) // 2
        print(f"x_offset:{x_offset} , y_offset:{y_offset}")
        new_right_image[y_offset:y_offset + right_part.shape[0], x_offset:x_offset + width] = right_part

    global count
    output_left = f"{count_num}.jpg"
    count = count_num + 1
    output_right= f"{count}.jpg"
    count = count + 1
    output_left_path = os.path.join(save_path, output_left)
    output_right_path = os.path.join(save_path, output_right)
    cv2.imwrite(output_left_path, new_left_image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    cv2.imwrite(output_right_path, new_right_image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    print(f"{output_left_path}")
    print(f"{output_right_path}")
    end_time = datetime.datetime.now()  # 结束时间
    print(f"切割成功,耗时{(end_time - start_time).seconds}秒.")

def crop_from_center():
    input_dir = input_dir_entry.get()
    output_dir = output_cut_dir_entry.get()
    global count
    count = int(count_entry.get())
    files= os.listdir(input_dir)
    files.sort(key = lambda x: int(x[0:-4]))
    for filename in files:
        if filename.endswith(".jpg") or filename.endswith(".png"):
            print(filename)
            input_path = os.path.join(input_dir, filename)
            # 执行切割操作
            real_auto_center_cut(input_path, output_dir, count)
    print(50*"#")
    print("自动裁剪图片完成!")
    print(50*"#")
    messagebox.showinfo("成功", "批量自动切图片完成!")

app = tk.Tk()
app.title("真自动图片裁剪")

tk.Label(app, text="原图路径:").pack()
input_dir_entry = tk.Entry(app, width=70)
input_dir_entry.pack()
tk.Button(app, text="浏览", command=lambda: browse_directory(input_dir_entry)).pack()

tk.Label(app, text="裁剪保存路径:").pack()
output_cut_dir_entry = tk.Entry(app, width=70)
output_cut_dir_entry.pack()
tk.Button(app, text="浏览", command=lambda: browse_directory(output_cut_dir_entry)).pack()

tk.Label(app, text="文件序号:").pack()
count_entry = tk.Entry(app)
count_entry.insert(0, "0")
count_entry.pack()

tk.Button(app, text="自动双页 -> 左、右单页", command=crop_from_center).pack()
def browse_directory(entry_field):
    directory = filedialog.askdirectory()
    entry_field.delete(0, tk.END)
    entry_field.insert(0, directory)

app.mainloop()
