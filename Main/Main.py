import pygame
import sys


#Initialize Pygame
pygame.init()

#Get the screen size of the current display
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

#Set up the display to adjust to screen size (resizable)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Resizable Window with White Background")

#Define a white color
WHITE = (255, 255, 255)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Check if the Escape key is pressed
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.VIDEORESIZE:
            # Adjust the screen size when the window is resized
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

#Fill the screen with a white background
    screen.fill(WHITE)

    # Update the display
    pygame.display.flip()

#Quit Pygame
pygame.quit()
sys.exit()