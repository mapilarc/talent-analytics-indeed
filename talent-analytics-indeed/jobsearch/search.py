import datetime
import getopt
import os
import random
import string
import sys
import re

from jobsearch.indeedsearch import IndeedSearch
from jobsearch.filestore import FileStore


'''
Created on Jul 8, 2015

@author: marcin
'''

DESTINATIONPATH = "/home/marcin/Downloads/"

def main():  
    query = ""
    location = ""
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"q:l:")
    except getopt.GetoptError:
        print ("indeedjobsearch.py -q <query> -l <location>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-q"):
            query = arg
        elif opt in ("-l"):
            location = arg
    
    print ('Query: ', query)
    print ('Location: ', location)
    
    finalPath = DESTINATIONPATH + datetime.date.today().strftime("%Y-%m-%d") + "/" 
    
    if not os.path.exists(finalPath):
        os.makedirs(finalPath)
    
    destinationFileName = re.sub('[^A-Za-z0-9]+', '', query + location)
    randomString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    destinationFileName = destinationFileName + randomString + "_{0}.xml"
    
    indeed = IndeedSearch(query, location)
    
    urls = indeed.getPartialUrls()
    for i in range(len(urls)):
        fs = FileStore(finalPath)
        fs.saveToFile( urls[i], destinationFileName.format(str(i)) )
    
    print("End.")

if __name__ == "__main__":
    main()