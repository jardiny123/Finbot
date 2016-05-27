# -*- coding: utf-8 -*- 
'''
ProgressDialog
Unauthorized copying of this file, via any medium is strictly prohibited 
Written by Ryan Lee <strike77@gmail.com>
Created in 23/05/2016 SDG
'''

from PyQt4 import QtCore, QtGui
import sys

class ProgressDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        super(ProgressDialog,self).__init__()
        self.resize(500, 500)
        self.Button = QtGui.QPushButton(self)
        self.Button.clicked.connect(self.Run_Something)
        self.Button.setText("Run")

    def Run_Something(self):
        self.progress = QtGui.QProgressDialog("Running","Cancel",0,0,self)
        self.progress.setWindowTitle('Please wait...')
        self.progress.setWindowModality(QtCore.Qt.WindowModal)
        self.progress.canceled.connect(self.progress.close)
        self.progress.show()

        self.TT = Test_Thread()
        self.TT.finished.connect(self.TT_Finished)
        self.progress.canceled.connect(self.progress.close)
        self.progress.show()
        self.TT.start()

    def TT_Finished(self):
        self.progress.setLabelText("Analysis finished")
        self.progress.setRange(0,1)
        self.progress.setValue(1)
        self.progress.setCancelButtonText("Close")
        self.progress.canceled.connect(self.progress.close)

class Test_Thread(QtCore.QThread):
    finished = QtCore.pyqtSignal()

    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        end = 10**7
        start = 0

        while start < end:
            start += 1

        self.finished.emit()
        self.terminate()



