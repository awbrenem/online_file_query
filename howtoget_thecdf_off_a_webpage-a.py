# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 09:57:38 2016

@author: KatieM
"""
#this was my attempt to get the cdf directly from the website.
#I did succeed in getting the data into a folder, but it must not have been in 
#the correct format, because it would not open as a cdf. 
# I didn't generalize the function because it didn't work.
import urllib2
#to generalize the function, you can set u, s, and e as variables, as in:
#getcdfs(u,s,e), where u, s, and e are in the correct format.
#note that 's' is the start-date and 'e' is the end-date.  
#that is, 's' is the first date we are getting the data for, and 'e' is the last.
u = 'http://rbsp.space.umn.edu/data/rbsp/rbspa/l3/'
s = '2014/12/26'
e = '2015/01/02'

#reads the webpage of the URL.
r = urllib2.urlopen(u)
fils = r.read()
r.close

#gets the years of available data from the webpage that was read.
#puts these years in a list "files"
fils = fils[374:len(fils) - 191]
files = [] + fils.split("<img")
files = files[1:len(files)]
for i in range(0,len(files)):
    files[i] = files[i][54:58]

#shortens the list "files" so that the first item in files is the year of 's' 
#and the last item in "files" is the year of 'e'
#then turns each year into the URL that holds the data for that year.
siy = files.index(s[0:4])
eiy = files.index(e[0:4])
if siy == eiy:
    files[siy] = u + files[siy] + "/"
    
else:
    fil2 = []
    for i in range(siy,eiy + 1):
        fil2 = fil2 + [files[i]]
        files[i] = u + files[i] + "/"
    files = files[siy:eiy + 1]

#Creates a list 'dats' of the data in each of the urls in 'files' 
dats = []
for each in files:
    w = urllib2.urlopen(each)
    file = w.readlines()
    for each in file:
        each = each[0:len(each) -3]
    for each in file:
        dats = dats + [each[len(each) - 47: len(each) - 39]]

#creates 'dei'--data end index  and 'dsi'--data start index.
#these are the indices in the 'dats'  list that correspond to the data 
#from the start/end date specified by s/e.
#then, 'dats' is set to include only the data sets between dei and dsi, including
#the data sets at dei and dsi.  
dei = dats.index(e[0:4] + e[5:7] + e[8:10])   
dsi = dats.index(s[0:4] + s[5:7] + s[8:10])
dats = dats[dsi:dei + 1]
dats2 = []
for each in dats:
    if each[0:4]in fil2:
        dats2 = dats2 + [each]
        
#gets the cdf data of the dates in 'dats' and puts the cdfs in a list 
#"cdfd"--cdf data.
aurls = []
for each in dats2:
    aurls = aurls + [ u + each[0:4] + '/rbspa_efw-l3_' + each + '_v01.cdf']

cdfd = []
for each in aurls:
    html = ''
    ht = urllib2.urlopen(each)
    htm = ht.read()
        
    cdfd = cdfd + [html]   

#put the cdfs in a new folder (I used 'C:/Users/KatieM/Desktop/', you should change
#this so that it will work on your computer).
#also checks to make sure the folder doesn't exist yet
from spacepy import pycdf
import os
pa = 'C:/Users/KatieM/Desktop/' + u[(len(u) - 14):(len(u))] + '/'

if os.path.exists(pa):
    print('ERROR')
    
else:
    #makes a folder
    os.makedirs(pa)

for i in range(0, len(dats2)):
    af = pa + dats2[i] + '.cdf'
    f = open(af, 'w')
    f.write(cdfd[i])
    #write in the cdf data from the index i in cdfd
    f.close()
#then you use this folder(pa) as an input in
#the function in hypothetical_cdfgraphfromfolder.py