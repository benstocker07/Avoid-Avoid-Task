import pygame
import sys
from pygame.locals import *
import random
import time
import sqlite3
import math
import os
import platform
import csv
from pygame.sprite import Group, Sprite, spritecollide, groupcollide
import pandas as pd
from scipy import stats
import timer
import decimal
from time import sleep
import scipy
import numpy
import tkinter as tk
import base64
import socket
import subprocess
import shutil
global sql_type
global ready
global buttonspeed
global joystick

pygame.joystick.init()

joystick_count = pygame.joystick.get_count()

if joystick_count > 0:

    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        print(f"Joystick {i}: {joystick.get_name()}")

    joystick = pygame.joystick.Joystick(0)
    print(f'\nUsing {joystick.get_name()}')

def read_joystick_direction(joystick, axis_state, threshold=0.2):
    pygame.event.pump()
    yaxis = joystick.get_axis(1)
    direction = None

    if not axis_state['held']:
        if yaxis < -threshold:
            direction = "Up"
            axis_state['held'] = True
        elif yaxis > threshold:
            direction = "Down"
            axis_state['held'] = True
    elif -threshold <= yaxis <= threshold:
        axis_state['held'] = False

    return direction


inlab = False
Test = False
stimtracker_available = True

if not inlab:
    inlab = False
    stimtracker_available = False
    Test = True

def triggers():

        try:
            global stimtracker_available
            stimtracker_available = True  

            import cdtest

        except ImportError as e:
                show_error(f"Failed to import cdtest: {e}")
                stimtracker_available = False

        except Exception as e:
                show_error(f"An error occurred while importing cdtest: {e}")
                exit()

        except FileNotFoundError as e:
                if any(x in str(e) for x in ["ftd2xx64.dll", "ftd2xx.dll", "libftd2xx.dylib"]):
                    show_error("StimTracker is not connected")
                    stimtracker_available = False

if inlab:
    triggers()

connection = sqlite3.connect('rJORT.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

deflection_buffer = []

false_count = 0

try:
        if not os.path.exists('Outputs'):
                os.makedirs('Outputs')

        if not os.path.exists('Bacukp'):
                os.makedirs('Backup')

except FileExistsError as e:
        print(e)
            
def sql_rt(participant_number, sql_type, ReactionTime, score):
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS RTs (
        pid INTEGER,
        trial_type TEXT,
        RT REAL,
        Score REAL
    );
    """)
    
    insert_sql = """
    INSERT INTO RTs (pid, trial_type, RT, Score)
    VALUES (?, ?, ?, ?);
    """
    cursor.execute(insert_sql, (participant_number, sql_type, ReactionTime, COLLISION_SCORE))
    connection.commit()   

def sql_deflection(participant_number, sql_type, direction, press_time):
    cursor = connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Deflections (
        pid INTEGER,
        trial_type TEXT,
        direction TEXT,
        time TEXT
    );
    """)
    
    sql_deflection = """
    INSERT INTO Deflections (pid, trial_type, direction, time)
    VALUES (?, ?, ?, ?);
    """
    
    cursor.execute(sql_deflection, (participant_number, sql_type, direction, press_time))
    connection.commit()

def sql_deflection_counter(participant_number, sql_type, counter):
    cursor = connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DeflectionCount (
        pid INTEGER,
        trial_type TEXT,
        deflections TEXT
    );
    """)
    
    sql_deflection_counter = """
    INSERT INTO DeflectionCount (pid, trial_type, deflections)
    VALUES (?, ?, ?);
    """
    
    cursor.execute(sql_deflection_counter, (participant_number, sql_type, counter))
    connection.commit()

def flush_deflection_buffer():
    if not deflection_buffer:
        return  
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Deflections (
        pid INTEGER,
        trial_type TEXT,
        direction TEXT,
        time TEXT
    );
    """)

    cursor.executemany("""
    INSERT INTO Deflections (pid, trial_type, direction, time)
    VALUES (?, ?, ?, ?);
    """, deflection_buffer)

    connection.commit()
    deflection_buffer.clear()

def runcount():
    filename = 'run_count.txt'
    try:
        with open(filename, 'r') as file:
            count = int(file.read().strip())
    except FileNotFoundError:
        count = 0
    except ValueError:
        count = 0

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

connection = sqlite3.connect('rJORT.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

def check_team_ready():
    cursor = connection.cursor()
    check_query = "SELECT COUNT(*) FROM Players WHERE status = 'False';"
    cursor.execute(check_query)
    count = cursor.fetchone()[0]
    TeamReady = count == 0

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
        center_text("Welcome to the task!")
        participant_number = "DEMO"
        #participant_number = input("\n\n" + " " * (os.get_terminal_size().columns // 2 - 10) + "Your Number: ")
        directoryname = f"Backup/Participant {participant_number}"
        os.makedirs(directoryname, exist_ok=True)
        break
        

with open(f'{directoryname}/Participant Statistics.csv', 'w+') as file:
                      file.write("Trial Type" + ',' + "Score")

if jcount > 0:
    pygame.joystick.init()
    joystick.init()
    pygame.event.get()
    joysticktimer = pygame.time.get_ticks()

with open(f'{directoryname}/Calibration Score.csv', 'w+') as file:
                      file.write(',' + 'Average')
                      file.write('\n')

with open(f'{directoryname}/Reaction Time.csv', 'w+') as file:
    file.write(',' + "Type" + ',' + "Reaction Time")
    file.write('\n')

def Total_Score():
    import pandas as pd
    scoredf = pd.read_csv(f'{directoryname}/Participant Statistics.csv')
    totalscore = scoredf['Score'].sum()
    print ('Total Score:', + totalscore)
    with open(f'{directoryname}/Participant Scores.csv', 'a+') as file:
                  file.write('\n')
                  file.write('\n')
                  file.write("Total Score" + ',' + str(totalscore))

def Stats_CSV():
    statsdf = pd.read_csv(f'{directoryname}/Participant Statistics.csv')
    Score_Mean = statsdf['Score'].sum()
    Breakdown_Score = statsdf.groupby(['Trial Type']).sum()

    with open('Outputs/Statistical Analyses.csv', 'a+') as file:
                      file.write("Combined Score" + ',' + str(Score_Mean))
                      file.write('\n')
                      file.write('\n')
                      file.write("Trial Scores" + ',' + str(Breakdown_Score))

def Trial_Analyses():
        trialdf = pd.read_csv(f'{directoryname}/Participant Statistics.csv')
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

def RestingState():

    title = 'Resting State'

    pygame.display.set_caption(title)

    def RSTimes():
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS RestingState (
                ParticipantNumber INT,
                RestingStateDuration VARCHAR
            )
        ''')
        cursor.execute('''
            INSERT INTO RestingState (ParticipantNumber, RestingStateDuration)
            VALUES (?, ?)
        ''', (participant_number, RS_Duration))
        connection.commit()
    
    WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption(title)

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)

    font = pygame.font.Font(None, 48)

    def page2():
        window.fill(BLACK)
        display_prompt(2)
        button_rect = display_continue_button()
        return button_rect

    def page1():
        window.fill(BLACK)
        display_prompt(1)
        button_rect = display_continue_button()
        return button_rect, None 

    def display_prompt(page):
        if page == 1:
            prompt_text = "We will now begin with two minutes of resting state EEG"
            left_arrow_text = "Please now fully relax and try not to focus on or think about anything"
            right_arrow_text = "Click continue when you are ready to proceed"
        else:
            prompt_text = "Some trials may contain a beep"
            left_arrow_text = "If you hear this, you must NOT follow the direction of the arrow"
            right_arrow_text = ""

        gap = 150
        
        prompt_surface = font.render(prompt_text, True, WHITE)
        prompt_rect = prompt_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - gap))
        window.blit(prompt_surface, prompt_rect)

        left_arrow_surface = font.render(left_arrow_text, True, WHITE)
        left_arrow_rect = left_arrow_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        window.blit(left_arrow_surface, left_arrow_rect)

        right_arrow_surface = font.render(right_arrow_text, True, WHITE)
        right_arrow_rect = right_arrow_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + gap))
        window.blit(right_arrow_surface, right_arrow_rect)

    def display_continue_button():
        button_text = "Continue"
        button_surface = font.render(button_text, True, BLACK)
        button_rect = button_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 350))
        pygame.draw.rect(window, GREEN, button_rect.inflate(20, 10))
        window.blit(button_surface, button_rect)

        return button_rect

    def countdown_screen():
        RS_start = time.time()
        if stimtracker_available:
            cdtest.start()
        for count in range(5, 0, -1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            window.fill(BLACK)

            if count == 1:
                countdown_text = f"Time remaining: {count} second"

            else:
                  
                countdown_text = f"Time remaining: {count} seconds"
                
            text_surface = font.render(countdown_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            window.blit(text_surface, text_rect)
            
            pygame.display.flip()
            time.sleep(1)
            
        RS_end = time.time()
        global RS_Duration
        RS_Duration = RS_end - RS_start
        RSTimes()
        
        if stimtracker_available:
            cdtest.stop()
            cdtest.split()
                    
    running = True
    current_page = 1
    button_rect, tone_button_rect = page1()

    global pg1_start, pg1_end, pg2_start, pg2_end
    pg1_start = time.time()
    pg1_end = None
    pg2_start = None
    pg2_end = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_rect.collidepoint(event.pos):
                        if current_page == 1:
                            pg1_end = time.time()
                            button_rect = countdown_screen()                        
                        else:
                            countdown_screen()

            
        pygame.display.flip()

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

      font = pygame.font.SysFont("Arial", 40)
      font_small = pygame.font.SysFont("Arial", 20)

      background = pygame.image.load("Stimuli/trial.jpeg")

      pygame.time.wait(1000)

      timer = pygame.time.get_ticks()
      timer2 = timer + 3000

      DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
      DISPLAYSURF.fill(WHITE)
      pygame.display.set_caption("rJORT")
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
              self.rect.move_ip(0,(-SPEED*0.4))
              SCORE = 0
              if (self.rect.top < 10):
                  SCORE += 1
                  self.rect.top = 0
                  self.rect.center = ((SCREEN_WIDTH/2), SCREEN_HEIGHT)
              global COLLISION_SCORE

      class Player(pygame.sprite.Sprite):
          global joystick
          def __init__(self):

              super().__init__()

              width = 10
              height = 15
              self.image = pygame.image.load("Stimuli/greendot.png")
              self.rect = self.image.get_rect()
              self.rect.x = SCREEN_WIDTH/2-80
              self.rect.y = SCREEN_HEIGHT/2

              self.joystick_count = pygame.joystick.get_count()
              if self.joystick_count == 0:
                  # No joysticks!
                  print("Check joystick connection")
              else:
                  self.my_joystick = joystick
                  self.my_joystick.init()

          def move(self):
            if self.joystick_count != 0:
                # Joystick input
                #horiz_axis_pos = self.my_joystick.get_axis(0)
                vert_axis_pos = self.my_joystick.get_axis(1)
                #self.rect.x += int(#horiz_axis_pos * buttonspeed)
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

      for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

      COLLISION_SCORE2 = COLLISION_SCORE/20
      Game_Running = True
      starterRT = time.time()
      counter = 0
      clock = pygame.time.Clock()

      Game_Running = True
      trial_active = True
      p300 = False
      p500 = False
      finishedRT = None
      direction = None
      deflection_count = 0
      score = None

      axis_state = {'held': False}

      while Game_Running:
                pygame.event.pump()
                keys = pygame.key.get_pressed()
                yaxis = 0

                
                for event in pygame.event.get():
                    direction = None

                    '''if event.type == pygame.JOYAXISMOTION and event.axis == 1:
                        yaxis = event.value
                        if yaxis < -0.2:
                            pressed_time = time.time()
                            direction = 'Up'
                        elif yaxis > 0.2:
                            pressed_time = time.time()
                            direction = 'Down'

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            pressed_time = time.time()
                            direction = 'Up'
                        elif event.key == pygame.K_DOWN:
                            pressed_time = time.time()
                            direction = 'Down'
                            '''
                            
                joy_direction = read_joystick_direction(joystick, axis_state)
                if joy_direction:
                    direction = joy_direction
                    pressed_time = time.time()
                    deflection_buffer.append((participant_number, sql_type, direction, pressed_time - starterRT))

                   
                    if direction:
                        counter += 1
                        if trial_active:
                            finishedRT = time.time()
                            trial_active = False
                            p300 = True
                            p500 = True
                
                    if counter == 1:
                        finishedRT = time.time()
                        ReactionTime = finishedRT - starterRT
                        print(f'Reaction Time: {ReactionTime}')
                        data = {'Type': ['GC'], 'Reaction Time': [ReactionTime]}
                        Reactiondf = pd.DataFrame(data)


                        Reactiondf.to_csv(f'{directoryname}/Reaction Time.csv', mode='a', header=False)
   
                        p300 = True
                        p500 = True
                        trial_active = False

                startRT = time.time()
                for event in pygame.event.get():

                    if event.type == QUIT:
                        pygame.display.quit()

                DISPLAYSURF.blit(background, (0,0))
                scores = font_small.render(str(SCORE), True, WHITE)
                DISPLAYSURF.blit(scores, (10,10))

                cscores = font_small.render(str(COLLISION_SCORE2), True, WHITE)
                DISPLAYSURF.blit(cscores, (SCREEN_WIDTH-60, 10))

                for entity in all_sprites:
                    entity.move()
                    DISPLAYSURF.blit(entity.image, entity.rect)

                collided = None

                if pygame.sprite.spritecollideany(P1, enemies):
                        COLLISION_SCORE = 1
                        collided = True

                timer = pygame.time.get_ticks()
                if timer > timer2:
                    pygame.init()

                    if ReactionTime =='000':
                        cdtest.noRT()

                    for entity in all_sprites:
                            entity.kill()
                    DISPLAYSURF.blit(background, (0,0))
                    pygame.display.update()

                    if COLLISION_SCORE == 1:
                       negativefeedback = pygame.image.load("Stimuli/redcross.png")
                       negrect = negativefeedback.get_rect(center = screen.get_rect().center)
                       DISPLAYSURF.blit(negativefeedback, negrect)
                       
                    elif COLLISION_SCORE == 0:
                       positivefeedback = pygame.image.load("Stimuli/greentick.png")
                       posrect = positivefeedback.get_rect(center = screen.get_rect().center)
                       DISPLAYSURF.blit(positivefeedback, posrect)

                    pygame.time.wait(1000)
                    pygame.display.update()

                    with open(f'{directoryname}/Participant Statistics.csv', 'a+') as file:
                      file.write('\n')
                      file.write("GC" + ',' + str(COLLISION_SCORE))

                    if jcount > 0:
                        joystick.init()

                    Game_Running = False
                    sql_deflection_counter(participant_number, sql_type, counter)

                    if collided:
                            score == 0

                    if not collided:
                            score == 1
                            
                    sql_rt(participant_number, sql_type, ReactionTime, score)

                    pygame.display.flip()
                    pygame.time.wait(1000)

                pygame.display.update()
                FramePerSec.tick(FPS)
                flush_deflection_buffer()

def LC():
      sql_type = "LC"

      reactiontime = '000'
      ReactionTime = reactiontime

      import cdtest
      
      global GC_SPEED
      os.environ['SDL_VIDEO_CENTERED'] = '1'
      pygame.init()
      SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
     
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
      SPEED = GC_SPEED * 0.572

      print('LC Speed: ', SPEED)
      
      if SPEED < 1:
        SPEED = 1.11

      COLLISION_SCORE = 0

      font = pygame.font.SysFont("Arial", 40)
      font_small = pygame.font.SysFont("Arial", 20)

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
          global joystick
          def __init__(self):

              super().__init__()

              width = 10
              height = 15

              self.image = pygame.image.load("Stimuli/greendot.png")

              self.rect = self.image.get_rect()

              self.rect.x = SCREEN_WIDTH/2-80
              self.rect.y = SCREEN_HEIGHT/2.5

              self.joystick_count = pygame.joystick.get_count()

              if self.joystick_count == 0:
                  print("No joystick mode")
              else:
                  self.my_joystick = joystick
                  self.my_joystick.init()

          def move(self):
                if self.joystick_count != 0:
                    #horiz_axis_pos = self.my_joystick.get_axis(0)
                    vert_axis_pos = self.my_joystick.get_axis(1)

                    #self.rect.x += int(#horiz_axis_pos * buttonspeed)
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
      trial_active = True
      p300 = False
      p500 = False
      finishedRT = None
      direction = None
      deflection_count = 0
      score = None

      axis_state = {'held': False}

      cdtest.LC()

      while Game_Running:
                
                pygame.event.pump()
                keys = pygame.key.get_pressed()
                yaxis = 0

                for event in pygame.event.get():
                    direction = None

                    '''if event.type == pygame.JOYAXISMOTION and event.axis == 1:
                        yaxis = event.value
                        if yaxis < -0.2:
                            pressed_time = time.time()
                            direction = 'Up'
                        elif yaxis > 0.2: 
                            pressed_time = time.time()
                            direction = 'Down'

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            pressed_time = time.time()
                            direction = 'Up'
                        elif event.key == pygame.K_DOWN:
                            pressed_time = time.time()
                            direction = 'Down'
                            '''
                                                     
                joy_direction = read_joystick_direction(joystick, axis_state)
                
                if joy_direction:
                    direction = joy_direction
                    pressed_time = time.time()
                    deflection_buffer.append((participant_number, sql_type, direction, pressed_time - starterRT))

                    if direction:
                        counter += 1
                        cdtest.LC_deflection()
                        if counter == 1:                            
                            cdtest.LC_RT()
                            
                        if trial_active:
                            finishedRT = time.time()
                            trial_active = False
                            p300 = True
                            p500 = True
                
                    if counter == 1:
                        finishedRT = time.time()
                        ReactionTime = finishedRT - starterRT
                        print(f'Reaction Time: {ReactionTime}')
                        data = {'Type': ['LC'], 'Reaction Time': [ReactionTime]}
                        Reactiondf = pd.DataFrame(data)
                        Reactiondf.to_csv(f'{directoryname}/Reaction Time.csv', mode='a', header=False)
   
                        p300 = True
                        p500 = True
                        trial_active = False                

                startRT = time.time()
                
                for event in pygame.event.get():

                    if event.type == QUIT:
                        pygame.display.quit()

                DISPLAYSURF.blit(background, (0,0))
                scores = font_small.render(str(SCORE), True, WHITE)
                DISPLAYSURF.blit(scores, (10,10))

                cscores = font_small.render(str(COLLISION_SCORE2), True, WHITE)
                DISPLAYSURF.blit(cscores, (SCREEN_WIDTH-60, 10))

                for entity in all_sprites:
                    entity.move()
                    DISPLAYSURF.blit(entity.image, entity.rect)

                collided = None

                if pygame.sprite.spritecollideany(P1, enemies):
                        COLLISION_SCORE = 1
                        collided = True

                timer = pygame.time.get_ticks()
                if timer > timer2:
                    pygame.init()
                    
                    if ReactionTime =='000':
                        cdtest.noRT()

                    cdtest.LC_end()
                    
                    for entity in all_sprites:
                            entity.kill()
                    DISPLAYSURF.blit(background, (0,0))
                    pygame.display.update()

                    if COLLISION_SCORE == 1:
                       negativefeedback = pygame.image.load("Stimuli/redcross.png")
                       negrect = negativefeedback.get_rect(center = screen.get_rect().center)
                       DISPLAYSURF.blit(negativefeedback, negrect)
                       
                    elif COLLISION_SCORE == 0:
                       positivefeedback = pygame.image.load("Stimuli/greentick.png")
                       posrect = positivefeedback.get_rect(center = screen.get_rect().center)
                       DISPLAYSURF.blit(positivefeedback, posrect)

                    pygame.time.wait(1000)
                    pygame.display.update()

                    with open(f'{directoryname}/Participant Statistics.csv', 'a+') as file:
                      file.write('\n')
                      file.write("LC" + ',' + str(COLLISION_SCORE))

                    if jcount > 0:
                        joystick.init()

                    Game_Running = False
                    sql_deflection_counter(participant_number, sql_type, counter)

                    if collided:
                            score == 0

                    if not collided:
                            score == 1
                            
                    sql_rt(participant_number, sql_type, ReactionTime, score)

                    pygame.display.flip()
                    pygame.time.wait(1000)

                pygame.display.update()
                FramePerSec.tick(FPS)
                flush_deflection_buffer()

def analysis():
    def analyse():

                cursor = connection.cursor()
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

    font = pygame.font.SysFont("Arial", 40)
    font_small = pygame.font.SysFont("Arial", 20)

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

      font = pygame.font.SysFont("Arial", 40)
      font_small = pygame.font.SysFont("Arial", 20)

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

              # greendot image
              self.image = pygame.image.load("Stimuli/greendot.png")


              # Fetch the rectangle object that has the dimensions of the image
              self.rect = self.image.get_rect()

              # Set initial position of greendot
              self.rect.x = SCREEN_WIDTH/2-80
              self.rect.y = SCREEN_HEIGHT/2-80

              # joystick count
              self.joystick_count = pygame.joystick.get_count()
              if self.joystick_count == 0:
                  # No joysticks!
                  print("Check joystick connection")
              else:
                  # Use joystick #0 and initialize it
                  self.my_joystick = joystick
                  self.my_joystick.init()

          def move(self):
            if self.joystick_count != 0:
                #horiz_axis_pos = self.my_joystick.get_axis(0)
                vert_axis_pos = self.my_joystick.get_axis(1)

                #self.rect.x += int(#horiz_axis_pos * buttonspeed)
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

          joystick = joystick

      starterRT = time.time()
      counter = 0

      Game_Running = True
      trial_active = True
      p300 = False
      p500 = False
      finishedRT = None
      direction = None
      deflection_count = 0

      axis_state = {'held': False}

      while Game_Running:
                pygame.event.pump()
                keys = pygame.key.get_pressed()
                yaxis = 0

                
                for event in pygame.event.get():
                    direction = None

                    '''if event.type == pygame.JOYAXISMOTION and event.axis == 1:
                        yaxis = event.value
                        if yaxis < -0.2:
                            pressed_time = time.time()
                            direction = 'Up'
                        elif yaxis > 0.2:
                            pressed_time = time.time()
                            direction = 'Down'

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            pressed_time = time.time()
                            direction = 'Up'
                        elif event.key == pygame.K_DOWN:
                            pressed_time = time.time()
                            direction = 'Down'
                            '''
                            
                joy_direction = read_joystick_direction(joystick, axis_state)
                if joy_direction:
                    direction = joy_direction
                    pressed_time = time.time()
                    deflection_buffer.append((participant_number, sql_type, direction, pressed_time - starterRT))
                   
                    if direction:

                        counter += 1
                        cdtest.GC_deflection()
                        if counter == 1:                            
                            cdtest.GC_RT()
                
                    if counter == 1:
                        finishedRT = time.time()
                        ReactionTime = finishedRT - starterRT
                        print(f'Reaction Time: {ReactionTime}')
                        data = {'Type': ['Calibration Trial'], 'Reaction Time': [ReactionTime]}
                        Reactiondf = pd.DataFrame(data)

                        with open('Outputs/Calibration Score.csv', 'a+') as file:
                            file.write('\n')
                            file.write("Calibration," + str(yaxis))

                        with open(f'{directoryname}/Calibration Score.csv', 'a+') as file:
                            file.write('\n')
                            file.write("Calibration," + str(yaxis))

                        Reactiondf.to_csv(f'{directoryname}/Reaction Time.csv', mode='a', header=False)
   
                        p300 = True
                        p500 = True
                        trial_active = False

                startRT = time.time()
                for event in pygame.event.get():

                    if event.type == QUIT:
                        pygame.display.quit()

                DISPLAYSURF.blit(background, (0,0))
                scores = font_small.render(str(SCORE), True, WHITE)
                DISPLAYSURF.blit(scores, (10,10))

                cscores = font_small.render(str(COLLISION_SCORE2), True, WHITE)
                DISPLAYSURF.blit(cscores, (SCREEN_WIDTH-60, 10))

                for entity in all_sprites:
                    entity.move()
                    DISPLAYSURF.blit(entity.image, entity.rect)

                if pygame.sprite.spritecollideany(P1, enemies):
                   COLLISION_SCORE == 1

                timer = pygame.time.get_ticks()
                if timer > timer2:
                    pygame.init()

                    if ReactionTime =='000':
                        cdtest.noRT()

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

                    with open(f'{directoryname}/Participant Statistics.csv', 'a+') as file:
                      file.write('\n')
                      file.write("Calibration Trial (2 Stim)" + ',' + str(COLLISION_SCORE))

                    if jcount > 0:
                        for i in range(jcount):
                            print(f"Joystick {i}: {joystick.get_name()}")
                            
                        joystick = pygame.joystick.Joystick()
                        joystick.init()

                    Game_Running = False
                    sql_deflection_counter(participant_number, sql_type, counter)
                    sql_rt(sql_type, ReactionTime, COLLISION_SCORE)

                    pygame.display.flip()
                    pygame.time.wait(1000)

                pygame.display.update()
                FramePerSec.tick(FPS)
                flush_deflection_buffer()

from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE

executed = False
global ready
ready = False

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

    font = pygame.font.SysFont("Arial", 40)
    font_small = pygame.font.SysFont("Arial", 20)

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

        prompt_text = "You will see two red objects and a green dot (yourself)"
        
        if jcount > 0:
            left_arrow_text = "Use the joystick (push forwards and backwards) to move away from the objects - don't let them hit you!"

        else:
            left_arrow_text = "You must use the up and down arrow keys to move away from the objects - don't let them hit you!"
            
        right_arrow_text = "There will be 20 practice trials to build your familiarity with the task."

        prompt_surface = font.render(prompt_text, True, BLACK)
        prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 300))
        screen.blit(prompt_surface, prompt_rect)

        left_arrow_surface = font.render(left_arrow_text, True, BLACK)
        left_arrow_rect = left_arrow_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(left_arrow_surface, left_arrow_rect)

        right_arrow_surface = font.render(right_arrow_text, True, BLACK)
        right_arrow_rect = right_arrow_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 300))
        screen.blit(right_arrow_surface, right_arrow_rect)

        pygame.draw.rect(screen, BLACK, checkbox_rect, 2)

        if checkbox_checked:
            pygame.draw.rect(screen, GREEN, (checkbox_rect.x + 2, checkbox_rect.y + 2, 26, 26))
            global ready

            ready = True
            if false_count == 0:
                break
                connection.close()

        if not checkbox_checked:
            ready = False

        ready_text = font_small.render("Ready:", True, BLACK)
        screen.blit(ready_text, (checkbox_rect.x - ready_text.get_width() - 10, checkbox_rect.y))

        scores = font_small.render(str(SCORE), True, WHITE)
        screen.blit(scores, (10, 10))

        pygame.display.flip()
        clock.tick(60)

def CB_Full():
      import cdtest
      ReactionTime = '000'
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

      FPS = 60
      FramePerSec = pygame.time.Clock()
      #SCREEN_WIDTH = 1000
      #SCREEN_HEIGHT = 1000
      global GC_SPEED
      SPEED = GC_SPEED/2
      #SCORE = 0
      COLLISION_SCORE = 0

      #Setting up Fonts
      font = pygame.font.SysFont("Arial", 40)
      font_small = pygame.font.SysFont("Arial", 20)

      background = pygame.image.load("Stimuli/trial.jpeg")
      pygame.time.wait(1000)

      timer = pygame.time.get_ticks()
      timer2 = timer + 4000

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
              self.rect.move_ip(0,(-SPEED*0.9))
              SCORE = 0
              if (self.rect.top < 10):
                  SCORE += 1
                  self.rect.top = 0
                  self.rect.center = ((SCREEN_WIDTH/2), SCREEN_HEIGHT)
              global COLLISION_SCORE

      class Player(pygame.sprite.Sprite):
        def __init__(self):
              global joystick

              super().__init__()
              width = 10
              height = 15

              self.image = pygame.image.load("Stimuli/greendot.png")
              self.rect = self.image.get_rect()

              self.rect.x = SCREEN_WIDTH/2-80
              self.rect.y = SCREEN_HEIGHT/2

              self.joystick_count = pygame.joystick.get_count()
              if self.joystick_count == 0:
                  print("Check the joystick connection")
              else:
                  self.my_joystick = joystick
                  self.my_joystick.init()

        def move(self):
                if self.joystick_count != 0:
                    #horiz_axis_pos = self.my_joystick.get_axis(0)
                    vert_axis_pos = self.my_joystick.get_axis(1)

                    #self.rect.x += int(#horiz_axis_pos * buttonspeed)
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
      startRT = time.time()

      starterRT = time.time()
      counter = 0

      Game_Running = True
      trial_active = True
      p300 = False
      p500 = False
      finishedRT = None
      direction = None
      deflection_count = 0
      score = None
      axis_state = {'held': False}

      while Game_Running:
                pygame.event.pump()
                keys = pygame.key.get_pressed()
                yaxis = 0
      
                for event in pygame.event.get():
                    direction = None

                    if event.type == pygame.JOYAXISMOTION and event.axis == 1:
                        yaxis = event.value
                        if yaxis < -0.2:
                            pressed_time = time.time()
                            direction = 'Up'
                        elif yaxis > 0.2:
                            pressed_time = time.time()
                            direction = 'Down'

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            pressed_time = time.time()
                            print('up')
                            direction = 'Up'
                        elif event.key == pygame.K_DOWN:
                            pressed_time = time.time()
                            print('down')
                            direction = 'Down'
                                             
                try:
                    joy_direction = read_joystick_direction(joystick, axis_state)

                except NameError as e:
                    pass

                try:
                    
                    if joy_direction or direction:
                        direction = joy_direction
                        pressed_time = time.time()
                        deflection_buffer.append((participant_number, sql_type, direction, pressed_time - starterRT))

                       
                        if direction or direction:
                            counter += 1
                            if trial_active:
                                finishedRT = time.time()
                                trial_active = False
                                p300 = True
                                p500 = True
                    
                        if counter == 1:
                            finishedRT = time.time()
                            ReactionTime = finishedRT - starterRT
                            print(f'Reaction Time: {ReactionTime}')
                            data = {'Type': ['Calibration Trial'], 'Reaction Time': [ReactionTime]}
                            Reactiondf = pd.DataFrame(data)

                            with open('Outputs/Calibration Score.csv', 'a+') as file:
                                file.write('\n')
                                file.write("Calibration (2 Stim)," + str(yaxis))

                            with open(f'{directoryname}/Calibration Score.csv', 'a+') as file:
                                file.write('\n')
                                file.write("Calibration (2 Stim)," + str(yaxis))

                            Reactiondf.to_csv(f'{directoryname}/Reaction Time.csv', mode='a', header=False)
       
                            p300 = True
                            p500 = True
                            trial_active = False
                            
                except UnboundLocalError as e:
                    pass

                startRT = time.time()
                for event in pygame.event.get():

                    if event.type == QUIT:
                        pygame.display.quit()

                DISPLAYSURF.blit(background, (0,0))
                scores = font_small.render(str(SCORE), True, WHITE)
                DISPLAYSURF.blit(scores, (10,10))

                cscores = font_small.render(str(COLLISION_SCORE2), True, WHITE)
                DISPLAYSURF.blit(cscores, (SCREEN_WIDTH-60, 10))

                for entity in all_sprites:
                    entity.move()
                    DISPLAYSURF.blit(entity.image, entity.rect)

                collided = None

                if pygame.sprite.spritecollideany(P1, enemies):
                        COLLISION_SCORE = 1
                        collided = True

                timer = pygame.time.get_ticks()
                if timer > timer2:

                    if ReactionTime =='000':
                        cdtest.noRT()
                    
                    pygame.init()

                    for entity in all_sprites:
                            entity.kill()
                    DISPLAYSURF.blit(background, (0,0))
                    pygame.display.update()

                    if COLLISION_SCORE == 1:
                       negativefeedback = pygame.image.load("Stimuli/redcross.png")
                       negrect = negativefeedback.get_rect(center = screen.get_rect().center)
                       DISPLAYSURF.blit(negativefeedback, negrect)
                       
                    elif COLLISION_SCORE == 0:
                       positivefeedback = pygame.image.load("Stimuli/greentick.png")
                       posrect = positivefeedback.get_rect(center = screen.get_rect().center)
                       DISPLAYSURF.blit(positivefeedback, posrect)

                    pygame.time.wait(1000)
                    pygame.display.update()

                    with open(f'{directoryname}/Participant Statistics.csv', 'a+') as file:
                      file.write('\n')
                      file.write("Calibration Trial (2 Stim)" + ',' + str(COLLISION_SCORE))

                    if jcount > 0:
                        joystick.init()

                    Game_Running = False
                    sql_deflection_counter(participant_number, sql_type, counter)

                    if collided:
                            score == 0

                    if not collided:
                            score == 1
                            
                    sql_rt(participant_number, sql_type, ReactionTime, score)

                    pygame.display.flip()
                    pygame.time.wait(1000)

                pygame.display.update()
                FramePerSec.tick(FPS)
                flush_deflection_buffer()

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

      # Starting position of the greendot
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
      font = pygame.font.SysFont("Arial", 40)
      font_small = pygame.font.SysFont("Arial", 20)

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

              # greendot image
              self.image = pygame.image.load("Stimuli/greendot.png")

              # Fetch the rectangle object that has the dimensions of the image
              self.rect = self.image.get_rect()

              # Set initial position of greendot
              self.rect.x = SCREEN_WIDTH/2-80
              self.rect.y = SCREEN_HEIGHT/2-80

              # joystick count
              self.joystick_count = pygame.joystick.get_count()
              if self.joystick_count == 0:
                  # No joysticks!
                  print("Check joystick connection")
              else:
                  # Use joystick #0 and initialize it
                  self.my_joystick = joystick
                  self.my_joystick.init()

          def move(self):
              if self.joystick_count != 0:

                  # joystick pos
                  #horiz_axis_pos = self.my_joystick.get_axis(0)
                  vert_axis_pos = self.my_joystick.get_axis(1)

                  # Move x and y, * speed
                  #self.rect.x = self.rect.x+int(#horiz_axis_pos*int(0))
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
      
      COLLISION_SCORE2 = COLLISION_SCORE/20
      if jcount > 0:
          joystick = joystick

      starterRT = time.time()
      counter = 0

      Game_Running = True
      trial_active = True
      p300 = False
      p500 = False
      finishedRT = None
      direction = None
      deflection_count = 0
      score = None
      axis_state = {'held': False}

      while Game_Running:
                pygame.event.pump()
                keys = pygame.key.get_pressed()
                yaxis = 0

                
                for event in pygame.event.get():
                    direction = None

                    '''if event.type == pygame.JOYAXISMOTION and event.axis == 1:
                        yaxis = event.value
                        if yaxis < -0.2:
                            pressed_time = time.time()
                            direction = 'Up'
                        elif yaxis > 0.2:
                            pressed_time = time.time()
                            direction = 'Down'

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            pressed_time = time.time()
                            direction = 'Up'
                        elif event.key == pygame.K_DOWN:
                            pressed_time = time.time()
                            direction = 'Down'
                            '''
                            
                joy_direction = read_joystick_direction(joystick, axis_state)
                
                if joy_direction:
                    direction = joy_direction
                    pressed_time = time.time()
                    deflection_buffer.append((participant_number, sql_type, direction, pressed_time - starterRT))

                    if direction:
                        counter += 1
                        if trial_active:
                            finishedRT = time.time()
                            trial_active = False
                            p300 = True
                            p500 = True
                
                    if counter == 1:
                        finishedRT = time.time()
                        ReactionTime = finishedRT - starterRT
                        print(f'Reaction Time: {ReactionTime}')
                        data = {'Type': ['Calibration Trial'], 'Reaction Time': [ReactionTime]}
                        Reactiondf = pd.DataFrame(data)

                        with open('Outputs/Calibration Score.csv', 'a+') as file:
                            file.write('\n')
                            file.write("Calibration (Last)," + str(yaxis))

                        with open(f'{directoryname}/Calibration Score.csv', 'a+') as file:
                            file.write('\n')
                            file.write("Calibration (Last)," + str(yaxis))

                        Reactiondf.to_csv(f'{directoryname}/Reaction Time.csv', mode='a', header=False)
   
                        p300 = True
                        p500 = True
                        trial_active = False

                startRT = time.time()
                for event in pygame.event.get():

                    if event.type == QUIT:
                        pygame.display.quit()

                DISPLAYSURF.blit(background, (0,0))
                scores = font_small.render(str(SCORE), True, WHITE)
                DISPLAYSURF.blit(scores, (10,10))

                cscores = font_small.render(str(COLLISION_SCORE2), True, WHITE)
                DISPLAYSURF.blit(cscores, (SCREEN_WIDTH-60, 10))

                for entity in all_sprites:
                    entity.move()
                    DISPLAYSURF.blit(entity.image, entity.rect)

                collided = None

                if pygame.sprite.spritecollideany(P1, enemies):
                        COLLISION_SCORE = 1
                        collided = True

                timer = pygame.time.get_ticks()
                if timer > timer2:
                    pygame.init()

                    if ReactionTime =='000':
                        cdtest.noRT()

                    for entity in all_sprites:
                            entity.kill()
                    DISPLAYSURF.blit(background, (0,0))
                    pygame.display.update()

                    if COLLISION_SCORE == 1:
                       negativefeedback = pygame.image.load("Stimuli/redcross.png")
                       negrect = negativefeedback.get_rect(center = screen.get_rect().center)
                       DISPLAYSURF.blit(negativefeedback, negrect)
                       
                    elif COLLISION_SCORE == 0:
                       positivefeedback = pygame.image.load("Stimuli/greentick.png")
                       posrect = positivefeedback.get_rect(center = screen.get_rect().center)
                       DISPLAYSURF.blit(positivefeedback, posrect)

                    pygame.time.wait(1000)
                    pygame.display.update()

                    with open(f'{directoryname}/Participant Statistics.csv', 'a+') as file:
                      file.write('\n')
                      file.write("Calibration Trial (last)" + ',' + str(COLLISION_SCORE))

                    if jcount > 0:
                        joystick.init()

                    Game_Running = False
                    sql_deflection_counter(participant_number, sql_type, counter)

                    if collided:
                            score == 0

                    if not collided:
                            score == 1
                            
                    sql_rt(participant_number, sql_type, ReactionTime, score)
                    pygame.display.flip()
                    pygame.time.wait(1000)

                pygame.display.update()
                FramePerSec.tick(FPS)
                flush_deflection_buffer()

def CC():
    import pandas as pd
    import math
    import numpy as np

    def calculate_tcs():
            RT_LowRef = 75
            RT_HighRef = 4000
            TCS_Min = 1
            TCS_Max = 13.5
            smoothing = 1.04

            df = pd.read_csv(f'{directoryname}/Reaction Time.csv')
            mean_rt_ms = df['Reaction Time'].mean()

            global tcs
            tcs = smoothing * ((RT_HighRef - mean_rt_ms) / (RT_HighRef - RT_LowRef)) * (TCS_Max - TCS_Min) + TCS_Min
            print(tcs)
            return round(tcs, 2)

    calculate_tcs()

    global Calibration_SPEED
    Calibration_SPEED = tcs


    with open(f'{directoryname}/Calibration Calculation.csv', 'w+') as file:
        file.write("Calibration Conversion Score" + ',' + str(tcs))
        file.write('\n')

num_operations = 40
order = [random.choice([LC]) for _ in range(num_operations)]

#RestingState()

intro()

for i in range(0, 3):
        CB_Full()
        
for operation in order:
    CC()
    operation()

analysis()
