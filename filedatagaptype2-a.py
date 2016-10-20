# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 11:23:11 2016

@author: KatieM
"""

#this is the function I wrote in the beginning of the summer that finds the days missing in the data on the website you gave.
#I think it should work for all the datasets at 'http://rbsp.space.umn.edu/data/rbsp/rbspa/'.
#I just noticed that this only works on python 3. In python 2.6, I think it should work if you substitute '
#'urllib2' for 'urllib.request'.
#I thought I should send this to you because I couldn't remember if I did.
def datagap(u):
    #read and decode the information on the first page.  
    import urllib.request
    fils = urllib.request.urlopen(u).read()
    fils = fils.decode()
    #seperate the years into different items in a list, and remove the irrelevant data connected to the date.
    fils = fils[374:len(fils) - 191]
    files = [] + fils.split("<img")
    files = files[1:len(files)]
    for i in range(0,len(files)):
        files[i] = files[i][54:58]
    #turns the years into urls that can be used to get the data for each year.
    for i in range(0,len(files)):
        files[i] = u + files[i] + "/"
    #replaces each url with the information read on that webpage.
    #then makes a list 'dats' containing only the dates (in the form yearmonthdate: as in '20150127')
    for each in files:
        file = urllib.request.urlopen(each).readlines()
        for each in file:
            each = each[0:len(each) -3]
        dats = []
        for each in file:
            each = each.decode()
            dats = dats + [each[len(each) - 47: len(each) - 39]]
        dats = dats[7:len(dats) - 3]
    #converts the dates from the format 'yearmonthdate' to the format required for calendar.timegm
    import calendar
    for i in range(0,len(dats)):
        yr = int(dats[i][0:4])
        mn = int(dats[i][4:6])
        dy = int(dats[i][6:8])
        dats[i] = [yr, mn, dy, 0, 0, 0]
        dats[i] = calendar.timegm(dats[i])
    #determines if there is a gap in the dates, if there is a gap, prints out the date immediately before that gap.
    for i in range(1, len(dats)):
        if int(dats[i]) - int(dats[i - 1]) != 86400:
            print(dats[i])
datagap('http://rbsp.space.umn.edu/data/rbsp/rbspa/l3/')