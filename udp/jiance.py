from collections import  deque
import numpy as np
#import imutils
import cv2
import time
#设定红色阈值，HSV空间
redLower = np.array([35, 43, 46])
redUpper = np.array([77, 255, 255])
#初始化追踪点的列表
mybuffer = 64
pts = deque(maxlen=mybuffer)

#遍历每一帧，检测红色瓶盖
def zhuizong(frame):
    # 转到HSV空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 根据阈值构建掩膜
    mask = cv2.inRange(hsv, redLower, redUpper)
    # 腐蚀操作
    mask = cv2.erode(mask, None, iterations=2)
    # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    mask = cv2.dilate(mask, None, iterations=2)
    # 轮廓检测
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    # 初始化瓶盖圆形轮廓质心
    center = None
    radius = 0
    # 如果存在轮廓
    if len(cnts) > 0:
        # 找到面积最大的轮廓
        c = max(cnts, key=cv2.contourArea)
        # 确定面积最大的轮廓的外接圆
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        # 计算轮廓的矩
        M = cv2.moments(c)
        # 计算质心
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))  # 圆心坐标将该数据输出即可
        # 只有当半径大于10时，才执行画图
        if radius > 0:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            # 把质心添加到pts中，并且是添加到列表左侧
            pts.appendleft(center)

        # print(center)
        # print(3.14 * radius * radius)
        # 遍历追踪点，分段画出轨迹
        for i in range(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue
            # 计算所画小线段的粗细
            thickness = int(np.sqrt(mybuffer / float(i + 1)) * 2.5)
            # 画出小线段
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    return center,radius

if __name__ =="__main__":
    # 打开摄像头
    camera = cv2.VideoCapture(2)
    # 等待两秒
    time.sleep(2)
    while True:
        # 读取帧
        (ret, frame) = camera.read()
        # 判断是否成功打开摄像头
        if not ret:
            print('No Camera')
            break
        center,radiuss = zhuizong(frame)
        cv2.imshow('Frame', frame)
        print(center)
        print(3.14 * radiuss * radiuss)
        # 键盘检测，检测到esc键退出
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    # 摄像头释放
    camera.release()
    # 销毁所有窗口
    cv2.destroyAllWindows()

