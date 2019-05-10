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
    c.execute("INSERT INTO recognition (Name, FirstSeen, LastSeen) "
              "VALUES (%s,%s,%s)", [str(x) for x in data_list])
    conn.commit()

    conn.close()

def update_mysql_table(name, last_seen):
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        passwd="admin",
        database="facedb",
    ) 
    c = conn.cursor()
    # Update single record 
    sql_update_query = """UPDATE recognition 
                          SET LastSeen = '{}' 
                          WHERE Name = '{}'""".format(last_seen, name)
    c.execute(sql_update_query)
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