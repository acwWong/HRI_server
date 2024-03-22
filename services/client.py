import os
import random
import time
import requests
from datetime import datetime

url = 'http://127.0.0.1:3000/uploadResult'

# 获取 resources 文件夹路径
resource_folder = 'resources'

# 获取 resources 文件夹中所有图片文件的路径列表
image_files = [os.path.join(resource_folder, img) for img in os.listdir(resource_folder)
               if os.path.isfile(os.path.join(resource_folder, img))
               and img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

while True:

    data = {
        'objectName': 'Name One',
        'actionName': 'Name Two',
        'objectAccuracy': round(random.uniform(90, 100), 1),
        'actionAccuracy': round(random.uniform(90, 100), 1),
        'timestamp': datetime.now().strftime('%y%m%d%H%M%S')
    }

    # 随机选择一个图片文件路径
    random_image_path = random.choice(image_files)

    files = {
        'objectImage': open(random_image_path, 'rb')
    }

    response = requests.post(url, files=files, data=data)
    if response.status_code == 200:
        print('Success:', response.json())
    else:
        print('Error:', response.text)

    files['objectImage'].close()

    time.sleep(1)

# files['objectImage'].close()
# files['actionImage'].close()