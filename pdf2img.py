import fitz
import os
import datetime
# 版本原因 需要下载 1.18.14版本的PyMuPDf
# pip install PyMuPDf==1.18.14
'''
将PDF转化为图片
pdfPath pdf文件的路径
imgPath 图像要保存的文件夹
zoom_x x方向的缩放系数
zoom_y y方向的缩放系数
rotation_angle 旋转角度
'''
def pdf_image(pdfPath, imgPath, zoom_x, zoom_y, rotation_angle):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间
    # 打开PDF文件
    pdf = fitz.open(pdfPath)
    # 逐页读取PDF
    for pg in range(0, pdf.pageCount):
        page = pdf[pg]
        # 设置缩放和旋转系数
        trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotation_angle)
        pm = page.getPixmap(matrix=trans, alpha=False)
        # 开始写图像
        new_image_path = os.path.join(imgPath, str(pg)+".jpg")
        print(new_image_path)
        pm.writePNG(new_image_path)
    pdf.close()
    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf2img时间=', (endTime_pdf2img - startTime_pdf2img).seconds)

input_filename = r"D:\Documents\aa.pdf"
output_folder = r"D:\Documents\


# 页面读取时未指定读取的dpi，采用默认读取 96dpi 可能会导致图片不清晰
# https://blog.csdn.net/weixin_40959890/article/details/132578609
# import fitz
# from PIL import Image
# doc = fitz.open(r"C:\Users\O-c-O\Desktop\11.pdf")
# for page_number in range(doc.page_count):
#     page = doc.load_page(page_number)
#     # 获取页面的图像对象
#     matrix = fitz.Matrix(1.0, 1.0)  # 1.0 表示原始尺寸
#     # pix = page.get_pixmap(matrix=matrix,dpi=200)
#     pix = page.get_pixmap(dpi=200, alpha=False)
#     print(pix.width,pix.height)
#     # 将图像转换为Pillow的Image对象
#     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#     # 保存图像为PNG格式，不进行压缩
#     dpi = 120  # 设置所需的 DPI 值
#     img.save(f'output_{page_number}.png', dpi=(dpi, dpi),)
#     # img.save(f'output_{page_number}.png',)
# # 关闭文档对象
# doc.close()