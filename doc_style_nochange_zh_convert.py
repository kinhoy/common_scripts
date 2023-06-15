#保留word原样格式不变的情况下 
#进行简体繁体的转化
# zh-cn 大陆简体 zh-tw 台灣正體
# zh-hk 香港繁體 zh-sg 马新简体
# zh-hans 简体
# zh-hant 繁體
# s2t 简体到繁体
# t2s 繁体到简体
import os
from zipfile import ZipFile
import zipfile
from zhconv import convert
from opencc import OpenCC
import shutil
import tempfile
input_file_path = 'aa.docx'
output_file_path = 'bb.docx'

document=ZipFile(input_file_path)
xml=document.read("word/document.xml")
input_text = xml.decode("utf-8")
# style = 'zh-hans'
# output_zhconv = convert(input_text, style) 用zhconv库识别
cc = OpenCC('t2s')
output_opencc = cc.convert(input_text)

input_text = output_opencc.encode('utf-8')
new_content = input_text

# 创建一个临时目录
temp_dir = tempfile.mkdtemp()
try:
    # 解压原始的 docx 文件到临时目录
    with zipfile.ZipFile(input_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    # 替换临时文件中的 word/document.xml 文件内容
    new_file_path = os.path.join(temp_dir, 'word/document.xml')
    with open(new_file_path, 'wb') as file:
        file.write(new_content)

    # 创建一个新的 docx 文件，并将临时文件中的所有内容添加到其中
    new_docx_file = output_file_path
    with zipfile.ZipFile(new_docx_file, 'w') as zip_ref:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, temp_dir)
                zip_ref.write(file_path, rel_path)

    # 将新的 docx 文件重命名为原始文件名
    # shutil.move(new_docx_file, input_file_path)
finally:
    # 清理临时目录
    shutil.rmtree(temp_dir)