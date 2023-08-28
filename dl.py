import os
import requests
from fake_useragent import UserAgent

base_url = 'https://xxxx_{}.pdf'
output_directory = 'temp'

# 创建存储PDF文件的目录
os.makedirs(output_directory, exist_ok=True)

# 创建UserAgent对象
user_agent = UserAgent()

i = 115
while True:
    url = base_url.format(i)
    filename = f'konbu_{i}.pdf'
    output_path = os.path.join(output_directory, filename)

    # 生成随机的用户代理字符串
    headers = {'User-Agent': user_agent.random}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f'Downloaded: {filename}')
        i += 1
    else:
        print(f'No more files to download.')
        break
print(f'**************finish download***********************')

