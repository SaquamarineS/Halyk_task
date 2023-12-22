import cv2
import imutils
import numpy as np
from utils.transform import four_point_transform


def dewarp_book(image):
    """Исправление искажений изображения (деварпинг).

    Параметры
    ----------
    image : numpy ndarray
        Входное изображение.

    Returns
    -------
    numpy ndarray
        Деварпированное изображение.

    """
    # Получение соотношения сторон изображения для сохранения лучшего качества разрешения выходного изображения
    ratio = image.shape[0] / 500.0
    # Копирование исходного изображения для операций фильтрации
    orig = image.copy()
    # Изменение размера входного изображения
    image = imutils.resize(image, height=500)

    # Преобразование в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Параметр sigma используется для автоматического обнаружения границ методом Canny
    sigma = 0.33

    # Вычисление медианы интенсивности пикселей одного канала
    v = np.median(image)

    # Применение автоматического обнаружения границ методом Canny с использованием вычисленной медианы
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # Применение морфологической операции расширения для соединения точек пикселей изображения
    '''kernel = np.ones((5,5),np.uint8)
    edged = cv2.dilate(edged,kernel,iterations = 1)'''

    # Поиск контуров
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    # Цикл по контурам
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    # Применение преобразования четырех точек для деварпинга книги
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    return warped
