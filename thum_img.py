from PIL import Image
import os

def create_thumbnail(image_path, thumbnail_path, size):
    try:
        # 打开原始图片
        image = Image.open(image_path)
        
        # 调整大小并保持宽高比
        image.thumbnail(size)
        
        # 保存缩略图
        image.save(thumbnail_path)
        
        print(f"缩略图 {thumbnail_path} 创建成功！")
    except IOError:
        print(f"无法创建缩略图 {thumbnail_path}！")

def batch_create_thumbnails(input_dir, output_dir, size):
    # 检查输出文件夹是否存在，如果不存在则创建它
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 遍历输入文件夹中的图片
    for filename in os.listdir(input_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            # 构造输入和输出文件的路径
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            # 创建缩略图
            create_thumbnail(input_path, output_path, size)

# 示例用法
batch_create_thumbnails("rename", "rename_thum", (169, 240))
