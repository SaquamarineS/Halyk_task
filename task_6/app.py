from flask import Flask, request, jsonify, send_file, render_template
import os
import uuid
import shutil
from task_5.runner import detect_signatures_in_image, has_signatures

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

OUTPUTS = 'outputs'
if not os.path.exists(OUTPUTS):
        os.makedirs(OUTPUTS)



@app.route('/')
def index():
    return render_template('index.html')

def save_image(image):
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    unique_filename = str(uuid.uuid4())
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename + '.jpg')
    image.save(image_path)
    return unique_filename

@app.route('/upload_images', methods=['POST'])
def upload_images():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files provided'}), 400

    files = request.files.getlist('files[]')
    if len(files) == 0:
        return jsonify({'error': 'No files selected'}), 400

    for file in files:
        if file.filename == '':
            return jsonify({'error': 'One or more files have no name'}), 400

        # Сохранение загруженного изображения
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

    return jsonify({'message': 'Images uploaded successfully'}), 200

# Пока обнаружение не работает
@app.route('/detect_signatures', methods=['POST'])
def detect_signatures():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Сохранение загруженного изображения
    file_id = save_image(file)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}.jpg")

    # Обработка изображения для поиска подписей
    output_folder = 'processed_images'
    detect_signatures_in_image(image_path, output_folder)

    # Проверка наличия подписей
    processed_image_path = os.path.join(output_folder, f"{file_id}.jpg")
    if os.path.exists(processed_image_path):
        has_signature = has_signatures(output_folder)
        if has_signature:
            return send_file(processed_image_path, mimetype='image/jpeg'), 200
        else:
            return jsonify({'error': 'No signatures found'}), 404
    else:
        return jsonify({'error': 'Signature detection failed'}), 500

@app.route('/download_images', methods=['GET'])
def download_images():
    output_folder = 'outputs'

    # Вызов методов для обработки загруженных изображений
    detect_signatures_in_image(app.config['UPLOAD_FOLDER'], output_folder)
    has_signature = has_signatures(output_folder)

    # Создание архива с обработанными изображениями в формате zip
    zip_path = shutil.make_archive('processed_images', 'zip', output_folder)

    # Отправка zip-архива пользователю
    return send_file(zip_path, as_attachment=True), 200

if __name__ == '__main__':
    app.run(debug=True)
