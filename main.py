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
sensor.set_brightness(1000)
sensor.skip_frames(time = 100)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False,(0,0x80,0))  # must turn this off to prevent image washout...
sensor.set_auto_exposure(False,100)

uart = UART(1, baudrate=115200)

world_coordinates = np.array([[40,140],
                     [180,140],
                     [180,40],
                     [40,40]])



detect_area = [0,65,319,175]
result_area = [122,83,83,35]
res_xy=[196,165]

nbytes = 1024
FLAG = 0


red = LED(1)    # 定义一个LED1   红灯
green = LED(2)  # 定义一个LED2   绿灯
blue = LED(3)   # 定义一个LED3   蓝灯
white = LED(4)  # 定义一个LED4   照明灯


#######################################
#返回透视矩阵
#XY为世界坐标，UV为相机坐标
def cal_mtx(UV:np.array,XY:np.array)->np.array:
    A = []
    B =[]
    for i in range(4):
        a = [[UV[i][0],UV[i][1],1,0,0,0,-XY[i][0]*UV[i][0],-XY[i][0]*UV[i][1]],
             [0,0,0,UV[i][0],UV[i][1],1,-XY[i][1]*UV[i][0],-XY[i][1]*UV[i][1]]]
        B+= [[XY[i][0]],
             [XY[i][1]]]
        A+=a

    A = np.array(A)
    B = np.array(B)

    x= np.solve(A,B)

    H = [[x[0][0], x[1][0], x[2][0]],
         [x[3][0], x[4][0], x[5][0]],
         [x[6][0], x[7][0], 1]]

    return np.array(H)
##########################################



######################
def map(img):

    for r in img.find_rects(threshold = 10000):
        #img.draw_rectangle(r.rect(), color = (255, 0, 0))
        point_num=0
        #if r.w()>=135 and r.h()<105 and r.w()<150 and r.h()>90:
        #if r.w()>=230 and r.h()<180 and r.w()<260 and r.h()>160:
        if r.w()>=113 and r.h()<85 and r.w()<120 and r.h()>75:
            img.draw_rectangle(r.rect(), color = (255, 0, 0))
            #print(r.rect())
            img_coordinate=[]

            points =[]
            for c in img.find_circles(roi =r.rect(),threshold = 1500, x_margin = 10, y_margin = 10, r_margin = 10,r_min = 2, r_max =6, r_step = 1):


                c_roi=(c.x()-c.r(),c.y()-c.r(),2*c.r(),2*c.r())
                threshold = (0, 58, -87, 127,-128, 127)
                blobs = img.find_blobs([threshold],roi = c_roi, pixels_threshold=int(0.2*4*c.r()*c.r()), area_threshold=1,
                                        merge=True, margin=10, invert=False)
                img.draw_circle(c.x(), c.y(),2, color = (0, 255, 0),thickness = 4)
                if len(blobs):
                    points.append([c[0], c[1], 1])


            for p in r.corners():
                img.draw_circle(p[0], p[1], 2, color = (0, 0, 255))
                img_coordinate.append([p[0], p[1]])
            if len(img_coordinate)!=4:
                break

            img_coordinate[0][1]-=3
            img_coordinate[1][1]-=3
            point_num += 1
            return  img_coordinate,points
    return None,None

#####################



#####################
def shi() :

      while(True):
          img = sensor.snapshot()


          for r in img.find_rects(threshold = 10000):             # 在图像中搜索矩形
            if r.w()>=60 and r.h()<90 and r.w()<90 and r.h()>60:
              img.draw_rectangle(r.rect(), color = (255, 0, 0))   # 绘制矩形外框，便于在IDE上查看识别到的矩形位置
              img1 = img.copy(1,1,r.rect())                           # 拷贝矩形框内的图像

                # 将矩形框内的图像使用训练好的模型进行分类
                # net.classify()将在图像的roi上运行网络(如果没有指定roi，则在整个图像上运行)
                # 将为每个位置生成一个分类得分输出向量。
                # 在每个比例下，检测窗口都以x_overlap（0-1）和y_overlap（0-1）为指导在ROI中移动。
                # 如果将重叠设置为0.5，那么每个检测窗口将与前一个窗口重叠50%。
                # 请注意，重叠越多，计算工作量就越大。因为每搜索/滑动一次都会运行一下模型。
                # 最后，对于在网络沿x/y方向滑动后的多尺度匹配，检测窗口将由scale_mul（0-1）缩小到min_scale（0-1）。
                # 下降到min_scale(0-1)。例如，如果scale_mul为0.5，则检测窗口将缩小50%。
                # 请注意，如果x_overlap和y_overlap较小，则在较小的比例下可以搜索更多区域...

                # 默认设置只是进行一次检测...更改它们以搜索图像...
              for obj in tf.classify(net , img1, min_scale=1.0, scale_mul=0.0, x_overlap=0.0, y_overlap=0.0,scale=1, offset=0):
                  #print("**********\nTop 1 Detections at [x=%d,y=%d,w=%d,h=%d]" % obj.rect())
                  sorted_list = sorted(zip(labels, obj.output()), key = lambda x: x[1], reverse = True)
                  # 打印准确率最高的结果
                  for i in range(1):
                      if sorted_list[i][1]<0.30:
                           continue
                      print("%s = %f" % (sorted_list[i][0], sorted_list[i][1]))
                      #uart.write('%s'%(sorted_list[i][0]))

                      if(sorted_list[i][0]=='bean'):
                        #uart.write('6,')
                        uart.write('1,-')
                        print('1,-')
                        break

                      if(sorted_list[i][0]=='orange'):
                        #uart.write('6,')
                        uart.write('1,-')
                        print('1,-')
                        break

                      if(sorted_list[i][0]=='cabbage'):
                        #uart.write('6,')
                        uart.write('1,-')
                        print('1,-')
                        break

                      if(sorted_list[i][0]=='potato'):
                        #uart.write('6,')
                        uart.write('2,-')
                        print('2,-')
                        break

                      if(sorted_list[i][0]=='durian'):
                        #uart.write('6,')
                        uart.write('2,-')
                        print('2,-')
                        break

                      if(sorted_list[i][0]=='cucumber'):
                        #uart.write('6,')
                        uart.write('2,-')
                        print('2,-')
                        break

                      if(sorted_list[i][0]=='peanut'):
                        #uart.write('6,')
                        uart.write('3,-')
                        print('3,-')
                        break

                      if(sorted_list[i][0]=='apple'):
                        #uart.write('6,')
                        uart.write('3,-')
                        print('3,-')
                        break

                      if(sorted_list[i][0]=='chili'):
                        #uart.write('6,')
                        uart.write('3,-')
                        print('3,-')
                        break

                      if(sorted_list[i][0]=='rice'):
                        #uart.write('6,')
                        uart.write('4,-')
                        print('4,-')
                        break

                      if(sorted_list[i][0]=='banana'):
                        #uart.write('6,')
                        uart.write('4,-')
                        print('4,-')
                        break

                      if(sorted_list[i][0]=='radish'):
                        #uart.write('6,')
                        uart.write('4,-')
                        print('4,-')
                        break

                      if(sorted_list[i][0]=='corn'):
                        #uart.write('6,')
                        uart.write('5,-')
                        print('5,-')
                        break

                      if(sorted_list[i][0]=='grape'):
                        #uart.write('6,')
                        uart.write('5,-')
                        print('5,-')
                        break

                      if(sorted_list[i][0]=='eggplant'):
                        #uart.write('6,')
                        uart.write('5,-')
                        print('5,-')
                        break
                  break
          break



####################


###################################

def weitiao():
    # 在图像中查找矩形
    img = sensor.snapshot()
    img.draw_rectangle(119, 111, 30, 27, color=(255,0,0))
    rects = img.find_rects(threshold = 10000)

    # 遍历所有检测到的矩形
    for r in rects:
        # 判断矩形大小是否符合要求
        #if r.w()>=140 and r.h()<175 and r.w()<175 and r.h()>135:
        if r.w()>=60 and r.h()<90 and r.w()<90 and r.h()>60:
            # 找到矩形的中心位置
            rect_center = (r.x() + r.w() // 2, r.y() + r.h() // 2)
            img.draw_cross(rect_center[0], rect_center[1])
            # 计算矩形中心点相对于目标位置的偏差
            dx = rect_center[0] - 134
            dy = rect_center[1] - 110
            # 判断矩形相对于车的位置

            if abs(dx) <=15 and abs(dy)<=13:
                print("okokok 6")
                uart.write('6,')
                #uart.write('1,-')
                #time.sleep(2)
                #sensor.set_framesize(sensor.QVGA)
                shi()
                time.sleep(2)
                while(True):
                    if uart.any():
                      data = uart.read(1)
                      if data == b'9':
                        print("Received '9'")
                        break
                      else :
                        continue
                break


            elif abs(dx) <= 15 and dy >13 and dy >0 :#0.5 * sensor.height():
                # 卡片在前面
                print("Card is in behind of the car  444")
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
                print("Card is front the car  333")
                uart.write('3,')
                uart.write('0,-')


#####################################################



show =True
if __name__ == '__main__':
    while(True):
        img = sensor.snapshot()
        #img = img.lens_corr(strength = 0.8, zoom = 1.0).histeq(adaptive=True, clip_limit=3)

        img_coordinate,points =map(img)#地图识别

        if img_coordinate==None:
            continue

        img_coordinate =np.array(img_coordinate)

        H= cal_mtx(img_coordinate,world_coordinates)


        real_point = []
        img.draw_rectangle(40,40,140,100, color = (0, 0, 255))

        show_points=[]
        for c in points:

            coord = np.array([[p] for p in c])#升维
            point = H*coord#透视变换

            x,y = point[0][0]/point[2][0],point[1][0]/point[2][0]
            #点不会太靠近边界
            if x>=40+5 and x<180-5 and y>=40+5 and y<=140-5:
                if show:
                    img.draw_circle(c[0], c[1], 3, color=(255, 0, 0), thickness=4)

                img.draw_circle(int(x), int(y),2, color = (0, 0, 255),thickness = 4)
                x,y = x-40,100-y+(40)
                x,y = (x*5),(y*5)
                show_points.append([x//20+1,y//20+1])
                x = (x//20)*20+10
                y = (y//20)*20+10
                real_point.append([int(x),int(y)])

        if len(points)!=3:
             continue
        print(len(points))

        #uart.write('go\n')
        #uart.write("%d,"%len(points))
        for x , y in real_point:
            print("({}, {})".format(x, y))
            uart.write("{},{},".format(x, y))

        uart.write('-')
        break




#####################
sensor.skip_frames(time = 20)
net_path = "128model_34_0.9939.tflite"                                  # 定义模型的路径
labels = [line.rstrip() for line in open("/sd/shibie.txt")]   # 加载标签
net = tf.load(net_path, load_to_fb=True)                                  # 加载模型
clock = time.clock()
#####################


#sensor.set_framesize(sensor.QQVGA)

while(True):
    if uart.any():
        data = uart.read(1)
        if data == b'9':
            print("Received '9'")
            while(True):
                weitiao()




