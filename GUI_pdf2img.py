import fitz
from PIL import Image
import os
import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def pdf_image(pdf_path, img_folder, zoom_x, zoom_y, rotation_angle, first_num):
    start_time = datetime.datetime.now()  # 开始时间
    try:
        pdf = fitz.open(pdf_path)
        for pg in range(pdf.page_count):
            # page = pdf[pg]
            page = pdf.load_page(pg)
            trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotation_angle)
            pm = page.get_pixmap(matrix=trans, alpha=False, dpi=600)
            img = Image.frombytes("RGB", [pm.width, pm.height], pm.samples)
            dpi = 600  # 设置所需的 DPI 值
            image_path = os.path.join(img_folder, f"{pg + first_num}.jpg")
            img.save(f'{image_path}', dpi=(dpi, dpi),)
            # pm.writePNG(image_path)
            print(image_path)
        
        pdf.close()
        end_time = datetime.datetime.now()  # 结束时间
        messagebox.showinfo("导出完成", f"PDF导出images成功,共耗费时间{(end_time - start_time).seconds}秒.")
    except Exception as e:
        messagebox.showerror("错误", f"出现了一个错误: {str(e)}")
        print(str(e))

def convert_button_click():
    pdf_path = input_pdf_var.get()
    img_folder = output_folder_var.get()
    zoom_x = float(zoom_x_entry.get())
    zoom_y = float(zoom_y_entry.get())
    count = int(count_num_entry.get())

    rotation_angle = float(rotation_entry.get())
    if pdf_path and img_folder: 
        input_pdf.delete(0, tk.END)  
        input_pdf.insert(0, pdf_path)  
        output_folder.delete(0, tk.END)
        output_folder.insert(0, img_folder)
        print(pdf_path)
        print(img_folder)
        print(zoom_x)
        print(zoom_y)
        print(rotation_angle)
        print(count)
        pdf_image(pdf_path, img_folder, zoom_x, zoom_y, rotation_angle, count)
        # input_pdf.delete(0, tk.END)  
        # output_folder.delete(0, tk.END)

def browse_output_folder():
    output_folder_var.set(filedialog.askdirectory()) 

def browse_input_file():
    input_pdf_var.set(filedialog.askopenfilename(title="选择要转换的PDF文件", filetypes=[("PDF Files", "*.pdf")]))

app = tk.Tk()
app.title("Pdf2Img")

input_label = tk.Label(app, text="PDF文件位置:")
input_label.pack()
input_pdf_var = tk.StringVar()
input_pdf = tk.Entry(app, width=70, textvariable=input_pdf_var)
input_pdf.pack()

input_button = tk.Button(app, text="浏览文件", command=browse_input_file)
input_button.pack()

output_label = tk.Label(app, text="导出图片位置:")
output_label.pack()
output_folder_var = tk.StringVar()
output_folder = tk.Entry(app, width=70, textvariable=output_folder_var)
output_folder.pack()

output_button = tk.Button(app, text="浏览目录", command=browse_output_folder)
output_button.pack()

zoom_x_label = tk.Label(app, text="x方向缩放系数:")
zoom_x_label.pack()
zoom_x_entry = tk.Entry(app)
zoom_x_entry.insert(0, "9.0")
zoom_x_entry.pack()

zoom_y_label = tk.Label(app, text="y方向缩放系数:")
zoom_y_label.pack()
zoom_y_entry = tk.Entry(app)
zoom_y_entry.insert(0, "9.0")
zoom_y_entry.pack()

rotation_label = tk.Label(app, text="旋转角度:")
rotation_label.pack()
rotation_entry = tk.Entry(app)
rotation_entry.insert(0, "0")
rotation_entry.pack()

count_num_label = tk.Label(app, text="文件序号首位:")
count_num_label.pack()
count_num_entry = tk.Entry(app)
count_num_entry.insert(0, "1")
count_num_entry.pack()

convert_button = tk.Button(app, text="开始导出", command=convert_button_click)
convert_button.pack()

app.mainloop()
