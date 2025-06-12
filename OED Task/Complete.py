
with open ('spwf.txt', 'r') as file:
    read = file.read().strip()

encoded_password = read

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

def check():
    while True:
        connection = create_connection()
        with connection.cursor() as cursor:
            check_query = "SELECT COUNT(*) FROM Players WHERE complete = False;"
            cursor.execute(check_query)
            result = cursor.fetchone()

            print(check_query)

            if result[0] == 0:
                print("All players have finished")
                connection.close()
                return True
            else:
                print("Not complete")
            time.sleep(1)
        connection.close()

def presentation():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Full Screen Pygame Example")
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    messages = [
        "You may be asking: what's the point?",
        "We have used this task to effectively study anxiety",
        "and... it works! We have found brain regions associated with goal conflict",
        "But now we need to study it further, and that can include exercise studies"
    ]

    for writing in messages:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        running = False

            screen.fill(WHITE)
            font = pygame.font.Font(None, 74)
            text = font.render(writing, True, BLACK)
            text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(text, text_rect)

            pygame.display.flip()
            pygame.time.delay(1000)

    pygame.quit() 

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

if check():
    presentation()
    analysis()
