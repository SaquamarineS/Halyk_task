from flask import Flask, render_template, request, jsonify
import os
import uuid
from task_5.runner import detect_signatures_in_image

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def save_image(image):
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    unique_filename = str(uuid.uuid4())
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename + '.jpg')
    image.save(image_path)
    return unique_filename


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_id = save_image(file)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}.jpg")

    # Обработка изображения для поиска подписей
    output_folder = 'processed_images'
    detect_signatures_in_image(image_path, output_folder)

    processed_image_path = os.path.join(output_folder, f"{file_id}.jpg")
    if os.path.exists(processed_image_path):
        return jsonify({'processed_image': processed_image_path}), 200
    else:
        return jsonify({'error': 'Signature detection failed'}), 500


if __name__ == '__main__':
    app.run(debug=True)
