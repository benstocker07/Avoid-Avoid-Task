with open ('spwf.txt', 'r') as file:
    read = file.read().strip()
    
encoded_password = read

import pygame
import sys
from pygame.locals import *
import random
import time
import math
import os
import csv
from pygame.sprite import Group, Sprite, spritecollide, groupcollide
import pandas as pd
from scipy import stats
import timer
import decimal
from time import sleep
import scipy
import numpy
import pymysql
import base64
import socket
import subprocess
import shutil
global sql_type
global ready
global buttonspeed

if not os.path.exists('Outputs'):
        os.makedirs('Outputs')
        
def complete():
    cursor = connection.cursor()

    update_complete = """
    UPDATE Players
    SET complete = %s
    WHERE pid = %s;
    """
    
    try:
        cursor.execute(update_complete, (True, participant_number))
        connection.commit()
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        cursor.close() 
        connection.close()  

    def cleanup():
        files = []
        files.append('OED Task.py')
        files.append('spwf.txt')
        
        for file in files:
            os.remove(str(f'{file}'))
    cleanup()
            
def installation():
    import pkg_resources
    packages_to_install = [
        "pygame", "pandas", "pymysql", "statsmodels",
        "seaborn", "numpy", "matplotlib", "scipy", "joystick"
    ]
    
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    
    if "pygame" not in installed_packages:
        print("Pygame not found, installing all packages...")
        for package in packages_to_install:
            try:
                subprocess.check_call(["pip", "install", package])
                print(f"Successfully installed {package}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install {package}: {e}")
    else:
        print("Pygame is already installed.")

installation()

def sql_rt(sql_type, ReactionTime):
    with connection.cursor() as cursor:
        sql_rt = """
        INSERT INTO RTs (pid, trial_type, RT)
        VALUES (%s, %s, %s);
        """
        cursor.execute(sql_rt, (participant_number, sql_type, ReactionTime))
        connection.commit()

def runcount():
    filename = 'run_count.txt'
    try:
        with open(filename, 'r') as file:
            count = int(file.read().strip())
    except FileNotFoundError:
        count = 0
    except ValueError:
        count = 0

    if count == 0:
        subprocess.run("gpupdate /force", shell=True)

    count += 1

    with open(filename, 'w') as file:
        file.write(str(count))

runcount()


hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

buttonspeed = 2.2

host='benstocker07.ddns.net'
user='benstocker07'
password=base64.b64decode(encoded_password.encode('utf-8')).decode('utf-8')
database='OED'

connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout = 60
    )

connection = pymysql.connect(host=host, user=user, password=password, database=database)

def write_to_database():
    global false_count

    try:
        with connection.cursor() as cursor:
            check_query = "SELECT COUNT(*) FROM Players WHERE ip_address = %s;"
            cursor.execute(check_query, (ip_address,))
            count = cursor.fetchone()[0]

            if count > 0:
                delete_query = "DELETE FROM Players WHERE ip_address = %s;"
                cursor.execute(delete_query, (ip_address,))

            count_false_query = "SELECT COUNT(*) FROM Players WHERE status = 'False';"
            cursor.execute(count_false_query)
            false_count = cursor.fetchone()[0]

            insert_query = """
            INSERT INTO Players (pid, ip_address, status, complete)
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(insert_query, (participant_number, ip_address, 'True' if ready else 'False', 'False'))
            connection.commit()
            
    finally:
        print("")

def check_team_ready():
    connection = pymysql.connect(host=host, user=user, password=password, database=database)

    try:
        with connection.cursor() as cursor:
            check_query = "SELECT COUNT(*) FROM Players WHERE status = 'False';"
            cursor.execute(check_query)
            count = cursor.fetchone()[0]
            TeamReady = count == 0

    finally:
        print("")

global GC_SPEED
GC_SPEED = 4.5

pygame.init()
pygame.joystick.init
global keys
keys = pygame.key.get_pressed()


COLLISION_SCORE = 0
COLLISION_SCORE2 = COLLISION_SCORE/20
COLLISIONSCORECONV = repr(COLLISION_SCORE2)
Average_Score = COLLISION_SCORE2/20
Average_Score_Output = repr(Average_Score)

jcount = pygame.joystick.get_count()

if jcount == 0:
    print("No joystick connected")
    control = pygame.K_f

def center_text(text):
    terminal_size = shutil.get_terminal_size()
    width = terminal_size.columns
    padding = (width - len(text)) // 2
    print(' ' * padding + text)

os.system('cls')

while True:
    center_text("Pick a random participant number to identify yourself! Keep an eye on the leaderboard for your score!")
    participant_number = input("\n\n" + " " * (os.get_terminal_size().columns // 2 - 10) + "Your Number: ")
    directoryname = f"OED Participant {participant_number}"
    os.makedirs(directoryname, exist_ok=True)


    with connection.cursor() as cursor:
        query = "SELECT COUNT(*) AS count FROM Players WHERE pid = %s;"
        cursor.execute(query, (participant_number,))
        result = cursor.fetchone()
        print(f'SQL participant number result: {result}')
    if result and result[0] == 0:
        print(f"Number {participant_number} accepted!")
        break
    else:
        print(f"Someone beat you to number {participant_number}!")        

with open(f'{directoryname}\Participant Statistics.csv', 'a+') as file:
                      file.write("Trial Type" + ',' + "Score")

if jcount > 0:

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    pygame.event.get()
    joysticktimer = pygame.time.get_ticks()

with open(f'{directoryname}\Calibration Score.csv', 'a+') as file:
                      file.write(',' + 'Average')
                      file.write('\n')

with open(f'{directoryname}\Reaction Time.csv', 'a+') as file:
    file.write(',' + "Type" + ',' + "Reaction Time")
    file.write('\n')

def Total_Score():
    import pandas as pd
    scoredf = pd.read_csv(f'{directoryname}\Participant Statistics.csv')
    totalscore = scoredf['Score'].sum()
    print ('Total Score:', + totalscore)
    with open(f'{directoryname}\Participant Scores.csv', 'a+') as file:
                  file.write('\n')
                  file.write('\n')
                  file.write("Total Score" + ',' + str(totalscore))

def Stats_CSV():
    statsdf = pd.read_csv(f'{directoryname}\Participant Statistics.csv')
    Score_Mean = statsdf['Score'].sum()
    Breakdown_Score = statsdf.groupby(['Trial Type']).sum()

    with open('Outputs/Statistical Analyses.csv', 'a+') as file:
                      file.write("Combined Score" + ',' + str(Score_Mean))
                      file.write('\n')
                      file.write('\n')
                      file.write("Trial Scores" + ',' + str(Breakdown_Score))

def Trial_Analyses():
        trialdf = pd.read_csv(f'{directoryname}\Participant Statistics.csv')
        trialdf.groupby("Trial Type")['Score'].describe()
        LC = trialdf[(trialdf['Trial Type'] == 'Low Conflict Trial')]
        GC = trialdf[(trialdf['Trial Type'] == 'High Conflict Trial')]
        Calibration_Analysis = trialdf[(trialdf['Trial Type'] == 'Calibration Trial')]

        ttest = stats.ttest_ind(GC['Score'], LC['Score']).pvalue
        ttest2 = stats.ttest_ind(GC['Score'], Calibration_Analysis['Score']).pvalue
        ttest3 = stats.ttest_ind(Calibration_Analysis['Score'], LC['Score']).pvalue

        with open('Outputs/Statistical Analyses.csv', 'a+') as file:
            file.write('\n')
            file.write("Goal Conflict - Low Conflict" + ',' + str(ttest))
            file.write('\n')
            file.write("Goal Conflict - Calibration" + ',' + str(ttest2))
            file.write('\n')
            file.write("Low Conflict - Calibration" + ',' + str(ttest3))

def GC():
      sql_type = "GC"
      os.environ['SDL_VIDEO_CENTERED'] = '1'
      pygame.init()
      SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
      pygame.joystick.init
      pygame.init()
      pygame.font.init

      cursor = connection.cursor()


      size = [SCREEN_WIDTH,SCREEN_HEIGHT-50]

      BLACK = (0, 0, 0)
      WHITE = (255, 255, 255)
      GREEN = (0, 255, 0)
      RED = (255, 0, 0)
      screen = pygame.display.set_mode(size, pygame.RESIZABLE)

      pygame.display.set_caption("Task")
      done = False

      clock = pygame.time.Clock()

      rect_x = 50
      rect_y = 50

      rect_change_x = 5
      rect_change_y = 5

      pygame.font.init
      font = pygame.font.Font(None, 32)

      pygame.display.flip()
      screen.fill(BLACK)
      pygame.draw.rect(screen, RED, [rect_x, rect_y, 50, 50])
      rect_x += rect_change_x
      rect_y += rect_change_y

      FPS = 60
      FramePerSec = pygame.time.Clock()

      global GC_SPEED

      SPEED = GC_SPEED*.93

      COLLISION_SCORE = 0

      font = pygame.font.SysFont("Verdana", 40)
      font_small = pygame.font.SysFont("Verdana", 20)

      background = pygame.image.load("Stimuli/trial.jpeg")

      pygame.time.wait(1000)

      timer = pygame.time.get_ticks()
      timer2 = timer + 3000

      DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
      DISPLAYSURF.fill(WHITE)
      pygame.display.set_caption("Open Day Task")
      pygame.mixer.init()
      SCORE = 0

      class Enemy(pygame.sprite.Sprite):
            def __init__(self):
              super().__init__()
              self.image = pygame.image.load("Stimuli/snake.png")
              self.rect = self.image.get_rect()

              speedcalc = random.randint(1,3)
              if speedcalc == 1:
                  gcspeed = 0
              if speedcalc == 2:
                  gcspeed = 15
              if speedcalc == 3:
                  gcspeed = 25

              self.rect.center = ((SCREEN_WIDTH/2), 0)
            def move(self):
              global SCORE
              self.rect.move_ip(0,SPEED)
              if (self.rect.bottom > SCREEN_HEIGHT-10):
                  SCORE += 1
                  self.rect.top = 0
                  self.rect.center = ((SCREEN_WIDTH/2), -SCREEN_HEIGHT)
              global COLLISION_SCORE

      class Enemy2(pygame.sprite.Sprite):
            def __init__(self):
              super().__init__()
              self.image = pygame.image.load("Stimuli/spider.png")
              self.rect = self.image.get_rect()
              self.rect.center = ((SCREEN_WIDTH/2), 0)
            def move(self):
              global SCORE
              self.rect.move_ip(0,(-SPEED*0.4))
              SCORE = 0
              if (self.rect.top < 10):
                  SCORE += 1
                  self.rect.top = 0
                  self.rect.center = ((SCREEN_WIDTH/2), SCREEN_HEIGHT)
              global COLLISION_SCORE

      class Player(pygame.sprite.Sprite):
          def __init__(self):

              super().__init__()

              width = 10
              height = 15
              self.image = pygame.image.load("Stimuli/silhouette.png")
              self.rect = self.image.get_rect()

              # Set initial position of silhouette
              self.rect.x = SCREEN_WIDTH/2-80
              self.rect.y = SCREEN_HEIGHT/2

              # joystick count
              self.joystick_count = pygame.joystick.get_count()
              if self.joystick_count == 0:
                  # No joysticks!
                  print("Check joystick connection")
              else:
                  # Use joystick #0 and initialize it
                  self.my_joystick = pygame.joystick.Joystick(0)
                  self.my_joystick.init()

          def move(self):
            # Check if joystick is connected
            if self.joystick_count != 0:
                # Joystick input
                horiz_axis_pos = self.my_joystick.get_axis(0)
                vert_axis_pos = self.my_joystick.get_axis(1)
                self.rect.x += int(horiz_axis_pos * buttonspeed)
                self.rect.y += int(vert_axis_pos * buttonspeed)

            else:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_UP]:
                    self.rect.y -= buttonspeed
                if keys[pygame.K_DOWN]:
                    self.rect.y += buttonspeed

      #Setting up Sprites
      P1 = Player()
      E1 = Enemy()
      E2 = Enemy2()

      #Creating Sprite Groups
      enemies = pygame.sprite.Group()
      enemies.add(E1)
      enemies.add(E2)
      all_sprites = pygame.sprite.Group()
      all_sprites.add(P1)
      all_sprites.add(E1)
      all_sprites.add(E2)

      #Adding a new User event (speed up)
      INC_SPEED = pygame.USEREVENT + 1
      pygame.time.set_timer(INC_SPEED, 1000)

      for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

      COLLISION_SCORE2 = COLLISION_SCORE/20
      Game_Running = True
      starterRT = time.time()
      counter = 0
      clock = pygame.time.Clock()

      while Game_Running:
          
                pygame.init()
                keys = pygame.key.get_pressed()

                for event in pygame.event.get():

                    if event.type == QUIT:
                        pygame.display.quit()

                pygame.event.pump()

                if jcount > 0:

                    joystick = pygame.joystick.Joystick(0)

                    yaxis = joystick.get_axis(1)

                    while yaxis > 0.2 or yaxis < -0.2:
                        finishedRT = time.time()
                        ReactionTime = finishedRT - starterRT
                        counter = counter + 1
                        break

                    if counter == 2:
                        data = {'Type':['GC Trial'], 'Reaction Time': [ReactionTime]}
                        Reactiondf = pd.DataFrame(data)
                        with open('Outputs/Calibration Score.csv', 'a+') as file:
                          file.write('\n')
                          file.write("GC" + ',' + str(yaxis))
                        Reactiondf.to_csv('Outputs/Reaction Time.csv', mode='a', header=False)
                

                pygame.event.pump()
                DISPLAYSURF.blit(background, (0,0))
                scores = font_small.render(str(SCORE), True, WHITE)
                DISPLAYSURF.blit(scores, (10,10))
                cscores = font_small.render(str(COLLISION_SCORE2), True, WHITE)
                DISPLAYSURF.blit(cscores, (SCREEN_WIDTH-60, 10))

                for entity in all_sprites:
                    entity.move()
                    DISPLAYSURF.blit(entity.image, entity.rect)

                if pygame.sprite.spritecollideany(P1, enemies):
                    COLLISION_SCORE = 1

                timer = pygame.time.get_ticks()
                if timer > timer2:
                    pygame.init()

                    for entity in all_sprites:
                            entity.kill()
                    DISPLAYSURF.blit(background, (0,0))
                    pygame.display.update()

                    if COLLISION_SCORE == 1:
                       negativefeedback = pygame.image.load("Stimuli/redcross.png")
                       negrect = negativefeedback.get_rect(center = screen.get_rect().center)
                       DISPLAYSURF.blit(negativefeedback, negrect)

                    else:
                       positivefeedback = pygame.image.load("Stimuli/greentick.png")
                       posrect = positivefeedback.get_rect(center = screen.get_rect().center)
                       DISPLAYSURF.blit(positivefeedback, posrect)

                    pygame.time.wait(1000)
                    pygame.display.update()

                    with open(f'{directoryname}\Participant Statistics.csv', 'a+') as file:
                      file.write('\n')
                      file.write("High Conflict Trial" + ',' + str(COLLISION_SCORE))

                    Game_Running = False

                    if COLLISION_SCORE == 0:
                        sqlscore = 1

                    if COLLISION_SCORE == 1:
                        sqlscore = 0

                    trial = "High"

                    try:
                        with connection.cursor() as cursor:
                            sql = "INSERT INTO OED (score, participant_no, trial) VALUES (%s, %s, %s)"
                            cursor.execute(sql, (sqlscore, participant_number, trial))
                        connection.commit()
                        print("GC Send complete")
                    except Exception as e:
                        print(f"Error: {e}")
                        connection.rollback()

                    pygame.display.flip()
                    pygame.time.wait(1000)

                pygame.display.update()
                FramePerSec.tick(FPS)

def LC():
      sql_type = "LC"
      global GC_SPEED
      os.environ['SDL_VIDEO_CENTERED'] = '1'
      pygame.init()
      SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
      pygame.joystick.init

      pygame.init()

      pygame.font.init

      size = [SCREEN_WIDTH,SCREEN_HEIGHT-50]
      BLACK = (0, 0, 0)
      WHITE = (255, 255, 255)
      GREEN = (0, 255, 0)
      RED = (255, 0, 0)
      screen = pygame.display.set_mode(size, pygame.RESIZABLE)


      pygame.display.set_caption("Task")

      done = False

      clock = pygame.time.Clock()

      rect_x = 50
      rect_y = 50

      rect_change_x = 5
      rect_change_y = 5
      pygame.font.init
      font = pygame.font.Font(None, 32)

      pygame.display.flip()
      screen.fill(BLACK)
      pygame.draw.rect(screen, RED, [rect_x, rect_y, 50, 50])

      rect_x += rect_change_x
      rect_y += rect_change_y

      FPS = 60
      FramePerSec = pygame.time.Clock()

      global GC_SPEED
      SPEED = GC_SPEED * 0.5
      if SPEED < 1:
        SPEED = 1.11

      COLLISION_SCORE = 0

      font = pygame.font.SysFont("Verdana", 40)
      font_small = pygame.font.SysFont("Verdana", 20)

      background = pygame.image.load("Stimuli/trial.jpeg")

      pygame.time.wait(1000)

      timer = pygame.time.get_ticks()
      timer2 = timer + 3000

      DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
      DISPLAYSURF.fill(WHITE)
      pygame.display.set_caption("EEG Task")
      pygame.mixer.init()
      SCORE = 0
      class Enemy(pygame.sprite.Sprite):
            def __init__(self):
              super().__init__()
              self.image = pygame.image.load("Stimuli/reddot.png")
              self.rect = self.image.get_rect()

              speedcalc = random.randint(1,3)
              if speedcalc == 1:
                  gcspeed = 0
              if speedcalc == 2:
                  gcspeed = 15
              if speedcalc == 3:
                  gcspeed = 25

              self.rect.center = ((SCREEN_WIDTH/2), 0)
            def move(self):
              global SCORE
              self.rect.move_ip(0,SPEED)
              if (self.rect.bottom > SCREEN_HEIGHT-10):
                  SCORE += 1
                  self.rect.top = 0
                  self.rect.center = ((SCREEN_WIDTH/2), -SCREEN_HEIGHT)
              global COLLISION_SCORE

      class Enemy2(pygame.sprite.Sprite):
            def __init__(self):
              super().__init__()
              self.image = pygame.image.load("Stimuli/reddot.png")
              self.rect = self.image.get_rect()
              self.rect.center = ((SCREEN_WIDTH/2), 0)
            def move(self):
              global SCORE
              self.rect.move_ip(0,((-SPEED)-0.4))
              SCORE = 0
              if (self.rect.top < 10):
                  SCORE += 1
                  self.rect.top = 0
                  self.rect.center = ((SCREEN_WIDTH/2), SCREEN_HEIGHT)
              global COLLISION_SCORE

      class Player(pygame.sprite.Sprite):
          def __init__(self):

              super().__init__()

              width = 10
              height = 15

              self.image = pygame.image.load("Stimuli/silhouette.png")

              self.rect = self.image.get_rect()

              self.rect.x = SCREEN_WIDTH/2-80
              self.rect.y = SCREEN_HEIGHT/2.5

              self.joystick_count = pygame.joystick.get_count()

              if self.joystick_count == 0:
                  print("No joystick mode")
              else:
                  self.my_joystick = pygame.joystick.Joystick(0)
                  self.my_joystick.init()

          def move(self):
                if self.joystick_count != 0:
                    horiz_axis_pos = self.my_joystick.get_axis(0)
                    vert_axis_pos = self.my_joystick.get_axis(1)

                    self.rect.x += int(horiz_axis_pos * buttonspeed)
                    self.rect.y += int(vert_axis_pos * buttonspeed)

                else:

                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_UP]:
                        self.rect.y -= buttonspeed
                    if keys[pygame.K_DOWN]:
                        self.rect.y += buttonspeed

      P1 = Player()
      E1 = Enemy()
      E2 = Enemy2()

      enemies = pygame.sprite.Group()
      enemies.add(E1)
      enemies.add(E2)
      all_sprites = pygame.sprite.Group()
      all_sprites.add(P1)
      all_sprites.add(E1)
      all_sprites.add(E2)

      INC_SPEED = pygame.USEREVENT + 1
      pygame.time.set_timer(INC_SPEED, 1000)

      COLLISION_SCORE2 = COLLISION_SCORE/20

      starterRT = time.time()
      counter = 0

      Game_Running = True
      while Game_Running:

                pygame.init()
                keys = pygame.key.get_pressed()

                pygame.joystick.init()

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.display.quit()

                pygame.event.pump()

                if jcount > 0:

                    joystick = pygame.joystick.Joystick(0)

                    yaxis = joystick.get_axis(1)

                    while yaxis > 0.2 or yaxis < -0.2:
                        finishedRT = time.time()
                        ReactionTime = finishedRT - starterRT
                        counter = counter + 1
                        sql_rt(sql_type, ReactionTime)
                        break

                    if counter == 2:

                        data = {'Type':['LC Trial'], 'Reaction Time': [ReactionTime]}
                        Reactiondf = pd.DataFrame(data)
                        with open('Outputs/Calibration Score.csv', 'a+') as file:
                          file.write('\n')
                          file.write("LC" + ',' + str(yaxis))
                        Reactiondf.to_csv('Outputs/Reaction Time.csv', mode='a', header=False)


                pygame.event.pump()

                DISPLAYSURF.blit(background, (0,0))
                scores = font_small.render(str(SCORE), True, WHITE)
                DISPLAYSURF.blit(scores, (10,10))
                cscores = font_small.render(str(COLLISION_SCORE2), True, WHITE)
                DISPLAYSURF.blit(cscores, (SCREEN_WIDTH-60, 10))

                for entity in all_sprites:
                    entity.move()
                    DISPLAYSURF.blit(entity.image, entity.rect)

                if pygame.sprite.spritecollideany(P1, enemies):
                    COLLISION_SCORE = 1

                timer = pygame.time.get_ticks()
                if timer > timer2:
                    pygame.init()
                    ##for line inrange(5,6):
                        ##dev.activate_line(lines = line)

                    #pygame.display.quit()
                    for entity in all_sprites:
                            entity.kill()

                    DISPLAYSURF.blit(background, (0,0))
                    pygame.display.update()
                    if COLLISION_SCORE == 1:

                       negativefeedback = pygame.image.load("Stimuli/redcross.png")
                       negrect = negativefeedback.get_rect(center = screen.get_rect().center)
                       DISPLAYSURF.blit(negativefeedback, negrect)
                    else:

                       positivefeedback = pygame.image.load("Stimuli/greentick.png")
                       posrect = positivefeedback.get_rect(center = screen.get_rect().center)
                       DISPLAYSURF.blit(positivefeedback, posrect)

                    pygame.time.wait(1000)
                    pygame.display.update()

                    with open(f'{directoryname}\Participant Statistics.csv', 'a+') as file:
                      file.write('\n')
                      file.write("Low Conflict Trial" + ',' + str(COLLISION_SCORE))

                    Game_Running = False

                    if COLLISION_SCORE == 0:
                        sqlscore = 1


                    if COLLISION_SCORE == 1:
                        sqlscore = 0

                    trial = "Low"

                    try:
                        with connection.cursor() as cursor:
                            sql = "INSERT INTO OED (score, participant_no, trial) VALUES (%s, %s, %s)"
                            cursor.execute(sql, (sqlscore, participant_number, trial))
                        connection.commit()
                        print("LC Send complete")
                    except Exception as e:
                        print(f"Error: {e}")
                        connection.rollback()

                    pygame.display.flip()
                    pygame.time.wait(1000)

                pygame.display.update()
                FramePerSec.tick(FPS)

def analysis():
    def analyse():

            with connection.cursor() as cursor:
                sql_query = """
                    SELECT *  # Fetch all columns
                    FROM OED 
                    WHERE participant_no = %s AND trial IN ('High', 'Low')
                """
                
                cursor.execute(sql_query, (participant_number,))
                
                results = cursor.fetchall()
                global l_count
                global h_count
                global high_percentage
                global low_percentage
                        
                high_score = 0
                low_score = 0
                h_count = 0
                l_count = 0
                high_trial_count = 0
                low_trial_count = 0
                
                if results:
                    for row in results:
                        trial = row[3]
                        score = row[2]
                        
                        if trial == 'High':
                            high_score = score
                            if score == 1:
                                h_count += 1
                            high_trial_count += 1
                            print(f'High: {score}')
                        elif trial == 'Low':
                            low_score = score
                            if score == 1:
                                l_count += 1
                            low_trial_count += 1
                            print(f'Low: {score}')

                low_percentage = (100 * l_count / low_trial_count) 
                high_percentage = (100 * h_count / high_trial_count) 
                
                low_percentage = round(low_percentage, 2)
                high_percentage = round(high_percentage, 2)

    analyse()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    pygame.joystick.init()

    pygame.font.init()
    SCORE = 0

    size = [SCREEN_WIDTH, SCREEN_HEIGHT - 50]
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    pygame.display.set_caption("Task")

    done = False
    clock = pygame.time.Clock()

    checkbox_checked = False
    checkbox_rect = pygame.Rect((SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT - 100), (30, 30))

    font = pygame.font.SysFont("Verdana", 40)
    font_small = pygame.font.SysFont("Verdana", 20)

    background = pygame.image.load("Stimuli/trial.jpeg")

    pygame.time.wait(1000)

    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption("EEG Task")
    pygame.mixer.init()


    global executed
    executed = False

    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if checkbox_rect.collidepoint(event.pos):
                    checkbox_checked = not checkbox_checked
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True

        screen.blit(background, (0, 0))
        global false_count

        prompt_text = "You have completed the task! Your results are as follows:"

        left_arrow_text = f"Easy trials: {l_count} ({low_percentage}%)"

        right_arrow_text = f"Hard trials: {h_count} ({high_percentage}%)"


        prompt_surface = font.render(prompt_text, True, BLACK)
        prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        screen.blit(prompt_surface, prompt_rect)

        left_arrow_surface = font.render(left_arrow_text, True, BLACK)
        left_arrow_rect = left_arrow_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(left_arrow_surface, left_arrow_rect)

        right_arrow_surface = font.render(right_arrow_text, True, BLACK)
        right_arrow_rect = right_arrow_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        screen.blit(right_arrow_surface, right_arrow_rect)

        pygame.draw.rect(screen, BLACK, checkbox_rect, 2)

        if checkbox_checked:
            pygame.draw.rect(screen, GREEN, (checkbox_rect.x + 2, checkbox_rect.y + 2, 26, 26))
            global ready
            pygame.quit()
            complete()
            sys.exit()


        ready_text = font_small.render("Exit:", True, BLACK)
        screen.blit(ready_text, (checkbox_rect.x - ready_text.get_width() - 10, checkbox_rect.y))

        scores = font_small.render(str(SCORE), True, WHITE)
        screen.blit(scores, (10, 10))

        pygame.display.flip()
        clock.tick(60)


def CB():
      sql_type = "CB"
      os.environ['SDL_VIDEO_CENTERED'] = '1'
      pygame.init()
      SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
      pygame.joystick.init


      pygame.init()

      pygame.font.init

      size = [SCREEN_WIDTH,SCREEN_HEIGHT-50]
      #SCREEN_WIDTH = 1000
      #SCREEN_HEIGHT = 1000
      BLACK = (0, 0, 0)
      WHITE = (255, 255, 255)
      GREEN = (0, 255, 0)
      RED = (255, 0, 0)
      screen = pygame.display.set_mode(size, pygame.RESIZABLE)

      pygame.display.set_caption("Task")

      done = False

      clock = pygame.time.Clock()

      rect_x = 50
      rect_y = 50

      rect_change_x = 5
      rect_change_y = 5

      pygame.font.init
      font = pygame.font.Font(None, 48)

      pygame.display.flip()
      screen.fill(BLACK)

      pygame.draw.rect(screen, RED, [rect_x, rect_y, 50, 50])

      rect_x += rect_change_x
      rect_y += rect_change_y

      FPS = 160
      FramePerSec = pygame.time.Clock()

      #SCREEN_WIDTH = 1000
      #SCREEN_HEIGHT = 1000

      global GC_SPEED
      SPEED = GC_SPEED-0.25
      #SCORE = 0
      COLLISION_SCORE = 0

      font = pygame.font.SysFont("Verdana", 40)
      font_small = pygame.font.SysFont("Verdana", 20)

      background = pygame.image.load("Stimuli/trial.jpeg")

      pygame.time.wait(1000)

      timer = pygame.time.get_ticks()
      timer2 = timer + 3000

      DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
      DISPLAYSURF.fill(WHITE)
      pygame.display.set_caption("EEG Task")
      pygame.mixer.init()
      global SCORE
      SCORE = 0
      class Enemy(pygame.sprite.Sprite):
            def __init__(self):
              super().__init__()
              self.image = pygame.image.load("Stimuli/reddot.png")
              self.rect = self.image.get_rect()
              self.rect.center = ((SCREEN_WIDTH/2), 0)

            def move(self):
              global SCORE
              self.rect.move_ip(0,SPEED)
              if (self.rect.bottom > SCREEN_HEIGHT-10):
                  SCORE += 1
                  #pygame.mixer.Sound("Stimuli/spawn.wav").play()
                  self.rect.move_ip(0,-SPEED)
                  self.rect.top = 0
                  self.rect.center = ((SCREEN_WIDTH/2), -SCREEN_HEIGHT)
              global COLLISION_SCORE

      class Player(pygame.sprite.Sprite):
          def __init__(self):

              super().__init__()

              # Variables to hold the height and width of the block
              width = 10
              height = 15

              # silhouette image
              self.image = pygame.image.load("Stimuli/silhouette.png")


              # Fetch the rectangle object that has the dimensions of the image
              self.rect = self.image.get_rect()

              # Set initial position of silhouette
              self.rect.x = SCREEN_WIDTH/2-80
              self.rect.y = SCREEN_HEIGHT/2-80

              # joystick count
              self.joystick_count = pygame.joystick.get_count()
              if self.joystick_count == 0:
                  # No joysticks!
                  print("Check joystick connection")
              else:
                  # Use joystick #0 and initialize it
                  self.my_joystick = pygame.joystick.Joystick(0)
                  self.my_joystick.init()

          def move(self):
            if self.joystick_count != 0:
                horiz_axis_pos = self.my_joystick.get_axis(0)
                vert_axis_pos = self.my_joystick.get_axis(1)

                self.rect.x += int(horiz_axis_pos * buttonspeed)
                self.rect.y += int(vert_axis_pos * buttonspeed)
                
            else:

                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    self.rect.y -= buttonspeed
                if keys[pygame.K_DOWN]:
                    self.rect.y += buttonspeed

      P1 = Player()
      E1 = Enemy()

      enemies = pygame.sprite.Group()
      enemies.add(E1)
      #enemies.add(E2)
      all_sprites = pygame.sprite.Group()
      all_sprites.add(P1)
      all_sprites.add(E1)

      INC_SPEED = pygame.USEREVENT + 1
      pygame.time.set_timer(INC_SPEED, 1000)

      #Game Loop
      #for line inrange(1,2):
                   #dev.activate_line(lines = line)
      COLLISION_SCORE2 = COLLISION_SCORE/20
      if jcount > 0:

          joystick = pygame.joystick.Joystick(0)

      starterRT = time.time()
      counter = 0

      Game_Running = True
      while Game_Running:
                keys = pygame.key.get_pressed()


                if jcount > 0:

                    pygame.joystick.init()
                    joystick = pygame.joystick.Joystick(0)
                    yaxis = joystick.get_axis(1)

                for event in pygame.event.get():

                    if event.type == QUIT:
                        pygame.display.quit()

                pygame.event.pump()

                if jcount > 0:

                    yaxis = joystick.get_axis(1)

                    while yaxis > 0.2 or yaxis < -0.2:
                        finishedRT = time.time()
                        ReactionTime = finishedRT - starterRT
                        counter = counter + 1
                        sql_rt(sql_type, ReactionTime)
                        break

                    if counter == 2:

                        data = {'Type':['Calibration Trial'], 'Reaction Time': [ReactionTime]}
                        Reactiondf = pd.DataFrame(data)
                        Reactiondf.to_csv('Outputs/Reaction Time.csv', mode='a', header=False)

                        with open('Outputs/Calibration Score.csv', 'a+') as file:
                          file.write('\n')
                          file.write("Calibration" + ',' + str(yaxis))


                pygame.event.pump()
                DISPLAYSURF.blit(background, (0,0))
                scores = font_small.render(str(SCORE), True, WHITE)
                DISPLAYSURF.blit(scores, (10,10))

                #COLLISION_SCORE2 = COLLISION_SCORE/20

                cscores = font_small.render(str(COLLISION_SCORE2), True, WHITE)
                DISPLAYSURF.blit(cscores, (SCREEN_WIDTH-60, 10))

                #Moves and Re-draws all Sprites
                for entity in all_sprites:
                    entity.move()
                    DISPLAYSURF.blit(entity.image, entity.rect)

                #To be run if collision happens
                if pygame.sprite.spritecollideany(P1, enemies):
                   #pygame.mixer.Sound("Stimuli/scream.wav").play()
                   COLLISION_SCORE = 1

                timer = pygame.time.get_ticks()
                if timer > timer2:
                    if jcount > 0:
                        axis2 = joystick.get_axis(1)


                    pygame.init()
                    ##for line inrange(1,2):
                            ##dev.activate_line(lines = line)

                    #pygame.display.quit()
                    for entity in all_sprites:
                            entity.kill()

                    DISPLAYSURF.blit(background, (0,0))
                    pygame.display.update()

                    if COLLISION_SCORE == 1:
                       negativefeedback = pygame.image.load("Stimuli/redcross.png")
                       negrect = negativefeedback.get_rect(center = screen.get_rect().center)
                       DISPLAYSURF.blit(negativefeedback, negrect)
                    else:
                       positivefeedback = pygame.image.load("Stimuli/greentick.png")
                       posrect = positivefeedback.get_rect(center = screen.get_rect().center)
                       DISPLAYSURF.blit(positivefeedback, posrect)

                    pygame.time.wait(1000)
                    pygame.display.update()

                    with open(f'{directoryname}\Participant Statistics.csv', 'a+') as file:
                      file.write('\n')
                      file.write("Calibration Trial" + ',' + str(COLLISION_SCORE))

                    if jcount > 0:

                        joystick = pygame.joystick.Joystick(0)
                        joystick.init()

                    Game_Running = False

                    pygame.display.flip()
                    pygame.time.wait(1000)

                pygame.display.update()
                FramePerSec.tick(FPS)

from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE

executed = False
global ready
ready = False

write_to_database()

def intro():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    pygame.joystick.init()

    pygame.font.init()
    SCORE = 0

    size = [SCREEN_WIDTH, SCREEN_HEIGHT - 50]
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    pygame.display.set_caption("Task")

    done = False
    clock = pygame.time.Clock()

    checkbox_checked = False
    checkbox_rect = pygame.Rect((SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT - 100), (30, 30))

    font = pygame.font.SysFont("Verdana", 40)
    font_small = pygame.font.SysFont("Verdana", 20)

    background = pygame.image.load("Stimuli/trial.jpeg")

    pygame.time.wait(1000)

    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption("EEG Task")
    pygame.mixer.init()

    click_to_play_text = font.render("Double click to play!", True, BLACK)
    guidance = font.render("Guidance here", True, BLACK)

    global executed
    executed = False

    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if checkbox_rect.collidepoint(event.pos):
                    checkbox_checked = not checkbox_checked
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True

        screen.blit(background, (0, 0))
        global false_count

        print(false_count)

        prompt_text = "You will see two objects and a silhouette (yourself)"
        if jcount > 0:
            left_arrow_text = "You must use the joystick (push up and down) to move away from the objects - don't let them hit you!"

        else:
            left_arrow_text = "You must use the up and down arrow keys to move away from the objects - don't let them hit you!"

        print(false_count)
            
        if false_count > 1:
            right_arrow_text = f"Waiting for {false_count+1}"

        if false_count == 1:
            right_arrow_text = f"Waiting for {false_count+1}"

        else:
            right_arrow_text = f"Waiting for {false_count+1}"

        prompt_surface = font.render(prompt_text, True, BLACK)
        prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        screen.blit(prompt_surface, prompt_rect)

        left_arrow_surface = font.render(left_arrow_text, True, BLACK)
        left_arrow_rect = left_arrow_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(left_arrow_surface, left_arrow_rect)

        right_arrow_surface = font.render(right_arrow_text, True, BLACK)
        right_arrow_rect = right_arrow_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        screen.blit(right_arrow_surface, right_arrow_rect)

        pygame.draw.rect(screen, BLACK, checkbox_rect, 2)

        if checkbox_checked:
            pygame.draw.rect(screen, GREEN, (checkbox_rect.x + 2, checkbox_rect.y + 2, 26, 26))
            global ready

            ready = True
            write_to_database()
            if false_count == 0:
                break
                connection.close()
                print(f'SQL connection closed')

        if not checkbox_checked:
            ready = False
            write_to_database()

        #connection.close()

        ready_text = font_small.render("Ready:", True, BLACK)
        screen.blit(ready_text, (checkbox_rect.x - ready_text.get_width() - 10, checkbox_rect.y))

        scores = font_small.render(str(SCORE), True, WHITE)
        screen.blit(scores, (10, 10))

        pygame.display.flip()
        clock.tick(60)


def CB_Full():
      sql_type = "CB_Full"
      os.environ['SDL_VIDEO_CENTERED'] = '1'
      pygame.init()
      SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
      pygame.joystick.init()

      pygame.font.init

      size = [SCREEN_WIDTH,SCREEN_HEIGHT-50]
      BLACK = (0, 0, 0)
      WHITE = (255, 255, 255)
      GREEN = (0, 255, 0)
      RED = (255, 0, 0)
      screen = pygame.display.set_mode(size, pygame.RESIZABLE)

      pygame.display.set_caption("Task")
      done = False

      clock = pygame.time.Clock()
      rect_x = 50
      rect_y = 50
      rect_change_x = 5
      rect_change_y = 5
      pygame.font.init
      font = pygame.font.Font(None, 32)

      pygame.display.flip()
      screen.fill(BLACK)

      pygame.draw.rect(screen, RED, [rect_x, rect_y, 50, 50])

      rect_x += rect_change_x
      rect_y += rect_change_y

      #Setting up FPS
      FPS = 60
      FramePerSec = pygame.time.Clock()
      #Other Variables for use in the program
      #SCREEN_WIDTH = 1000
      #SCREEN_HEIGHT = 1000
      global GC_SPEED
      SPEED = GC_SPEED/2
      #SCORE = 0
      COLLISION_SCORE = 0

      #Setting up Fonts
      font = pygame.font.SysFont("Verdana", 40)
      font_small = pygame.font.SysFont("Verdana", 20)

      background = pygame.image.load("Stimuli/trial.jpeg")

      #delay after the instruction screen
      pygame.time.wait(1000)

      timer = pygame.time.get_ticks()
      timer2 = timer + 4000

      #TASK GAME WINDOW SIZE
      DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
      DISPLAYSURF.fill(WHITE)
      pygame.display.set_caption("EEG Task")
      pygame.mixer.init()
      SCORE = 0

      class Enemy(pygame.sprite.Sprite):
            def __init__(self):
              super().__init__()
              self.image = pygame.image.load("Stimuli/reddot.png")
              self.rect = self.image.get_rect()
              self.rect.center = ((SCREEN_WIDTH/2), 0)
            def move(self):
              global SCORE
              self.rect.move_ip(0,SPEED)
              if (self.rect.bottom > SCREEN_HEIGHT-10):
                  self.rect.move_ip(0,-SPEED)
                  #pygame.mixer.Sound("Stimuli/spawn.wav").play()
                  self.rect.top = 0
                  self.rect.center = ((SCREEN_WIDTH/2), -SCREEN_HEIGHT)
              global COLLISION_SCORE
              #print ("Red Dot Dimensions:" , self.rect)

      class Enemy2(pygame.sprite.Sprite):
            def __init__(self):
              super().__init__()
              self.image = pygame.image.load("Stimuli/reddot.png")
              self.rect = self.image.get_rect()
              self.rect.center = ((SCREEN_WIDTH/2), 0)
            def move(self):
              global SCORE
              self.rect.move_ip(0,(-SPEED*0.9))
              SCORE = 0
              if (self.rect.top < 10):
                  SCORE += 1
                  self.rect.top = 0
                  self.rect.center = ((SCREEN_WIDTH/2), SCREEN_HEIGHT)
              global COLLISION_SCORE

      class Player(pygame.sprite.Sprite):
        def __init__(self):

              super().__init__()
              width = 10
              height = 15

              self.image = pygame.image.load("Stimuli/silhouette.png")
              self.rect = self.image.get_rect()

              self.rect.x = SCREEN_WIDTH/2-80
              self.rect.y = SCREEN_HEIGHT/2

              self.joystick_count = pygame.joystick.get_count()
              if self.joystick_count == 0:
                  print("Check the joystick connection")
              else:
                  self.my_joystick = pygame.joystick.Joystick(0)
                  self.my_joystick.init()

        def move(self):
                if self.joystick_count != 0:
                    horiz_axis_pos = self.my_joystick.get_axis(0)
                    vert_axis_pos = self.my_joystick.get_axis(1)

                    self.rect.x += int(horiz_axis_pos * buttonspeed)
                    self.rect.y += int(vert_axis_pos * buttonspeed)

                else:

                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_UP]:
                        self.rect.y -= buttonspeed
                    if keys[pygame.K_DOWN]:
                        self.rect.y += buttonspeed

      P1 = Player()
      E1 = Enemy()
      E2 = Enemy2()

      enemies = pygame.sprite.Group()
      enemies.add(E1)
      enemies.add(E2)
      all_sprites = pygame.sprite.Group()
      all_sprites.add(P1)
      all_sprites.add(E1)
      all_sprites.add(E2)

      INC_SPEED = pygame.USEREVENT + 1
      pygame.time.set_timer(INC_SPEED, 1000)

      #for line inrange(3,4):
        #dev.activate_line(lines = line)

      COLLISION_SCORE2 = COLLISION_SCORE/20
      startRT = time.time()

      starterRT = time.time()
      counter = 0
      pygame.joystick.init()

      Game_Running = True
      
      while Game_Running:
                keys = pygame.key.get_pressed()
                pygame.event.pump()

                if jcount > 0:

                    joystick = pygame.joystick.Joystick(0)

                    yaxis = joystick.get_axis(1)

                    while yaxis > 0.2 or yaxis < -0.2:
                        finishedRT = time.time()
                        ReactionTime = finishedRT - starterRT
                        print(ReactionTime)
                        counter = counter + 1
                        sql_rt(sql_type, ReactionTime)
                        break

                    if counter == 2:

                        data = {'Type':['Calibration Trial'], 'Reaction Time': [ReactionTime]}
                        Reactiondf = pd.DataFrame(data)
                        with open('Outputs/Calibration Score.csv', 'a+') as file:
                          file.write('\n')
                          file.write("Calibration (2 Stim)" + ',' + str(yaxis))
                        Reactiondf.to_csv('Outputs/Reaction Time.csv', mode='a', header=False)


                startRT = time.time()
                for event in pygame.event.get():

                    if event.type == QUIT:
                        pygame.display.quit()

                DISPLAYSURF.blit(background, (0,0))
                scores = font_small.render(str(SCORE), True, WHITE)
                DISPLAYSURF.blit(scores, (10,10))

                cscores = font_small.render(str(COLLISION_SCORE2), True, WHITE)
                DISPLAYSURF.blit(cscores, (SCREEN_WIDTH-60, 10))

                #Moves and Re-draws all Sprites
                for entity in all_sprites:
                    entity.move()
                    DISPLAYSURF.blit(entity.image, entity.rect)

                #To be run if collision happens
                if pygame.sprite.spritecollideany(P1, enemies):
                   ##pygame.mixer.Sound("Stimuli/scream.wav").play()
                   COLLISION_SCORE == 1

                timer = pygame.time.get_ticks()
                if timer > timer2:
                    pygame.init()

                    ##for line inrange(3,4):
                            ##dev.activate_line(lines = line)

                    for entity in all_sprites:
                            entity.kill()
                    DISPLAYSURF.blit(background, (0,0))
                    pygame.display.update()

                    if COLLISION_SCORE == 1:
                       negativefeedback = pygame.image.load("Stimuli/redcross.png")
                       negrect = negativefeedback.get_rect(center = screen.get_rect().center)
                       DISPLAYSURF.blit(negativefeedback, negrect)
                    else:
                       positivefeedback = pygame.image.load("Stimuli/greentick.png")
                       posrect = positivefeedback.get_rect(center = screen.get_rect().center)
                       DISPLAYSURF.blit(positivefeedback, posrect)

                    pygame.time.wait(1000)
                    pygame.display.update()

                    with open(f'{directoryname}\Participant Statistics.csv', 'a+') as file:
                      file.write('\n')
                      file.write("Calibration Trial (2 Stim)" + ',' + str(COLLISION_SCORE))

                    if jcount > 0:

                        joystick = pygame.joystick.Joystick(0)
                        joystick.init()

                    Game_Running = False

                    pygame.display.flip()
                    pygame.time.wait(1000)

                pygame.display.update()
                FramePerSec.tick(FPS)

def CB_last():
      sql_type = "CB_last"
      os.environ['SDL_VIDEO_CENTERED'] = '1'
      pygame.init()
      SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
      pygame.joystick.init

      pygame.init()

      pygame.font.init

      size = [SCREEN_WIDTH,SCREEN_HEIGHT-50]
      #SCREEN_WIDTH = 1000
      #SCREEN_HEIGHT = 1000
      BLACK = (0, 0, 0)
      WHITE = (255, 255, 255)
      GREEN = (0, 255, 0)
      RED = (255, 0, 0)
      screen = pygame.display.set_mode(size, pygame.RESIZABLE)

      pygame.display.set_caption("Task")

      # Loop until the user clicks the close button.
      done = False

      clock = pygame.time.Clock()

      # Starting position of the silhouette
      rect_x = 50
      rect_y = 50

      # Speed and direction of rectangle
      rect_change_x = 5
      rect_change_y = 5

      # font
      pygame.font.init
      font = pygame.font.Font(None, 32)

      pygame.display.flip()
      screen.fill(BLACK)

      # Draw the rectangle
      pygame.draw.rect(screen, RED, [rect_x, rect_y, 50, 50])

      # Move the rectangle starting point
      rect_x += rect_change_x
      rect_y += rect_change_y

      #Setting up FPS
      FPS = 160
      FramePerSec = pygame.time.Clock()
      global GC_SPEED
      SPEED = GC_SPEED-0.25
      #SCORE = 0
      COLLISION_SCORE = 0

      #Setting up Fonts
      font = pygame.font.SysFont("Verdana", 40)
      font_small = pygame.font.SysFont("Verdana", 20)

      background = pygame.image.load("Stimuli/trial.jpeg")

      #delay after the instruction screen
      pygame.time.wait(1000)

      timer = pygame.time.get_ticks()
      timer2 = timer + 3000

      #TASK GAME WINDOW SIZE
      DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
      DISPLAYSURF.fill(WHITE)
      pygame.display.set_caption("EEG Task")
      pygame.mixer.init()
      global SCORE
      SCORE = 0
      class Enemy(pygame.sprite.Sprite):
            def __init__(self):
              super().__init__()
              self.image = pygame.image.load("Stimuli/reddot.png")
              self.rect = self.image.get_rect()
              self.rect.center = ((SCREEN_WIDTH/2), 0)
            def move(self):
              global SCORE
              self.rect.move_ip(0,SPEED)
              if (self.rect.bottom > SCREEN_HEIGHT-10):
                  SCORE += 1
                  self.rect.move_ip(0,-SPEED)
                  self.rect.top = 0
                  self.rect.center = ((SCREEN_WIDTH/2), -SCREEN_HEIGHT)
              global COLLISION_SCORE

      class Player(pygame.sprite.Sprite):
          def __init__(self):

              super().__init__()

              width = 10
              height = 15

              # silhouette image
              self.image = pygame.image.load("Stimuli/silhouette.png")


              # Fetch the rectangle object that has the dimensions of the image
              self.rect = self.image.get_rect()

              # Set initial position of silhouette
              self.rect.x = SCREEN_WIDTH/2-80
              self.rect.y = SCREEN_HEIGHT/2-80

              # joystick count
              self.joystick_count = pygame.joystick.get_count()
              if self.joystick_count == 0:
                  # No joysticks!
                  print("Check joystick connection")
              else:
                  # Use joystick #0 and initialize it
                  self.my_joystick = pygame.joystick.Joystick(0)
                  self.my_joystick.init()

          def move(self):
              if self.joystick_count != 0:

                  # joystick pos
                  horiz_axis_pos = self.my_joystick.get_axis(0)
                  vert_axis_pos = self.my_joystick.get_axis(1)

                  # Move x and y, * speed
                  self.rect.x = self.rect.x+int(horiz_axis_pos*int(0))
                  self.rect.y = self.rect.y+int(vert_axis_pos*int(4))

      P1 = Player()
      E1 = Enemy()


      enemies = pygame.sprite.Group()
      enemies.add(E1)
      #enemies.add(E2)
      all_sprites = pygame.sprite.Group()
      all_sprites.add(P1)
      all_sprites.add(E1)

      INC_SPEED = pygame.USEREVENT + 1
      pygame.time.set_timer(INC_SPEED, 1000)

      #Game Loop
      #for line inrange(1,2):
                   #dev.activate_line(lines = line)
      COLLISION_SCORE2 = COLLISION_SCORE/20
      if jcount > 0:
          joystick = pygame.joystick.Joystick(0)

      starterRT = time.time()
      counter = 0

      Game_Running = True
      while Game_Running:
                keys = pygame.key.get_pressed()

                if jcount > 0:

                    pygame.joystick.init()
                    joystick = pygame.joystick.Joystick(0)
                    yaxis = joystick.get_axis(1)

                for event in pygame.event.get():

                    if event.type == QUIT:
                        pygame.quit()
                        return

                pygame.event.pump()

                if jcount > 0:

                    joystick = pygame.joystick.Joystick(0)

                    yaxis = joystick.get_axis(1)

                    if yaxis > 0.2 or yaxis < -0.2:
                        finishedRT = time.time()
                        ReactionTime = finishedRT - starterRT
                        counter = counter + 1
                        sql_rt(sql_type, ReactionTime)
                        break
                    else:
                        ReactionTime = 0

                    if counter == 2:
                        data = {'Type':['Calibration Trial'], 'Reaction Time': [ReactionTime]}
                        Reactiondf = pd.DataFrame(data)
                        #print ("Counter value: " + str(counter))
                        with open('Outputs/Calibration Score.csv', 'a+') as file:
                          file.write('\n')
                          file.write("CB_Last" + ',' + str(yaxis))
                        #print (Reactiondf)
                        Reactiondf.to_csv('Outputs/Reaction Time.csv', mode='a', header=False)

                pygame.event.pump()
                DISPLAYSURF.blit(background, (0,0))
                scores = font_small.render(str(SCORE), True, WHITE)
                DISPLAYSURF.blit(scores, (10,10))

                #COLLISION_SCORE2 = COLLISION_SCORE/20

                cscores = font_small.render(str(COLLISION_SCORE2), True, WHITE)
                DISPLAYSURF.blit(cscores, (SCREEN_WIDTH-60, 10))

                #Moves and Re-draws all Sprites
                for entity in all_sprites:
                    entity.move()
                    DISPLAYSURF.blit(entity.image, entity.rect)


                #To be run if collision happens
                if pygame.sprite.spritecollideany(P1, enemies):
                   #pygame.mixer.Sound("Stimuli/scream.wav").play()
                   COLLISION_SCORE = 1

                timer = pygame.time.get_ticks()
                if timer > timer2:

                    pygame.init()
                    ##for line inrange(1,2):
                            ##dev.activate_line(lines = line)

                    #pygame.display.quit()
                    for entity in all_sprites:
                            entity.kill()
                    DISPLAYSURF.blit(background, (0,0))
                    pygame.display.update()

                    if COLLISION_SCORE == 1:
                       negativefeedback = pygame.image.load("Stimuli/redcross.png")
                       negrect = negativefeedback.get_rect(center = screen.get_rect().center)
                       DISPLAYSURF.blit(negativefeedback, negrect)
                    else:
                       positivefeedback = pygame.image.load("Stimuli/greentick.png")
                       posrect = positivefeedback.get_rect(center = screen.get_rect().center)
                       DISPLAYSURF.blit(positivefeedback, posrect)

                    pygame.time.wait(1000)
                    pygame.display.update()

                    with open(f'{directoryname}\Participant Statistics.csv', 'a+') as file:
                      file.write('\n')
                      file.write("Calibration Trial" + ',' + str(COLLISION_SCORE))

                    joystick = pygame.joystick.Joystick(0)
                    joystick.init()

                    Game_Running = False

                    pygame.display.update()
                    pygame.time.wait(1000)

                    cbchange = pygame.image.load("Stimuli/cbchange.png")
                    cbchangedimensions = cbchange.get_rect(center = screen.get_rect().center)
                    screen.fill(WHITE)
                    DISPLAYSURF.blit(cbchange, cbchangedimensions)

                    pygame.display.update()
                    pygame.time.wait(5000)

                    with open(f'{directoryname}\Reaction Time.csv', 'a+') as file:
                      file.write('\n')
                      file.write(',' + "Calibration Trial" + ',' + str(COLLISION_SCORE))

                    if jcount > 0:

                        joystick = pygame.joystick.Joystick(0)
                        joystick.init()

                    Game_Running = False

                    pygame.display.flip()
                    pygame.time.wait(1000)

                pygame.display.update()
                FramePerSec.tick(FPS)

def Calibration_calculator():
    import pandas as pd
    import math
    import numpy as np

    df = pd.read_csv(f'{directoryname}\Reaction Time.csv')
    CBProcessing = df['Reaction Time'].mean()
    Calibrationaverage = -CBProcessing
    caconv = (Calibrationaverage)
    logsquaredca = 10*np.exp(caconv)
    squared =(logsquaredca*logsquaredca)
    print ("Squared Value:" , squared)
    fivelogca = math.sqrt(squared)
    print ("Square Root Value:" , fivelogca)

    if fivelogca < 2:
        fivelogca = 3
    else:
        fivelogca = math.sqrt(squared)

    if fivelogca == math.isnan:
        fivelogca = buttonspeed

    if fivelogca > 10:
        fivelogca = 10
    else:
        fivelogca = math.sqrt(squared)

    global Calibration_SPEED
    Calibration_SPEED = fivelogca


    with open(f'{directoryname}\Calibration Calculation.csv', 'a+') as file:
        file.write("Calibration Average Score" + ',' + str(Calibrationaverage))
        file.write('\n')
        file.write("Calibration Conversion Score" + ',' + str(caconv))
        file.write('\n')
        file.write("Log Conversion" + ',' + str(squared))
        file.write('\n')
        file.write("Final Calibration Multiplier" + ',' + str(fivelogca))

num_operations = 40
order = [random.choice([GC, LC]) for _ in range(num_operations)]
intro()

Calibration = CB_Full()


for operation in order:
    CB_Full()
    operation()

analysis()
