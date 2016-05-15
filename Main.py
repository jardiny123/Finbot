# -*- coding: utf-8 -*-
'''
Main.py
Unauthorized copying of this file, via any medium is strictly prohibited
Written by Ryan Lee <strike77@gmail.com>
Created in 13/03/2016 SDG
'''

import sys
#import plotly
# import plotly.plotly as py
# print plotly.__version__  # version >1.9.4 required
# from plotly.graph_objs import Scatter, Layout
#import plotly.graph_objs as go

import locale
from PyQt4 import QtGui, QtCore
from PyQt4 import uic
from CustomWidget import QCustomQWidget
from DataManager import DataHandler


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("StackedWidetForm.ui")
        self.ui.backButton.hide()
        self.ui.homeButton.hide()

        self.ui.searchButton.clicked.connect(self.onSearchButtonClicked)

        self.ui.listWidget.itemClicked.connect(self.onItemSelected)

        # self.ui.next_2.clicked.connect(self.onNextButtonClicked)
        # self.ui.next_3.clicked.connect(self.onNextButtonClicked)
        #
        # self.ui.back_2.clicked.connect(self.onBackButtonClicked)
        # self.ui.back_3.clicked.connect(self.onBackButtonClicked)
        # self.ui.back_4.clicked.connect(self.onBackButtonClicked)
        #
        # self.ui.home_2.clicked.connect(self.onHomeButtonClicked)
        # self.ui.home_3.clicked.connect(self.onHomeButtonClicked)
        # self.ui.home_4.clicked.connect(self.onHomeButtonClicked)

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
        dataHandler = DataHandler()
        result = dataHandler.searchDatabase('20151120', '20151230')


        sort_on = "rate"
        decorated = [(dict_[sort_on], dict_) for dict_ in result]
        decorated.sort(reverse=True)
        sortedResult = [dict_ for (key, dict_) in decorated]


        # sortedResult = sorted(result, key=lambda k: k['rate'], reverse=True)
        print 'load data done'

        # Update UI
        self.setListWidget(sortedResult)

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
        print ("onItemSelected: %d" % self.ui.listWidget.currentRow())

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
    # py.sign_in('pointe77', 'g8eyv8nzr1')

    # Set locale information
    locale.setlocale(locale.LC_ALL, '')

    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()

    # requestHandler = RequestHandler()
    # result = requestHandler.searchDatabase('20151120', '20151230')

    # for item in result:
    #     # Retrieves data from list
    #     companyName = item["name"]
    #     weekData = item["week"]
    #
    #     weekData = weekData.replace("'", "\"")
    #     weekData = weekData.replace(": ", ":\"")
    #     weekData = weekData.replace(",", "\",")
    #     weekData = weekData.replace("}", "\"}")
    #
    #     print "company :" + companyName
    #     #print weekData
    #
    #     weekDataDict = {}
    #     jsonWeekData = json.loads(weekData)
    #
    #     for key, value in (jsonWeekData.iteritems()):
    #         date_object = datetime.strptime(key, '%Y%m%d')
    #         weekDataDict[date_object] = value
    #
    #     break;
    #
    # x_value = []
    # y_value = []
    # for key, value in sorted(weekDataDict.iteritems()):
    #     x_value.append(key)
    #     y_value.append(value)
        # print "key: " + str(key) + ", value: " + str(value)

    # plotly.offline.plot({
    #     "data": [
    #         Scatter(x=x_value, y=y_value)
    #     ],
    #     "layout": Layout(
    #     title=companyName
    #     )
    # },filename= item["shortCode"] + "_demo")


    # py.image.save_as({'data': Scatter(x=x_value, y=y_value)}, 'your_image_filename.png')

    # trace = go.Scatter(
    #     x = x_value,
    #     y = y_value
    # )
    # data = [trace]
    # layout = go.Layout(title='A Simple Plot', width=800, height=640)
    # fig = go.Figure(data=data, layout=layout)
    # py.image.save_as(fig, filename='a-simple-plot.png')
# main end


