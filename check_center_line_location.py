import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image  
import matplotlib.pyplot as plt
import numpy as np
import os 

img_path = r"D:\Documents\cut"


def cut_center(image):
    print(f'裁剪之前的图片尺寸{image.shape}')
    # img.shape[0]：图像的垂直尺寸（高度）
    # img.shape[1]：图像的水平尺寸（宽度）
    cut_width_left = 300
    cut_width_right = 300
    origin_width = image.shape[1]
    origin_high = image.shape[0]
    # 裁剪坐标为[y0:y1, x0:x1]
    central_line_part = image[0:origin_high, origin_width//2-cut_width_left:origin_width//2+cut_width_right]
    return central_line_part

def get_images(img_path):
    images = []
    files = os.listdir(img_path)
    n = len(files)
    for _ in range(5):
        ind = np.random.randint(0, n)
        img_dir = os.path.join(img_path, files[ind])
        print(img_dir)
        img = cv.imread(img_dir)
        img = cut_center(img)
        images.append(img)
    return images
images = get_images(img_path)  

plt.subplot(141), plt.imshow(images[0]), plt.title('img1')
plt.xticks([]), plt.yticks([])

plt.subplot(142), plt.imshow(images[1]), plt.title('img2')
plt.xticks([]), plt.yticks([])

plt.subplot(143), plt.imshow(images[2]), plt.title('img3')
plt.xticks([]), plt.yticks([])

plt.subplot(144), plt.imshow(images[3]), plt.title('img4')
plt.xticks([]), plt.yticks([])

plt.tight_layout()
plt.show()