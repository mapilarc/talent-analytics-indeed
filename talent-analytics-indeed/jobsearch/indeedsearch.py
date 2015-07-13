import sys
import math

import urllib.request
from urllib.parse import quote

import xml.etree.cElementTree as ET

'''
Created on Jul 8, 2015

@author: marcin
'''



class IndeedSearch(object):
    '''
    classdocs
    '''
    PUBLISHER = ""
    URL_HEADER_PATTERN = "http://api.indeed.com/ads/apisearch?v=2&publisher={0}&l={1}&co=pl&limit=1&q={2}"
    URL_PATTERN = "http://api.indeed.com/ads/apisearch?v=2&publisher={0}&l={1}&co=pl&limit=25&q={2}&start={3}"

    query = ""
    location = ""

    def __init__(self, query, location):
        '''
        Constructor
        '''
        self.query = quote(query, safe='')
        self.location =  quote(location, safe='')
    
    def getSearchCount(self):
        searchCount = 0
        url = self.URL_HEADER_PATTERN.format(self.PUBLISHER, self.location, self.query)

        try:
            wp = urllib.request.urlopen(url)                     
            doc = ET.fromstring(wp.read())

            for elem in doc.findall(".//totalresults"): 
                searchCount = int(elem.text)
                
            return searchCount
            
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            raise
        
    def getPartialUrls(self):
        urls = []
        
        searchCount = self.getSearchCount()
        urlCount = math.ceil(searchCount / 25)
        
        for i in range(0, urlCount):
            urls.append( self.URL_PATTERN.format(self.PUBLISHER, self.location, self.query,str(25 * i)) )
        
        return urls