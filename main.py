import cv2
import numpy as np

def prog1():
    from djitellopy import Tello
    import threading
    tello = Tello()
    tello.connect()

    print(tello.get_battery())
    print(tello.get_temperature())

    input()

    tello.streamon()
    frame_read = tello.get_frame_read()

    tello.takeoff()
    print("sus")
    while True:
        img = cv2.cvtColor(frame_read.frame, cv2.COLOR_RGB2BGR)
        cv2.imshow("drone", img)
        key = cv2.waitKey(1) & 0xff
        if key == 27:  # ESC
            break
        elif key == ord('w'):
            threading.Thread(target=tello.move_forward, args=[50]).start()
        elif key == ord('s'):
            threading.Thread(target=tello.move_back, args=[50]).start()
        elif key == ord('a'):
            threading.Thread(target=tello.move_left, args=[50]).start()
        elif key == ord('d'):
            threading.Thread(target=tello.move_right, args=[50]).start()
        elif key == ord('e'):
            threading.Thread(target=tello.rotate_clockwise, args=[30]).start()
        elif key == ord('q'):
            threading.Thread(target=tello.rotate_counter_clockwise, args=[30]).start()
        elif key == ord('r'):
            threading.Thread(target=tello.move_up, args=[50]).start()
        elif key == ord('f'):
            threading.Thread(target=tello.move_down, args=[50]).start()
    tello.land()

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