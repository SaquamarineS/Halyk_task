from signature_methods import *


if __name__ == "__main__":
    # Путь к директории с тестовыми изображениями
    test_image_directory = r'C:\Users\77003\PycharmProjects\Halyk_task\task_5\test_signature'

    # Путь к сохраненной модели для распознавания подписей
    model_path = 'signature_detection_model.h5'

    # Загрузка модели для распознавания подписей
    signature_model = load_signature_detection_model(model_path)

    # Извлечение подписей из тестовых изображений
    extract_signatures(test_image_directory, signature_model)

    # Пример тестирования на новых данных для нескольких изображений
    test_image_directory = r'C:\Users\77003\PycharmProjects\Halyk_task\task_5\test_signature'  # Указать путь к директории с тестовыми изображениями
    for filename in os.listdir(test_image_directory):
        if filename.endswith(".jpg"):
            test_image_path = os.path.join(test_image_directory, filename)
            prediction_result = predict_signatures(test_image_path, signature_model)
            if prediction_result >= 0.5:
                print(f"Файл '{filename}' содержит подпись")
            else:
                print(f"Файл '{filename}' НЕ содержит подписи")



