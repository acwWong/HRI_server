import uuid

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制为16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

def unique_filename(original_filename):
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    unique_name = f"{uuid.uuid4()}.{ext}"
    return unique_name

@app.route('/uploadResult', methods=['POST'])
def receive_data():
    delete_existing_files(app.config['UPLOAD_FOLDER'])

    objectImage = request.files.get('objectImage')
    actionImage = request.files.get('actionImage')
    objectName = request.form.get('objectName')
    actionName = request.form.get('actionName')
    objectAccuracy = request.form.get('objectAccuracy')
    actionAccuracy = request.form.get('actionAccuracy')
    timestamp = request.form.get('timestamp')

    if not all([objectImage, actionImage, objectName, actionName, objectAccuracy, actionAccuracy, timestamp]):
        return jsonify({"message": "Missing data"}), 400

    if objectImage and allowed_file(objectImage.filename):
        objectImageName = secure_filename(objectImage.filename)
        objectImage.save(os.path.join(app.config['UPLOAD_FOLDER'], objectImageName))
    else:
        return jsonify({"message": "Invalid object image"}), 400

    if actionImage and allowed_file(actionImage.filename):
        actionImageName = secure_filename(actionImage.filename)
        actionImage.save(os.path.join(app.config['UPLOAD_FOLDER'], actionImageName))
    else:
        return jsonify({"message": "Invalid action image"}), 400

    try:
        float(objectAccuracy)
        float(actionAccuracy)
    except ValueError:
        return jsonify({"message": "Invalid accuracy value"}), 400

    return jsonify({"message": "Data received and processed."}), 200


if __name__ == '__main__':
    app.run(debug=True, port=3000)
