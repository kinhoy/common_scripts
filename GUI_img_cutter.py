import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import subprocess

#从图片右上角开始计算边框范围切割 
def crop_image(image_path, output_dir, crop_width, crop_height):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # 打开图像
    image = Image.open(image_path)
    # 获取图像尺寸
    image_width, image_height = image.size
    # 计算切割区域的位置
    crop_left = image_width - crop_width
    crop_top = 0
    # 切割图像
    cropped_image = image.crop((crop_left, crop_top, image_width, crop_height))
    # 获取原始图像的文件名
    image_filename = os.path.basename(image_path)
    # 构建输出路径
    output_path = os.path.join(output_dir, image_filename)
    # 保存切割后的图像
    cropped_image.save(output_path)
    print(output_path)

#从图片中间线切割图片 
def crop_and_rename_images(input_dir, output_dir, count):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # 遍历输入文件夹中的所有图片文件 images.sort(key = lambda x: int(x[4:-4])) 
    for idx, filename in enumerate(sorted(os.listdir(input_dir), key = lambda x: int(x[0:-4]))):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            print(filename)
            # 构建输入图像的完整路径
            input_path = os.path.join(input_dir, filename)
            # 打开图像
            image = Image.open(input_path)
            # 获取图像尺寸
            image_width, image_height = image.size
            # 计算切割位置（中间线）
            crop_line = image_width // 2
            # 切割图像
            left_image = image.crop((0, 0, crop_line, image_height))
            right_image = image.crop((crop_line, 0, image_width, image_height))
            # 构建输出文件名
            output_filename_left = f"{count}.jpg"
            count = count + 1
            output_filename_right= f"{count}.jpg"
            count = count + 1
            
            # 构建输出路径
            output_left_path = os.path.join(output_dir, output_filename_left)
            output_right_path = os.path.join(output_dir, output_filename_right)
            # 保存切割后的图像
            left_image.save(output_left_path)
            print(output_left_path)
            right_image.save(output_right_path)
            print(output_right_path)

# 批量从右上角按需要切割的区域尺寸
# 先手动裁剪一张取得数值比较好
# crop_width = 6231  # 切割宽度
# crop_height = 4744  # 切割高度
# 操作1 批量从右上角按切割高度和宽度裁剪图片
def crop_right_to_left_image():
    input_dir = input_dir_entry.get()
    output_dir = output_cut_dir_entry.get()
    crop_width = int(crop_width_entry.get())
    crop_height = int(crop_height_entry.get())
    for filename in os.listdir(input_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            print(filename)
            input_path = os.path.join(input_dir, filename)
            # 执行切割操作
            crop_image(input_path, output_dir, crop_width, crop_height)
    messagebox.showinfo("完成", "批量从右上角按切割高度和宽度裁剪图片完成!")

# 操作2 批量从中间切图片 
def crop_from_center():
    count_num = int(count_entry.get())
    output_cut_dir = output_cut_dir_entry.get()
    output_center_cut_dir = output_center_cut_dir_entry.get()
    crop_and_rename_images(output_cut_dir, output_center_cut_dir, count_num)
    messagebox.showinfo("完成", "批量从中间切图片完成!")

# Create the main application window
app = tk.Tk()
app.title("扫描图片裁剪")

# Create labels and entry widgets for input and output directories
tk.Label(app, text="原图路径:").pack()
input_dir_entry = tk.Entry(app, width=70)
input_dir_entry.pack()
tk.Button(app, text="浏览", command=lambda: browse_directory(input_dir_entry)).pack()

tk.Label(app, text="从右上往左下切图片存放路径:").pack()
output_cut_dir_entry = tk.Entry(app, width=70)
output_cut_dir_entry.pack()
tk.Button(app, text="浏览", command=lambda: browse_directory(output_cut_dir_entry)).pack()

tk.Label(app, text="裁切宽度:").pack()
crop_width_entry = tk.Entry(app)
crop_width_entry.pack()

tk.Label(app, text="裁切高度:").pack()
crop_height_entry = tk.Entry(app)
crop_height_entry.pack()

tk.Button(app, text="右上往左下切", command=crop_right_to_left_image).pack()

tk.Label(app, text="中间切图片存放路径:").pack()
output_center_cut_dir_entry = tk.Entry(app, width=70)
output_center_cut_dir_entry.pack()
tk.Button(app, text="浏览", command=lambda: browse_directory(output_center_cut_dir_entry)).pack()

tk.Label(app, text="文件编排序号首位:").pack()
count_entry = tk.Entry(app)
count_entry.insert(0, "0")
count_entry.pack()

tk.Button(app, text="中间切", command=crop_from_center).pack()

def browse_directory(entry_field):
    directory = filedialog.askdirectory()
    entry_field.delete(0, tk.END)
    entry_field.insert(0, directory)

app.mainloop()
