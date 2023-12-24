import cv2
import os
import matplotlib.pyplot as plt
from skimage import measure, morphology
from skimage.color import label2rgb
from skimage.measure import regionprops
import numpy as np

def detect_signatures_in_image(input_folder, output_folder):
    # Параметры используются для удаления маленьких связанных пикселей-выбросов
    threshold1 = 84
    threshold2 = 250
    threshold3 = 100
    threshold4 = 18


    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg"):
            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path, 0)
            img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]

            # Анализ связанных компонентов с помощью фреймворка scikit-learn
            blobs = img > img.mean()
            blobs_labels = measure.label(blobs, background=1)

            image_label_overlay = label2rgb(blobs_labels, image=img)

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
                # выбираем области с достаточно большими площадями
                if (region.area >= 250):
                    if (region.area > the_biggest_component):
                        the_biggest_component = region.area

            average = (total_area / counter)
            print("Наибольшая компонента: " + str(the_biggest_component))
            print("Среднее: " + str(average))

            # Расчет параметров на основе эксперимента, подстраивайте под свои случаи
            # a4_small_size_outliar_constant используется в качестве порогового значения для удаления связанных пикселей-выбросов,
            # меньших, чем a4_small_size_outliar_constant для отсканированных документов формата A4
            a4_small_threshold = ((average / threshold1) * threshold2) + threshold3
            print("a4_small_threshold: " + str(a4_small_threshold))

            # Расчет параметров на основе эксперимента, подстраивайте под свои случаи
            # a4_big_size_outliar_constant используется в качестве порогового значения для удаления связанных пикселей-выбросов,
            # больших, чем a4_big_size_outliar_constant для отсканированных документов формата A4
            a4_big_threshold = a4_small_threshold * threshold4
            print("a4_big_threshold: " + str(a4_big_threshold))

            pre_version = morphology.remove_small_objects(blobs_labels, a4_small_threshold)
            component_sizes = np.bincount(pre_version.ravel())
            too_small = component_sizes > (a4_big_threshold)
            too_small_mask = too_small[pre_version]
            pre_version[too_small_mask] = 0
            plt.imsave('pre_version.png', pre_version)
            img = cv2.imread('pre_version.png', 0)
            img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            # Сохраняем результаты в каталог outputs
            output_path = os.path.join(output_folder, f"{output_folder}_{filename}")
            cv2.imwrite(output_path, img)


def has_signatures(input_folder):
    threshold1 = 84
    threshold2 = 250
    threshold3 = 100
    threshold4 = 18

    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg"):
            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path, 0)
            img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]

            blobs = img > img.mean()
            blobs_labels = measure.label(blobs, background=1)

            the_biggest_component = 0
            total_area = 0
            counter = 0
            average = 0.0
            for region in regionprops(blobs_labels):
                if region.area > 10:
                    total_area = total_area + region.area
                    counter = counter + 1

                if region.area >= 250:
                    if region.area > the_biggest_component:
                        the_biggest_component = region.area

            average = total_area / counter
            a4_small_threshold = ((average / threshold1) * threshold2) + threshold3
            a4_big_threshold = a4_small_threshold * threshold4

            component_sizes = np.bincount(blobs_labels.ravel())
            too_small = component_sizes > a4_big_threshold

            if np.any(too_small):
                return True

    return False


if __name__ == "__main__":
    # Получаем список файлов формата JPG в каталоге inputs
    input_folder = 'inputs'
    output_folder = 'outputs'

    # Активация функции
    detect_signatures_in_image(input_folder, output_folder)
