# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 10:27:02 2016

@author: KatieM
"""
#function takes a folder of ASCII table text files,
#and makes a graph from the files in the folder
#using the given y limits.  
def graphfiles2(folder, yn, ym):
    import numpy as np
    import datetime as dt
    import matplotlib.pyplot as plt
    import glob
    folder = glob.glob(folder)
#opens the first file in the folder, reads it, and puts it's text in a list.
    f = open(folder[0], 'r')
    d = f.readlines()
    f.close()
#creates a list "file" that contains the data of the file
    file = []
    for each in d[5:len(d)]:
        each = each[0:len(each) - 1]
        file = file + each.split(", ")
#creates a list "labels" which contains the labels for all the variables.    
    labels = d[2].split(", ")
#finds the integer "varl" which is the number of variables in the graph.
    leng = d[5].split(", ")
    varl = len(leng)
#constructs a list of of the values in the first file, 
#seperated by the type of value (ex: [[xvalues], [y1values], [y2values]])      
    values = []
    for i in range(0,varl):
        values = values + [[]]
    values[0] = values[0] + file[0:len(file) - (varl - 1):varl]
    for i in range(1,len(values)):
        values[i] = values[i] + file[i:len(file) - (varl - i - 1):varl]

#puts the values in all the other files into the list "values",
#each in the correct list.              
    for each in folder[0:len(folder) + 1]:
        f = open(each, 'r')
        data = f.readlines()
        f.close()
    
        file = []
        for each in data[5:len(data)]:
            each = each[0:len(each) - 1]
            file = file + each.split(", ")
        values[0] = values[0] + file[0:len(file) - (varl - 1):varl]
        for i in range(1,len(values)):
            values[i] = values[i] + file[i:len(file) - (varl - i - 1):varl]
    

    
   
 
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
    

    
graphfiles2("C:/Users/KatieM/Desktop/Graphs2/*", -5, 5)
