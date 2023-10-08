import os
import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import os

# 批量将图片四周裁剪或者用白色填充

fill_with_white = False

def batch_wipe_image(input_path, output_path, top, bottom, left, right, wipe_with_white):
    start_time = datetime.datetime.now()  # 开始时间
    try:
        for filename in os.listdir(input_path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                original_image = Image.open(os.path.join(input_path, filename))
                width, height = original_image.size
                # 计算裁剪后的图片尺寸
                new_width = width - left -right
                new_height = height - top - bottom
                # 进行裁剪
                cut_left = left
                cut_top = top
                cut_right = width - right
                cut_bottom = height - bottom
                cropped_image = original_image.crop((cut_left, cut_top, cut_right, cut_bottom))
                # cropped_image.show()
                if wipe_with_white:
                    # 创建一个新的白色背景图片
                    new_image = Image.new("RGB", (width, height), (255, 255, 255))
                    # 将原始图片粘贴到新的白色背景图片中心
                    x_offset = (width - new_width) // 2
                    y_offset = (height - new_height) // 2
                    new_image.paste(cropped_image, (x_offset, y_offset))
                    new_path = os.path.join(output_path, filename)
                    new_image.save(new_path, quality=95)
                    print(new_path)
                else:
                    # 直接裁剪图片保存
                    new_path = os.path.join(output_path, filename)
                    cropped_image.save(new_path, quality=95)
                    print("直接裁剪保存")
                    print(new_path)

        end_time = datetime.datetime.now()  # 结束时间
        messagebox.showinfo("擦除完成", f"图片擦除成功，共耗费时间{(end_time - start_time).seconds}秒.")
    except Exception as e:
        messagebox.showerror("错误", f"出现了一个错误: {str(e)}")
        print(str(e))

def convert_button_click():
    img_input_folder = input_folder.get()
    img_output_folder = output_folder.get()
    top = int(top_entry.get())
    bottom = int(bottom_entry.get())
    left = int(left_entry.get())
    right = int(right_entry.get())
    global fill_with_white

    if img_input_folder and img_output_folder: 
        input_folder.delete(0, tk.END)  
        input_folder.insert(0, img_input_folder)  
        output_folder.delete(0, tk.END)
        output_folder.insert(0, img_output_folder)
        
        batch_wipe_image(img_input_folder, img_output_folder, top, bottom, left, right, fill_with_white)
        # input_folder.delete(0, tk.END)  
        # output_folder.delete(0, tk.END)

def check_fill_with_white():
    global fill_with_white
    if checkbox_var.get():
        print("本次使用白色填充擦除部分")
        fill_with_white = True
    else:
        print("本次未使用白色填充擦除部分，直接裁减")
        fill_with_white = False

app = tk.Tk()
app.title("图片边缘擦除")

input_label = tk.Label(app, text="图片目录:")
input_label.pack()
input_folder = tk.Entry(app, width=70)
input_folder.pack()

input_button = tk.Button(app, text="浏览目录", command=lambda: input_folder.insert(0, filedialog.askdirectory(title="选择待擦除图片目录")))
input_button.pack()

output_label = tk.Label(app, text="导出图片位置:")
output_label.pack()
output_folder = tk.Entry(app, width=70)
output_folder.pack()

output_button = tk.Button(app, text="浏览目录", command=lambda: output_folder.insert(0, filedialog.askdirectory(title="选择导出图片目录")))
output_button.pack()

top_label = tk.Label(app, text="顶部向下擦除高度:")
top_label.pack()
top_entry = tk.Entry(app)
top_entry.insert(0, "100")
top_entry.pack()

bottom_label = tk.Label(app, text="底部向上擦除高度:")
bottom_label.pack()
bottom_entry = tk.Entry(app)
bottom_entry.insert(0, "100")
bottom_entry.pack()

left_label = tk.Label(app, text="左侧向内擦除宽度:")
left_label.pack()
left_entry = tk.Entry(app)
left_entry.insert(0, "130")
left_entry.pack()

right_label = tk.Label(app, text="右侧向内擦除宽度:")
right_label.pack()
right_entry = tk.Entry(app)
right_entry.insert(0, "130")
right_entry.pack()

checkbox_var = tk.BooleanVar()
checkbox = tk.Checkbutton(app, text="是否用白色填充擦除部分", variable=checkbox_var, command=check_fill_with_white)
checkbox.pack()

convert_button = tk.Button(app, text="批量擦除", command=convert_button_click)
convert_button.pack()

app.mainloop()
