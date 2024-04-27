import sensor, image, time,tf
from machine import UART
import time
import pyb
from pyb import LED
from machine import Pin
import openmv_numpy as np

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_brightness(800)
sensor.skip_frames(time = 100)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
#sensor.set_auto_exposure(False,100)

uart = UART(1, baudrate=115200)
weitiao_threshold = [(68, 100, -78, 127, -11, 127)]
threshold = [(68, 100, -78, 127, -98, 127)]

def adjust_car_position():
    # 在图像中查找矩形
    img = sensor.snapshot()
    img.draw_rectangle(120, 104, 30, 26, color=(255,0,0))
    rects = img.find_blobs(weitiao_threshold , margin=1 , merge=True ,invert=0 )

    # 遍历所有检测到的矩形
    for r in rects:
        # 判断矩形大小是否符合要求
        #if r.w()>=140 and r.h()<175 and r.w()<175 and r.h()>135:
        if r.w()>=60 and r.h()<90 and r.w()<90 and r.h()>60:
            # 找到矩形的中心位置
            rect_center = (r.x() + r.w() // 2, r.y() + r.h() // 2)
            img.draw_cross(rect_center[0], rect_center[1],color=(255,0,0))
            # 计算矩形中心点相对于目标位置的偏差
            dx = rect_center[0] - 135
            dy = rect_center[1] - 117
            # 判断矩形相对于车的位置

            if abs(dx) <=15 and abs(dy)<=13:
                print("okokok 6")
                uart.write('6,')
                uart.write('1,-')
                #sensor.set_framesize(sensor.QVGA)
                #shi()
                break


            elif abs(dx) <= 15 and dy >13 and dy >0 :#0.5 * sensor.height():
                # 卡片在前面
                print("Card is in front of the car  444")
                uart.write('4,')
                uart.write('0,-')

            elif dx < -15:
                # 卡片在车左侧
                print("Card is on the left of the car  222")
                uart.write('2,')
                uart.write('0,-')


            elif dx > 15:
                # 卡片在车右侧
                print("Card is on the right of the car  111")
                uart.write('1,')
                uart.write('0,-')

            else:
                # 卡片在车后面
                print("Card is behind the car  333")
                uart.write('3,')
                uart.write('0,-')

while(True):
    #if uart.any():
     #   data = uart.read(1)
      #  if data == b'9':
       #     print("Received '9'")
        #    while(True):
                adjust_car_position()

