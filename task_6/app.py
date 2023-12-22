import fitz
from flask import Flask, request, jsonify
import cv2
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Загрузка предварительно обученной модели
model = load_model('signature_detection_model.h5')


def extract_images_from_pdf(pdf_path):
    images = []
    pdf_document = fitz.open(pdf_path)

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 4)[:, :, :3]
        images.append(img)

    pdf_document.close()
    return images


# Маршрут для обнаружения подписей в PDF-файле
@app.route('/detect_signature_in_pdf', methods=['POST'])
def detect_signature_in_pdf():
    file = request.files['file']
    file_bytes = file.read()

    # Проверка типа загруженного файла (pdf или изображение)
    if file.filename.lower().endswith('.pdf'):
        images = extract_images_from_pdf(file_bytes)
    else:
        img = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        images = [gray_img]

    # Обнаружение подписей на каждом изображении
    signature_results = []
    for idx, image in enumerate(images):
        resized_img = cv2.resize(image, (128, 128))
        resized_img = np.expand_dims(resized_img, axis=-1)
        resized_img = np.expand_dims(resized_img, axis=0)

        prediction = model.predict(resized_img)
        if prediction[0][0] >= 0.5:
            result = f"На странице {idx + 1} обнаружена подпись"
        else:
            result = f"На странице {idx + 1} подписей не обнаружено"

        signature_results.append(result)

    return jsonify({"results": signature_results})


if __name__ == '__main__':
    app.run(debug=True)
