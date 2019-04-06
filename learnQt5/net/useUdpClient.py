import socket
import threading
import struct
import os
import numpy
import cv2
address = ('127.0.0.1', 8080)

class rec():
    def __init__(self, resolution = [640,480], windowName = "video"):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = input('请输入')
        self.client.sendto(message.encode('utf-8'), address)
        print('发送成功')
        self.resolution = resolution
        self.name = windowName
        self.src=911+15
        self.interval=0
        self.path=os.getcwd()
        self.img_quality = 15

    def close(self):
        self.client.close()

    def processImage(self):
        while(1):
            data, add = self.client.recvfrom(1024*1024)
            data2 = numpy.fromstring(data, dtype='uint8')
            self.image = cv2.imdecode(data2, 1)
            cv2.imshow(self.name, self.image)

if __name__ == "__main__":
    shou = rec()
    shou.processImage()
    print('接shossss')

    shou.close()
