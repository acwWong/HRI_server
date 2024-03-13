import requests
from datetime import datetime

url = 'http://127.0.0.1:3000/uploadResult'

files = {
    'objectImage': open('img.png', 'rb'),
    'actionImage': open('img_1.png', 'rb')
}

data = {
    'objectName': 'Name One',
    'actionName': 'Name Two',
    'accuracy': 98.7,
    'timestamp': datetime.now().strftime('%y%m%d%H%M%S')
}


response = requests.post(url, files=files, data=data)


if response.status_code == 200:
    print('Success:', response.json())
else:
    print('Error:', response.text)

files['objectImage'].close()
files['actionImage'].close()
