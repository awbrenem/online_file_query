"""
Determines which online L2 or L3 files need to be replaced based on age and size. 
Calls appropriate bash script to recreate these files. 

Uses Find_available_files_online_age.py


Written by Aaron W Breneman, Dec, 2019

"""



#import py_compile
#py_compile.compile('/Users/aaronbreneman/Desktop/code/Aaron/github.umn.edu/online_file_query/Find_available_files_online_age.py')

import pprint
import sys
sys.path.append('/Users/aaronbreneman/Desktop/code/Aaron/github.umn.edu/online_file_query/')
from Find_available_files_online_age import Find_available_files_online_age
import datetime as datetime
import subprocess


#----------------------------------------------------------------
#INPUT

#max age(days) of an online file
maxdeltadays = 400
minsize = 68

#where to look for files
#url = 'http://rbsp.space.umn.edu/data/rbsp/rbspa/l2/e-spinfit-mgse/2018'
#ftype = 'l2_e-spinfit-mgse'
url = 'http://rbsp.space.umn.edu/data/rbsp/rbspa/l2/vsvy-hires/2016'
ftype = 'l2_vsvy-hires'
#----------------------------------------------------------------

result = Find_available_files_online_age()
files = result.list_files(url, ftype, maxdeltadays, minsize)

#These are the online files that I want to rerun
pprint.pprint(files)



"""-------------------------------------"""
"""Now call doy_convert.py with the dates you desire to rerun L2, L3 files for"""
"""-------------------------------------"""

for i in len(files): 
    currdate = datetime.datetime.now()
    tinput = (currdate - files[i]).days


    """-------------------------------------"""
    """Open the script file, modify the date"""
    """-------------------------------------"""

    f = open("/Users/aaronbreneman/Desktop/code/Aaron/github.umn.edu/online_file_query/rbsp_efw_l2_driver_custom.bash", "r+")
    f.seek(0)
    f_content = f.readlines()

    tst = '' 
    j=0
    while(tst != "i="): 
        val = f_content[j]
        tst = val[0:2]
        j = j+1

    f_content[j-1] = 'i='+str(tinput)+'\n'
    f_content[j]   = 'istop='+str(tinput)+'\n'

    f.seek(0)
    f.write(''.join(f_content))
    f.close()



    """-------------------------------"""
    """Call the bash script"""
    """-------------------------------"""

    tmp = subprocess.call("/Users/aaronbreneman/Desktop/code/Aaron/github.umn.edu/online_file_query/rbsp_efw_l2_driver_custom.bash")


