import cv2
def prog1():
    from djitellopy import Tello
    import threading, time
    tello = Tello()
    event = threading.Event()
    tello.connect()

    print(tello.get_battery())
    print(tello.get_temperature())

    tello.streamon()
    frame_read = tello.get_frame_read()
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter('video_out.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    def keycheck():
        while(True):
            event.clear()
            event.wait()
            if key == 27:
                break
            elif key == 13:
                tello.land()
            elif key == 32:
                tello.takeoff()
            elif key == ord('w'):
                tello.move_forward(50)
            elif key == ord('s'):
                tello.move_back(50)
            elif key == ord('a'):
                tello.move_left(50)
            elif key == ord('d'):
                tello.move_right(50)
            elif key == ord('e'):
                tello.rotate_clockwise(30)
            elif key == ord('q'):
                tello.rotate_counter_clockwise(30)
            time.sleep(0.6)

    threading.Thread(target=keycheck).start()

    while True:
        img = frame_read.frame
        video.write(img)
        cv2.imshow("drone", img)
        key = cv2.waitKey(25) & 0xff
        if key == 27:
            event.set()
            break
        elif key == ord('f'):
            cv2.imwrite('image_out.png', img)
        elif key == 255:
            pass
        else:
            event.set()
    cv2.destroyAllWindows()
    video.release()
    tello.streamoff()
    tello.end()

def prog2():
    from ultralytics import YOLO
    cap = cv2.VideoCapture("video_in.avi")
    model = YOLO("yolo11n.pt")
    results = model('video_in.avi', stream=True)
    for r in results:
        ret, frame = cap.read()
        for box in r.boxes:
            if box.conf[0] > 0.4:
                [x1, y1, x2, y2] = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
    cap.release()
    cv2.destroyAllWindows()

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