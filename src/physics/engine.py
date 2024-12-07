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

        bg_image_path = os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'background', 'background_03.jpg')  # Construct the path
        print(bg_image_path)

        

        bg_original = pygame.image.load(bg_image_path)
        self.bg = pygame.transform.scale(bg_original, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.LEVEL_LENGTH = 5000  # Set level length for each level

        self.LEVEL_LENGTH = 5000  # Set level length for each level

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

        # Initialize and display the start screen
        death_screen = DeathScreen(self.DISPLAYSURF)
        start_screen = StartScreen(self.DISPLAYSURF)
        high_score_screen = HighScore(self.DISPLAYSURF)
        player_id = "player1"

        current_level = 1
        P1 = Player(self.SCREEN_HEIGHT)
        E1 = Enemy()
        camera = Camera(P1, self.SCREEN_WIDTH)
        cherry = Consumable(400, 650)
    
        platforms = []
        Engine.generate_platforms(platforms, self.LEVEL_LENGTH)
        door = Door(self.LEVEL_LENGTH - 200, self.SCREEN_HEIGHT - 450)  # Place door near the end of the level


         # Main game loop
        while game_state.current != game_state.states['QUIT']:
            if game_state.is_current('START_MENU'):
                start_screen.draw()
                pygame.display.flip()

                for event in pygame.event.get():
                    result = start_screen.handle_event(event)
                    if result == 'START_GAME':
                        P1.username = start_screen.username
                        P1.find_score(P1.username)  # Find the score of the player from the database
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
                    if event.type == pygame.QUIT:
                        game_state.set_state('QUIT')
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.mixer.music.stop()
                            pygame.quit()
                            sys.exit()


                lvl_sheet = os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'Platforms', 'generic-grassdirt-tileset', 'lavatiles.png')

                level_data = LevelGeneration(os.path.join(PROJECT_ROOT, 'assets', 'level_files', 'l5.csv'), 16, lvl_sheet)
                level_data.load_level()

                # Get rows and columns for the aspect ratio calculation
                rows = len(level_data.level_data)
                cols = len(level_data.level_data[0]) if rows > 0 else 0

                # Calculate aspect ratio of the level
                aspect_ratio = cols / rows if rows > 0 else 1
                # print(aspect_ratio)

                # Calculate tile size to make the level fill the screen vertically
                scale_factor = self.SCREEN_HEIGHT / rows
                self.tile_size = int(scale_factor)

                # Re-adjust the width to match the height scaling, so the aspect ratio is preserved
                self.level_width = int(self.tile_size * cols)
                level_gen = LevelGeneration(os.path.join(PROJECT_ROOT, 'assets', 'level_files', 'l5.csv'), self.tile_size, lvl_sheet)
                level_gen.load_level()

                # Update player and camera
                P1.Update(level_gen, E1, camera, self.SCREEN_HEIGHT)
                camera.update()
                cherry.update(P1, P1.hp)

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

                P1.Draw(self.DISPLAYSURF, camera)
                E1.Draw(self.DISPLAYSURF, camera)
                cherry.draw(self.DISPLAYSURF, camera)

                level_gen.generate_level(self.DISPLAYSURF, camera, P1)

                P1.hp.Draw(self.DISPLAYSURF, self.SCREEN_HEIGHT, self.SCREEN_WIDTH)
                
                door.Draw(self.DISPLAYSURF, camera)

                # Check if player is dead
                if P1.hp.health_count <= 0:
                    # Save the score at the end of the game
                    game_state.set_state('DEATH_SCREEN')
                    P1.update_score(P1.username, P1.score)  # Update the score in the database

                # Display score
                score_text = self.font.render(f"Score: {P1.get_score()}", True, (255, 255, 255))
                self.DISPLAYSURF.blit(score_text, (50, 120))  # Display in the top-left corner

                pygame.display.flip()  # Update the full display Surface to the screen

            # Death Screen Loop
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
            

            # Update display
        pygame.display.update()
        MAIN_CLOCK.tick(TPS)

        pygame.quit()
