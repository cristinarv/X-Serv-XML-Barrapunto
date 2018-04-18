#!/usr/bin/python
# -*- coding: utf-8 -*-
# Cristina del Río
#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib.request

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True
            
    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.title = "Title: " + self.theContent + "."
                print(self.title)  # imprimes el titulo
                # To avoid Unicode trouble
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.link = " Link: " + self.theContent + "."
                htmlFile.write("<a href=" + self.theContent + ">" + self.title + "</a><br>\n")
                print(self.link)
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
            
# --- Main prog

if len(sys.argv)<2:
    print ("Usage: python xml-parser-barrapunto.py <document>")
    print()
    print (" <document>: file name of the document to parse")
    sys.exit(1)
    
# Load parser and driver

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!
url = "barrapunto.html"
htmlFile = open(url, "w")
html= "<head><meta http-equiv='Content-Type'content='text/html;" + "charset=utf-8'/></head><br>"
htmlFile.write(html)              
xmlFile = open(sys.argv[1],"r")
theParser.parse(xmlFile)
htmlFile.close()
print ("Parse complete")
