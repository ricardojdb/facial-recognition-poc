import mysql.connector

def create_mysql_table():
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        passwd="admin",
        database="facedb",
    ) 
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS recognition(Name TEXT, FirstSeen TEXT, LastSeen TEXT)")
    conn.commit()

    conn.close()

def insert_mysql_table(data_list):
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        passwd="admin",
        database="facedb",
    ) 
    c = conn.cursor()
    for data in data_list:
        c.execute("INSERT INTO recognition (Name, FirstSeen, LastSeen) VALUES (%s,%s,%s)", [str(x) for x in data])
        conn.commit()

    conn.close()

def delete_mysql_table():
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        passwd="admin",
        database="facedb",
    ) 
    c = conn.cursor()
    c.execute("DELETE FROM recognition")

    conn.commit()
    conn.close()