import requests
from datetime import datetime

url = 'http://127.0.0.1:3000/uploadResult'

with open('img.png', 'rb') as object_img, open('img_1.png', 'rb') as action_img:
    files = {
        'objectImage': object_img,
        'actionImage': action_img
    }

    data = {
        'objectName': 'Name One',
        'actionName': 'Name Two',
        'objectAccuracy': 98.7,
        'actionAccuracy': 96.9,
        'timestamp': datetime.now().strftime('%y%m%d%H%M%S')
    }

    response = requests.post(url, files=files, data=data)

# 检查响应
if response.status_code == 200:
    print('Success:', response.json())
else:
    print('Error:', response.text)
