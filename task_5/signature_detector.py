import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Путь к каталогу с фотографиями подписей
images_directory = r'task_5/teachers_signature'


# Создание датасета из изображений
def create_dataset(directory):
    image_data = []
    labels = []

    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            img = cv2.imread(os.path.join(directory, filename))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Преобразование в оттенки серого
            img = cv2.resize(img, (128, 128))  # Изменение размера изображения
            img = np.expand_dims(img, axis=-1)  # Добавление измерения канала

            # Добавление данных и меток
            image_data.append(img)
            labels.append(1)  # Метка 1 для изображений с подписью

    return np.array(image_data), np.array(labels)


# Загрузка данных
images, labels = create_dataset(images_directory)

# Создание модели нейронной сети
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Компиляция модели
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Обучение модели
model.fit(images, labels, epochs=10, batch_size=32, validation_split=0.2)

# Сохранение модели
model.save('signature_detection_model.h5')


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

# Пример использования функции
image_path_with_multiple_signatures = 'task_5/test_signature/img_1.jpg'
multiple_signatures = extract_signatures(image_path_with_multiple_signatures)



# Пример тестирования на новых данных
'''test_image_path = 'путь_к_тестовому_изображению.jpg'
prediction_result = predict_signatures(test_image_path)
if prediction_result >= 0.5:
    print("Изображение содержит подпись")
else:
    print("Изображение НЕ содержит подписи")
'''