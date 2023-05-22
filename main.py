# -*- coding: utf-8 -*-
import os
import sys
import asyncio
from threading import Thread
from PyQt5.QtWidgets import QMainWindow,QApplication
from LCUapi import *
from Ui_MainWindow import *


class MyMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent =None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)

def thread_task():
    asyncio.run(main())

if __name__ == '__main__':
    t = Thread(target=thread_task)
    t.start()

    app = QApplication(sys.argv)
    myWindow = MyMainWindow()
    myWindow.show()
    os._exit(app.exec_()) 
