#Find out what files are available online for download

#Only working for Python3 at the moment

#Example:
#url = 'http://themis.ssl.berkeley.edu/data/rbsp/rbspa/l1/mscb1/2014/'
#ext = 'cdf'
#filesonline = Find_available_files_online()
#files = filesonline.listFD(url, ext)


#Written by Aaron W Breneman, 2019-04-09

class Find_available_files_online:

    def __init__(self):
        self.__dict__.update()


    def listFD(self, url, ext=''):
        from bs4 import BeautifulSoup
        import requests

        page = requests.get(url).text
        print(page)
        soup = BeautifulSoup(page, 'html.parser')
        return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
