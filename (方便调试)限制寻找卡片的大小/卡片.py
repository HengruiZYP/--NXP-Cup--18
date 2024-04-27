import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_brightness(2000)
sensor.skip_frames(time = 100)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False,(0,0x80,0))  # must turn this off to prevent image washout...
sensor.set_auto_exposure(False,100)
while(True):
    img = sensor.snapshot()

    # 查找所有矩形
    rects = img.find_rects(threshold=1000)

    # 在图像上绘制矩形，并输出矩形长和宽
    for r in rects:
        if r.w() >= 90 and r.h() < 165 and r.w() < 166 and r.h() > 50:
            img.draw_rectangle(r.rect(), color=(255, 0, 0))
            print("Width: %d, Height: %d" % (r.w(), r.h()))
