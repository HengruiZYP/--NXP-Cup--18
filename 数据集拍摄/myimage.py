from machine import UART
import pyb
import struct
from pyb import LED
import sensor, image, time, math, tf
import os, nncu
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA) # we run out of memory if the resolution is much bigger...
sensor.set_brightness(1500) # ����ͼ������ Խ��Խ��
sensor.skip_frames(time = 20)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()



save_img_num = 0;
img = sensor.snapshot()
for r in img.find_rects(roi=[65,31,211,149],threshold = 30000):
    img.draw_rectangle(r.rect(), color = (255, 0, 0))


    img1 = img.copy(r.rect())
    save_img_num += 1;
    image_pat = "/num"+str(save_img_num)+".jpg"
    img1.save(image_pat,quality=100)


