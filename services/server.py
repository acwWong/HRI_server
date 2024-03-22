from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制为16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

data = {}
def delete_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadResult', methods=['POST'])
def receive_data():
    delete_existing_files(app.config['UPLOAD_FOLDER'])

    objectImage = request.files.get('objectImage')
    objectName = request.form.get('objectName')
    actionName = request.form.get('actionName')
    objectAccuracy = request.form.get('objectAccuracy')
    actionAccuracy = request.form.get('actionAccuracy')
    timestamp = request.form.get('timestamp')

    if not all([objectImage, objectName, actionName, objectAccuracy, actionAccuracy, timestamp]):
        return jsonify({"message": "Missing data"}), 400

    if objectImage and allowed_file(objectImage.filename):
        objectImageName = secure_filename(objectImage.filename)
        objectImage.save(os.path.join(app.config['UPLOAD_FOLDER'], objectImageName))
    else:
        return jsonify({"message": "Invalid object image"}), 400

    try:
        float(objectAccuracy)
        float(actionAccuracy)
    except ValueError:
        return jsonify({"message": "Invalid accuracy value"}), 400

    write_data_to_file(objectName, objectAccuracy, actionName, actionAccuracy)

    return jsonify({"message": "Data received and processed."}), 200

def write_data_to_file(object_name, object_accuracy, action_name, action_accuracy):
    with open('data.txt', 'w') as file:
        file.write(f"Object Name: {object_name}\n")
        file.write(f"Object Accuracy: {object_accuracy}\n")
        file.write(f"Action Name: {action_name}\n")
        file.write(f"Action Accuracy: {action_accuracy}\n")

def get_data():
    data = {}
    try:
        with open('data.txt', 'r') as file:
            for line in file:
                key, value = line.strip().split(': ')
                data[key.strip()] = value.strip()
    except FileNotFoundError:
        pass

    return data


if __name__ == '__main__':
    app.run(debug=True, port=3000)
