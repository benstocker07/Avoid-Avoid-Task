import sqlite3
import time
from datetime import datetime

def create_db_connection():
    connection = sqlite3.connect('rJORT.db')
    create_table_if_not_exists(connection)
    return connection

def create_table_if_not_exists(connection):
    with connection:
        connection.execute("""
        CREATE TABLE IF NOT EXISTS Triggers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trigger_code INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
        """)

def log_trigger(connection, trigger_code):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    with connection:
        connection.execute("INSERT INTO Triggers (trigger_code, timestamp) VALUES (?, ?)", (trigger_code, current_time))

import pyxid2

devices = pyxid2.get_xid_devices()
global dev
dev = devices[0]

global trigger_count
trigger_count = 0

db_connection = create_db_connection()

def calibration():
    global trigger_count
    dev.activate_line(bitmask=1)
    log_trigger(db_connection, "1")

def LC():
    global trigger_count
    dev.activate_line(bitmask=2)
    log_trigger(db_connection, "2")

def GC():
    global trigger_count
    dev.activate_line(bitmask=3)
    log_trigger(db_connection, "3")

def start():
    global trigger_count
    dev.activate_line(bitmask=64)
    log_trigger(db_connection, "64")

def stop():
    global trigger_count
    dev.activate_line(bitmask=128)
    log_trigger(db_connection, "128")

def split():
    global trigger_count
    dev.activate_line(bitmask=129)
    log_trigger(db_connection, "129")

def close_connection():
    db_connection.close()
