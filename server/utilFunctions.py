from werkzeug.utils import secure_filename
import pandas as pd
import os
from datetime import datetime

UPLOAD_FOLDER = './uploads/'
UPLOADS_DATE_DATA_PATH = 'resources/uploadDates.txt'
UPLOADS_STATS_DATA_PATH = 'resources/'
TMP_FOLDER = './tmp/'
ALLOWED_EXTENSIONS = {'csv'}

# Check if file extention is allowed
def allowedFile(fileName):
    return '.' in fileName and \
            fileName.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# The below method stops an upload from overwriting a prev uploaded file
def renameFileIfNameInPath(originalName):
    inc = 1
    name = originalName
    while os.path.isfile(UPLOAD_FOLDER + name):
        splitOriginalName = originalName.rsplit('.', 1)
        name = splitOriginalName[0] + '(' + str(inc) + ').' + splitOriginalName[1]
        inc += 1
    else:
        return name;

# Save the file and its stats locally
def saveCsvFile(file, key):
    pdData = replaceEmptyStrings(file, key)
    secureFileName = secure_filename(key)
    fileName = renameFileIfNameInPath(secureFileName)
    saveUploadDate(fileName)
    saveContentYearStats(pdData, fileName)
    pdData.to_csv(UPLOAD_FOLDER + fileName, index = False)

# Save timestamp of files upload to .txt file
def saveUploadDate(name):
    createFileIfNotInit(UPLOADS_DATE_DATA_PATH)
    with open(UPLOADS_DATE_DATA_PATH, "a") as file:  
        timeStamp = str(datetime.now())
        file.write(timeStamp + ": " + name + "\n")

# This doesnt scale very well, real solution would use a database
def clearDataFromUploadDate(fileName):
    with open(UPLOADS_DATE_DATA_PATH, 'r') as file:
        lines = file.readlines()
    with open(UPLOADS_DATE_DATA_PATH, 'w') as file:
        for line in lines:
            if not fileName in line:
                file.write(line)

# This doesnt scale very well, real solution would use a database
def clearDataFromYearStats(fileName):
    path = getStatsPath(fileName)
    if os.path.isfile(path):
        os.remove(path)

# Uses pandas module to edit the file contents, removing empty strings and replacing with "BLANK"
def replaceEmptyStrings(file, fileName):
    path = TMP_FOLDER + "tmp_" + fileName
    file.save(path)
    pdData = pd.read_csv(path)
    #replaces empty strings which pandas reads as NaNs
    pdData["state"].fillna('BLANK', inplace=True)
    os.remove(path)
    return pdData

# Creates a file for given path if file 
def createFileIfNotInit(path):
    if not os.path.exists(path):
        with open(path, 'w'): 
            pass

# Agg year counts and outputs to a file for later access
def saveContentYearStats(pdData, fileName):
    path = getStatsPath(fileName)
    createFileIfNotInit(path)
    with open(path, 'w') as file:
        pdData["date"] = pd.to_datetime(pdData["date"])
        file.write(pdData["date"].groupby(pdData.date.dt.year).agg('count').to_json())

# Returns the path for the stats file
def getStatsPath(fileName):
    fileName = fileName[:-4] + "Stats" + ".txt"
    return UPLOADS_STATS_DATA_PATH + fileName

def checkValidPageNumber(pageNumber, numberOfRows):
    if pageNumber < 1:
        pageNumber = 1
    elif (pageNumber*500) -500 > numberOfRows:
        pageNumber = (numberOfRows//500) + 1
    return pageNumber
