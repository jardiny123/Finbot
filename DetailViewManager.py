# -*- coding: utf-8 -*- 
'''
DetailViewManager
Unauthorized copying of this file, via any medium is strictly prohibited 
Written by Ryan Lee <strike77@gmail.com>
Created in 15/05/2016 SDG
'''

import json
import locale
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from dateutil.relativedelta import relativedelta

from PyQt4 import QtGui, QtCore

class StockData():
    chartFileName = 'simple_stock_plot.png'
    companyName = None
    shortCode = None
    startPrice = None
    endPrice = None
    rate = None
    weekData = None

    startDate = None
    endDate = None

    def drawChart(self, stockData, startDate = None, endDate = None):
        print ("ENTER drawChart")

        # start and end date
        self.startDate = datetime.strptime(startDate, '%Y%m%d') - relativedelta(months=2)
        self.endDate = datetime.strptime(endDate, '%Y%m%d') #+ relativedelta(months=1)

        print ("start date: %s" % str(self.startDate))
        print ("end date: %s" % str(self.endDate))

        # Retrieves data from list
        self.companyName = stockData["name"]
        self.weekData = stockData["week"]
        self.shortCode =stockData["shortCode"]
        self.startPrice = stockData["startPrice"]
        self.endPrice = stockData["endPrice"]
        self.rate = stockData["rate"]

        self.weekData = self.weekData.replace("'", "\"")
        self.weekData = self.weekData.replace(": ", ":\"")
        self.weekData = self.weekData.replace(",", "\",")
        self.weekData = self.weekData.replace("}", "\"}")

        self.weekDataDict = {}
        jsonWeekData = json.loads(self.weekData)
        #
        # # Set key to year month date format
        for key, value in (jsonWeekData.iteritems()):
            dateObject = datetime.strptime(key, '%Y%m%d')
            self.weekDataDict[dateObject] = value

        # Filter out data for drawing chart
        x_value, y_value = self.filterChartData(self.weekDataDict)

        # Draw chart
        trace = go.Scatter(x = x_value, y = y_value)
        layout = go.Layout(title=self.companyName, width=800, height=480)
        fig = go.Figure(data=[trace], layout=layout)
        py.image.save_as(fig, filename=self.chartFileName)
        print "LEAVE drawChart"

    def loadChartData(self, imageSize):
        print "ENTER loadChartData"
        pixmap = QtGui.QPixmap(self.chartFileName)
        scaledPixmap = pixmap.scaled(imageSize, QtCore.Qt.KeepAspectRatio)
        print "LEAVE loadChartData"
        return scaledPixmap

    def filterChartData(self, weekDataDict):
        print "ENTER filterDateForChart"

        x_value = []
        y_value = []

        for key, value in sorted(weekDataDict.iteritems()):
            if key >= self.startDate and key <= self.endDate :
                x_value.append(key)
                y_value.append(value)

        print "LEAVE filterDateForChart"
        return x_value, y_value

    def getCompanyName(self):
        return str(self.companyName)

    def getShortCode(self):
        return self.shortCode

    def getStartPrice(self):
        return locale.currency(int(self.startPrice), grouping=True)

    def getEndPrice(self):
        return locale.currency(int(self.endPrice), grouping=True)

    def getRate(self):
        return str(self.rate) + '%'

    def getCurrentPrice(self):
        sortedWeekData = sorted(self.weekDataDict.iteritems())
        currentPrice = str(sortedWeekData[-1][1])
        return locale.currency(int(currentPrice), grouping=True)
