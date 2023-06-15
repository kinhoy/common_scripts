import datetime
import os
import fitz  # fitz就是pip install PyMuPDF

# 是版本原因，需要下载    1.18.14版本的PyMuPDf
# pip install PyMuPDf==1.18.14

def pyMuPDF_fitz(pdfPath, imagePath):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间

    print("imagePath=" + imagePath)
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 2.0  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 2.0
        # 将缩放系数zoom_x和zoom_y设置为2.0，以增加图像的缩放比例。这样可以间接提高图像的清晰度
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath): 
            os.makedirs(imagePath)

        pix.writePNG(imagePath + '/' + 'img_%s.png' % pg)  # 将图片写入指定的文件夹内
    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf2img时间=', (endTime_pdf2img - startTime_pdf2img).seconds)


pdf_path = "./b.pdf"
output_path = "./bbbbs_img"
pyMuPDF_fitz(pdf_path, output_path)

# if __name__ == "__main__":
#     # 1、PDF地址
#     pdfPath = './a.pdf'
#     # 2、需要储存图片的目录
#     imagePath = './a_img'
#     pyMuPDF_fitz(pdfPath, imagePath)