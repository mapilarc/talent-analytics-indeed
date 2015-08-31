import datetime
import getopt
import os
from glob import glob
import random
import string
import sys
import re
import logging
import os.path

import xml.etree.cElementTree as ET

from jobsearch.indeedsearch import IndeedSearch
from jobsearch.filestore import FileStore


'''
Created on Jul 8, 2015

@author: marcin
'''

DESTINATIONPATH = "/home/marcin/Downloads/indeed/"
DOWNLOADURL = "http://pl.indeed.com/rc/clk?jk="

def main():  
    logging.basicConfig(filename=DESTINATIONPATH + 'offerdetails.log',level=logging.DEBUG, format='%(asctime)s %(message)s')

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
    
    files = [y for x in os.walk(finalPath) for y in glob(os.path.join(x[0], '*.xml'))]
    
    for file in files:
        with open (file, "r") as myfile:
            content = myfile.read().replace('\n', '')
            doc = ET.fromstring(content)

            for elem in doc.findall(".//result"):
                jobkey = elem.find("jobkey").text #let's suppose there is no error :)
                url = elem.find("url").text #let's suppose there is no error :)
                try:
                    if not os.path.isfile(DESTINATIONPATH + 'offerdetails/' + jobkey + '.html'):
                        fs = FileStore(DESTINATIONPATH + 'offerdetails/')
                        fs.saveToFile( DOWNLOADURL + jobkey, jobkey + '.html' )
                        logging.debug(jobkey + ";original;ok")
                except Exception as e:
                    logging.debug(jobkey + ";original;error:" + str(e))
                        
                try:
                    if not os.path.isfile(DESTINATIONPATH + 'indeedofferdetails/' + jobkey + '.html'):                
                        fs = FileStore(DESTINATIONPATH + 'indeedofferdetails/')
                        fs.saveToFile( url, jobkey + '.html' )
                        logging.debug(jobkey + ";indeed;ok")
                except Exception as e:
                    logging.debug(jobkey + ";indeed;error:" + str(e))
                            
    print("End.")

if __name__ == "__main__":
    main()