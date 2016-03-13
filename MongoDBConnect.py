# -*- coding: utf-8 -*-
'''
MongoDBConnect.py
Unauthorized copying of this file, via any medium is strictly prohibited
Written by Ryan Lee <strike77@gmail.com>
Created in 13/03/2016 SDG
'''

import pymongo

class MongoDBConnect(object):
    connection = None
    db = None
    collection = None

    # Constructor
    def __init__(self):
        # Connect to local Mongo DB
        self.connection = pymongo.MongoClient("localhost", 27017)

    def setDbAndCollection(self, dbName = None, collectionName = None):
        # Get DB in the list
        dbList = self.connection.database_names()

        # check dbList contains given dbName
        if(dbName in dbList):
            self.db = self.connection.get_database(dbName)
        elif (dbName):
            self.db = self.connection[dbName]
            print("Create a new db name with ", dbName)
        else:
            print("DB name is empty!")

        if(self.db):
            # Get collections from given DB
            collectionList = self.db.collection_names()

            if(collectionName in collectionList):
                self.collection = self.db.get_collection(collectionName)
            elif(collectionName):
                self.collection = self.db[collectionName]
                print("Create a new collection name with ", collectionName)
            else:
                print("Collection name is empty!")
    #def end

    def updateChartData(self, shortCode, companyName, date, price, lastModified):
        # Check given primary key exists in the db
        count = self.collection.find({"short_code" : shortCode}).count()
        if(count == 0):
            self.collection.insert({"short_code" : shortCode})

        if (date and price):
            self.collection.update_one(
                {"short_code" : shortCode},
                {
                    "$set" : {
                        "company_name": companyName,
                        "last_modified": lastModified,
                        date: price
                    }
                }
            )
    #def end

    def postData(self, dictionary):
        # Remove existing data and then insert new data
        self.collection.remove({})
        result = self.collection.insert(dictionary)
        return result
    #def end

    def getData(self):
        return self.collection.find()
    #def end

    def printCollection(self):
        # Fetch Document
        for doc in self.collection.find():
            print(doc)
    #def end

    def findData(self, shortCode):
        return self.collection.find(
            {'short_code' : shortCode},
            {'_id':0}
        )
    #def end
#class end


