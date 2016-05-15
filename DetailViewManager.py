# -*- coding: utf-8 -*- 
'''
DetailViewManager
Unauthorized copying of this file, via any medium is strictly prohibited 
Written by Ryan Lee <strike77@gmail.com>
Created in 15/05/2016 SDG
'''

import json
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from dateutil.relativedelta import relativedelta

from PyQt4 import QtGui, QtCore

class StockData():
    chartFileName = 'simple_stock_plot.png'

    def drawChart(self, stockData, startDate = None, endDate = None):
        print ("ENTER drawChart")

        # start and end date
        self.startDate = datetime.strptime(startDate, '%Y%m%d') - relativedelta(months=2)
        self.endDate = datetime.strptime(endDate, '%Y%m%d') #+ relativedelta(months=1)

        print ("start date: %s" % str(self.startDate))
        print ("end date: %s" % str(self.endDate))

        # Retrieves data from list
        companyName = stockData["name"]
        weekData = stockData["week"]

        weekData = weekData.replace("'", "\"")
        weekData = weekData.replace(": ", ":\"")
        weekData = weekData.replace(",", "\",")
        weekData = weekData.replace("}", "\"}")

        weekDataDict = {}
        jsonWeekData = json.loads(weekData)

        # Set key to year month date format
        for key, value in (jsonWeekData.iteritems()):
            dateObject = datetime.strptime(key, '%Y%m%d')
            weekDataDict[dateObject] = value

        # Filter out data for drawing chart
        x_value, y_value = self.filterChartData(weekDataDict)

        # Draw chart
        trace = go.Scatter(x = x_value, y = y_value)
        layout = go.Layout(title=companyName, width=800, height=480)
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
                print key
                x_value.append(key)
                y_value.append(value)

        print "LEAVE filterDateForChart"
        return x_value, y_value
