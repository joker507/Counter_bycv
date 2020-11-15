# -*- coding: utf-8 -*-
# @Time : 2020/8/14 13:45
# @Author : XXX
# @Site : 
# @File : Count.py
# @Software: PyCharm ,


import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

class Count:
    def show(self, name, img):
        '''展示图片'''
        cv2.imshow(name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def run(self,img):
        #统一大小
        img = cv2.resize(img,(500,500))
        blur = cv2.GaussianBlur(img,(5,5),0)

        #灰度化
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度处理

        #二值化
        ret, th1 = cv2.threshold(gray_img,120, 255, cv2.THRESH_BINARY)

        #开运算
        #卷积核大小
        #腐蚀
        kernel = np.ones((7, 7), np.uint8)
        erosion = cv2.erode(th1, kernel, iterations=1)  # 腐蚀
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)) #获取结构元素
        # mb = cv2.morphologyEx(th1,cv2.MORPH_OPEN,kernel,iterations=2)

        #距离变换
        dist_img = cv2.distanceTransform(erosion, cv2.DIST_L2, cv2.DIST_MASK_3)  # 距离变换

        #归一化
        dist_output = cv2.normalize(dist_img, 0, 1.0, cv2.NORM_MINMAX)  # 归一化

        #取距离变换后的掩膜，也就是分割后的图像
        ret, th2 = cv2.threshold(dist_output*50 ,0.3, 255, cv2.THRESH_BINARY)

        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(th2, cv2.MORPH_OPEN, kernel)
        # self.show('opening', opening)
        #轮廓检测
        opening = np.array(opening, np.uint8)
        _, contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 轮廓提取
        count = 0
        #统计轮廓
        for cnt in contours:
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x), int(y))
            radius = int(radius)
            circle_img = cv2.circle(img, center, radius, (255, 255, 255), 1)
            area = cv2.contourArea(cnt)
            area_circle = 3.14 * radius * radius
            # print(area/area_circle)
            # if area / area_circle <= 0.5:
            #     # img = cv2.drawContours(img, cnt, -1, (0,0,255), 5)#差（红色）
            #     img = cv2.putText(img, 'bad', center, font, 0.5, (0, 0, 255))
            # elif area / area_circle >= 0.6:
            #     # img = cv2.drawContours(img, cnt, -1, (0,255,0), 5)#优（绿色）
            #     img = cv2.putText(img, 'good', center, font, 0.5, (0, 0, 255))
            # else:
            #     # img = cv2.drawContours(img, cnt, -1, (255,0,0), 5)#良（蓝色）
            #     img = cv2.putText(img, 'normal', center, font, 0.5, (0, 0, 255))
            font = cv2.FONT_HERSHEY_COMPLEX
            img = cv2.putText(img, str(count), center, font, 0.5, (0, 0, 255))
            count += 1
        img = cv2.putText(img, ('sum=' + str(count)), (50, 50), font, 1, (255, 0, 0))

        print('玉米粒共有：', count)
        return count, img

if __name__ == '__main__':

    img_path = str(sys.argv[1]) #参数接收

    # img_path = 'img/1.jpg'
    img = cv2.imread(img_path)
    app = Count()
    count, result = app.run(img)
    cv2.imwrite('result_'+ img_path, result)
    app.show('result',result)