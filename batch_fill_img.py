# from PIL import Image
# import os

# def resize_and_save(image_path, target_size):
#     image = Image.open(image_path)
#     old_size = image.size
#     new_size = max(old_size)
#     new_image = Image.new("RGB", (new_size, new_size), (255, 255, 255))
#     offset = ((new_size - old_size[0]) // 2, (new_size - old_size[1]) // 2)
#     new_image.paste(image, offset)
#     resized_image = new_image.resize(target_size)
#     resized_image.save(image_path)

# folder_path = "test"  # 替换为实际的文件夹路径
# target_size = (3300, 4850)  # 设置目标尺寸 3228x4911

# # 遍历文件夹中的所有图片文件
# for filename in os.listdir(folder_path):
#     if filename.endswith(".jpg") or filename.endswith(".png"):  # 根据需要修改文件类型
#         image_path = os.path.join(folder_path, filename)
#         resize_and_save(image_path, target_size)


# import os
# from PIL import Image

# folder_path = "test"  # 替换为实际的文件夹路径

# max_width = 0
# max_height = 0

# # 遍历文件夹中的所有图片文件
# for filename in os.listdir(folder_path):
#     if filename.endswith(".jpg") or filename.endswith(".png"):  # 根据需要修改文件类型
#         image_path = os.path.join(folder_path, filename)
#         image = Image.open(image_path)
#         width, height = image.size
        
#         # 更新最大分辨率
#         max_width = max(max_width, width)
#         max_height = max(max_height, height)

# # 输出最大分辨率
# print("最大分辨率：{}x{}".format(max_width, max_height))



# 遍历文件夹中的所有图片文件
from PIL import Image
import os

def resize_and_pad(image_path, output_path, target_size):
    image = Image.open(image_path)
    old_size = image.size

    # 计算填充后的图像位置
    x_offset = (target_size[0] - old_size[0]) // 2
    y_offset = (target_size[1] - old_size[1]) // 2

    # 创建白色背景的新图像
    new_image = Image.new("RGB", target_size, (0, 0, 0))

    # 将原始图像粘贴到新图像的偏移位置
    new_image.paste(image, (x_offset, y_offset))

    # 保存处理后的图像，覆盖原始图像
    # new_filename = "img_" + filename
    new_image_path = os.path.join(output_path, filename)
    new_image.save(new_image_path)

folder_path = "test"  # 替换为实际的文件夹路径
save_path = "test_fill"  # 替换为实际的文件夹路径
target_size = (3300, 4850) # 设置目标尺寸

if not os.path.exists(save_path):
    os.makedirs(save_path)
# 遍历文件夹中的所有图片文件
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # 根据需要修改文件类型
        image_path = os.path.join(folder_path, filename)
        resize_and_pad(image_path, save_path, target_size)
