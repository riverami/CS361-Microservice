# microService.py
# Author: Miles Rivera
# Description: Microservice to send and receive data from a database file.
# References:
# https://docs.python.org/3/library/sqlite3.html
# https://docs.python.org/3/library/socket.html

import sys
from os.path import exists
import sqlite3
import time
import socket


def getData(data1):
    returnData = cur.execute("SELECT * FROM data WHERE title = '" + data1 + "'")
    return returnData


def insertData(data1, data2, data3):
    cur.execute("INSERT INTO data VALUES (" + "'" + str(data1) + "'" + ", " + str(data2) + ", " + str(data3) + ")")
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
    cur.execute("CREATE TABLE data(title, year, score)")
    cur.execute("INSERT INTO data VALUES ('Movie1', 1990, 9.1), ('Movie2', 1952, 7.4), ('Movie3', 1984, 6.2)")
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

    if words[0] == "GET" and words[1] != "" and words[1] is not None:
        sqlData = getData(str(words[1].strip()))
        listData = sqlData.fetchall()
        retData = str(listData)
    elif words[0].strip() == "POST" and words[1].strip() != "" and words[1].strip() is not None and \
            words[2].strip() != "" and words[2].strip() is not None and words[3].strip() != "" \
            and words[3].strip() is not None:

        data1 = words[1].strip()
        data2 = words[2].strip()
        data3 = words[3].strip()

        insertData(data1, data2, data3)
        retData = "Data has been entered"
    else:
        retData = "Please enter a valid command with valid arguments"

    servConn.send(retData.encode())

    # wait for a bit so no redundant commands are received.
    retData = ""
    message = ""
    words = ""
    time.sleep(1)



