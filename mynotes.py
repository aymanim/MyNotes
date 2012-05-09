


import os
import sys
import datetime
import errno
import subprocess
from optparse import OptionParser
import parsedatetime.parsedatetime as pdt 
import parsedatetime.parsedatetime_consts as pdc



def initParser(args):

    parser = OptionParser()
    

    parser.add_option("-d", "--date",
                  action="store", type="string", dest="date")

    
    (options, args) = parser.parse_args(args)
    return options

def parseDate(dateString):

    c = pdc.Constants()
    p = pdt.Calendar(c)
    result = p.parse(dateString)

    year = result[0][0]
    monthDay = '%0*d' %(2, result[0][1]) + '%0*d' %(2, result[0][2])

    return (year, monthDay)


def main():


    options = initParser(sys.argv)

    pathToDataFiles = "/Users/ajsingh/myNotes/"
    editor = "subl"


    if(options.date):
        (year, monthDay) = parseDate(options.date)
    
    else:
        now = datetime.datetime.now()
        year = now.year
        monthDay = '%0*d' %(2, now.month) + '%0*d' %(2, now.day)

    currDir = pathToDataFiles + '%0*d' %(4, year)
    currFile = currDir + "/" + monthDay + ".txt"

    #currDir = pathToDataFiles + '%0*d' %(4, 2011)
    #currFile = currDir + "/" + '%0*d' %(2, now.month) + '%0*d' %(2, 1) + ".txt"

    try:
        os.makedirs(currDir)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise

    subprocess.call([editor, currFile])




if __name__ == "__main__":
    main()

