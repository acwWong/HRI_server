from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def delete_existing_files(directory):
    # 删除指定目录下的所有文件
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


@app.route('/uploadResult', methods=['POST'])
def receive_data():
    # 在处理新的上传前，删除之前的所有文件
    delete_existing_files(app.config['UPLOAD_FOLDER'])


    objectImage = request.files.get('objectImage')
    actionImage = request.files.get('actionImage')

    objectName = request.form.get('objectName')
    actionName = request.form.get('actionName')
    accuracy = request.form.get('accuracy')
    timestamp = request.form.get('timestamp')

    if not all([objectImage, actionImage, objectName, actionName, accuracy, timestamp]):
        return jsonify({"message": "Missing data"}), 400


    filename1 = secure_filename(objectImage.filename)
    objectImage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
    filename2 = secure_filename(actionImage.filename)
    actionImage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))

    try:
        accuracy = float(accuracy)
    except ValueError:
        return jsonify({"message": "Invalid accuracy value"}), 400
    return jsonify({"message": "Data received and processed."}), 200


if __name__ == '__main__':
    app.run(debug=True, port=3000)
