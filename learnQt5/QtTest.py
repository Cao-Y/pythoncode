import sys
from PyQt5 import QtWidgets,QtCore
from learnUI import *



class my_Windows(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(my_Windows,self).__init__()
        self.setupUi(self)
        self.show()



if __name__ =="__main__":
    app = QtWidgets.QApplication(sys.argv)
    mywindow = my_Windows()
    sys.exit(app.exec_())