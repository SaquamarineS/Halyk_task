import color_correlation
import cv2
import dewapper
import signature_extractor
import unsharpen

source_image = cv2.imread("test.jpg")
img = 0

try:
    # Чтение входного изображения и вызов функции dewarp_book
    # для обрезки полей и выпрямления страницы книги
    img = dewapper.dewarp_book(source_image)
    cv2.imwrite("шаг 1 - страница_выровнена.jpg", img)
    print("- шаг 1 (обрезка с полями + выпрямление страницы книги): ОК")
except Exception as e:
    print("Ошибка типа: " + str(e))
    print("ОШИБКА В ОБРЕЗКЕ И ВЫПРЯМЛЕНИИ КНИГИ! ПРОВЕРЬТЕ ОСВЕЩЕНИЕ,"
          " ТЕНИ, УРОВЕНЬ ЗУМА И Т.Д. НА ВАШЕМ ИЗОБРАЖЕНИИ КНИГИ!")

try:
    # Вызов метода extract_signature для извлечения подписи
    img = signature_extractor.extract_signature(cv2.cvtColor(img,
                                                             cv2.COLOR_BGR2GRAY))
    cv2.imwrite("шаг 2 - извлечение_подписи.jpg", img)
    print("- шаг 2 (извлечение подписи): ОК")
except Exception as e:
    print("Ошибка типа: " + str(e))
    print("ОШИБКА ПРИ ИЗВЛЕЧЕНИИ ПОДПИСИ! ПРОВЕРЬТЕ ОСВЕЩЕНИЕ, ТЕНИ,"
          " УРОВЕНЬ ЗУМА И Т.Д. НА ВАШЕМ ИЗОБРАЖЕНИИ КНИГИ!")

try:
    # Вызов метода unsharpen_mask для улучшения резкости изображения
    unsharpen.unsharpen_mask(img)
    cv2.imwrite("шаг 3 - улучшение_резкости.jpg", img)
    print("- шаг 3 (улучшение резкости): ОК")
except Exception as e:
    print("Ошибка типа: " + str(e))
    print("ОШИБКА ПРИ УЛУЧШЕНИИ РЕЗКОСТИ КНИГИ! ПРОВЕРЬТЕ ОСВЕЩЕНИЕ,"
          " ТЕНИ, УРОВЕНЬ ЗУМА И Т.Д. НА ВАШЕМ ИЗОБРАЖЕНИИ КНИГИ!")

try:
    # Вызов метода funcBrightContrast для коррекции цвета
    img = color_correlation.funcBrightContrast(img)
    cv2.imwrite("шаг 4 - корреляция_цвета.jpg", img)
    print("- шаг 4 (корреляция цвета): ОК")
except Exception as e:
    print("Ошибка типа: " + str(e))
    print("ОШИБКА В КОРРЕКЦИИ ЦВЕТА КНИГИ! ПРОВЕРЬТЕ ОСВЕЩЕНИЕ, ТЕНИ,"
          " УРОВЕНЬ ЗУМА И Т.Д. НА ВАШЕМ ИЗОБРАЖЕНИИ КНИГИ!")

cv2.imwrite("вывод.jpg", img)
