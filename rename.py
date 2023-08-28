import os
import shutil

# 获取源文件夹中的所有文件
source_folder = "main"  
target_folder = "renamellll"  
files = os.listdir(source_folder)

# 对文件进行排序
files.sort(key = lambda x: int(x[0:-4]))
# files.sort(key = lambda x: int(x[5:-12]))

#逆序
# reversed_files = files[::-1] 
# print(reversed_files)
# print(files)


# 创建目标文件夹
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 遍历文件并修改文件名并复制到目标文件夹
# offset = 1;
for i, file_name in enumerate(files):
    print(file_name)
    # new_file_name = str((i+1)*2) + ".jpg"
    new_file_name = str(i+1) + ".jpg"
    print(new_file_name)
    print("*"*20)
    source_file_path = os.path.join(source_folder, file_name)
    target_file_path = os.path.join(target_folder, new_file_name)
    shutil.copy(source_file_path, target_file_path)
    # offset = offset + 1
    # if file_name.startswith("img_") and file_name.endswith(".jpg"):
    #     new_file_name = str(i+1) + ".jpg"
    #     print(new_file_name)
    #     source_file_path = os.path.join(source_folder, file_name)
    #     target_file_path = os.path.join(target_folder, new_file_name)
    #     shutil.copy(source_file_path, target_file_path)
# 01234
# 12345
# 246810