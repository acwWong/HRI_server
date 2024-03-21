import random
import time
import requests
from datetime import datetime

url = 'http://127.0.0.1:3000/uploadResult'



# print(type(open('img.png', 'rb')))

# data = {
#     'objectName': 'Name One',
#     'actionName': 'Name Two',
#     'objectAccuracy': 98.7,
#     'actionAccuracy': 96.9,
#     'timestamp': datetime.now().strftime('%y%m%d%H%M%S')
# }


# response = requests.post(url, files=files, data=data)


while True:

    data = {
        'objectName': 'Name One',
        'actionName': 'Name Two',
        'objectAccuracy': round(random.uniform(90, 100), 1),
        'actionAccuracy': round(random.uniform(90, 100), 1),
        'timestamp': datetime.now().strftime('%y%m%d%H%M%S')
    }

    print(data)


    files = {
        'objectImage': open('img_3.png', 'rb')
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