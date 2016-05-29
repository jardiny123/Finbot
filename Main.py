# -*- coding: utf-8 -*-
'''
Main.py
Unauthorized copying of this file, via any medium is strictly prohibited
Written by Ryan Lee <strike77@gmail.com>
Created in 13/03/2016 SDG
'''

import sys
import locale
import math
import urllib
import plotly
import plotly.plotly as py
print "poltly version: " + plotly.__version__  # version >1.9.4 required

from PyQt4 import QtGui, QtCore
from PyQt4 import uic
from ProgressDialog import ProgressDialog

from CustomWidget import QCustomQWidget
from DataManager import DataHandler
from DetailViewManager import StockData
import feedparser
import Color

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("StackedWidetForm.ui")
        self.ui.backButton.setStyleSheet("color: " + Color.WHITE + "background-color: " + Color.BUTTON_BLUE)
        self.ui.homeButton.setStyleSheet("color: " + Color.WHITE + "background-color: " + Color.BUTTON_BLUE)
        self.ui.searchButton.setStyleSheet("color: " + Color.WHITE + "background-color: " + Color.BUTTON_BLUE)

        self.ui.backButton.hide()
        self.ui.homeButton.hide()

        self.ui.searchButton.clicked.connect(self.onSearchButtonClicked)
        self.ui.listWidget.itemClicked.connect(self.onItemSelected)
        self.ui.backButton.clicked.connect(self.onBackButtonClicked)
        self.ui.homeButton.clicked.connect(self.onHomeButtonClicked)

        pixmap = QtGui.QPixmap('firstbuild-logo-2.jpg')
        scaledPixmap = pixmap.scaled(self.ui.imageLabel_2.size(), QtCore.Qt.KeepAspectRatio)

        self.ui.imageLabel_2.setPixmap(scaledPixmap)
        self.ui.imageLabel_2.raise_()

        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.setStyleSheet("background-color: " + Color.WHITE)

        self.getLatestNews()
        self.ui.show()

    def getLatestNews(self):
        print "Enter getLatestNews"
        d = feedparser.parse('http://file.mk.co.kr/news/rss/rss_50200011.xml')

        self.ui.newsLabel_1.setText(d.entries[0].title)
        self.ui.newsLabel_2.setText(d.entries[1].title)
        self.ui.newsLabel_3.setText(d.entries[2].title)
        self.ui.newsLabel_4.setText(d.entries[3].title)
        self.ui.newsLabel_5.setText(d.entries[4].title)
        self.ui.newsLabel_6.setText(d.entries[5].title)

    def onSearchButtonClicked(self):
        print "onSearchButtonClicked"

        # Get question
        question = '%s' % self.ui.lineEdit.text()
        print question

        nextIndex = self.ui.stackedWidget.currentIndex() + 1
        self.ui.stackedWidget.setCurrentIndex(nextIndex)
        self.ui.backButton.show()
        self.ui.homeButton.show()

        # Retrieve stock information from DB
        self.startDate = '20151120'
        self.endDate = '20151230'

        dataHandler = DataHandler()
        result = dataHandler.searchDatabase(self.startDate, self.endDate)

        # sorting data decreasing order
        sort_on = "rate"
        decorated = [(dict_[sort_on], dict_) for dict_ in result]
        decorated.sort(reverse=True)
        self.sortedResult = [dict_ for (key, dict_) in decorated]

        # Update UI
        self.setListWidget(self.sortedResult)

    def onNextButtonClicked(self):
        print "onNextButtonClicked!"
        nextIndex = self.ui.stackedWidget.currentIndex() + 1
        self.ui.stackedWidget.setCurrentIndex(nextIndex)

    def onBackButtonClicked(self):
        print "onBackButtonClicked!"
        previousIndex = self.ui.stackedWidget.currentIndex() - 1
        self.ui.stackedWidget.setCurrentIndex(previousIndex)

        if self.ui.stackedWidget.currentIndex == 0:
            self.ui.backButton.hide()
            self.ui.homeButton.hide()

    def onHomeButtonClicked(self):
        print "onHomeButtonClicked!"
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.backButton.hide()
        self.ui.homeButton.hide()

    def onItemSelected(self):
        selectedItemIndex = self.ui.listWidget.currentRow()
        print ("onItemSelected - Data: %d" % selectedItemIndex)

        # Draw chart
        stockData = StockData()
        stockData.drawChart(self.sortedResult[selectedItemIndex], self.startDate, self.endDate)

        stockData.getCurrentPrice()

        # Encoding Company Name information
        codec = QtCore.QTextCodec.codecForName("UTF-8")
        companyName = codec.toUnicode(stockData.getCompanyName())

        # Fill in stock information
        self.ui.companyLabel.setText('Company: ' + companyName + ' (' +  stockData.getShortCode() + ')')
        self.ui.startPriceLabel.setText('Start: ' + stockData.getStartPrice())
        self.ui.endPriceLabel.setText('End: ' + stockData.getEndPrice())
        self.ui.rateLabel.setText('Increased: ' + stockData.getRate())
        self.ui.currentPriceLabel.setText('Current Price: ' + stockData.getCurrentPrice())

        self.ui.companyLabel.setStyleSheet("color: " + Color.WHITE)
        self.ui.startPriceLabel.setStyleSheet("color: " + Color.WHITE)
        self.ui.endPriceLabel.setStyleSheet("color: " + Color.WHITE)
        self.ui.rateLabel.setStyleSheet("color: " + Color.WHITE)
        self.ui.currentPriceLabel.setStyleSheet("color: " + Color.WHITE)

        # Load chart data
        chartImage = stockData.loadChartData(self.ui.imageLabel.size())
        self.ui.imageLabel.setPixmap(chartImage)

        # url encoding company name
        encodedCompanyName = urllib.quote_plus(stockData.getCompanyName())

        # Get News for the company from google news
        d = feedparser.parse('https://news.google.com/news?hl=ko&ned=us&ie=UTF-8&oe=UTF-8&output=rss&q=' + encodedCompanyName)

        print len(d['entries'])
        for post in d.entries:
            print post.title + ": " + post.link + ""

        self.ui.detailNewsLabel_1.setText(d.entries[0].title)
        self.ui.detailNewsLabel_2.setText(d.entries[1].title)
        self.ui.detailNewsLabel_3.setText(d.entries[2].title)
        self.ui.detailNewsLabel_4.setText(d.entries[3].title)

        self.ui.detailNewsLabel_1.setStyleSheet("color: " + Color.WHITE)
        self.ui.detailNewsLabel_2.setStyleSheet("color: " + Color.WHITE)
        self.ui.detailNewsLabel_3.setStyleSheet("color: " + Color.WHITE)
        self.ui.detailNewsLabel_4.setStyleSheet("color: " + Color.WHITE)

        self.ui.groupBox_1.setStyleSheet("color: " + Color.LIGHT_GRAY)
        self.ui.groupBox_3.setStyleSheet("color: " + Color.LIGHT_GRAY)

        nextIndex = self.ui.stackedWidget.currentIndex() + 1
        self.ui.stackedWidget.setCurrentIndex(nextIndex)

    def setBackground(self):
        print "setBackground"

    def setListWidget(self, result):

        correlationValue = 90
        itemCount = 0

        for item in result:

            companyName = item["name"]
            shortCode = item["shortCode"]
            rate = item["rate"]
            startPrice = item["startPrice"]
            endPrice = item["endPrice"]

            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setCompanyQLabel(companyName)
            myQCustomQWidget.setStartPriceValue(locale.currency(int(startPrice), grouping=True))
            myQCustomQWidget.setEndPriceValue(locale.currency(int(endPrice), grouping=True))
            myQCustomQWidget.setRateValue(str(rate) + '%')
            myQCustomQWidget.setShortCodeValue(shortCode)

            # codec = QtCore.QTextCodec.codecForName("UTF-8")
            # description = codec.toUnicode("코이즈 써니전자 조일알미늄 서원 SDN 케엔씨글로벌")
            # myQCustomQWidget.setDescriptionQLabel(description)

            x = (itemCount+2) * (itemCount+2) * (itemCount+2) * (itemCount+2)
            result = correlationValue - math.log(x, 2)
            myQCustomQWidget.setProgressbarValue(result)

            # Create QListWidgetItem
            myQListWidgetItem = QtGui.QListWidgetItem(self.ui.listWidget)

            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())

            if itemCount % 2 == 0:
                myQListWidgetItem.setBackgroundColor(Color.BLACK_CODE_1)
            else:
                myQListWidgetItem.setBackgroundColor(Color.BLACK_CODE_2)

            # Add QListWidgetItem into QListWidget
            self.ui.listWidget.addItem(myQListWidgetItem)
            self.ui.listWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
            itemCount += 1

if __name__ == "__main__":
    print("Start Finbot...")
    py.sign_in('pointe77', 'g8eyv8nzr1')

    # Set locale information
    locale.setlocale(locale.LC_ALL, '')

    # Launch app
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()

    app.exec_()
# main end


