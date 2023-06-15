import os
from PIL import Image
Image.MAX_IMAGE_PIXELS = 1000000000 
# 要切割的图片路径和名称
image_path = "D:\BaiduNetdiskDownload\map_img\skyland.png"
# 输出文件夹
output_folder = "D:\BaiduNetdiskDownload\map_img\compressed"


# def tile_image(img_path, output_dir, num_levels=4, scale_factor=0.5):
#     img = Image.open(img_path)
#     width, height = img.size
#     print(width)
#     print(height)

# def tile_image(img_path, output_dir, num_levels=4, scale_factor=0.5):
#     img = Image.open(img_path)
#     width, height = img.size
    
#     # 整个金字塔的总瓦片数
#     num_tiles = sum(pow(4,i) for i in range(num_levels))
    
#     # 逐层处理瓦片
#     for level in range(num_levels):
#         # 计算当前层级的瓦片大小和数量
#         tile_size = int(pow(scale_factor,level) * max(width,height))
#         num_cols = int((width-1) // tile_size) + 1
#         num_rows = int((height-1) // tile_size) + 1
        
#         # 生成并保存当前层级的所有瓦片
#         for row in range(num_rows):
#             # print(str(num_rows)+" "+str(row))
#             for col in range(num_cols):
#                 x0 = col * tile_size
#                 y0 = row * tile_size
#                 x1 = min(x0 + tile_size, width)
#                 y1 = min(y0 + tile_size, height)
                
#                 tile = img.crop((x0, y0, x1, y1))
#                 tile = tile.resize((256,256), Image.LANCZOS)
                
#                 # filename = "{}.png".format(col)

#                 filename = "{}_{}_{}.png".format(level, row, col)
#                 # 生成保存文件路径
#                 # save_path = os.path.join(output_dir, str(level), str(row))
#                 # if not os.path.exists(save_path):
#                 #     os.makedirs(save_path)
                
#                 filepath = os.path.join(output_dir, filename)
#                 tile.save(filepath)
#                 print(filepath+" success")
        
#         # 更新进度
#         num_tiles -= pow(4,level)
#         print("Processed level {} ({}/{} tiles)".format(level, num_tiles, sum(pow(4,i) for i in range(num_levels))))

# 示例用法
#tile_image(image_path, output_folder, num_levels=8, scale_factor=0.85)

def compress_image(infile, outfile, quality=95):
    """
    infile: 原始文件路径
    outfile: 输出文件路径
    quality: 压缩质量
    """
    with Image.open(infile) as im:
        im.save(outfile, "PNG", optimize=True, quality=quality)

def compressed_to_jpg_image(infile, output):
    # 先通过 convert 方法转成 RGB 格式，然后另存为 jpg 格式，图片效果没有明显减弱，但是大小迅速减少。
    with Image.open(infile) as im:
        im = im.convert('RGB')
        fn = output + "\compressed_to_jpg.jpg"
        im.save(fn)

if __name__ == '__main__':
    infile = image_path
    outfile = output_folder+'\skyland_compressed.png'
    # compress_image(infile, outfile)
    compressed_to_jpg_image("D:\BaiduNetdiskDownload\map_img\compressed\mainland_compressed.png","D:\BaiduNetdiskDownload\map_img\compressed")


