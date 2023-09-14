import pytesseract
from PIL import Image
import os
# import cv2

#记录自动识别和手动命名文件的数量
auto_num = 0
manual_num = 0

pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files\Tesseract-OCR\tesseract.exe"

input_folder = r"D:\Documents\center"
output_cut_folder = r"D:\Documents\center\cut"
output_folder = r"D:\Documents\center\rename"



def crop_bottom_rec(image_path, output_path, filename, height=440):
    img = Image.open(image_path)
    width, original_height = img.size
    top = original_height - height
    # 截切图片
    cropped_img = img.crop((0, top, width, original_height))
    # img = cv2.imread(image_path)
    # original_height, width, _ = img.shape
    # top = original_height - height
    # bottom = original_height
    # cropped_img = img[top:bottom, 0:width]

    # 使用Tesseract进行数字识别
    result = pytesseract.image_to_string(cropped_img, config='--psm 6 digits').strip()
    
    # 检查是否识别出数字
    if result.isdigit():
        # 构建新的文件名
        new_filename = result + ".jpg"
        global auto_num
        auto_num = auto_num + 1
    else:
        # 如果未能识别出数字，手动输入数字作为新文件名
        cropped_img.show()
        user_input = input(f"未能识别数字，输入新文件名： ")
        new_filename = user_input + ".jpg"
        global manual_num
        manual_num = manual_num + 1
    # 构建新的文件路径
    new_image_path = os.path.join(output_path, new_filename)
    
    # 更改文件名前先经常是否存在因为识别错误导致已存在重复文件名
    if os.path.isfile(new_image_path):
        cropped_img.show()
        new_filename = new_filename + "-0.jpg"
        new_image_path = os.path.join(output_path, new_filename)
        print(f"检测到文件名重复，更改为 {new_image_path}")

    # 更改文件名
    img.save(new_image_path)
    # cv2.imwrite(new_image_path,img)
    print(f"已将文件 {image_path} 更改为 {new_image_path}")

# 裁剪出适合用OCR识别页码的图片位置
def crop_bottom(image_path, output_path, height=440):
    img = Image.open(image_path)
    width, original_height = img.size
    top = original_height - height
    # 截切图片
    cropped_img = img.crop((0, top, width, original_height))
    cropped_img.save(output_path)

all_files = os.listdir(input_folder)
image_files = [file for file in all_files if file.lower().endswith(('.jpg', '.png'))]
image_count = len(image_files)
# 遍历输入文件夹中的所有图片文件
for filename in all_files:
    if filename.endswith(".jpg") or filename.endswith(".png"):
        input_path = os.path.join(input_folder, filename)
        
        # 第一步 切出页码所在部分 划出大概范围（土办法）
        # if not os.path.exists(output_cut_folder):
        #     os.makedirs(output_cut_folder)
        # output_path = os.path.join(output_cut_folder, filename)
        # crop_bottom(input_path, output_path)

        # 第二步 开始识别
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        crop_bottom_rec(input_path, output_folder, filename)
        image_count = image_count - 1 
        print(f"***********剩余文件数量： {image_count}***********")
print("完成文件名更改")
print(f"自动识别命名的数量： {auto_num}  手动命名的数量： {manual_num}")
        


