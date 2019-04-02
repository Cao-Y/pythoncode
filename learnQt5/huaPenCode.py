import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5 import QtCore,QtGui
import cv2
from huapen import *

class my_Window(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(my_Window, self).__init__()
        self.setupUi(self)
        self.cap = cv2.VideoCapture(0) #获取0号摄像头
        self.timer = QtCore.QTimer()
        self.timer.start()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.start)    #0号摄像头开始使用
        self.show()

    def start(self):
        flag, image = self.cap.read()  #读取摄像头
        #show1 = cv2.resize(image, (640, 480))
        show = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  #处理读取的图像信息
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_5.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 摄像头信息传给label


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = my_Window()
    sys.exit(app.exec_())