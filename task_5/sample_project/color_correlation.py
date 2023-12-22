import cv2

contrast = 0
brightness = 0


def funcBrightContrast(img, bright=0):
    """Изменение контрастности и яркости изображения.

    Параметры
    ----------
    img : numpy ndarray
        Входное изображение.
    bright : int
        Уровень яркости.

    Returns
    -------
    numpy ndarray
        Изображение с корректированной яркостью/контрастностью.

    """
    effect = apply_brightness_contrast(img, bright, contrast)
    # сохранение окончательного изображения
    # cv2.imwrite("./outputs/" + output_img, effect)
    return effect


def apply_brightness_contrast(input_img, brightness=255, contrast=127):
    """Выполнение цветовой коррекции входного изображения.

    Параметры
    ----------
    input_img : numpy ndarray
        Входное изображение.
    brightness : int
        Уровень яркости.
    contrast : int
        Уровень контрастности.

    Returns
    -------
    numpy ndarray
        Изображение с корректированной яркостью.

    """
    brightness = 80
    contrast = 60

    # если яркость не равна 0
    if (brightness != 0):
        if (brightness > 0):
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        # вычисление значения альфа
        alpha_b = (highlight - shadow) / 255
        # установка значения гамма
        gamma_b = shadow
        # изменение яркости для использования cv2.addWeighted()
        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()
    # если контрастность не равна 0
    if contrast != 0:
        f = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        # вычисление значения альфа
        alpha_c = f
        # установка значения гамма
        gamma_c = 127*(1-f)
        # изменение контрастности для использования cv2.addWeighted()
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
    # возвращаем цветокорректированное изображение
    return buf
