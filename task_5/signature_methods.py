import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Функция для загрузки обученной модели
def load_signature_detection_model(model_path):
    model = load_model(model_path)
    return model

# Тестирование модели на новых данных
def predict_signatures(test_image_path, model):
    test_image = cv2.imread(test_image_path)
    test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
    test_image = cv2.resize(test_image, (128, 128))
    test_image = np.expand_dims(test_image, axis=-1)
    test_image = np.expand_dims(test_image, axis=0)  # Добавление измерения батча

    prediction = model.predict(test_image)
    return prediction[0][0]  # Возвращаем результат предсказания

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

            # Предсказание подписи с помощью модели
            test_image_gray_resized = cv2.resize(test_image_gray, (128, 128))
            test_image_gray_resized = np.expand_dims(test_image_gray_resized, axis=-1)
            test_image_gray_resized = np.expand_dims(test_image_gray_resized, axis=0)
            prediction = model.predict(test_image_gray_resized)

            if prediction >= 0.5:
                contours, _ = cv2.findContours(test_image_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Создание новой папки для каждого изображения с подписями
                signature_folder = os.path.join(output_directory, f'signature_{filename}')
                if not os.path.exists(signature_folder):
                    os.makedirs(signature_folder)

                i = 1
                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    signature = test_image[y:y + h, x:x + w]

                    # Сохранение каждой обнаруженной подписи в отдельный файл
                    signature_path = os.path.join(signature_folder, f'signature_{i}.jpg')
                    cv2.imwrite(signature_path, signature)

                    print(f"Файл '{filename}' содержит подпись. Извлеченная подпись сохранена в '{signature_path}'")
                    i += 1
            else:
                print(f"Файл '{filename}' НЕ содержит подписи")






