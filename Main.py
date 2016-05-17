# -*- coding: utf-8 -*-
'''
Main.py
Unauthorized copying of this file, via any medium is strictly prohibited
Written by Ryan Lee <strike77@gmail.com>
Created in 13/03/2016 SDG
'''

import sys
import locale
import plotly
import plotly.plotly as py
print "poltly version: " + plotly.__version__  # version >1.9.4 required

from PyQt4 import QtGui
from PyQt4 import uic

from CustomWidget import QCustomQWidget
from DataManager import DataHandler
from DetailViewManager import StockData


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("StackedWidetForm.ui")
        self.ui.backButton.hide()
        self.ui.homeButton.hide()

        self.ui.searchButton.clicked.connect(self.onSearchButtonClicked)
        self.ui.listWidget.itemClicked.connect(self.onItemSelected)
        self.ui.backButton.clicked.connect(self.onBackButtonClicked)
        self.ui.homeButton.clicked.connect(self.onHomeButtonClicked)

        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.show()

    def onSearchButtonClicked(self):
        print "onSearchButtonClicked"
        print self.ui.textEdit.toPlainText()
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

    def onHomeButtonClicked(self):
        print "onHomeButtonClicked!"
        self.ui.stackedWidget.setCurrentIndex(0)

    def onItemSelected(self):
        selectedItemIndex = self.ui.listWidget.currentRow()
        print ("onItemSelected - Data: %d" % selectedItemIndex)

        # Draw chart
        stockData = StockData()
        stockData.drawChart(self.sortedResult[selectedItemIndex], self.startDate, self.endDate)

        # Set Company information
        self.ui.companyLabel.setText('Company: ' + stockData.getCompanyName() + ' (' +  stockData.getShortCode() + ')')
        self.ui.startPriceLabel.setText('Start Price: ' + stockData.getStartPrice())
        self.ui.endPriceLabel.setText('End Price: ' + stockData.getEndPrice())
        self.ui.rateLabel.setText('Increased: ' + stockData.getRate())

        # Load chart data
        chartImage = stockData.loadChartData(self.ui.imageLabel.size())
        self.ui.imageLabel.setPixmap(chartImage)

        nextIndex = self.ui.stackedWidget.currentIndex() + 1
        self.ui.stackedWidget.setCurrentIndex(nextIndex)

    def setBackground(self):
        print "setBackground"

    def setListWidget(self, result):

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
            myQCustomQWidget.setShortCodeQLabel(shortCode)
            myQCustomQWidget.setRateQLabel(str(rate) + '%')
            myQCustomQWidget.setStartPriceQLabel("Start price: " + locale.currency(int(startPrice), grouping=True))
            myQCustomQWidget.setEndPriceQLabel("End price: " + locale.currency(int(endPrice), grouping=True))

            # Create QListWidgetItem
            myQListWidgetItem = QtGui.QListWidgetItem(self.ui.listWidget)

            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())

            if itemCount % 2 == 1:
                myQListWidgetItem.setBackgroundColor(QtGui.QColor.fromRgb(248,248,248,255))

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


