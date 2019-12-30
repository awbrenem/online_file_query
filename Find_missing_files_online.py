"""
Created Dec, 2019

Finds missing L2, L3 files online.
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

On xwaves7 run with /opt/local/bin/python3.7

@author: Aaron W Breneman
"""


class Find_missing_files_online:

    def __init__(self):
        self.__dict__.update()


    """""""""""""""""""""""""""""""""""""""""""""""""""
    Grab the names of all the files at stated URL 
    """""""""""""""""""""""""""""""""""""""""""""""""""
    def get_online_filenames(self, url, ftype, versionf):
        from bs4 import BeautifulSoup
        import urllib.request
        import re
        import datetime


        content = urllib.request.urlopen(url).read()
        soup2 = BeautifulSoup(content, features="html.parser")
        #print(soup2.get_text())
        #print(soup2.a.get_text())
        #print(soup2.title.string)



        #First splice up URL to find year requested. We want to do this in case there are NO files available online.
        #This way we will still have this info available in our dictionary for other routines to use.
        year_requested = url[-4:]


        files = soup2.get_text()
        f2 = files.split('\n')


        filename = []
        dateonline = []; dateonlinev2 = []; datecreated = []
        size = []; version = []
        yr = []; mn = []; dy = []


        #Grab names of all the files online and extract useful info from them
        for i in range(len(f2)):

            # Check to see if current line contains a filename.
            #m = re.search("rbsp[ab]{1}_efw-" + ftype + "_[0-9]{8}_v[0-9]{2}.cdf*", f2[i])
            m = re.search("rbsp[ab]{1}_efw-" + ftype + "_[0-9]{8}_v" + versionf + ".cdf*", f2[i])
            if m:
                ftst = f2[i]
                loc = ftst.find("cdf")
                datetmp = ftst[loc - 13:loc - 5]
                dateonline.append(datetmp)
                dateonlinev2.append(datetime.datetime.strptime(datetmp,"%Y%m%d"))
                size.append(float(ftst[-5:-2]))
                filename.append(ftst[:loc+3])
                version.append(ftst[loc-4:loc-1])
                yr.append(int(ftst[loc-13:loc-9]))
                mn.append(int(ftst[loc-9:loc-7]))
                dy.append(int(ftst[loc-7:loc-5]))

                ttst = ftst[loc+3:loc+3+10]
                datecreated.append(datetime.datetime.strptime(ttst,"%Y-%m-%d"))

        if len(filename) == 0:
            dict =  { "filename":[None], "dateonline":[None], "dateonlinev2":[None], "datecreated":[None], "version":[None], "yr":[None], "mn":[None], "dy":[None], "size":[None], "year_requested":year_requested}
        else:
            dict =  { "filename":filename, "dateonline":dateonline, "dateonlinev2":dateonlinev2, "datecreated":datecreated, "version":version, "yr":yr, "mn":mn, "dy":dy, "size":size, "year_requested":year_requested}
        return dict




    """""""""""""""""""""""""""""""""""""""""""""""""""
    List files online that are older than specified age 
    """""""""""""""""""""""""""""""""""""""""""""""""""
    def list_old_files(self, Filenames, maxdeltadays):
        import datetime

        if Filenames["filename"][0] == None:
            finaldates = [None]
            return finaldates


        finaldates = []
        datescreated = Filenames["datecreated"]
        datesonline = Filenames["dateonlinev2"]

        currenttime = datetime.datetime.today()

        b = 0
        for i in datescreated:
            #Number of days since current file was created
            deltadays = (currenttime - i).days
            if deltadays >= maxdeltadays: finaldates.append(datesonline[b])
            b = b + 1

        return finaldates


    """""""""""""""""""""""""""""""""""""""""""""""""""
    List files online that are smaller than specified size 
    """""""""""""""""""""""""""""""""""""""""""""""""""
    def list_small_files(self, Filenames, minsize):

        if Filenames["filename"][0] == None:
            finaldates = [None]
            return finaldates

        finaldates = []
        datesonline = Filenames["dateonlinev2"]
        sizes = Filenames["size"]

        for i in range(len(datesonline)):
            if sizes[i] < minsize: finaldates.append(datesonline[i])

        return finaldates



    """""""""""""""""""""""""""""""""""""""""""""""""""
    List files online that are completely missing 
    """""""""""""""""""""""""""""""""""""""""""""""""""
    def list_missing_files(self, Filenames):
        import datetime

        finaldates = []
        dateonline = Filenames["dateonline"]


        # Here I have the list of strings "dateonline". I need to turn it into a datetime object so I can compare it to later array
        tmpp = Filenames["filename"][0]


        #If there are NO files online then return a list of all days in year
        if tmpp == None:

            yrtmp = int(Filenames["year_requested"])

            sdate = datetime.datetime(yrtmp, 1, 1)   # start date
            edate = datetime.datetime(yrtmp, 12, 31)   # end date
            delta = edate - sdate       # as timedelta

            for i in range(delta.days + 1):
                day = sdate + datetime.timedelta(days=i)
                finaldates.append(day.strftime("%Y%m%d"))
                #print(day.strftime("%Y%m%d"))

            return finaldates


        d0 = Filenames["dateonlinev2"][0]
        datefin = [d0]
        for i in range(len(dateonline)): datefin.append(datetime.datetime.strptime(dateonline[i],"%Y%m%d"))



        #If files do exist, go through each day of the year to see if it's missing
        date = d0
        for i in range(365):

            deltadays = []
            for q in datefin: deltadays.append((date - q).days)


            #if this is true then this day already has this file. Otherwise we'll need to create it.
            testexists = (0 in deltadays)


            if not testexists:
                finaldates.append(date)

            date += datetime.timedelta(days=1)

        return finaldates



    """""""""""""""""""""""""""""""""""""""""""""""""""
    Return only days that are unique. 
    """""""""""""""""""""""""""""""""""""""""""""""""""
    def uniquefiles(self, allfiles):

        unique_files = []
        for i in allfiles:
            if i not in unique_files and i != "":
                unique_files.append(i)

        unique_files

        return unique_files




    """""""""""""""""""""""""""""""""""""""""""""""""""
    Starting on Oct 1st, 2015 probe 1 on RBSPa malfunctioned 
    """""""""""""""""""""""""""""""""""""""""""""""""""
    def get_bad_probes(self, date0):
        import datetime

        #contains variables from bash script bad_probe_rbsp{a,b}
        bad_probe = [0, 0]

        dbad_v1a = datetime.datetime(2015, 10, 1) #date of switch to v34 on RBSPa
        tdiff = (date0 - dbad_v1a).days

        if tdiff >= 0:
            bad_probe = [1, 0]

        return bad_probe


    """""""""""""""""""""""""""""""""""""""""""""""""""
    Use boom pair '34' on RBSPa after Oct 1st, 2015 
    """""""""""""""""""""""""""""""""""""""""""""""""""
    def get_boom_pairs(self, date0):
        import datetime

        #contains variables from bash script bp_rbsp{a,b}
        boom_pairs = [12, 12]


        dbad_v1a = datetime.datetime(2015, 10, 1) #date of switch to v34 on RBSPa
        tdiff = (date0 - dbad_v1a).days

        if tdiff >= 0:
            boom_pairs = [34, 12]

        return boom_pairs



    """""""""""""""""""""""""""""""""""""""""""""""""""
    modify the bash script in preparation for file creation
    """""""""""""""""""""""""""""""""""""""""""""""""""
    def modifyscript(self, date0, sc, type, version, bad_probes, boom_pairs, testing):
        import datetime

        nowdate = datetime.datetime.now()
        tinput = (nowdate - date0).days



        #Open the script and read its contents
        if testing == 1:
            f = open("/Users/aaronbreneman/Desktop/code/Aaron/github.umn.edu/online_file_query/rbsp_efw_l2_driver_custom.bash", "r")
        else:
            f = open("/Volumes/UserA/user_homes/kersten/RBSP_l2/rbsp_efw_l2_driver_custom.bash", "r")
        f.seek(0)
        f_content = f.readlines()
        f.close()


        #Modify certain lines
        f_content[31] = 'i='+str(tinput)+'\n'
        f_content[32] = 'istop='+str(tinput)+'\n'
        f_content[33] = 'bp_rbspa='+str(boom_pairs[0])+'\n'
        f_content[34] = 'bp_rbspb='+str(boom_pairs[1])+'\n'
        f_content[35] = 'version='+str(version[1:2])+'\n'
        f_content[36] = 'bad_probe_rbspa='+str(bad_probes[0])+'\n'
        f_content[37] = 'bad_probe_rbspb='+str(bad_probes[1])+'\n'
        f_content[38] = 'type='+type+'\n'
        f_content[49] = '\tfor p in '+sc+'; do\n'


        #Find out where the last line of file resides (need to check this b/c it sometimes has extra line)
        tststr = "/bin/rm -vrf $TEMPDIR"
        b = 0
        finloc = 0
        for i in f_content:

            if i[0:21] == tststr:
                finloc = b

            b = b+1


        #adjusted file content excluding any extra lines at end
        f_content2 = f_content[0:int(finloc)+1]


        #Reopen the file to write contents to it.
        if testing == 1:
            f = open("/Users/aaronbreneman/Desktop/code/Aaron/github.umn.edu/online_file_query/rbsp_efw_l2_driver_custom.bash", "w")
        else:
            f = open("/Volumes/UserA/user_homes/kersten/RBSP_l2/rbsp_efw_l2_driver_custom.bash", "w")



        #Rewrite modified lines to the file
        f.seek(0)
        f.write(''.join(f_content2))
        f.close()



    """
    ftype:
        l2_e-spinfit-mgse
        l2_vsvy-hires
        l2_esvy_despun
        l2_fbk
        l2_spec
        l3
    """
    def main():

        testing = 0



        import sys
        if testing == 1:
            sys.path.append('/Users/aaronbreneman/Desktop/code/Aaron/github.umn.edu/online_file_query/')
        else:
            sys.path.append('/Volumes/UserA/user_homes/kersten/RBSP_l2/')
        from Find_missing_files_online import Find_missing_files_online
        import subprocess

        l2_l3 = 'l2'

        year = ["2013","2014","2015"]
        sc = ["a","b"]

        #All of these arrays must be the same size
        type = ["vsvy-hires","esvy_despun","e-spinfit-mgse","fbk","spec"]
        ftype = ["l2_vsvy-hires","l2_esvy_despun","l2_e-spinfit-mgse","l2_fbk","l2_spec"]
        #min possible size of online files
        minsize = [68,73,2.3,85,39]
        #Required version of online file
        versions = ["01","02","02","01","01"]
        #max possible age(days) of an online file
        maxdeltadays = [100,100,100,100,100]



        for yeart in year:
            for sct in sc:
                b=0
                for typet in type:

#                    print("***********")
#                    print(yeart+' - '+sct+' - '+typet)

                    #where to look for files
                    url = "http://rbsp.space.umn.edu/data/rbsp/rbsp"+sct+"/"+l2_l3+"/"+typet+"/"+yeart


                    files = Find_missing_files_online()
                    Filenames = files.get_online_filenames(url, ftype[b], versions[b])
                    Filenames.keys()



                    missingfiles = files.list_missing_files(Filenames)
#                    print(missingfiles)
                    oldfiles = files.list_old_files(Filenames, maxdeltadays[b])
#                    print(oldfiles)
                    smallfiles = files.list_small_files(Filenames, minsize[b])
#                    print(smallfiles)


                    #Combine the three arrays to find all the unique days files need to be created for.

                    allfiles = missingfiles + oldfiles + smallfiles
                    uniquefiles = files.uniquefiles(allfiles)


#                    print(uniquefiles)





                    #Modify and call the bash script for each file to be created
                    for i in uniquefiles:


                        #Determine values for bad probe and boom pair
                        bad_probes = files.get_bad_probes(i)
                        boom_pairs = files.get_boom_pairs(i)


                        files.modifyscript(i, sct, typet, versions[b], bad_probes, boom_pairs, testing)


                        #Call the bash script
                        #tmp = subprocess.call("/Users/aaronbreneman/Desktop/code/Aaron/github.umn.edu/online_file_query/rbsp_efw_l2_driver_custom.bash")
                        if testing != 1:
                            tmp = subprocess.call("/Volumes/UserA/user_homes/kersten/RBSP_l2/rbsp_efw_l2_driver_custom.bash")



                    b = b + 1



    if __name__ == "__main__": main()

