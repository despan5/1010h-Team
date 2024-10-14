import pygame
import sys
from player import Player
from platform import Platform
from screen import Screen
from enemy import Enemy
from pygame.locals import *

pygame.init()
FPS = 60
FramePerSec = pygame.time.Clock()

info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
DISPLAY_SURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg_path = 'C:/Users/thoma/Documents/GitHub/1010h-Team/Sprites/game_background.jpg'
sprite_path = 'C:/Users/thoma/Documents/GitHub/1010h-Team/Sprites/female/doux/base/move.png'

def main():
    screen = Screen(SCREEN_WIDTH, SCREEN_HEIGHT, bg_path)   
    player = Player(SCREEN_HEIGHT, sprite_path)
    enemy = Enemy()
    platforms = [
        Platform(400, 700, 200, 20),
        Platform(700, 600, 200, 20),
        Platform(1000, 500, 200, 20),
    ]

    #Game Loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return None
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        #checks for updates using update function
        screen.Draw_Background()

        player.Update(platforms, enemy, SCREEN_HEIGHT)
        for platform in platforms:
            platform.Draw(DISPLAY_SURF)
        player.Draw(screen.get_surface())
        enemy.Draw(screen.get_surface())

        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__ == '__main__':
    main()