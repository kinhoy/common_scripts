import os
from PIL import Image
# 列出目录下所有的图片，存在 images 这个列表中
img_path = 'C:/Users/h9h/Desktop/a_img/'
img_output_path = 'C:/Users/h9h/Desktop/a_out_img/'
images = os.listdir(img_path)
#文件名按数字排序
images.sort(key = lambda x: int(x[4:-4])) 
def compressed_to_jpg_image(img,num):
    # 先通过 convert 方法转成 RGB 格式，然后另存为 jpg 格式，图片效果没有明显减弱，但是大小迅速减少。
    with Image.open(img) as im:
        im = im.convert('RGB')
        fn = img_output_path +"compressed_" +str(num)+ ".jpg"
        im.save(fn)

if not os.path.exists(img_output_path):  # 判断存放图片的文件夹是否存在
    os.makedirs(img_output_path)  # 若图片文件夹不存在就创建
for i in range(len(images)):
    # 构建图片路径
    path = img_path + images[i]
    print(path)
    
    try:
        compressed_to_jpg_image(path,i)
    # 输出处理失败的图片路径
    except:
        print('*'*30)
        print('Error: '+ path +' failed!')
        print('*'*30)
        continue
    

