import cv2


def cartoon_filter(img_dir, save_file_name):
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
    def rgb_img(img_dir):
        # Считывает данные из файла изображения BGR в файл RGB
        img = cv2.imread(img_dir)
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def hsv_img(img_dir):
        # Считывает данные из файла изображения RGB в массив HSV
        hsv = cv2.imread(img_dir)
        return cv2.cvtColor(hsv, cv2.COLOR_RGB2HSV)

    def img_read(img_dir):
        # Считывает данные из файла изображения RGB в массив изображений в оттенках серого
        rgb = rgb_img(img_dir)
        hsv = hsv_img(img_dir)
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        return rgb, hsv, gray
    
    def cartoon_filter(josh_rgb):
        # Количество шагов снижения (экземпляров)
        numDownSamples = 2
        # Количество шагов двусторонней фильтрации
        numBilateralFilters = 7
        # Первый шаг
        # Нисходящее изображение с использованием Гауссовой пирамиды 
        print('Шаг 1')
        img_color = josh_rgb
        for _ in range(numDownSamples):
            img_color = cv2.pyrDown(img_color)
        # Повторно применяем небольшой двусторонний фильтр 
        print('Шаг 2')
        for _ in range(numBilateralFilters):
            img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
        # Вверх по образцу изображения до исходного размера
        print('Шаг 3')
        for _ in range(numDownSamples):
            img_color = cv2.pyrUp(img_color)
        # Комбинируем шаги шаги 2 и 3
        # Преобразование в оттенки серого и применение медианного размытия
        img_gray = cv2.cvtColor(josh_rgb, cv2.COLOR_RGB2GRAY)
        img_blur = cv2.medianBlur(img_gray, 7)
        # Четвертый шаг
        # Обнаружение и усиление краев
        print('Шаг 4')
        img_edge = cv2.adaptiveThreshold(img_blur, 255,
                                        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
        # Пятый шаг
        # Объедините цветное изображение из шага 1 с краевой маской из шага 4.
        print('Шаг 5')
        img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
        return cv2.bitwise_and(img_color, img_edge)

    josh_rgb, josh_hsv, josh_gray = img_read(img_dir)
    josh = cartoon_filter(cv2.cvtColor(josh_rgb, cv2.COLOR_RGB2BGR))
    cv2.imwrite(save_file_name, josh)
    print('Готова обработка и сохранка cartoon_filter')