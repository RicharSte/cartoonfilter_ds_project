import cv2


def apply_cartoon_filter(image):
    """
    Из фотографии создает мультяшное изображение и выводит его.
    На вход получает путь к исходному изображению.
    
    Изменение изображение делится на 5 шагов:
    1. Примените bilateral filter (цветовой фильтр), чтобы уменьшить цветовую палитру изображения.
    2. Преобразуйте исходное цветное изображение в grayscale (оттенки серого).
    3. Примените median blur (медиальное размытие), чтобы уменьшить шум изображения.
    4. Используйте adaptive thresholding (адаптивное пороговое значение) для обнаружения и выделения ребер в маске ребер.
    5. Объедините цветное изображение из шага 1 с краевой маской из шага 4.
    """
    # Считывает данные из файла и переводит в различные форматы
    img = image
    
    josh_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    josh_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    josh_gray = cv2.cvtColor(josh_rgb, cv2.COLOR_RGB2GRAY)
        
    # Количество шагов снижения (экземпляров)
    numDownSamples = 2
    # Количество шагов двусторонней фильтрации
    numBilateralFilters = 7
    # Первый шаг
    # Нисходящее изображение с использованием Гауссовой пирамиды 
    for _ in range(numDownSamples):
        josh_rgb = cv2.pyrDown(josh_rgb)
    # Повторно применяем небольшой двусторонний фильтр 
    for _ in range(numBilateralFilters):
        josh_rgb = cv2.bilateralFilter(josh_rgb, 9, 9, 7)
    # Вверх по образцу изображения до исходного размера
    for _ in range(numDownSamples):
        josh_rgb = cv2.pyrUp(josh_rgb)
    # Комбинируем шаги шаги 2 и 3
    # Преобразование в оттенки серого и применение медианного размытия
    josh_blur = cv2.medianBlur(josh_gray, 7)
    # Четвертый шаг
    # Обнаружение и усиление краев
    img_edge = cv2.adaptiveThreshold(josh_blur, 255,
                                    cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
    # Пятый шаг
    # Объедините цветное изображение из шага 1 с краевой маской из шага 4.
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    try:
        img_result = cv2.bitwise_and(josh_rgb, img_edge)
    except cv2.error:
        raise TypeError("Changed the photo")
    else:
        img_result = cv2.cvtColor(img_result, cv2.COLOR_RGB2BGR)
        return img_result
    