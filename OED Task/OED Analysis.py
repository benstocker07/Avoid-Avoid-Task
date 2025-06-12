encoded_password = 'TUF0Y2hhdHRheDEt'

import pymysql
import base64
import time
import pygame
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation

host = 'benstocker07.ddns.net'
user = 'benstocker07'
password = base64.b64decode(encoded_password.encode('utf-8')).decode('utf-8')
database = 'OED'

def create_connection():
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

def analysis():
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    mngr = plt.get_current_fig_manager()
    mngr.full_screen_toggle() 

    def animate(i):
        conn = create_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT COUNT(score) AS total_score_count FROM OED WHERE score <> 0")
            total_score_count = cursor.fetchone()['total_score_count']
            cursor.execute("SELECT COUNT(*) AS total_entries FROM OED")
            total_entries = cursor.fetchone()['total_entries']

            overall_percentage = (total_score_count / total_entries * 100) if total_entries else 0

            cursor.execute("SELECT CAST(participant_no AS CHAR) AS participant_no, COUNT(score) AS score_count FROM OED WHERE score <> 0 GROUP BY participant_no")
            data = cursor.fetchall()

        participant_nos = [row['participant_no'] for row in data]
        score_counts = [row['score_count'] for row in data]

        ax1.clear()
        ax1.bar(participant_nos, score_counts, width=0.25)
        ax1.set_title("Open Day Scores:\n\nTotal Trials Run: {}\nOverall Percentage: {:.2f}%".format(total_score_count, overall_percentage))

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()

analysis()
