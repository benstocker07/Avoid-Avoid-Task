import pygame
import time

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() < 3:
    print("Joystick 2 not connected.")
    pygame.quit()
    exit()

joystick = pygame.joystick.Joystick(2)
joystick.init()
print(f"Using joystick: {joystick.get_name()}")

axis_held = False
THRESHOLD = 0.2

try:
    while True:
        pygame.event.pump()
        yaxis = joystick.get_axis(1)

        if not axis_held:
            if yaxis < -THRESHOLD:
                print("Down")
                axis_held = True
            elif yaxis > THRESHOLD:
                print("Up")
                axis_held = True
        elif -THRESHOLD <= yaxis <= THRESHOLD:
            axis_held = False

        time.sleep(0.05)

except KeyboardInterrupt:
    pygame.quit()
