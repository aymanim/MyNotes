import os
import re
import sys
import datetime
import errno
import subprocess
from optparse import OptionParser
import parsedatetime.parsedatetime as pdt 
import parsedatetime.parsedatetime_consts as pdc

defaultFileExtension = ".txt"
defaultPathToDataFiles = "/Users/ajsingh/SkyDrive/myNotes/"
defaultEditor = "subl"
pathToScript = "/Users/ajsingh/dev/mynotes/"


pathToTemplateEntry = pathToScript + "template_entry.html"
pathToTemplateYear = pathToScript + "template_year.html"
pathToTemplateBase = pathToScript + "template_base.html"

def initParser(args):

    parser = OptionParser()

    parser.add_option("-d", "--date", action="store", type="string",    
                        dest="date", help="Override date. Enter it in a string\
                        form. Ex: \"Tomorrow\" or \"March 4th 2012\"")

    parser.add_option("-e", "--editor", action="store", type="string", 
                        dest="editor", help="Override the editor.")
    
    parser.add_option("-r", "--root", action="store", type="string", 
                        dest="root", help="Change the root location of this\
                        file. The directory structure will be preserved")

    parser.add_option("-v", "--view", action="store_true",  
                        dest="view", help="Generate a view in the form of a flat\
                        HTML file")
    
    (options, args) = parser.parse_args(args)

    return options


def parseDate(dateString):

    c = pdc.Constants()
    p = pdt.Calendar(c)
    result = p.parse(dateString)

    year = result[0][0]
    monthDay = '%0*d' %(2, result[0][1]) + '%0*d' %(2, result[0][2])

    return (year, monthDay)

def generateView(rootDir):
    regExFilename = re.compile('[0-9][0-9][0-9][0-9]\.txt')
    regExDir = re.compile('[0-9][0-9][0-9][0-9]')


    templateEntryData = open(pathToTemplateEntry).read()
    templateBaseData = open(pathToTemplateBase).read()
    templateYearData = open(pathToTemplateYear).read()

    yearData = {}

    allData = ""

    for dirname, dirnames, filenames in os.walk(rootDir):
        for filename in filenames:
            if(regExFilename.match(filename) != None):

                year = dirname.split("/")[-1]

                

                filePath = os.path.join(dirname, filename)
                fileData = open(filePath).read()
                fileName = filePath.split("/")[-1].split(".")[0]

                dataAppliedToTemplate = templateEntryData.replace("{{ date }}", fileName)
                dataAppliedToTemplate = dataAppliedToTemplate.replace("{{ data }}", fileData) 
                
                try:
                    yearData[year] += dataAppliedToTemplate 
                except:
                    yearData[year] = dataAppliedToTemplate

    # maybe sort here if needed

    sortedYears = sorted(yearData)

    for year in sortedYears:
        
        perYearData = templateYearData.replace("{{ year }}", year)
        perYearData = perYearData.replace("{{ year_data }}", yearData[year])

        allData += perYearData


    print templateBaseData.replace("{{ full_data }}", allData)


def main():

    options = initParser(sys.argv)

    if(options.root):
        pathToDataFiles = options.root #make sure we have a / in the end
    else:        
        pathToDataFiles = defaultPathToDataFiles
    
    if(options.editor):
        editor = options.editor
    else:
        editor = defaultEditor

    if(options.date):
        (year, monthDay) = parseDate(options.date)
    
    else:
        now = datetime.datetime.now()
        year = now.year
        monthDay = '%0*d' %(2, now.month) + '%0*d' %(2, now.day)

    if(options.view):
        generateView(pathToDataFiles)
        return


    currDir = pathToDataFiles + '%0*d' %(4, year)
    currFile = currDir + "/" + monthDay + defaultFileExtension

    try:
        os.makedirs(currDir)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise

    subprocess.call([editor, currFile])

    generateView(pathToDataFiles)






if __name__ == "__main__":
    main()

