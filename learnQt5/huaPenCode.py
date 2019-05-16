# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5 import QtCore,QtGui
import cv2
from huapen import *
import time
import serial
import serial.tools.list_ports
import re

class my_Window(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(my_Window, self).__init__()
        self.setupUi(self)
        self.cap = cv2.VideoCapture(0) #获取0号摄像头
        self.command = 'a'  # 传输给控制板的命令
        self.message = []
        self.all_ports =[]
        self.timer = QtCore.QTimer()
        self.timer1 = QtCore.QTimer()
        self.timer.start()
        self.timer1.start()
        self.timer.setInterval(1)
        self.timer1.setInterval(1.5)
        self.timer.timeout.connect(self.start)    #0号摄像头开始使用
        self.textEdit.setPlainText("Start to use")
        self.ser = self.read_ports()
        self.timer1.timeout.connect(self.displayMessage)
        self.lineEdit.textChanged['QString'].connect(self.receve)
        self.Button.clicked.connect(self.displayMessage)  #点击按钮发送信息给控制板
        self.Button.clicked.connect(self.displayText1) #点击按钮在文本框中显示信息
        self.show()

    def displayText1(self):  #设置文本框显示信息
        self.textEdit.append("update message")


    def receve(self):  #获得文本框输入信息
        self.command = self.lineEdit.text()

    def read_ports(self):
        """获取当下所有设备号"""
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) <= 0:
            self.all_ports = []
        else:
            for ports in port_list:
                port_list_0 = ''.join(str(i) for i in list(ports)[0])
                self.all_ports.append(port_list_0)
                ser = serial.Serial(self.all_ports[0], 115200)
            return ser


    def start(self):
        try:
            flag, image = self.cap.read()  # 读取摄像头
            show = cv2.resize(image, (200, 200))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 处理读取的图像信息
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            self.label_5.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 摄像头信息传给label
        except:
            self.textEdit.append("start camera error")
            self.cap.release
            self.timer.stop()



    def recevemessage(self):  #发送给控制板信息，并读取控制板传来的信息
        self.number = []
        self.number = self.all_ports
        if self.number:
            time.sleep(1.0)
            self.ser.write(self.command.encode('utf-8'))
            time.sleep(2.8)
            allMessage = self.ser.read(self.ser.inWaiting())
            return allMessage
        else :
            return 0

    def allsendandreceve(self):
        self.number = []
        self.number = self.all_ports
        if self.number:
            self.ser = serial.Serial(self.number[0], 115200)
            time.sleep(1.0)
            self.ser.write(self.command.encode('utf-8'))
            time.sleep(2.8)
            allMessage = self.ser.read(self.ser.inWaiting())
            return allMessage
        else :
            return 0


    def displayMessage(self):  #获得信息，使用正则表达式处理信息，将信息显示在界面上
        allMessage = self.recevemessage()  #收到信息
        if allMessage:
            a = re.compile(r'(?<=:).*?(?=@)')  # 正则表达式截取信息
            message = a.findall(allMessage.decode('utf-8'))
            for i in range(6):  # 处理数据 str-> float
                message[i] = float(message[i])

            self.displayText(message)
            '''将信息显示在界面上'''
            self.lcdNumber.display(message[0])
            self.lcdNumber_2.display(message[1])
            self.lcdNumber_3.display(message[2])
            self.lcdNumber_4.display(message[3])
            self.lcdNumber_5.display(message[4])
            self.lcdNumber_6.display(message[5])
        else :
            self.textEdit.append("connect sensor error")

    def displayText(self,message):
        if(message[1]) > 30:
            self.textEdit.append("The flowers are thirsty")
        if(message[4]) > 40:
            self.textEdit.append("The flowers are sunburned")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = my_Window()
    sys.exit(app.exec_())