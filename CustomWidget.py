# -*- coding: utf-8 -*- 
'''
QCustomQWidget
Unauthorized copying of this file, via any medium is strictly prohibited 
Written by Ryan Lee <strike77@gmail.com>
Created in 14/05/2016 SDG
'''

from PyQt4 import QtGui, QtCore


class QCustomQWidget (QtGui.QWidget):
    def __init__ (self, parent = None):
        super(QCustomQWidget, self).__init__(parent)

        # Set company name and delta value
        self.textQVBoxLayout = QtGui.QVBoxLayout()
        self.textCompanyQLabel = QtGui.QLabel()
        self.textRateQLabel = QtGui.QLabel()

        self.textQVBoxLayout.addWidget(self.textCompanyQLabel)
        self.textQVBoxLayout.addWidget(self.textRateQLabel)

        # SEt start and and price
        self.textQVBoxLayout2 = QtGui.QVBoxLayout()
        self.textEndPriceQLabel = QtGui.QLabel()
        self.textStartPriceQLabel = QtGui.QLabel()

        self.textQVBoxLayout2.addWidget(self.textEndPriceQLabel)
        self.textQVBoxLayout2.addWidget(self.textStartPriceQLabel)

        # Set short code
        self.allQHBoxLayout = QtGui.QHBoxLayout()
        self.textShortCodeQLabel = QtGui.QLabel()

        # add everything in the box layout
        self.allQHBoxLayout.addWidget(self.textShortCodeQLabel, 1)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 2)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout2, 5)

        self.setLayout(self.allQHBoxLayout)
        self.setLabelStyleSheet()

    def setLabelStyleSheet(self):
        self.textCompanyQLabel.setStyleSheet('''color: rgb(0, 0, 255);''')
        self.textShortCodeQLabel.setStyleSheet('''color: rgb(255, 0, 0);''')
        self.textRateQLabel.setStyleSheet('''color: rgb(255, 0, 0);''')
        self.textEndPriceQLabel.setStyleSheet('''color: rgb(96, 96, 96);''')
        self.textStartPriceQLabel.setStyleSheet('''color: rgb(96, 96, 96);''')

    def setCompanyQLabel (self, text):
        codec = QtCore.QTextCodec.codecForName("UTF-8")
        localeText = codec.toUnicode(text)

        self.textCompanyQLabel.setText(localeText)

    def setShortCodeQLabel (self, text):
        self.textShortCodeQLabel.setText(text)

    def setRateQLabel(self, text):
        self.textRateQLabel.setText(text)

    def setStartPriceQLabel(self, text):
        self.textStartPriceQLabel.setText(text)

    def setEndPriceQLabel(self, text):
        self.textEndPriceQLabel.setText(text)



