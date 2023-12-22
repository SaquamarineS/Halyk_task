import cv2


def unsharpen_mask(image):
    """Смягчение входного изображения.

    Parameters
    ----------
    image : numpy ndarray
        Входное изображение.

    Returns
    -------
    numpy ndarray
        Смягченное изображение.

    """
    # Применение фильтра GaussianBlur для использования его в маске нерезкости
    gaussian_3 = cv2.GaussianBlur(image, (9, 9), 10.0)
    # Вычисление взвешенной суммы двух массивов (исходного изображения и фильтра GaussianBlur)
    # для выполнения маски нерезкости
    unsharp_image = cv2.addWeighted(image, 1.5, gaussian_3, -0.5, 0, image)
    # Возврат изображения после применения маски нерезкости
    return unsharp_image
