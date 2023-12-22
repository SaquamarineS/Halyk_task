import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from signature_detector import model

# Функция для загрузки обученной модели
def load_signature_detection_model(model_path):
    model = load_model(model_path)
    return model

# Функция для обнаружения подписей на изображениях
def extract_signatures(image_directory, model):
    output_directory = os.path.join(image_directory, 'detected_signatures')
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(image_directory):
        if filename.endswith(".jpg"):
            test_image_path = os.path.join(image_directory, filename)
            test_image = cv2.imread(test_image_path)
            test_image_gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
            test_image_gray = cv2.resize(test_image_gray, (128, 128))
            test_image_gray = np.expand_dims(test_image_gray, axis=-1)
            test_image_gray = np.expand_dims(test_image_gray, axis=0)

            prediction = model.predict(test_image_gray)
            if prediction >= 0.5:
                signature_path = os.path.join(output_directory, f'signature_{filename}')
                cv2.imwrite(signature_path, test_image)

                print(f"Файл '{filename}' содержит подпись. Извлеченная подпись сохранена в '{signature_path}'")
            else:
                print(f"Файл '{filename}' НЕ содержит подписи")

# Тестирование модели на новых данных
def predict_signatures(test_image_path):
    test_image = cv2.imread(test_image_path)
    test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
    test_image = cv2.resize(test_image, (128, 128))
    test_image = np.expand_dims(test_image, axis=-1)
    test_image = np.expand_dims(test_image, axis=0)  # Добавление измерения батча

    prediction = model.predict(test_image)
    return prediction[0][0]  # Возвращаем результат предсказания

def extract_signatures(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    signatures = []
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        signature = img[y:y + h, x:x + w]  # Вырезаем область с подписью
        signatures.append(signature)
        cv2.imwrite(f'signature_{i + 1}.jpg', signature)  # Сохраняем каждую подпись в отдельный файл

    return signatures


# Путь к директории с тестовыми изображениями
test_image_directory = r'C:\Users\77003\PycharmProjects\Halyk_task\task_5\test_signature'

# Путь к сохраненной модели для распознавания подписей
model_path = 'signature_detection_model.h5'

# Загрузка модели для распознавания подписей
signature_model = load_signature_detection_model(model_path)

# Извлечение подписей из тестовых изображений
extract_signatures(test_image_directory)
