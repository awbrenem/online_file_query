# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 19:55:09 2016

@author: KatieM
"""
#this was my attempt to graph a the cdf data in a given folder on python. 
#when I try to run this with the folder created in 
#howtoget_thecdf_off_a_webpage.py, I get the error "NOT_A_CDF_OR_NOT_SUPPORTED.
#strangely, I got this error even when I used the cdfs I got from Autoplot
  
def graphcdffolder(folder, yn, ym):
    import numpy as np
    import datetime as dt
    import matplotlib.pyplot as plt
    import glob
    from spacepy import pycdf
    folder = glob.glob(folder)
#opens the first file in the folder, reads it, and puts it's text in a list.
    f = pycdf.CDF(folder[0])
    d = f['data'][...]
    f.close()  
#creates a list "labels" which contains the labels for all the variables.    
    labels = f_dat.keys()
#finds the integer "varl" which is the number of variables in the graph.
    leng = d[5]
    varl = len(leng)
#constructs a list of of the values in the first file, 
#seperated by the type of value (ex: [[xvalues], [y1values], [y2values]])      
    values = []
    for i in range(0,varl):
        values = values + [[]]
    values[0] = values[0] + d[0:len(d) - (varl - 1):varl]
    for i in range(1,len(values)):
        values[i] = values[i] + d[i:len(d) - (varl - i - 1):varl]

#puts the values in all the other files into the list "values",
#each in the correct list.              
    for each in folder[0:len(folder) + 1]:
        f = pycdf.CDF(each)
        data =  f['data'][...]
        f.close()
        values[0] = values[0] + data[0:len(data) - (varl - 1):varl]
        for i in range(1,len(values)):
            values[i] = values[i] + data[i:len(data) - (varl - i - 1):varl]
    
#changes the x values to a number of seconds. 
    import calendar
    vall = []
    for i in range(0, len(values[0])):
        val = [int(values[0][i][0:4]), 
            int(values[0][i][5:7]), 
            int(values[0][i][8:10]), 
            int(values[0][i][11:13]), 
            int(values[0][i][14:16]), 
            int(values[0][i][17:19])]
        vall = vall + [val]
        values[0][i] = calendar.timegm(val)
    im = values[0].index(min(values[0]))
    yr1 = vall[im][0]
    mn1 = vall[im][1]
    dy1 = vall[im][2]
    hr1 = vall[im][3]
    mi1 = vall[im][4]
    sc1 = vall[im][5]
    s = min(values[0])
    b =  max(values[0]) -  s
#labels the x axis based on the range of x values   
    if b > 63115200:
        b = 31557600
        c = "Time(years)"
    elif b > 172800:
        b = 86400
        c = "Time(days)"
    elif b > 7200:
        b = 3600
        c = "Time(hours)"
    elif b > 120:
        b = 60
        c = "Time(minutes)"
    else:
        b = 1
        c = "Time(seconds)"    
    
    for i in range(0, len(values[0])):
        values[0][i] = (values[0][i] - s) / b
#labels the x axis based on the range of x values and start time.  
    xl =c + ". Start time: " + "{}/{}/{}, {}:{}:{}".format(str(yr1), str(mn1), str(dy1), str(hr1), str(mi1), str(sc1))       
    plt.xlabel(xl)

#makes sure that if all the y variables have the same units,
#that the y axis is labeled instead of having a legend.
    if len(labels) == 1 and varl != 1:
        plt.ylabel(labels[0])
        for i in range(1,len(values)):
            plt.plot(values[0], values[i])
    else:
#plots the plot, with the labels of all the y variables in a legend.
        for i in range(1,len(values)):
            plt.plot(values[0], values[i], label=labels[i])
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
   
#sets the graph to have the given y limits.
    plt.ylim(yn, ym)
#gives the graph the title specified in the files
    T = d[1][9:len(d[1]) - 1]
    plt.title(T)
#shows the graph.
    plt.show() 
    

#example (you can use any folder of cdfs)  
graphcdffolder("C:/Users/KatieM/Desktop/Graphs2/*", -5, 5)

