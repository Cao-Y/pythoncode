#-*- coding: UTF-8 -*-
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5 import QtGui,QtCore
from cameratest2 import *
import cv2



class my_Window(QMainWindow,Ui_MainWindow): #继承Qt Designer设计的ui
    def __init__(self):
        super(my_Window, self).__init__()
        self.setupUi(self)
        self.cap = cv2.VideoCapture(0) #获取0号摄像头
        self.textBrowser.append('摄像头1\n')
        self.cap2 = cv2.VideoCapture(2)  #获取2号摄像头
        self.textBrowser.append('摄像头2')
        self.timer = QtCore.QTimer()
        self.timer.start()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.start)  #0号摄像头开始使用
        self.timer.timeout.connect(self.start2)   #2号摄像头开始使用
        self.comboBox.currentIndexChanged.connect(self.selectChange)  #下拉菜单切换摄像头
        self.comboBox_2.currentIndexChanged.connect(self.selectChange2)
        self.show()

    def selectChange(self,i):  #切换摄像头
        self.cap.release()
        #self.cap2.release()
        self.cap = cv2.VideoCapture(i)
       # self.cap2 = cv2.VideoCapture(i-1)

    def selectChange2(self,i):  #切换摄像头
        self.cap2.release()
        #self.cap2.release()
        self.cap2= cv2.VideoCapture(i+2)
       # self.cap2 = cv2.VideoCapture(i-1)



    def start(self): #开启摄像头

        flag, image = self.cap.read()

        #show = cv2.resize(image, (640, 480))
        show = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # print(show.shape[1], show.shape[0])
        # show.shape[1] = 640, show.shape[0] = 480
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(showImage))  #摄像头信息传给label

    def start2(self):#开启另外摄像头

        flag, image = self.cap2.read()

        #show = cv2.resize(image, (640, 480))
        show = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # print(show.shape[1], show.shape[0])
        # show.shape[1] = 640, show.shape[0] = 480
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_2.setPixmap(QtGui.QPixmap.fromImage(showImage))  #摄像头信息传给label


if __name__ =='__main__':
    app =QApplication(sys.argv)
    myWin =my_Window()
    sys.exit(app.exec_())
