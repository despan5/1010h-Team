import pygame
import sys
import random
import os
from pygame.locals import *
from camera import Camera
from player import Player
from enemy import Enemy
<<<<<<< HEAD
from obstacles import Obstacles, Door
=======
from obstacles import Obstacles
from constants import TPS, MAIN_CLOCK, WHITE
>>>>>>> ae71b9a (PYGM-19: Add preliminary setup for global constants (#7))

pygame.init()

# Screen information
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

base_path = os.path.dirname(__file__)  # Get the directory where the script is located
bg_image_path = os.path.join(base_path, '..', 'Sprites', 'game_background.jpg')  # Construct the full path

bg_original = pygame.image.load(bg_image_path)
bg = pygame.transform.scale(bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))

LEVEL_LENGTH = 5000  # Set level length for each level

# Platform generation
def generate_platforms(platforms, level_length):
    x = 400
    while x < level_length:
        y = random.randint(400, 700)
        width = random.randint(100, 300)
        height = 20
        platform = Obstacles(x, y, width, height)
        platforms.append(platform)
        x += random.randint(300, 600)

def main():
    current_level = 1
    P1 = Player(SCREEN_HEIGHT)
    E1 = Enemy()
    camera = Camera(P1, SCREEN_WIDTH)

    platforms = []
    generate_platforms(platforms, LEVEL_LENGTH)
    door = Door(LEVEL_LENGTH - 200, SCREEN_HEIGHT - 450)  # Place door near the end of the level

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return None
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.QUIT()
                    sys.exit()

        # Update player and camera
        P1.Update(platforms, E1, camera, SCREEN_HEIGHT)
        camera.update()

        # Check if player reaches the door to go to the next level
        if door.Check_Collision(P1):
            current_level += 1
            P1.rect.center = (160, SCREEN_HEIGHT - 300)  # Reset player position
            platforms = []
            generate_platforms(platforms, LEVEL_LENGTH)  # Generate new random platforms
            door = Door(LEVEL_LENGTH - 200, SCREEN_HEIGHT - 450)  # Place door at the end of the new level

        # Background scrolling logic
        DISPLAYSURF.blit(bg, (camera.offset_x % SCREEN_WIDTH, 0))
        if camera.offset_x % SCREEN_WIDTH != 0:
            DISPLAYSURF.blit(bg, (camera.offset_x % SCREEN_WIDTH - SCREEN_WIDTH, 0))

        # Draw platforms, player, enemy, and door with camera offset applied
        for platform in platforms:
            platform.Draw(DISPLAYSURF, camera)

        P1.Draw(DISPLAYSURF, camera)
        E1.Draw(DISPLAYSURF, camera)
        P1.hp.Draw(DISPLAYSURF, SCREEN_HEIGHT, SCREEN_WIDTH)
        
        door.Draw(DISPLAYSURF, camera)

        # Update display
        pygame.display.update()
        MAIN_CLOCK.tick(TPS)

if __name__ == '__main__':
    main()
