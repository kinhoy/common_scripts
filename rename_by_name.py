import os
import shutil

def rename_images(input_folder, output_folder):
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 获取输入文件夹下的所有文件名
    files = os.listdir(input_folder)

    # 过滤出图片文件（可以根据需要修改文件类型的判断条件）
    image_files = [file for file in files if file.endswith(('.jpg', '.jpeg', '.png'))]

    # 按名称排序
    image_files.sort()

    # 遍历图片文件并重新命名
    for index, file in enumerate(image_files):
        # 构造新的文件名
        new_name = f"{index + 1}.jpg"  # 可以根据需要修改文件名的格式和后缀名
        print(file)
        # 构造输入和输出文件的完整路径
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, new_name)

        # 复制文件到输出文件夹
        shutil.copy2(input_path, output_path)

    print("图片重命名完成！")

# 指定输入和输出文件夹路径
input_folder = r"D:\Documents\配图"
output_folder = r"D:\Documents\配图\rename"
rename_images(input_folder, output_folder)
