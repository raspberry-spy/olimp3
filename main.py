# simple example demonstrating how to control a Tello using your keyboard.
# For a more fully featured example see manual-control-pygame.py
#
# Use W, A, S, D for moving, E, Q for rotating and R, F for going up and down.
# When starting the script the Tello will takeoff, pressing ESC makes it land
#  and the script exit.

# 简单的演示如何用键盘控制Tello
# 欲使用全手动控制请查看 manual-control-pygame.py
#
# W, A, S, D 移动， E, Q 转向，R、F上升与下降.
# 开始运行程序时Tello会自动起飞，按ESC键降落
# 并且程序会退出

from djitellopy import Tello
import cv2, math, time, threading

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