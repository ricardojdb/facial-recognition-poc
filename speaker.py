from datetime import datetime

import win32com.client as wincl
from datetime import datetime

import pandas as pd
import numpy as np

import mysql.connector
import json

def speak(msg):
    print(msg)
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(msg)

responses_file = "utils/responses.json"

print("Listening..")
while True:
    conn =  mysql.connector.connect(
            host="localhost",
            user="admin",
            passwd="admin",
            database="facedb")

    df = pd.read_sql("SELECT Name, FirstSeen, max(LastSeen) as LastSeen FROM recognition GROUP BY Name ORDER BY LastSeen desc", conn)

    messages = json.load(open(responses_file, "rb"))

    for i, row in df.iterrows():
        first_seen = datetime.strptime(row["FirstSeen"], '%d/%m/%y %H:%M:%S')
        last_seen = datetime.strptime(row["LastSeen"], '%d/%m/%y %H:%M:%S')

        difference = (last_seen-first_seen).seconds

        if difference < 20 and messages["new_messages"].get(row["Name"], 0):
            name = row["Name"]
            message = messages["new_messages"][name]
            time_now = datetime.now().strftime('%d/%m/%y %H:%M:%S')

            speak(message)
            messages["log"] = {name: {"message":message, 
                                      "time":time_now}}
            messages["new_messages"].pop(row["Name"])
            
            json.dump(messages, open(responses_file, "w"))

    conn.close()
