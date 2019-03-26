import sys
from PyQt5.QtCore import Qt,QBasicTimer
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider,
    QVBoxLayout, QApplication,QLabel,QProgressBar,QComboBox)
from PyQt5.QtGui import QPixmap


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Horizontal, self)
        self.label = QLabel(self)
        self.label.setText("hello")
        self.pbar = QProgressBar(self)
        combo =QComboBox(self)
        combo.addItem("first")
        combo.addItem("second")
        combo.addItem("third")


        self.timer = QBasicTimer()
        self.step=0

        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)
        vbox.addWidget(self.label)
        vbox.addWidget(self.pbar)


        self.setLayout(vbox)
        sld.valueChanged.connect(lcd.display)
        sld.valueChanged.connect(self.changeValue)
        combo.activated[str].connect(self.onActivated)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Signal and slot')
        self.show()
        self.timer.start(100,self)

    def timerEvent(self, e):
        if self.step >=100:
            self.timer.stop()
            self.label.setText("finish")
            return
        self.step =self.step +1
        self.pbar.setValue(self.step)

    def keyPressEvent(self, e):
        if e.key() ==Qt.Key_Escape:
            self.close()

    def changeValue(self,value):
        if value == 50:
            self.label.setText("ooooooooooo")

    def onActivated(self,text):
        self.label.setText(text)
        self.label.adjustSize()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())