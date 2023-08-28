import os
from PIL import Image

def batch_resize_images(input_folder, output_folder, scale):
    """
    批量按指定的倍数缩小图片
    :param input_folder: 输入图片文件夹路径
    :param output_folder: 输出图片文件夹路径
    :param scale: 缩小倍数，如0.5表示缩小一半
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            resize_image(input_path, output_path, scale)

def resize_image(input_image, output_image, scale):
    """
    按指定的倍数缩小图片
    :param input_image: 输入图片路径
    :param output_image: 输出图片路径
    :param scale: 缩小倍数，如0.5表示缩小一半
    """
    image = Image.open(input_image)
    width, height = image.size
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    resized_image.save(output_image)

# 示例用法
input_folder = "rename"  # 输入图片文件夹路径
output_folder = "output_folder2"  # 输出图片文件夹路径
scale_factor = 0.4  # 缩小倍数，如0.5表示缩小一半 
# 0.8 141mb
# 0.6 90mb

batch_resize_images(input_folder, output_folder, scale_factor)
