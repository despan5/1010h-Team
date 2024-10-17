import pygame
import sys
import random
import os
from pygame.locals import *
from camera import Camera
from player import Player
from enemy import Enemy
from obstacles import Obstacles
from constants import TPS, MAIN_CLOCK, WHITE
<<<<<<< HEAD
from pterodactyl import PterodactylManager  # Import PterodactylManager
=======
>>>>>>> origin/main

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

# Platform generation
def generate_platforms(platforms, camera):
    last_platform = platforms[-1]
    if last_platform.rect.right < SCREEN_WIDTH - camera.offset_x:
        new_platform = Obstacles(last_platform.rect.right + random.randint(100, 300), random.randint(300, 700), 200, 20)
        platforms.append(new_platform)

def remove_offscreen_platforms(platforms, camera):
    platforms[:] = [platform for platform in platforms if platform.rect.right > -camera.offset_x]

def main():
    P1 = Player(SCREEN_HEIGHT)
    E1 = Enemy()
    platforms = [
        Obstacles(400, 700, 200, 20),
        Obstacles(700, 600, 200, 20),
        Obstacles(1000, 500, 200, 20),
    ]
    camera = Camera(P1, SCREEN_WIDTH)

    # Initialize Pterodactyl Manager
    pterodactyl_manager = PterodactylManager(SCREEN_WIDTH, SCREEN_HEIGHT)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Update player and camera
        P1.Update(platforms, E1, camera, SCREEN_HEIGHT)
        camera.update()  # Now camera always follows the player
        remove_offscreen_platforms(platforms, camera)
        generate_platforms(platforms, camera)

        # Random chance to generate a pterodactyl
        if random.randint(0, 100) < 1:  # Adjust the probability as needed
            pterodactyl_manager.generate_pterodactyl()

        # Update pterodactyls
        pterodactyl_manager.update_pterodactyls()

        # Background scrolling logic
        DISPLAYSURF.blit(bg, (camera.offset_x % SCREEN_WIDTH, 0))
        if camera.offset_x % SCREEN_WIDTH != 0:
            DISPLAYSURF.blit(bg, (camera.offset_x % SCREEN_WIDTH - SCREEN_WIDTH, 0))

        # Draw platforms, player, and enemy with camera offset applied
        for platform in platforms:
            platform.Draw(DISPLAYSURF, camera)

        P1.Draw(DISPLAYSURF, camera)
        E1.Draw(DISPLAYSURF, camera)

        # Draw the pterodactyls
        pterodactyl_manager.draw(DISPLAYSURF)

        # Update display
        pygame.display.update()
        MAIN_CLOCK.tick(TPS)

if __name__ == '__main__':
    main()
