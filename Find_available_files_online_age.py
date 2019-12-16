"""
Created Dec, 2019 

Grabs list of files online and determines their age, size, etc.
Outputs a list that can be used as input to scripts on xwaves7 to
create new L2, L3 files.

---------------------------------------
Variable input options for list_files

url: URL of the EFW data. e.g. http://rbsp.space.umn.edu/data/rbsp/rbspa/l2/vsvy-hires/2016

ftype: 
    l2_e-spinfit-mgse
    l2_vsvy_hires
    l2_esvy_despun 
    l2_fbk
    l2_spec 
    l3

maxdeltadays: maximum age of the file (days)
minsize: minimum allowable file size in MB


@author: Aaron W Breneman
"""


class Find_available_files_online_age:

    def __init__(self):
        self.__dict__.update()

    def list_files(self, url, ftype, maxdeltadays, minsize):
        import sys
        sys.path.append('/Users/aaronbreneman/Desktop/code/Aaron/github.umn.edu/online_file_query/')
        #from Find_available_files_online import Find_available_files_online
        import time
        import re
        from datetime import datetime
        from bs4 import BeautifulSoup
        import requests
        import urllib.request
        import pdb
        

        #list of datetime objects containing days older than "maxdeltadays"
        finaldates = []


        content = urllib.request.urlopen(url).read()
        soup2 = BeautifulSoup(content, features="html.parser")

        print(soup2.get_text())
        print(soup2.a.get_text())
        print(soup2.title.string)

        files = soup2.get_text()
        f2 = files.split('\n')
        #All available files
        #for i in range(len(f2)):
        #    print(f2[i])


        for i in range(len(f2)):

            #Check to see if current line contains a filename
            #m = re.search("rbsp[ab]{1}_efw-l2_e-spinfit-mgse_[0-9]{8}_v[0-9]{2}.cdf*", f2[i])
            m = re.search("rbsp[ab]{1}_efw-"+ftype+"_[0-9]{8}_v[0-9]{2}.cdf*", f2[i])
            if m:

                ftst = f2[i]
                loc = ftst.find("cdf")
                date = ftst[loc+3:loc+3+16]
                size = float(ftst[-5:-2])
                fn = ftst[:loc+3]
                version = ftst[loc-4:loc-1]
                date = int(ftst[loc-13:loc-9])
                mn = int(ftst[loc-9:loc-7])
                dy = int(ftst[loc-7:loc-5])
                d0 = datetime(date,mn,dy)
                d0_unix = datetime.timestamp(d0)

                #extract timestamp
                dateTS = int(ftst[loc+3:loc+3+4])
                mnTS = int(ftst[loc+8:loc+8+2])
                dyTS = int(ftst[loc+11:loc+11+2])
                timeTS = ftst[loc+14:loc+14+5]
                timeTS0 = datetime(dateTS,mnTS,dyTS)
                T0_unix = datetime.timestamp(timeTS0)

                #current time
                currenttime = time.time()

                #Number of days since current file was created
                deltadays = (currenttime - T0_unix)/86400


                #for i in range(len(date_str)):
                #    x.append(datetime.strptime(date_str[i], "%Y-%m-%d %H:%M:%S"))

                if deltadays >= maxdeltadays and size <= minsize: finaldates.append(d0)

        return finaldates
