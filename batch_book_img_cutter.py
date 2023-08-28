from PIL import Image
import os

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
def crop_and_rename_images(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    count = 0
    # 遍历输入文件夹中的所有图片文件 images.sort(key = lambda x: int(x[4:-4])) 
    for idx, filename in enumerate(sorted(os.listdir(input_dir),key = lambda x: int(x[0:-4]))):
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
            output_filename_right= f"img_{count}.jpg"
            count = count + 1
            output_filename_left = f"img_{count}.jpg"
            count = count + 1
            # 构建输出路径
            output_left_path = os.path.join(output_dir, output_filename_left)
            output_right_path = os.path.join(output_dir, output_filename_right)
            # 保存切割后的图像
            left_image.save(output_left_path)
            print(output_left_path)
            right_image.save(output_right_path)
            print(output_right_path)


# 输入文件夹路径和输出文件夹路径
input_dir = "aaaa"
output_dir = "aaaa_cutter"

# 批量从右上角按需要切割的区域尺寸
# 先手动裁剪一张取得数值比较好
crop_width = 6337  # 切割宽度
crop_height = 4831  # 切割高度

# 操作1 遍历输入文件夹中的所有图片文件
# for filename in os.listdir(input_dir):
#     if filename.endswith(".jpg") or filename.endswith(".png"):
#         # 构建输入图像的完整路径
#         input_path = os.path.join(input_dir, filename)
#         # 执行切割操作
#         crop_image(input_path, output_dir, crop_width, crop_height)

# folder = r"D:\Documents\原图\rename"
# 操作2 批量从中间切图片 
output_center_dir = "aaaa_cutter_center"
crop_and_rename_images(output_dir, output_center_dir)
