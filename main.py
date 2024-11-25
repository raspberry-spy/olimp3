import cv2


def prog1():
    from djitellopy import Tello
    import threading, time
    # Инициализация дрона
    tello = Tello()
    event = threading.Event()
    tello.connect()

    print(f'Заряд батареи: {tello.get_battery()}%')
    print(f'Температура: {tello.get_temperature()} ℃')

    # Включение камеры дрона
    tello.streamon()
    # Создание объекта чтения кадров
    frame_read = tello.get_frame_read()
    # Получение данных о разрешении камеры
    height, width, _ = frame_read.frame.shape
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
            elif key == ord('a'):  # Поворот налево на A
                tello.move_left(50)
            elif key == ord('d'):  # Поворот направо на D
                tello.move_right(50)
            elif key == ord('e'):  # Поворот по часовой стрелке на 30 градусов клавишей E
                tello.rotate_clockwise(30)
            elif key == ord('q'):  # Поворот против часовой стрелки на 30 градусов клавишей Q
                tello.rotate_counter_clockwise(30)
            time.sleep(0.6)

    threading.Thread(target=keycheck).start()

    while True:
        frame = frame_read.frame # Получение кадра
        video.write(frame) # Вывод видео с камеры
        cv2.imshow("drone", frame)
        key = cv2.waitKey(25) & 0xff
        if key == 27: # Для выхода из цикла
            event.set()
            break
        elif key == ord('f'): # Сохранение скриншота клавишей F
            cv2.imwrite('image_out_1.png', frame)
        elif key == 255:
            pass
        else:
            event.set()
    cv2.destroyAllWindows() # Завершение с cv2
    video.release() # Завершение записи
    tello.streamoff() # Завершение видео потока с дрона
    tello.end() # Завершение работы с дроном


def prog2():
    from ultralytics import YOLO
    model = YOLO("roofs.pt") # Инициализация модели машинного обучения
    results = model('video_in_2.avi', stream=True) # Запись результатов работы модели
    cap = cv2.VideoCapture("video_in_2.avi") # Создание объекта чтения из файла video_in_2.avi
    fps = int(cap.get(cv2.CAP_PROP_FPS)) # Получение данных о количестве кадров в секунду
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # Получение данных о ширине
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Получение данных о высоте
    w = width // 2
    h = height // 2
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
                cv2.putText(frame, f'{xc - w} {yc - h}', (x1, yc), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
        video.write(frame) # Запись кадра в видео
    video.release() # Завершение записи
    cap.release() # Завершение чтения
    cv2.destroyAllWindows() # Завершение работы с cv2


def prog3():
    from djitellopy import Tello
    import time, numpy as np


    lower1 = np.array([160, 100, 50])
    upper1 = np.array([180, 255, 255])
    lower2 = np.array([0, 100, 50])
    upper2 = np.array([15, 255, 255])

    # Инициализация дрона
    tello = Tello()
    tello.connect()

    print(f'Заряд батареи: {tello.get_battery()}%')
    print(f'Температура: {tello.get_temperature()} ℃')

    # Включение камеры дрона
    tello.streamon()
    # Создание объекта чтения кадров
    frame_read = tello.get_frame_read()
    # Получение данных о разрешении камеры
    height, width, _ = frame_read.frame.shape
    # Создание объекта для записи видео в файл video_out_3.avi
    video = cv2.VideoWriter('video_out_3.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))
    while True:
        # Получение кадра
        frame = frame_read.frame

        template = cv2.imread('drone.png')
        w, h = template.shape[:-1]

        res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        threshold = .8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        video.write(frame)
        cv2.imshow("drone", frame)
        key = cv2.waitKey(25) & 0xff
        if key == 27:
            break

    cv2.destroyAllWindows()
    video.release()
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
