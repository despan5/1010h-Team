import pygame
import sys
import random
import os
from pygame.locals import *
from control.camera import Camera
from physics.player import Player
from physics.enemy import Enemy
from physics.obstacles import Obstacles, Door
from constants import TPS, MAIN_CLOCK, WHITE, PROJECT_ROOT
from physics.consumable import Consumable


class Engine:

    def __init__(self):
        pygame.init()

        # Initialize Music
        pygame.mixer.init()

        # Screen information
        self.info = pygame.display.Info()
        self.SCREEN_WIDTH = self.info.current_w
        self.SCREEN_HEIGHT = self.info.current_h

        self.DISPLAYSURF = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.DISPLAYSURF.fill(WHITE)
        pygame.display.set_caption("Game")

        bg_image_path = os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'game_background.jpg')  # Construct the path
        print(bg_image_path)

        bg_original = pygame.image.load(bg_image_path)
        self.bg = pygame.transform.scale(bg_original, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.LEVEL_LENGTH = 5000  # Set level length for each level

        self.LEVEL_LENGTH = 5000  # Set level length for each level

    # Platform generation
    @staticmethod
    def generate_platforms(platforms, level_length):
        x = 400
        while x < level_length:
            y = random.randint(400, 700)
            width = random.randint(100, 300)
            height = 20
            platform = Obstacles(x, y, width, height)
            platforms.append(platform)
            x += random.randint(300, 600)

    def run_engine(self):
        current_level = 1
        P1 = Player(self.SCREEN_HEIGHT)
        E1 = Enemy()
        camera = Camera(P1, self.SCREEN_WIDTH)
        cherry = Consumable(400, 650)

        platforms = []
        Engine.generate_platforms(platforms, self.LEVEL_LENGTH)
        door = Door(self.LEVEL_LENGTH - 200, self.SCREEN_HEIGHT - 450)  # Place door near the end of the level

        # Load Music
        pygame.mixer.music.load('assets/sound/song1.mp3')

        # Play the music (-1 means loop indefinitely)
        pygame.mixer.music.play(-1)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return None
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.mixer.music.stop()
                        pygame.QUIT()
                        sys.exit()

            # Update player and camera
            P1.Update(platforms, E1, camera, self.SCREEN_HEIGHT)
            camera.update()
            cherry.update(P1)

            # Check if player reaches the door to go to the next level
            if door.Check_Collision(P1):
                current_level += 1
                P1.rect.center = (160, self.SCREEN_HEIGHT - 300)  # Reset player position
                platforms = []
                Engine.generate_platforms(platforms, self.LEVEL_LENGTH)  # Generate new random platforms
                door = Door(self.LEVEL_LENGTH - 200, self.SCREEN_HEIGHT - 450)  # Place door at the end of the new level

            # Background scrolling logic
            self.DISPLAYSURF.blit(self.bg, (camera.offset_x % self.SCREEN_WIDTH, 0))
            if camera.offset_x % self.SCREEN_WIDTH != 0:
                self.DISPLAYSURF.blit(self.bg, (camera.offset_x % self.SCREEN_WIDTH - self.SCREEN_WIDTH, 0))

            # Draw platforms, player, enemy, and door with camera offset applied
            for platform in platforms:
                platform.Draw(self.DISPLAYSURF, camera)

            P1.Draw(self.DISPLAYSURF, camera)
            E1.Draw(self.DISPLAYSURF, camera)
            cherry.draw(self.DISPLAYSURF, camera)
            P1.hp.Draw(self.DISPLAYSURF, self.SCREEN_HEIGHT, self.SCREEN_WIDTH)
            
            door.Draw(self.DISPLAYSURF, camera)

            # Update display
            pygame.display.update()
            MAIN_CLOCK.tick(TPS)
