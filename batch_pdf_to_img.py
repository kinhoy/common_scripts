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
        zoom_x = 1.33333333  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1.33333333
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        pix.writePNG(imagePath + '/' + 'img_%s.png' % pg)  # 将图片写入指定的文件夹内

    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf2img时间=', (endTime_pdf2img - startTime_pdf2img).seconds)


if __name__ == "__main__":
    # 批量导出pdf为图片格式
    pdf_path = 'C:/Users/user/Desktop/aa/'
    to_img_output_path = 'C:/Users/user/Desktop/aa_out/'
    if not os.path.exists(to_img_output_path):
        os.makedirs(to_img_output_path)
    files = os.listdir(pdf_path)
    # images.sort(key = lambda x: int(x[4:-4])) 
    for i in range(len(files)):
        # 构建图片路径
        print('*'*30)
        path = pdf_path + files[i]
        img_path = to_img_output_path + files[i][:-4].strip() #去空格
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        print("PDF路径:"+path)
        print("存放路径："+img_path)
        pyMuPDF_fitz(path, img_path)
        print('*'*30)