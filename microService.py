# microService.py
# Author: Miles Rivera
# Description: Microservice to send and receive data from a database file.
# References:
# https://docs.python.org/3/library/sqlite3.html
# https://docs.python.org/3/library/socket.html

#Table:
#date, water temp (F), air temp(F), time of the first peak high tide
#weather(date, water_temp, air_temp, first_peak_time)

import sys
from os.path import exists
import sqlite3
import time
import socket


def getDataBetweenDate(lowDate, highDate):
    returnData = cur.execute("SELECT * FROM weather WHERE date BETWEEN '" + lowDate + "' AND '" + highDate + "'")
    return returnData


def getDataBetweenWaterTemp(lowTemp, highTemp):
    #lowTemp = int(lowTemp)
    #highTemp = int(highTemp)
    returnData = cur.execute("SELECT * FROM weather WHERE water_temp BETWEEN " + lowTemp + " AND " + highTemp)
    return returnData


def getDataBetweenAirTemp(lowTemp, highTemp):
    returnData = cur.execute("SELECT * FROM weather WHERE air_temp BETWEEN " + lowTemp + " AND " + highTemp)
    return returnData


def getDataBetweenPeakTime(lowTime, highTime):
    returnData = cur.execute("SELECT * FROM weather WHERE first_peak_time BETWEEN '" + lowTime + "' AND '" + highTime + "'")
    return returnData


def insertData(newDate, newWaterTemp, newAirTemp, newTime):
    cur.execute("INSERT INTO weather VALUES (" + "'" + str(newDate) + "'" + ", " + str(newWaterTemp)
                + ", " + str(newAirTemp) + ", " + str(newTime) + ")")
    conn.commit()


# Check if database file exists. Open if so.
if exists("data.db"):

    # Connection Object
    conn = sqlite3.connect("data.db")
    # Cursor object. Allows execution of SQL commands.
    cur = conn.cursor()

# Otherwise create the database file and initialize the table with some data.
else:

    f = open("data.db", "x")
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE weather(date, water_temp, air_temp, first_peak_time)")
    cur.execute("INSERT INTO weather VALUES ('07-31-2022', 80, 95, '16:00'),"
                " ('08-01-2022', 95, 80, '17:00'), ('06-15-2022', 70, 80, '12:00')")
    conn.commit()


host = socket.gethostname()
port = 5000

serverSocket = socket.socket()
serverSocket.bind((host, port))

serverSocket.listen(1)
servConn, servAddress = serverSocket.accept()

# Leave service running.
while True:
    time.sleep(1)
    message = servConn.recv(1024).decode()
    if not message:
        break
    print(message)
    words = message.split(',')
    message = ""
    retData = ""
    print(words[0])
    print(words[1])
    print(words[2])

    if words[0] == "GETONDATE" and words[1] != "" and words[1] is not None and\
            words[2].strip() != "" and words[2].strip() is not None:
        sqlData = getDataBetweenDate(str(words[1].strip()), str(words[2].strip()))
        listData = sqlData.fetchall()
        retData = str(listData)

    elif words[0] == "GETONWATERTEMP" and words[1] != "" and words[1] is not None and\
            words[2].strip() != "" and words[2].strip() is not None:
        sqlData = getDataBetweenWaterTemp(words[1].strip(), words[2].strip())
        listData = sqlData.fetchall()
        retData = str(listData)

    elif words[0] == "GETONAIRTEMP" and words[1] != "" and words[1] is not None and\
            words[2].strip() != "" and words[2].strip() is not None:
        sqlData = getDataBetweenAirTemp(str(words[1].strip()), str(words[2].strip()))
        listData = sqlData.fetchall()
        retData = str(listData)

    elif words[0] == "GETONPEAKTIME" and words[1] != "" and words[1] is not None and \
            words[2].strip() != "" and words[2].strip() is not None:
        sqlData = getDataBetweenPeakTime(str(words[1].strip()), str(words[2].strip()))
        listData = sqlData.fetchall()
        retData = str(listData)

    elif words[0].strip() == "POST" and words[1].strip() != "" and words[1].strip() is not None and \
            words[2].strip() != "" and words[2].strip() is not None and words[3].strip() != "" \
            and words[3].strip() is not None and words[4].strip() != "" and words[4].strip() is not None:

        newDate = words[1].strip()
        newWaterTemp = words[2].strip()
        newAirTemp = words[3].strip()
        newTime = words[4].strip()

        insertData(newDate, newWaterTemp, newAirTemp, newTime)
        retData = "Data has been entered"
    else:
        retData = "Please enter a valid command with valid arguments"

    servConn.send(retData.encode())

    # wait for a bit so no redundant commands are received.
    retData = ""
    message = ""
    words = ""
    time.sleep(1)



