from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import dateData
import csvContent
from utilFunctions import *
import json

DEBUG = True

UPLOAD_FOLDER = './uploads/'
UPLOADS_DATE_DATA_PATH = 'resources/uploadDates.txt'

app = Flask(__name__)
app.config.from_object(__name__)

# ToDo investigate security risk of CORS, does security matter for a short project?
cors = CORS(app, supports_credentials=True)

# Get list of prev uploaded files
@app.route('/csv', methods=['GET'])
def getAllCsvFiles():
    csvDataList = []
    createFileIfNotInit(UPLOADS_DATE_DATA_PATH)
    with open(UPLOADS_DATE_DATA_PATH, "r") as file:
        for line in file.readlines():
            nameDate = line.split(': ')
            formattedDateTime = nameDate[0].split(".")[0]
            dateDataObject = dateData.createDateData(nameDate[1], formattedDateTime)
            csvDataList.append(dateDataObject.__dict__)

    return jsonify({
        'status': 'success',
        'csvDataList': csvDataList
    })

# Upload a file
@app.route('/csv', methods=['POST'])
def handleUploadedCsvFile():
    if not request.files:
        return "File not found", 400

    for key, file in request.files.items():
        if key == '':
           return "File not found", 400
        elif file and allowedFile(key):
            saveCsvFile(file, key)
    return "File(s) read succesfully", 200

# Download a file
@app.route('/csv/download/<fileName>', methods=['GET'])
def downloadFile(fileName):
    if os.path.isfile(UPLOAD_FOLDER + fileName):
        return send_from_directory(app.config["UPLOAD_FOLDER"], fileName)
    else:
        return "File not Found", 404

# View a file
@app.route('/csv/view/<fileName>/<pageNumber>', methods=['GET'])
def viewFile(fileName, pageNumber):
    pageNumber = int(pageNumber) + 1
    if os.path.isfile(UPLOAD_FOLDER + fileName) and pageNumber > 0:
        csvContentList = []
        with open(UPLOAD_FOLDER + fileName, 'r') as file:
            lines = file.readlines()
            lines = lines[1:]

        for i in range(min(pageNumber*500, len(lines))-500, min(pageNumber*500, len(lines))):
            line = lines[i]
            line = line.split(',')
            contentObject = csvContent.createCsvContent(line[0],line[1],line[2],line[3],line[4],
            line[5],line[6],line[7],line[8],line[9],line[10].strip())
            csvContentList.append(contentObject.__dict__)

        if (pageNumber*500) -500 > len(lines):
            pageNumber -= 1

        return jsonify({
        'status': 'success',
        'csvContentList': csvContentList,
        'pageNumber': pageNumber
        })
    else:
        return "File not Found", 404

# Delete a file
@app.route('/csv/delete/<fileName>', methods=['DELETE'])
def deleteFile(fileName):
    clearDataFromUploadDate(fileName)
    clearDataFromYearStats(fileName)
    if os.path.isfile(UPLOAD_FOLDER + fileName):
        os.remove(UPLOAD_FOLDER + fileName)
        return "Success", 200
    else:
        return "File not Found", 404

# Get files year stats
@app.route('/csv/stats/<fileName>', methods=['GET'])
def getFilesStats(fileName):
    path = getStatsPath(fileName)
    if not os.path.exists(path):
        return "File not Found", 404
    else:
        with open(path, "r") as file:
            csvYearStats = json.loads(file.read())

    return jsonify({
        'status': 'success',
        'csvYearStats': csvYearStats
    })

if __name__ == '__main__':
    app.run()