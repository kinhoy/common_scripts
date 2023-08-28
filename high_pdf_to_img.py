import os
import datetime
# pdfimages -png ./aaa.pdf ./aaa_high/img

# os.chdir(r'C:\Users\Hider\Desktop\pdf-test')
from pdf2image import convert_from_path

def pdf_to_image(file_path,output_path):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间
    if not os.path.exists(output_path): 
        os.makedirs(output_path)
    print('#'*100)
    first = 51
    last = 77
    images = convert_from_path(pdf_path=file_path,
                               dpi=600,
                               first_page = first,
                               last_page = last,
                               thread_count=16,
                               poppler_path='D:\\Develop\\poppler-0.68.0_x86\\bin')
    print('*'*100)
    for index, img in enumerate(images):
        indexss = index + first - 1
        print('正在转换第%s页...' % (indexss))
        output_dir = os.path.join(output_path, 'img_%s.png' % (indexss))
        img.save(output_dir)
    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf2img时间=', (endTime_pdf2img - startTime_pdf2img).seconds)
file_path = 'aaa.pdf'
out_path = 'aaa_high'

if __name__ == '__main__':
    pdf_to_image(file_path,out_path)



# pdf_path：文件路径
# dpi：图片分辨率 默认200
# thread_count：转换的线程数
# poppler_path：指定路径，或者将poppler添加到环境变量path中
# fmt：指定输出格式，目前支持：jpg、png、ppm等