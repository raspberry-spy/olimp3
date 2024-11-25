import cv2

# --------- ЗАДАНИЕ_1 ---------
def prog1():
    from djitellopy import Tello
    import threading, time

    tello = Tello() # Инициализация дрона
    event = threading.Event() # Инициализация объекта для передачи событий между потоками
    tello.connect() # Подключение к дрону

    print(f'Заряд батареи: {tello.get_battery()}%')
    print(f'Температура: {tello.get_temperature()} ℃')

    tello.streamon() # Включение камеры дрона
    frame_read = tello.get_frame_read() # Создание объекта чтения кадров
    height, width, _ = frame_read.frame.shape # Получение данных о разрешении камеры
    # Создание объекта для записи видео в файл video_out_1.avi
    video = cv2.VideoWriter('video_out_1.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    # Осуществление управления движением дрона через клавиатуру
    def keycheck():
        while True:
            event.clear()
            event.wait()
            if key == 27:  # Выход на Escape
                break
            elif key == 13:  # Посадка дрона на Enter
                tello.land()
            elif key == 32:  # Выключение дрона на Пробел
                tello.takeoff()
            elif key == ord('w'):  # Движение вперёд на W
                tello.move_forward(50)
            elif key == ord('s'):  # Движение назад на S
                tello.move_back(50)
            elif key == ord('a'):  # Движение влево на A
                tello.move_left(50)
            elif key == ord('d'):  # Движение вправо на D
                tello.move_right(50)
            elif key == ord('e'):  # Поворот по часовой стрелке на 30 градусов клавишей E
                tello.rotate_clockwise(30)
            elif key == ord('q'):  # Поворот против часовой стрелки на 30 градусов клавишей Q
                tello.rotate_counter_clockwise(30)
            time.sleep(0.6)

    threading.Thread(target=keycheck).start() # Запуск потока для проверки нажатия клавиш

    while True:
        frame = frame_read.frame # Получение кадра
        video.write(frame) # Вывод видео с камеры
        cv2.imshow("drone", frame)
        key = cv2.waitKey(25) & 0xff
        if key == 27: # Выход на Escape
            event.set()
            break
        elif key == ord('f'): # Сохранение скриншота клавишей F
            cv2.imwrite('image_out_1.png', frame)
        elif key == 255:
            pass
        else:
            event.set()
    cv2.destroyAllWindows() # Закрытие окна вывода видео
    video.release() # Завершение записи
    frame_read.stop() # Завершение работы объекта чтения кадров
    tello.streamoff() # Завершение видео потока с дрона
    tello.end() # Завершение работы с дроном


# ---------- ЗАДАНИЕ_2 ----------
def prog2():
    from ultralytics import YOLO
    model = YOLO("roofs.pt") # Инициализация модели машинного обучения
    results = model('video_in_2.avi', stream=True) # Запись результатов работы модели
    cap = cv2.VideoCapture("video_in_2.avi") # Создание объекта чтения из файла video_in_2.avi
    fps = int(cap.get(cv2.CAP_PROP_FPS)) # Получение данных о количестве кадров в секунду
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # Получение данных о ширине кадра
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Получение данных о высоте кадра
    w = width // 2 # Координаты центра кадра по оси X
    h = height // 2 # Координаты центра кадра по оси Y
    # Создание объекта для записи видео в файл video_out_2.avi
    video = cv2.VideoWriter('video_out_2.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))
    for r in results: # Перебор результатов для каждого кадра
        ret, frame = cap.read() # Получения кадра с видео
        for box in r.boxes: # Перебор обводки каждого распознанного объекта
            if box.conf[0] > 0.4: # Если значение совпадения больше 40%...
                [x1, y1, x2, y2] = box.xyxy[0] # Получения координат обводки
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # Замена координат обводки на координаты
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2) # Запись обводки на кадр с видео
                xc = (x1 + x2) // 2 # Вычисление центра координат обводки по оси X
                yc = (y1 + y2) // 2 # Вычисление центра координат обводки по оси Y
                # Вставка текста с информацией о расположении обводки на кадре
                cv2.putText(frame, f'{xc - w} {yc - h}', (x1, yc), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
        video.write(frame) # Запись кадра в видео
    video.release() # Завершение записи
    cap.release() # Завершение чтения
    cv2.destroyAllWindows() # Закрытие окна вывода видео


# ---------- ЗАДАНИЕ_3 ----------
def prog3():
    from djitellopy import Tello
    import time, numpy as np

    lower1 = np.array([160, 100, 50])
    upper1 = np.array([180, 255, 255])
    lower2 = np.array([0, 100, 50])
    upper2 = np.array([15, 255, 255])

    tello = Tello()
    tello.connect()

    print(f'Заряд батареи: {tello.get_battery()}%')
    print(f'Температура: {tello.get_temperature()} ℃')

    tello.streamon()
    frame_read = tello.get_frame_read()
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter('video_out_3.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))
    while True:
        frame = frame_read.frame
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, lower1, upper1)
        mask2 = cv2.inRange(hsv, lower2, upper2)
        mask = cv2.add(mask1, mask2)
        frame = cv2.bitwise_and(frame, frame, mask=mask)

        video.write(frame)
        cv2.imshow("drone", frame)
        key = cv2.waitKey(25) & 0xff
        if key == 27:
            break

    cv2.destroyAllWindows()
    video.release()
    frame_read.stop()
    tello.streamoff()
    tello.end()


# ---- ИНТЕРФЕЙС_ПРОВЕРКИ_ЗАДАНИЙ ----
while True:
    uinput = input("Введите номер задания (1-3), 0 для выхода\n")
    if uinput == "1":
        prog1()
    elif uinput == "2":
        prog2()
    elif uinput == "3":
        prog3()
    elif uinput == "0":
        print("Выход из программы")
        break
