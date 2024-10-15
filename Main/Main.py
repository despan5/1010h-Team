import pygame
import sys
import random
import os
from pygame.locals import *
from camera import Camera
from player import Player
from enemy import Enemy
from obstacles import Obstacles
from pterodactyl import PterodactylManager  # Import PterodactylManager

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Predefined colors
WHITE = (255, 255, 255)

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

def generate_platforms(platforms):
    last_platform = platforms[-1]
    if last_platform.rect.right < SCREEN_WIDTH:
        new_platform = Obstacles(last_platform.rect.right + random.randint(100, 300), random.randint(300, 700), 200, 20)
        platforms.append(new_platform)

def remove_offscreen_platforms(platforms):
    platforms[:] = [platform for platform in platforms if platform.rect.right > 0]

def main():
    P1 = Player(SCREEN_HEIGHT)
    E1 = Enemy()
    platforms = [
        Obstacles(400, 700, 200, 20),
        Obstacles(700, 600, 200, 20),
        Obstacles(1000, 500, 200, 20),
    ]

    # Initialize Pterodactyl Manager without camera
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

        # Update player and remove offscreen platforms
        P1.Update(platforms, E1, SCREEN_HEIGHT)
        remove_offscreen_platforms(platforms)
        generate_platforms(platforms)

        # Random chance to generate a pterodactyl
        if random.randint(0, 100) < 1:
            pterodactyl_manager.generate_pterodactyl()

        # Update and draw pterodactyls
        pterodactyl_manager.update_pterodactyls()
        pterodactyl_manager.draw(DISPLAYSURF)

        # Background scrolling logic
        DISPLAYSURF.blit(bg, (0, 0))  # No camera offset required

        # Draw platforms, player, and enemy
        for platform in platforms:
            platform.Draw(DISPLAYSURF)

        P1.Draw(DISPLAYSURF)
        E1.Draw(DISPLAYSURF)

        # Update display
        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__ == '__main__':
    main()
