import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QFontDialog
from untitled import *

class MyWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.changeFont)

    def changeFont(self):
        font,ok = QFontDialog.getFont()
        if ok:
            self.label.setFont(font)


if __name__ =='__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
