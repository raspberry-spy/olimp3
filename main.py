import cv2, time

def prog1():
    from djitellopy import Tello
    import threading
    tello = Tello()
    tello.connect()

    print(tello.get_battery())
    print(tello.get_temperature())

    tello.send_command_without_return('streamoff')
    tello.streamon()
    frame_read = tello.get_frame_read()
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    while True:
        rgb = frame_read.frame
        img = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        video.write(rgb)
        cv2.imshow("drone", img)
        key = cv2.waitKey(1) & 0xff
        if key == 27:
            cv2.destroyAllWindows()
            video.release()
            break
        elif key == 13:
            threading.Thread(target=tello.send_command_without_return, args=['land']).start()
        elif key == 32:
            threading.Thread(target=tello.send_command_without_return, args=['takeoff']).start()
        elif key == ord('w'):
            threading.Thread(target=tello.send_command_without_return, args=['forward 50']).start()
        elif key == ord('s'):
            threading.Thread(target=tello.send_command_without_return, args=['back 50']).start()
        elif key == ord('a'):
            threading.Thread(target=tello.send_command_without_return, args=['left 50']).start()
        elif key == ord('d'):
            threading.Thread(target=tello.send_command_without_return, args=['right 50']).start()
        elif key == ord('e'):
            threading.Thread(target=tello.send_command_without_return, args=['cw 30']).start()
        elif key == ord('q'):
            threading.Thread(target=tello.send_command_without_return, args=['ccw 30']).start()
        elif key == ord('z'):
            threading.Thread(target=tello.send_command_without_return, args=['rc 0 100 0 0']).start()
        elif key == ord('x'):
            threading.Thread(target=tello.send_command_without_return, args=['stop']).start()
        elif key == ord('c'):
            threading.Thread(target=tello.send_command_without_return, args=['emergency']).start()
        elif key == ord('f'):
            cv2.imwrite('image.png', img)

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