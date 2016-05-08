# -*- coding: utf-8 -*-
'''
Main.py
Unauthorized copying of this file, via any medium is strictly prohibited
Written by Ryan Lee <strike77@gmail.com>
Created in 13/03/2016 SDG
'''

import plotly
print plotly.__version__  # version >1.9.4 required
from plotly.graph_objs import Scatter, Layout
import MongoDBConnect
import json, ast
from datetime import datetime

import HttpServer


class RequestHandler():
   # Search DB
    def searchDatabase(self, startDate, endDate):
        # Establish DB Connection
        dbAdaptor = MongoDBConnect.MongoDBConnect()
        # dbAdaptor.setDbAndCollection('stock', 'chart_data')

        # Get data from DB
        dbAdaptor.setDbAndCollection('stock', 'companies')
        companies = dbAdaptor.getData()

        # Switch DB
        dbAdaptor.setDbAndCollection('stock', 'chart_data')

        # Counter
        index = 1

        resultList = []

        # Load data from DB and search the result
        for companyList in companies:
            for shortCode in companyList:

                # exclude those keys from send queue
                if(shortCode == '_id' or shortCode == 'last_modified'):
                    continue;
                else:
                    # Get record from shortCode
                    result = dbAdaptor.findData(shortCode)

                    for value in result:
                        try:
                            # Get start and end date
                            start = value.get("week").get(startDate)
                            end = value.get("week").get(endDate)
                            companyName = value.get("company_name")
                            delta = 1.0

                            if((start != None and end != None) and end > start):
                                # Calculate delta for filter
                                gap = (float(end - start)/float(start))

                                if(gap > delta):

                                    company = {}

                                    rate = "{:.0%}".format(gap)
                                    print("[%d] %s, %s, start: %d, end: %d, delta: %s" % (index, companyName, shortCode, start, end, rate))

                                    # Fill in the dictionary
                                    company["name"] = companyName.encode('utf-8')
                                    company["shortCode"] = str(shortCode)
                                    company["startPrice"] = str(start)
                                    company["endPrice"] = str(end)
                                    company["rate"] = rate

                                    weekValue = value.get("week")

                                    # Remove 'u' string in front of key
                                    weekValue = ast.literal_eval(json.dumps(weekValue))
                                    company["week"] = str(weekValue)

                                    # fill in the list
                                    resultList.append(company)

                                index += 1
                        except:
                            print("Exception] short code: %s" % shortCode)

        return resultList
    # def end

if __name__ == "__main__":
    print("Start Finbot...")

    # test = HttpServer.MyHttpServer()
    # test.start()

    requestHandler = RequestHandler()
    result = requestHandler.searchDatabase('20151120', '20151230')

    for item in result:
        # Retrieves data from list
        companyName = item["name"]
        weekData = item["week"]

        weekData = weekData.replace("'", "\"")
        weekData = weekData.replace(": ", ":\"")
        weekData = weekData.replace(",", "\",")
        weekData = weekData.replace("}", "\"}")

        print "company :" + companyName
        #print weekData

        weekDataDict = {}
        jsonWeekData = json.loads(weekData)

        for key, value in (jsonWeekData.iteritems()):
            date_object = datetime.strptime(key, '%Y%m%d')
            weekDataDict[date_object] = value

        break;

    x_value = []
    y_value = []
    for key, value in sorted(weekDataDict.iteritems()):
        x_value.append(key)
        y_value.append(value)
        # print "key: " + str(key) + ", value: " + str(value)

    plotly.offline.plot({
        "data": [
            Scatter(x=x_value, y=y_value)
        ],
        "layout": Layout(
        title=companyName
        )
    },filename= item["shortCode"] + "_demo")

# main end


