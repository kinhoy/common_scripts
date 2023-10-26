import paddlehub as hub
from matplotlib import pyplot as plt
import cv2
import numpy as np

text_detector = hub.Module(name="chinese_text_detection_db_server", enable_mkldnn=True)       # mkldnn加速仅在CPU下有效

img = cv2.imread('76.jpg')
copy = img.copy()
result = text_detector.detect_text(images=[img],output_dir='.',visualization=True)
# ,use_gpu=True)
# print(result)

# 参数
# def detect_text(paths=[],
#                 images=[],
#                 use_gpu=False,
#                 output_dir='detection_result',
#                 box_thresh=0.5,
#                 visualization=False)
# paths (list[str]): 图片的路径；
# images (list[numpy.ndarray]): 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
# use_gpu (bool): 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
# box_thresh (float): 检测文本框置信度的阈值；
# visualization (bool): 是否将识别结果保存为图片文件；
# output_dir (str): 图片的保存路径，默认设为 detection_result；

# 返回
# res (list[dict]): 识别结果的列表，列表中每一个元素为 dict，各字段为：
# data (list): 检测文本框结果，文本框在原图中的像素坐标，4*2的矩阵，依次表示文本框左下、右下、右上、左上顶点的坐标
# ave_path (str): 识别结果的保存路径, 如不保存图片则save_path为''

data = result[0]['data']
center = img.shape[1]//2
print(f"center:{center}")
min_left = img.shape[1]
max_right = 0
center_left = 0
center_right = img.shape[1]

# i = 0
for re in data:
    # 0左下、1右下、2右上、3左上
    # [[6053, 4508], [6156, 4508], [6156, 4590], [6053, 4590]]
    box = [re[1],re[0],re[3],re[2]]
    box = np.intp(box)
    # boxPoints返回四个点顺序：右下→左下→左上→右上
    # cv2.drawContours(copy, [box], 0, (0,0, 255), 3)
    # cv2.putText(copy, str(i)+":"+str(re[2][0]-re[3][0]), (re[2][0],re[2][1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
    # min_left = min(re[0][0],re[3][0],min_left)
    # max_right = max(re[1][0],re[2][0],max_right)
    # i = i+1
    tmp1 = (re[3][0]+re[2][0])//2
    tmp2 = (re[0][0]+re[1][0])//2
    if tmp1 < center or tmp2 < center:
        # 框在左
        min_left = min(re[0][0],re[3][0],min_left)
        center_left = max(re[1][0],re[2][0],center_left)
        cv2.drawContours(copy, [box], 0, (255,0, 0), 3)
    else:
        # 框在右
        print(f"右上x:{re[2][0]} 右下x:{re[1][0]} center:{center}")
        center_right = min(re[0][0],re[3][0],center_right)
        max_right = max(re[1][0],re[2][0],max_right)
        cv2.drawContours(copy, [box], 0, (0,0, 255), 3)

    

print(f"左侧 {min_left} {center_left}, 右侧 {center_right}  {max_right}")
# 裁剪坐标为[y0:y1, x0:x1]
# img.shape[0]：图像的垂直尺寸（高度）
# img.shape[1]：图像的水平尺寸（宽度）
# cut_part = copy[0:copy.shape[0],min_left:max_right]

offset  = 80 if (min_left-80) > 0 else 0
# 裁剪
left_part = copy[0:copy.shape[0], min_left-offset:center_left+offset]
right_part = copy[0:copy.shape[0], center_right-offset:max_right+offset]
print(f"left_part:{left_part.shape} , right_part:{right_part.shape}")

height = img.shape[0]
width = left_part.shape[1]
# 创建新的白色背景图像
new_left_image = np.ones((height, center, 3), dtype=np.uint8) * 255
new_right_image = new_left_image.copy()

print(f"new_left_image:{new_left_image.shape} , new_right_image:{new_right_image.shape}")

if left_part.shape[1] >= new_left_image.shape[1]:
    new_left_image = left_part
else:
    x_offset = (center - width) // 2
    y_offset = (height - left_part.shape[0]) // 2
    print(f"x_offset:{x_offset} , y_offset:{y_offset}")
    new_left_image[y_offset:y_offset + left_part.shape[0], x_offset:x_offset + width] = left_part
if right_part.shape[1] >= new_right_image.shape[1]:
    new_right_image = right_part
else:
    width = right_part.shape[1]
    x_offset = (center - width) // 2
    y_offset = (height - right_part.shape[0]) // 2
    print(f"x_offset:{x_offset} , y_offset:{y_offset}")
    new_right_image[y_offset:y_offset + right_part.shape[0], x_offset:x_offset + width] = right_part

plt.subplot(161), plt.imshow(img), plt.title('Original')
plt.xticks([]), plt.yticks([])

plt.subplot(162), plt.imshow(copy), plt.title('after')
plt.xticks([]), plt.yticks([])

plt.subplot(163), plt.imshow(left_part), plt.title('left_part')
plt.xticks([]), plt.yticks([])

plt.subplot(164), plt.imshow(right_part), plt.title('right_part')
plt.xticks([]), plt.yticks([])

plt.subplot(165), plt.imshow(new_left_image), plt.title('new_left_image')
plt.xticks([]), plt.yticks([])

plt.subplot(166), plt.imshow(new_right_image), plt.title('new_right_image')
plt.xticks([]), plt.yticks([])


plt.tight_layout()
plt.show()