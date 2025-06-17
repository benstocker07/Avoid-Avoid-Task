import pymysql
import base64
import socket

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print("Your IP address is:", ip_address)

encoded_password = 'TUF0Y2hhdHRheDEt'
host='benstocker07.ddns.net'
user='benstocker07'
password=base64.b64decode(encoded_password.encode('utf-8')).decode('utf-8')
database='OED'

connection = pymysql.connect(host=host, user=user, password=password, database=database)

def clear_table():
    connection = pymysql.connect(host=host, user=user, password=password, database=database)

    try:
        with connection.cursor() as cursor:
            delete_query = "DELETE FROM Players;"
            cursor.execute(delete_query)
        connection.commit()
    finally:
        connection.close()

try:
    with connection.cursor() as cursor:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Players (
            pid VARCHAR(255),
            ip_address VARCHAR(45) NOT NULL,
            status VARCHAR(20) NOT NULL
        );
        """
        cursor.execute(create_table_query)
    connection.commit()
finally:
    connection.close()

ready = False    

def set_ready(status):
    global ready
    ready = status

def write_to_database():
    connection = pymysql.connect(host=host, user=user, password=password, database=database)

    try:
        with connection.cursor() as cursor:
            insert_query = """
            INSERT INTO Players (ip_address, status) 
            VALUES (%s, %s);
            """
            cursor.execute(insert_query, (ip_address, 'True' if ready else 'False'))
        connection.commit()
    finally:
        connection.close()

write_to_database()
clear_table()
set_ready(True)
