from flask import Flask, request, jsonify, send_file
import os
import uuid
from task_5.runner import detect_signatures_in_image


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'  # Папка для сохранения загруженных изображений
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def save_image(image):
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    unique_filename = str(uuid.uuid4())  # Генерация уникального идентификатора
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename + '.jpg')
    image.save(image_path)  # Сохранение изображения на сервере

    return unique_filename  # Возвращаем уникальный идентификатор файла


# Загрузка изображения
@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']
    unique_filename = str(uuid.uuid4())  # Генерация уникального имени файла
    image_path = os.path.join('uploads', unique_filename + '.jpg')
    image.save(image_path)  # Сохранение загруженного изображения

    # Вызываем вашу функцию для обработки загруженного изображения
    output_folder = 'processed_images'
    detect_signatures_in_image('uploads', output_folder)

    processed_image_path = os.path.join(output_folder, unique_filename + '.jpg')
    if os.path.exists(processed_image_path):
        return send_file(processed_image_path, mimetype='image/jpeg'), 200
    else:
        return jsonify({'error': 'Signature detection failed'}), 500



if __name__ == '__main__':
    app.run(debug=True)
