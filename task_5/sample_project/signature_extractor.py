import cv2
import matplotlib.pyplot as plt
from skimage import measure, morphology
from skimage.measure import regionprops
import numpy as np

# Параметры используются для удаления маленьких связанных пикселей-выбросов
constant_parameter_1 = 84
constant_parameter_2 = 250
constant_parameter_3 = 100

# Параметр используется для удаления больших связанных пикселей-выбросов
constant_parameter_4 = 18

def extract_signature(source_image):
    """Извлекает подпись из входного изображения.

    Parameters
    ----------
    source_image : numpy ndarray
        Входное изображение.

    Returns
    -------
    numpy ndarray
        Изображение с извлеченной подписью.
    """
    # Чтение входного изображения
    img = source_image
    img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  # преобразование в двоичное

    # Анализ связанных компонентов с помощью фреймворка scikit-learn
    blobs = img > img.mean()
    blobs_labels = measure.label(blobs, background=1)
    # image_label_overlay = label2rgb(blobs_labels, image=img)

    fig, ax = plt.subplots(figsize=(10, 6))

    the_biggest_component = 0
    total_area = 0
    counter = 0
    average = 0.0
    for region in regionprops(blobs_labels):
        if (region.area > 10):
            total_area = total_area + region.area
            counter = counter + 1
        # print region.area # (для отладки)
        # Выбор областей с достаточно большой площадью
        if (region.area >= 250):
            if (region.area > the_biggest_component):
                the_biggest_component = region.area

    average = (total_area/counter)
    print("Самая большая компонента: " + str(the_biggest_component))
    print("Средняя площадь: " + str(average))

    # Экспериментальное вычисление коэффициентов, подберите их для вашего случая
    # a4_small_size_outliar_constant используется в качестве порогового значения для удаления связанных выбросов,
    # которые меньше a4_small_size_outliar_constant для документов формата A4
    a4_small_size_outliar_constant = ((average/constant_parameter_1)*constant_parameter_2)+constant_parameter_3
    print("Порог для маленьких выбросов: " + str(a4_small_size_outliar_constant))

    # Экспериментальное вычисление коэффициентов, подберите их для вашего случая
    # a4_big_size_outliar_constant используется в качестве порогового значения для удаления связанных выбросов,
    # которые больше a4_big_size_outliar_constant для документов формата A4
    a4_big_size_outliar_constant = a4_small_size_outliar_constant*constant_parameter_4
    print("Порог для больших выбросов: " + str(a4_big_size_outliar_constant))

    # Удаление связанных пикселей, которые меньше a4_small_size_outliar_constant
    pre_version = morphology.remove_small_objects(blobs_labels, a4_small_size_outliar_constant)
    # Удаление связанных пикселей, которые больше порога a4_big_size_outliar_constant,
    # чтобы избавиться от ненужных связанных пикселей, таких как заголовки таблиц и т. д.
    component_sizes = np.bincount(pre_version.ravel())
    too_small = component_sizes > (a4_big_size_outliar_constant)
    too_small_mask = too_small[pre_version]
    pre_version[too_small_mask] = 0
    # Сохранение pre-version - изображения с цветовой разметкой, учитывая связанные компоненты
    plt.imsave('pre_version.png', pre_version)

    # Чтение pre-version
    img = cv2.imread('pre_version.png', 0)
    # Преобразование в двоичное
    img = cv2.threshold(img, 0, 255,
                        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # Сохранение результата
    # cv2.imwrite("output.png", img)
    return img
