from datetime import datetime

import win32com.client as wincl
import pandas as pd
import numpy as np

import mysql.connector
import time

def speak(msg):
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(msg)

messages = {
    "Ricardo":"Hola Ricard, bienvenido al Show Room", 
    }

t = time.time()
while True:
    conn =  mysql.connector.connect(
            host="localhost",
            user="admin",
            passwd="admin",
            database="facedb",
    )
    df = pd.read_sql("SELECT Name, FirstSeen, max(LastSeen) as LastSeen FROM recognition GROUP BY Name ORDER BY LastSeen desc", conn)

    for i, row in df.iterrows():
        first_seen = datetime.strptime(row["FirstSeen"], ('%d/%m/%y %H:%M:%S'))
        last_seen = datetime.strptime(row["LastSeen"], ('%d/%m/%y %H:%M:%S'))

        difference = (last_seen-first_seen).seconds

        if difference < 10:
            if messages.get(row["Name"], 0):
                speak(messages[row["Name"]])
                messages.pop(row["Name"])

    et = int(time.time()-time)

    conn.close()

    print("{} seconds".format(et), end="\r")
    if et > 120:
        break