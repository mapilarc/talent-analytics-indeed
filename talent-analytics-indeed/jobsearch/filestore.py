import urllib.request
import urllib.parse

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
        
            