import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Button Checker")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Print the name of the key that was pressed
            print(f"Key pressed: {pygame.key.name(event.key)}")

    # Fill the screen with black
    screen.fill((0, 0, 0))
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
