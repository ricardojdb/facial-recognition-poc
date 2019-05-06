from datetime import datetime

import win32com.client as wincl
from datetime import datetime

import pandas as pd
import numpy as np

import mysql.connector
import json

def speech2text_cortana(msg):
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(msg)

def speak_cortana(name):
    responses_file = "utils/responses.json"
    messages = json.load(open(responses_file, "rb"))
    if messages["new_messages"].get(name, 0):
        speech2text_cortana(messages["new_messages"][name])
        time_now = datetime.now().strftime('%d/%m/%y %H:%M:%S')
        messages["log"] = {name: {"message":messages["new_messages"], 
                                    "time":time_now}}
        messages["new_messages"].pop(name)

        json.dump(messages, open(responses_file, "w"))
        return True
    return False

if __name__ == "__main__":
    print("Listening..")
    while True:
        conn =  mysql.connector.connect(
                host="localhost",
                user="admin",
                passwd="admin",
                database="facedb")

        df = pd.read_sql(
            "SELECT Name, FirstSeen, max(LastSeen) as LastSeen "
            "FROM recognition GROUP BY Name ORDER BY LastSeen desc", conn)

        for i, row in df.iterrows():
            first_seen = datetime.strptime(row["FirstSeen"], '%d/%m/%y %H:%M:%S')
            last_seen = datetime.strptime(row["LastSeen"], '%d/%m/%y %H:%M:%S')

            difference = (last_seen-first_seen).seconds

            if difference < 20:
                name = row["Name"]
                speak_cortana(name)

        conn.close()
