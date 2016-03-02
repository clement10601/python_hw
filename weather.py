#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import urllib,urllib2, json
import requests
import argparse
import sys

ARG_LOCATION=''
ARG_UNIT='f'
ARG_ALL=1
ARG_CURRENT=1
ARG_FORECAST=0
ARG_SUN=1
ARG_DEFAULT_ALL=1
sun=""
current = ""
forecast=0
data=""

baseurl = 'https://query.yahooapis.com/v1/public/yql?'

def getweather():
    global data
    global ARG_LOCATION
    global ARG_UNIT
    global ARG_CURRENT
    global ARG_SUN
    global ARG_FORECAST

    url_start = "https://query.yahooapis.com/v1/public/yql?q="
    url_end = "&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
    yql_url = url_start+"SELECT%20*%20FROM%20weather.bylocation%20WHERE%20location%3D%22"+ARG_LOCATION+"%22%20and%20unit%3D%22"+ARG_UNIT+"%22%20%7C%20truncate(count%3D"+str(ARG_FORECAST)+")"+url_end
    
    result = urllib2.urlopen(yql_url).read()
    global data
    data = json.loads(result)
    printresult(data['query']['results']['weather']['rss']['channel'])
    #print data['query']['results']
#
def printresult(data):
    global sun,current,forecast
    global ARG_LOCATION
    global ARG_UNIT
    global ARG_CURRENT
    global ARG_SUN
    global ARG_FORECAST

    sun = data['astronomy']
    current = data['item']['condition']
    forecast = data['item']['forecast']

    if ARG_CURRENT ==0:
        print ARG_LOCATION+", "+current['text']+", "+current['temp']+ARG_UNIT.upper()
    if ARG_SUN ==0:
        print "sunrise:"+sun['sunrise']+ ", "+"sunset:"+sun['sunset']

    for i in range(ARG_FORECAST):
        date = data['item']['forecast'][i]['date']
        day = data['item']['forecast'][i]['day']
        low = data['item']['forecast'][i]['low']
        high = data['item']['forecast'][i]['high']
        text = data['item']['forecast'][i]['text']
        print("%s %s %s~%s%s %s" % (date,day,low,high,ARG_UNIT.upper(),text))
        
def cli_parser():
    global ARG_LOCATION
    global ARG_UNIT
    global ARG_CURRENT
    global ARG_SUN
    global ARG_FORECAST
    readconfig()
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-l","--locations",help="Set locations")
    parser.add_argument("-u","--unit",help="Set unit c or C or f or F",choices=['c','f'],default='c')
    
    parser.add_argument("-c","--current",help="Current Condition",action='store_true')
    parser.add_argument("-s",help="Print Sunrise/Sunset times",action='store_true')

    groupA = parser.add_mutually_exclusive_group()
    groupA.add_argument("-a","--auto",help="Equal to -c -d5 -s",action='store_true')
    groupA.add_argument("-d","--days",help="Set forecast days",type=int,default=5)

    args = parser.parse_args()

    if not ARG_LOCATION:
        ARG_LOCATION = args.locations

    if args.unit:
        ARG_UNIT = args.unit

    if args.current:
        ARG_CURRENT=0

    if args.s:
        ARG_SUN = 0

    if args.auto:
        ARG_CURRENT=0
        ARG_FORECAST = 5
        ARG_SUN = 0

    if args.days:
        ARG_FORECAST = args.days

    return 0

def readconfig():
    success = False
    LOCATION = ""
    global ARG_LOCATION
    global ARG_UNIT
    UNIT=""
    try:
        import config
        success = True
    except ImportError:
        success = False
    
    if success:
        ARG_LOCATION = config.LOCATION
        ARG_UNIT = config.UNIT
    
    return 0

if __name__ == "__main__":
    cli_parser()
    getweather()
