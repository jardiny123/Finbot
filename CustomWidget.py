# -*- coding: utf-8 -*- 
'''
QCustomQWidget
Unauthorized copying of this file, via any medium is strictly prohibited 
Written by Ryan Lee <strike77@gmail.com>
Created in 14/05/2016 SDG
'''

from PyQt4 import QtGui, QtCore
import Color


class QCustomQWidget (QtGui.QWidget):
    def __init__ (self, parent = None):
        super(QCustomQWidget, self).__init__(parent)

        # For Company information
        self.ComponyInfoVBoxLayout = QtGui.QVBoxLayout()

        self.textCompanyName = QtGui.QLabel()
        self.textShortCode = QtGui.QLabel()

        self.ComponyInfoVBoxLayout.addWidget(self.textCompanyName)
        self.ComponyInfoVBoxLayout.addWidget(self.textShortCode)

        # Set financial info
        self.dataVBoxLayout = QtGui.QVBoxLayout()
        self.financialInfoHBoxLayout = QtGui.QHBoxLayout()

        # Create field for financial info
        self.textStartPriceLabel = QtGui.QLabel()
        self.textEndPriceLabel = QtGui.QLabel()
        self.textRateLabel = QtGui.QLabel()

        self.textStartPriceValue = QtGui.QLabel()
        self.textEndPriceValue = QtGui.QLabel()
        self.textRateValue = QtGui.QLabel()

        # Add fields in the box layout
        self.financialInfoHBoxLayout.addWidget(self.textStartPriceLabel)
        self.financialInfoHBoxLayout.addWidget(self.textStartPriceValue)

        self.financialInfoHBoxLayout.addWidget(self.textEndPriceLabel)
        self.financialInfoHBoxLayout.addWidget(self.textEndPriceValue)

        self.financialInfoHBoxLayout.addWidget(self.textRateLabel)
        self.financialInfoHBoxLayout.addWidget(self.textRateValue)
        self.financialInfoHBoxLayout.setContentsMargins(0,5,0,5)

        self.descriptionHBoxLayout = QtGui.QHBoxLayout()

        # Create field for showing progress bar
        self.progressBar = QtGui.QProgressBar()
        self.progressBar.setRange (0, 100)
        self.progressBar.setValue(100)
        self.descriptionHBoxLayout.addWidget(self.progressBar)
        self.descriptionHBoxLayout.addSpacing(1700)
        self.progressBar.setContentsMargins(0,5,0,5)

        # Add financial data and description
        self.dataVBoxLayout.addLayout(self.financialInfoHBoxLayout, 0)
        self.dataVBoxLayout.addLayout(self.descriptionHBoxLayout, 0)

        # Set short code
        self.searchResultHBoxLayout = QtGui.QHBoxLayout()

        # add everything in the box layout
        self.searchResultHBoxLayout.addLayout(self.ComponyInfoVBoxLayout, 1)
        self.searchResultHBoxLayout.addLayout(self.dataVBoxLayout, 4)

        self.searchResultHBoxLayout.setContentsMargins(10, 30, 10, 30)

        self.setLabelText()
        self.setLabelStyleSheet()
        self.setLayout(self.searchResultHBoxLayout)

    def setLabelText(self):
        self.textStartPriceLabel.setText("START: ")
        self.textStartPriceLabel.setFixedWidth(92)
        self.textEndPriceLabel.setText("END: ")
        self.textEndPriceLabel.setFixedWidth(65)
        self.textRateLabel.setText("RATE: ")
        self.textRateLabel.setFixedWidth(77)

    def setLabelStyleSheet(self):
        self.textCompanyName.setStyleSheet("color: " + Color.CYAN + "background-color: " + Color.LABEL_TRANSPARENT_BG + "font-size:32px;")
        self.textShortCode.setStyleSheet("color: " + Color.WHITE + "background-color: " + Color.LABEL_TRANSPARENT_BG)

        self.textStartPriceLabel.setStyleSheet("color: " + Color.RED + "background-color: " + Color.LABEL_TRANSPARENT_BG)
        self.textEndPriceLabel.setStyleSheet("color: " + Color.RED + "background-color: " + Color.LABEL_TRANSPARENT_BG)
        self.textRateLabel.setStyleSheet("color: " + Color.RED + "background-color: " + Color.LABEL_TRANSPARENT_BG)

        self.textStartPriceValue.setStyleSheet("color: " + Color.WHITE + "background-color: " + Color.LABEL_TRANSPARENT_BG)
        self.textEndPriceValue.setStyleSheet("color: " + Color.WHITE + "background-color: " + Color.LABEL_TRANSPARENT_BG)
        self.textRateValue.setStyleSheet("color: " + Color.WHITE + "background-color: " + Color.LABEL_TRANSPARENT_BG)

        self.progressBar.setStyleSheet("color: " + Color.WHITE + "background-color: " + Color.LABEL_TRANSPARENT_BG)

    def setCompanyQLabel (self, text):
        codec = QtCore.QTextCodec.codecForName("UTF-8")
        localeText = codec.toUnicode(text)

        self.textCompanyName.setText(localeText)

    def setDescriptionQLabel(self, text):
        self.textDescriptionValue.setText(text)

    def setProgressbarValue(self, value):
        self.progressBar.setValue(value)

    def setStartPriceValue(self, text):
        self.textStartPriceValue.setText(text)

    def setEndPriceValue(self, text):
        self.textEndPriceValue.setText(text)

    def setRateValue(self, text):
        self.textRateValue.setText(text)

    def setShortCodeValue(self, text):
        self.textShortCode.setText("(" + text + ")")

