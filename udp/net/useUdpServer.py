import socket
import cv2
import time
import numpy
import struct
address = ('127.0.0.1',8080)

class camera():
    def __init__(self, resolution = (640, 480)):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp
        self.server.bind(address)
        self.data, self.add = self.server.recvfrom(10)
        print('接受成功', self.add, self.data)
        self.resolution = resolution
        self.img_quality = 15

    def close(self):
        self.server.close()


    def processConnection(self):
        camera = cv2.VideoCapture(0)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.img_quality]
        while (1):
            time.sleep(0.13)
            (grabbed, self.img) = camera.read()
            self.img = cv2.resize(self.img, self.resolution)
            result, imgencode = cv2.imencode('.jpg', self.img, encode_param)
            img_code = numpy.array(imgencode)
            self.imgdata = img_code.tostring()
            self.server.sendto(self.imgdata, self.add)  # 发送图片信息(图片长度,分辨率,图片内容)


if __name__ == '__main__':
    # server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp
    # server.bind(address)

    my_Cam = camera()
    my_Cam.processConnection()
    print('发发发发发发')
    if 0xFF == ord('q'):
        my_Cam.close()



