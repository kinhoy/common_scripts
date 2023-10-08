import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image

def resize_image(input_image, output_image, scale):
    # 按指定的倍数缩小图片 scale: 缩小倍数，如0.5表示缩小一半
    image = Image.open(input_image)
    width, height = image.size
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    resized_image = resized_image.convert('RGB')
    resized_image.save(output_image)
    print(f"缩图 {output_image} 创建成功！")

def create_thumbnail(image_path, thumbnail_path, size):
    try:
        image = Image.open(image_path)
        # 调整大小并保持宽高比
        image.thumbnail(size)
        # 保存缩略图
        image.save(thumbnail_path)
        print(f"缩略图 {thumbnail_path} 创建成功！")
    except Exception as e:
        print(f"出现了一个错误: {str(e)}")
        print(f"无法创建缩略图 {thumbnail_path}！")
        image = image.convert('RGB')
        image.save(thumbnail_path)
        print(f"cannot write mode RGBA as JPEG 再次尝试转缩略图 {thumbnail_path} 创建成功！")

def batch_resize_images(input_folder, output_folder, scale):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            resize_image(input_path, output_path, scale)

def batch_create_thumbnails(input_dir, output_dir, size):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for filename in os.listdir(input_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            # 构造输入和输出文件的路径
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            # 创建缩略图
            create_thumbnail(input_path, output_path, size)

def get_resize_images_max_size(input_path):
    total_width = 0
    total_height = 0
    max_width = 0
    max_height = 0
    count = 0
    # 遍历文件夹中的所有图片文件
    for filename in os.listdir(input_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):  # 根据需要修改文件类型
            image_path = os.path.join(input_path, filename)
            image = Image.open(image_path)
            width, height = image.size
            print("分辨率：{}x{}".format(width, height))
            total_width += width
            total_height += height
            count += 1
            # 更新最大分辨率
            max_width = max(max_width, width)
            max_height = max(max_height, height)
    if count > 0:
        average_width = total_width // count
        average_height = total_height // count
        print("平均分辨率：{}x{}".format(average_width, average_height))
        print("最大分辨率：{}x{}".format(max_width, max_height))
        messagebox.showinfo("分辨率数据如下", f"平均分辨率：{str(average_width)}x{str(average_height)} 最大分辨率：{str(max_width)}x{str(max_height)}")
    else:
        print("没有找到任何图片文件")

def resize_images_and_create_thumbnails():
    scale_factor = float(scale_entry.get())
    input_folder = input_folder_var.get()
    output_resize_images = output_resize_images_var.get()
    output_thumbnails = output_thumbnails_var.get()
    width = int(thumbnail_width_entry.get())  # 获取宽度值
    height = int(thumbnail_height_entry.get())  # 获取高度值
    thum_size = (width, height)
    try:
        if input_folder and output_thumbnails and output_resize_images: 
            batch_resize_images(input_folder, output_resize_images, scale_factor)
            batch_create_thumbnails(input_folder, output_thumbnails, thum_size)
            messagebox.showinfo("成功", "原图缩放和生成缩略图成功!")
            get_resize_images_max_size(output_resize_images)
        else:
            messagebox.showinfo("提示", "三个文件夹需要同时输入")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print(str(e))

def browse_input_folder():
    input_folder = filedialog.askdirectory()
    input_folder_var.set(input_folder)

def browse_output_resize_images_folder():
    output_folder = filedialog.askdirectory()
    output_resize_images_var.set(output_folder)

def browse_output_thumbnails_folder():
    output_folder = filedialog.askdirectory()
    output_thumbnails_var.set(output_folder)

# Create the main application window
app = tk.Tk()
app.title("EBOOK资源生成工具")

# Create and place widgets in the window
input_folder_label = tk.Label(app, text="原图路径:")
input_folder_label.pack()

input_folder_var = tk.StringVar()
input_folder_entry = tk.Entry(app, width=70, textvariable=input_folder_var)
input_folder_entry.pack()

browse_input_button = tk.Button(app, text="浏览", command=browse_input_folder)
browse_input_button.pack()


scale_label = tk.Label(app, text="缩小倍数:")
scale_label.pack()

scale_entry = tk.Entry(app)
scale_entry.insert(0, "0.5")
scale_entry.pack()

output_resize_images_label = tk.Label(app, text="原图缩放图片保存路径:")
output_resize_images_label.pack()

output_resize_images_var = tk.StringVar()
output_resize_images_entry = tk.Entry(app, width=70, textvariable=output_resize_images_var)
output_resize_images_entry.pack()

browse_output_resize_images_button = tk.Button(app, text="浏览", command=browse_output_resize_images_folder)
browse_output_resize_images_button.pack()


thumbnail_size_label = tk.Label(app, text="缩略图大小:")
thumbnail_size_label.pack()

thumbnail_width_entry = tk.Entry(app)
thumbnail_width_entry.insert(0, "169")
thumbnail_width_entry.pack()

thumbnail_height_entry = tk.Entry(app)
thumbnail_height_entry.insert(0, "240")
thumbnail_height_entry.pack()

output_thumbnails_label = tk.Label(app, text="原图转缩略图保存路径:")
output_thumbnails_label.pack()

output_thumbnails_var = tk.StringVar()
output_thumbnails_entry = tk.Entry(app, width=70, textvariable=output_thumbnails_var)
output_thumbnails_entry.pack()

browse_output_thumbnails_button = tk.Button(app, text="浏览", command=browse_output_thumbnails_folder)
browse_output_thumbnails_button.pack()


process_button = tk.Button(app, text="开始转化", command=resize_images_and_create_thumbnails)
process_button.pack()

# Start the main loop
app.mainloop()
