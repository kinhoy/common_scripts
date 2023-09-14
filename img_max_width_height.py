import os
from PIL import Image

# folder_path = "test"  
# 替换为实际的文件夹路径
folder_path = r"D:\Projects"


max_width = 0
max_height = 0

# 遍历文件夹中的所有图片文件
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # 根据需要修改文件类型
        image_path = os.path.join(folder_path, filename)
        image = Image.open(image_path)
        width, height = image.size
        print("分辨率：{}x{}".format(width, height))
        # 更新最大分辨率
        max_width = max(max_width, width)
        max_height = max(max_height, height)

# 输出最大分辨率
print("最大分辨率：{}x{}".format(max_width, max_height))

