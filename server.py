from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import threading

app = Flask(__name__)

# 存储数据的结构
data_storage = {
    "images": [],  # 存储(时间戳, 图片)元组
    "object_names": []  # 存储(时间戳, 字符串)元组
}

# 锁，用于同步对数据存储的访问
lock = threading.Lock()


# 清理旧数据的函数
def clean_old_data():
    with lock:
        now = datetime.now()
        data_storage["images"] = [(ts, img) for ts, img in data_storage["images"] if now - ts <= timedelta(seconds=5)]
        data_storage["object_names"] = [(ts, string) for ts, string in data_storage["object_names"] if
                                   now - ts <= timedelta(seconds=5)]


@app.route('/uploadResult', methods=['POST'])
def receive_data():
    # 假设图片作为base64编码的字符串接收，实际项目中可能需要调整
    image = request.json.get('object_image')
    print(image)
    object_name = request.json.get('object_name')
    print(object_name)
    timestamp = datetime.now()

    with lock:
        data_storage["images"].append((timestamp, image))
        data_storage["object_names"].append((timestamp, object_name))

    # 清理旧数据
    clean_old_data()

    # 假设这里的发送操作是将数据发送给B，具体实现取决于B的API如何设计
    # send_to_B(data_storage)

    return jsonify({"message": "Data received and processed."}), 200


if __name__ == '__main__':
    app.run(debug=True)