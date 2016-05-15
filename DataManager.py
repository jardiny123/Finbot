# -*- coding: utf-8 -*- 
'''
DataManager
Unauthorized copying of this file, via any medium is strictly prohibited 
Written by Ryan Lee <strike77@gmail.com>
Created in 14/05/2016 SDG
'''

import MongoDBConnect
import json, ast
from datetime import datetime


class DataHandler():
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
                            delta = 0.5

                            if((start != None and end != None) and end > start):
                                # Calculate delta for filter
                                gap = (float(end - start)/float(start))

                                if(gap > delta):

                                    company = {}

                                    # rate = "{:.0%}".format(gap)
                                    #rate = "{:.0}".format(gap * 100)
                                    rate = round(gap * 100, 2)
                                    print("[%d] %s, %s, start: %d, end: %d, rate: %ld" % (index, companyName, shortCode, start, end, rate))

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






