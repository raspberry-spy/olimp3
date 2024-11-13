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

tello.streamon()
frame_read = tello.get_frame_read()

tello.takeoff()

def movin():
    while True:
        img = cv2.cvtColor(frame_read.frame, cv2.COLOR_RGB2BGR)
        cv2.imshow("drone", img)
        key = cv2.waitKey(1) & 0xff

threading.Thread(target=movin).start()

print("sus")
while True:
    # In reality you want to display frames in a seperate thread. Otherwise
    #  they will freeze while the drone moves.
    # 在实际开发里请在另一个线程中显示摄像头画面，否则画面会在无人机移动时静
    if key == 27:  # ESC
        break
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
    elif key == ord('r'):
        tello.move_up(50)
    elif key == ord('f'):
        tello.move_down(50)

tello.land()