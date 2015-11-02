import urllib.request

'''
Created on Jul 9, 2015

@author: marcin
'''

class FileStore(object):

    storagePath = ''

    def __init__(self, storagePath = './'):
        self.storagePath = storagePath
    
    def saveToFile(self, url, destination):
        urllib.request.urlretrieve(url,self.storagePath + destination)
    
    def getContent(self, url):
        f = urllib.request.urlopen(url)
        return f.read().decode("utf8")
    
    def saveTextToFile(self, text, destination):
        file = open(self.storagePath + destination, "w")
        file.write(text)
        file.close()
        
            