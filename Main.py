# -*- coding: utf-8 -*-
'''
Main.py
Unauthorized copying of this file, via any medium is strictly prohibited
Written by Ryan Lee <strike77@gmail.com>
Created in 13/03/2016 SDG
'''

import MongoDBConnect

if __name__ == "__main__":
    print("Start Finbot...")

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
                        start = value.get('week').get('20160129')
                        end = value.get('week').get('20150930')

                        if((start != None and end != None) and end > start):

                            # Calculate gap for filter
                            gap = (float(end - start)/float(start))

                            if(gap > 1.0):
                                gap = "{:.0%}".format(gap)
                                print("[%d] short code: %s, start: %d, end: %d, gap: %s" % (index, shortCode,start,end, gap))
                                index += 1
                    except:
                        print("Exception] short code: %s" % shortCode)

# main end


