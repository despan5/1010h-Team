import pygame
import sys
import random
import os
from pygame.locals import *
from constants import TPS, MAIN_CLOCK, WHITE, PROJECT_ROOT
from physics.player import Player
from physics.enemy import Enemy
from physics.obstacles import Obstacles, Door
from physics.consumable import Consumable
from ui.game_state import GameState
from ui.start_screen import StartScreen
from ui.death_screen import DeathScreen
from ui.high_score import HighScore
from control.level_generation import LevelGeneration
from control.health import Health
from control.camera import Camera


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

        bg_image_path = os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'background', 'background_03.jpg')
        bg_original = pygame.image.load(bg_image_path)
        self.bg = pygame.transform.scale(bg_original, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.LEVEL_LENGTH = 5000
        self.font = pygame.font.Font(None, 36)  # Default font with size 36


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
        # Initialize game state
        game_state = GameState()

        # Initialize and display UI components
        death_screen = DeathScreen(self.DISPLAYSURF)
        start_screen = StartScreen(self.DISPLAYSURF)
        high_score_screen = HighScore(self.DISPLAYSURF)

        # Player and game objects
        P1 = Player(self.SCREEN_HEIGHT)
        platforms = []
        Engine.generate_platforms(platforms, self.LEVEL_LENGTH)
        door = Door(self.LEVEL_LENGTH - 200, self.SCREEN_HEIGHT - 450)
        enemies = [
            Enemy(x=980, y=785, movement_range=160, platforms=platforms, screen_height=self.SCREEN_HEIGHT),
            Enemy(x=1840, y=330, movement_range=150, platforms=platforms, screen_height=self.SCREEN_HEIGHT),
            Enemy(x=2935, y=755, movement_range=150, platforms=platforms, screen_height=self.SCREEN_HEIGHT),
        ]
        cherry = Consumable(400, 650)
        camera = Camera(P1, self.SCREEN_WIDTH)

        # Main game loop
        while game_state.current != game_state.states['QUIT']:
            if game_state.is_current('START_MENU'):
                start_screen.draw()
                pygame.display.flip()

                for event in pygame.event.get():
                    result = start_screen.handle_event(event)
                    if result == 'START_GAME':
                        P1.username = start_screen.username
                        P1.find_score(P1.username)
                        game_state.set_state('GAME_RUNNING')
                    elif result == 'SCORE_SCREEN':
                        game_state.set_state('HIGH_SCORE')
                    elif result == 'QUIT':
                        game_state.set_state('QUIT')

            elif game_state.is_current('HIGH_SCORE'):
                high_score_screen.draw()
                pygame.display.flip()

                for event in pygame.event.get():
                    result = high_score_screen.handle_event(event)
                    if result == 'RETURN':
                        game_state.set_state('START_MENU')
                    elif result == 'QUIT':
                        game_state.set_state('QUIT')

            elif game_state.is_current('GAME_RUNNING'):
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        game_state.set_state('PAUSE')
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()

                lvl_sheet = os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'Platforms', 'generic-grassdirt-tileset', 'lavatiles.png')
                level_data = LevelGeneration(os.path.join(PROJECT_ROOT, 'assets', 'level_files', 'l5.csv'), 16, lvl_sheet)
                level_data.load_level()

                # Calculate tile size
                rows = len(level_data.level_data)
                scale_factor = self.SCREEN_HEIGHT / rows
                self.tile_size = int(scale_factor)
                self.level_width = int(self.tile_size * len(level_data.level_data[0]))
                level_gen = LevelGeneration(os.path.join(PROJECT_ROOT, 'assets', 'level_files', 'l5.csv'), self.tile_size, lvl_sheet)
                level_gen.load_level()

                # Update game objects
                P1.Update(level_gen, enemies, camera, self.SCREEN_HEIGHT)
                for enemy in enemies:
                    enemy.update()
                camera.update()
                cherry.update(P1, P1.hp)

                # Check door collision
                if door.Check_Collision(P1):
                    P1.rect.center = (160, self.SCREEN_HEIGHT - 300)
                    platforms = []
                    Engine.generate_platforms(platforms, self.LEVEL_LENGTH)
                    door = Door(self.LEVEL_LENGTH - 200, self.SCREEN_HEIGHT - 450)

                # Draw objects
                self.DISPLAYSURF.blit(self.bg, (camera.offset_x % self.SCREEN_WIDTH, 0))
                if camera.offset_x % self.SCREEN_WIDTH != 0:
                    self.DISPLAYSURF.blit(self.bg, (camera.offset_x % self.SCREEN_WIDTH - self.SCREEN_WIDTH, 0))
                P1.Draw(self.DISPLAYSURF, camera)
                for enemy in enemies:
                    enemy.Draw(self.DISPLAYSURF, camera)
                cherry.draw(self.DISPLAYSURF, camera)
                level_gen.generate_level(self.DISPLAYSURF, camera, P1)
                P1.hp.Draw(self.DISPLAYSURF, self.SCREEN_HEIGHT, self.SCREEN_WIDTH)
                door.Draw(self.DISPLAYSURF, camera)

                # Handle death
                if P1.hp.health_count <= 0:
                    game_state.set_state('DEATH_SCREEN')
                    P1.update_score(P1.username, P1.score)

                # Display score
                score_text = self.font.render(f"Score: {P1.get_score()}", True, (255, 255, 255))
                self.DISPLAYSURF.blit(score_text, (50, 120))

                if game_state.is_current('PAUSE'):
                    # Create the text surface
                    pause_text = self.font.render('PAUSED', True, (255, 255, 255))

                    # Get the rectangle of the text surface
                    pause_text_rect = pause_text.get_rect()

                    # Center the rectangle on the screen
                    pause_text_rect.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)

                    # Blit the text surface onto the display surface
                    self.DISPLAYSURF.blit(pause_text, pause_text_rect)

                pygame.display.flip()

            elif game_state.is_current('DEATH_SCREEN'):
                death_screen.draw()
                pygame.display.flip()

                for event in pygame.event.get():
                    result = death_screen.handle_event(event, game_state, P1)
                    if result == 'RESTART':
                        P1.hp.reset()
                        cherry.reset()
                        game_state.set_state('GAME_RUNNING')
                    elif result == 'QUIT':
                        game_state.set_state('QUIT')

            elif game_state.is_current('PAUSE'):
                pause_text = self.font.render('PAUSED', True, (255, 255, 255))
                self.DISPLAYSURF.blit(pause_text, (1000, 1000))

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        game_state.set_state('GAME_RUNNING')
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit() 

            MAIN_CLOCK.tick(TPS)

        pygame.quit()
