import paddlehub as hub
from matplotlib import pyplot as plt
import cv2
import numpy as np
import time
from tqdm import trange

text_detector = hub.Module(name="chinese_text_detection_db_server", enable_mkldnn=True)       # mkldnn加速仅在CPU下有效

img = cv2.imread('26.jpg')
copy = img.copy()
result = text_detector.detect_text(images=[img],output_dir='.',visualization=True)
data = result[0]['data']

cut_part_number = 12
line_width = img.shape[1] // cut_part_number
for i in range(cut_part_number):
    i = i + 1
    cv2.line(copy,(i*line_width,0),(i*line_width,img.shape[0]),(0,255,0),3)
# 从左到右设定一个区域 识别的文本边框中点位于区域内 才作为有效边框
l = img.shape[1] // cut_part_number * 1
r = img.shape[1] // cut_part_number * 11

min_left = img.shape[1]
max_right = 0
min_up = img.shape[0]
max_down = 0
for re in data:
    # 0左下、1右下、2右上、3左上 官网写的有误!!!
    # 0左上、1右上、2右下、3左下 此为真!!!
    box = [re[1],re[0],re[3],re[2]]
    box = np.intp(box)
    tmp = (re[1][0] - re[0][0]) // 2
    if tmp < l or tmp > r:
        continue
    tmp = (re[2][0] - re[3][0]) // 2
    if tmp < l or tmp > r:
        continue
    # boxPoints返回四个点顺序：右下→左下→左上→右上
    cv2.drawContours(copy, [box], 0, (0,0, 255), 3)
    # cv2.putText(copy, "A", (re[0][0],re[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
    min_left = min(re[0][0],re[3][0],min_left)
    max_right = max(re[1][0],re[2][0],max_right)
    min_up = min(re[0][1],re[1][1],min_up)
    max_down = max(re[2][1],re[3][1],max_down)
# cv2.drawContours(copy, [max_s_box], 0, (255,0, 0), 3)
print(f"左侧 {min_left}, 右侧 {max_right} 上侧 {min_up}, 下侧 {max_down}")
# 裁剪坐标为[y0:y1, x0:x1]
# img.shape[0]：图像的垂直尺寸（高度）
# img.shape[1]：图像的水平尺寸（宽度）

# offset  = 80 if (min_left-80) > 0 else 0
offset = 0
# 裁剪
cut_part = img[min_up:max_down+offset, min_left:max_right+offset]
print(f"cut_part:{cut_part.shape}")

height = img.shape[0]
width = cut_part.shape[1]
# 创建新的白色背景图像
new_image = np.ones((img.shape[0], img.shape[1], 3), dtype=np.uint8) * 255
print(f"new_image:{new_image.shape}")

x_offset = (img.shape[1] - cut_part.shape[1]) // 2
y_offset = (img.shape[0] - cut_part.shape[0]) // 2
print(f"x_offset:{x_offset} , y_offset:{y_offset}")
# 合成图片
new_image[y_offset:y_offset + cut_part.shape[0], x_offset:x_offset + width] = cut_part

# 插入页码
cv2.putText(new_image, "26", (new_image.shape[1]//2,new_image.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 0), 8)

plt.subplot(131), plt.imshow(copy), plt.title('drawContours')
plt.xticks([]), plt.yticks([])

plt.subplot(132), plt.imshow(cut_part), plt.title('cut_part')
plt.xticks([]), plt.yticks([])

plt.subplot(133), plt.imshow(new_image), plt.title('new_image')
plt.xticks([]), plt.yticks([])

plt.tight_layout()
plt.show()

# for i in trange(1000):
#     # do something
#     print(1*"$")
#     time.sleep(0.5)