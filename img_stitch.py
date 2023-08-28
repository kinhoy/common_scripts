# 图片拼接
from PIL import Image
# pil paste可以进行图片拼接
import cv2
import numpy as np

file_path="C:/Users/user/Desktop/underground/"
path = file_path + str(0)+".png"
img_out=cv2.imread(path)

num=12
for i in range(1,num):
    path=file_path+str(i)+".png"
    print(path)
    img_tmp=cv2.imread(path)
    #横向
    img_out = np.concatenate((img_out, img_tmp), axis=1)
# 纵向
# img_out = np.concatenate((img_out, img_tmp)) 
# cv2.imshow("IMG",img_out)
cv2.imwrite(file_path+"res.png",img_out)
# cv2.waitKey(0)