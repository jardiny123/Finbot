# -*- coding: utf-8 -*-
'''
HttpServer
Unauthorized copying of this file, via any medium is strictly prohibited 
Written by Ryan Lee <strike77@gmail.com>
Created in 15/03/2016 SDG
'''

import MongoDBConnect
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import threading
import json, ast
import socket


PORT_NUMBER = 8080

# This class will handles any incoming request from the browser
class ServiceHandler(BaseHTTPRequestHandler):

    server = None

    # Handler for the GET requests
    def do_GET(self):
        print "Received GET request - path: " + self.path

        # Handles if requested uri is '/index.html'
        if self.path == "/index.html":
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            # send query to DB
            result = self.searchDatabase('20151120', '20151230')
            totalCount = len(result)
            count = 0

            # Create response in json format
            returnValue = '[\n'
            for item in result:
                # Retrieves data from list
                companyName = item["name"]
                shortCode = item["shortCode"]
                startPrice = item["startPrice"]
                endPrice = item["endPrice"]
                rate = item["rate"]
                weekData = item["week"]

                weekData = weekData.replace("'", "\"")
                weekData = weekData.replace(": ", ":\"")
                weekData = weekData.replace(",", "\",")
                weekData = weekData.replace("}", "\"}")

                # Create json message
                returnValue += '\t{\n'

                if(companyName):
                    returnValue += "\t\t\"company\":\"" + companyName + "\",\n"

                if(shortCode):
                    returnValue += "\t\t\"short_code\":\"" + shortCode + "\",\n"

                if(startPrice):
                    returnValue += "\t\t\"start_price\":\"" + startPrice + "\",\n"

                if(endPrice):
                    returnValue += "\t\t\"end_price\":\"" + endPrice + "\",\n"

                if(rate):
                    returnValue += "\t\t\"rate\":\"" + rate + "\",\n"

                if(weekData):
                    returnValue += "\t\t\"week\":" + weekData + "\n"

                if(count < totalCount-1):
                    returnValue += '\t},\n'
                else:
                    returnValue += '\t}\n'

                count += 1;

            returnValue += ']'

            print returnValue

            # Send the html message
            self.wfile.write(returnValue)
        else:
            self.send_error(404,'Page Not Found: %s' % self.path)
        return

    #Handler for the POST requests
    def do_POST(self):
        print "Received POST request - path: " + self.path

        # Handles if requested uri is '/send'
        if self.path=="/send":
            headers=self.headers
            print "content-type: " + self.headers.get("Content-type")
            content_length = int(self.headers.get("content-length"))
            print "content length: %d" % content_length

            post_body = self.rfile.read(content_length)
            print "post body: " + post_body

            self.send_response(200)
            self.end_headers()
            self.wfile.write("<p>Thanks!</p>");
        return

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

class MyHttpServer(threading.Thread):

    server = None

    def run(self):
        try:
            # Create a web server and define the handler to manage the incoming request
            self.server = HTTPServer(('', PORT_NUMBER), ServiceHandler)

            serverAddress = socket.gethostbyname(socket.gethostname())

            print("Started http server on %s:%d" % (serverAddress, PORT_NUMBER))

            # Wait forever for incoming http requests
            self.server.serve_forever()
        except KeyboardInterrupt:
            print '^C received, shutting down the web server'
            self.server.socket.close()

    def stopServer(self):
         self.server.socket.close()

# class end






