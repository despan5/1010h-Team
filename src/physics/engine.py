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
from physics.Egg import Egg


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

        # Enemy configurations for 5 levels
        self.enemy_configs = {
            1: [{"x": 890, "y": 390, "movement_range": 125, "speed": 8},
                {"x": 1500, "y": 220, "movement_range": 150, "speed": 8}],
            2: [{"x": 1600, "y": 525, "movement_range": 350, "speed": 6},
                {"x": 1125, "y": 80, "movement_range": 175, "speed": 4},
                {"x": 2350, "y": 220, "movement_range": 175, "speed": 6},
                {"x": 1500, "y": 725, "movement_range": 800, "speed": 6}],
            3: [{"x": 530, "y": 440, "movement_range": 340, "speed": 5},
                {"x": 1710, "y": 555, "movement_range": 300, "speed": 5},
                {"x": 1600, "y": 725, "movement_range": 775, "speed": 9}],
            4: [{"x": 1200, "y": 580, "movement_range": 200, "speed": 5},
                {"x": 1575, "y": 440, "movement_range": 120, "speed": 5},
                {"x": 1990, "y": 250, "movement_range": 160, "speed": 9},
                {"x": 1800, "y": 725, "movement_range": 800, "speed": 13}],
            5: [{"x": 1000, "y": 725, "movement_range": 500, "speed": 16},
                {"x": 2400, "y": 725, "movement_range": 250, "speed": 12},
                {"x": 1880, "y": 415, "movement_range": 110, "speed": 4},
                {"x": 1150, "y": 385, "movement_range": 150, "speed": 4},
                {"x": 770, "y": 610, "movement_range": 140, "speed": 4}],
        }

        # Fruit configurations for 5 levels
        self.fruit_configs = {
            1: [{"x": 1060, "y": 140}],
            2: [{"x": 1600, "y": 360}],
            3: [{"x": 2500, "y": 250}],
            4: [{"x": 1320, "y": 365}, {"x": 1750, "y": 365}],
            5: [{"x": 970, "y": 535}, {"x": 1850, "y": 600}],
        }

        # Egg configurations for 5 levels
        self.egg_configs = {
            1: [{"x": 950, "y": 410}],
            2: [{"x": 1600, "y": 550}],
            3: [{"x": 1800, "y": 565}, {"x": 1300, "y": 410}],
            4: [{"x": 1600, "y": 475}],
            5: [{"x": 1885, "y": 440}],
        }

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

    def load_enemies_for_level(self, current_level, platforms):
        enemy_configs = self.enemy_configs.get(current_level, [])
        return pygame.sprite.Group(
            *[
                Enemy(
                    x=config["x"],
                    y=config["y"],
                    movement_range=config["movement_range"],
                    platforms=platforms,
                    screen_height=self.SCREEN_HEIGHT,
                )
                for config in enemy_configs
            ]
        )

    def load_fruits_for_level(self, current_level):
        fruit_configs = self.fruit_configs.get(current_level, [])
        return pygame.sprite.Group(*[Consumable(x=config["x"], y=config["y"]) for config in fruit_configs])

    def load_eggs_for_level(self, current_level):
        egg_configs = self.egg_configs.get(current_level, [])
        return pygame.sprite.Group(*[Egg(x=config["x"], y=config["y"]) for config in egg_configs])
    
    def draw_you_won_screen(self):
        """Displays the 'You Won' screen."""
        # Stop the background music
        pygame.mixer.music.stop()

        # Play the "You Won" sound effect
        victory_sound_path = os.path.join(PROJECT_ROOT, "assets", "sound", "you_win.mp3")
        if os.path.exists(victory_sound_path):
            victory_sound = pygame.mixer.Sound(victory_sound_path)
            victory_sound.play()

        # Render the "You Won" screen
        font_path = os.path.join(PROJECT_ROOT, "assets", "fonts", "DarkSouls.ttf")
        victory_font = pygame.font.Font(font_path, 120) if os.path.exists(font_path) else pygame.font.Font(None, 120)

        victory_text = victory_font.render("YOU WON!", True, (255, 215, 0))  # Golden text
        text_rect = victory_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))

        self.DISPLAYSURF.fill((0, 0, 0))  # Black background
        self.DISPLAYSURF.blit(victory_text, text_rect)
        pygame.display.flip()

        pygame.time.delay(5000)  # Hold for 5 seconds

    def draw_darksouls_death_screen(self):
        """Displays the Dark Souls-style death screen with sound."""
        # Pause background music
        pygame.mixer.music.pause()

        # Path to the death sound
        death_sound_path = os.path.join(PROJECT_ROOT, "assets", "sound", "you_died.mp3")
        
        # Load and play the sound
        if os.path.exists(death_sound_path):  # Check if the sound file exists
            death_sound = pygame.mixer.Sound(death_sound_path)
            death_sound.set_volume(1.0)  # Ensure the volume is set to max
            death_sound.play()
            print("Playing death sound...")
        else:
            print(f"Death sound not found at {death_sound_path}")
        
        # Render "YOU DIED" text
        font_path = os.path.join(PROJECT_ROOT, "assets", "fonts", "DarkSouls.ttf")
        if os.path.exists(font_path):
            death_font = pygame.font.Font(font_path, 120)  # Large font size
        else:
            death_font = pygame.font.Font(None, 120)  # Fallback to a default font
        
        death_text = death_font.render("YOU DIED", True, (178, 34, 34))  # Dark red
        text_rect = death_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))

        # Black background and text
        self.DISPLAYSURF.fill((0, 0, 0))  # Black background
        self.DISPLAYSURF.blit(death_text, text_rect)  # Draw text
        pygame.display.flip()

        # Hold the screen for 5 seconds
        pygame.time.delay(5000)

        # Resume background music
        pygame.mixer.music.unpause()


    def run_engine(self):
        game_state = GameState()

        # Initialize UI components
        death_screen = DeathScreen(self.DISPLAYSURF)
        start_screen = StartScreen(self.DISPLAYSURF)
        high_score_screen = HighScore(self.DISPLAYSURF)

        # Player and game objects
        P1 = Player(self.SCREEN_HEIGHT)
        platforms = []
        Engine.generate_platforms(platforms, self.LEVEL_LENGTH)
        door = Door(self.LEVEL_LENGTH - 200, self.SCREEN_HEIGHT - 450)

        current_level = P1.current_level
        enemies = self.load_enemies_for_level(current_level, platforms)
        fruits = self.load_fruits_for_level(current_level)
        eggs = self.load_eggs_for_level(current_level)
        camera = Camera(P1, self.SCREEN_WIDTH)

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

            elif game_state.is_current('GAME_RUNNING'):
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        game_state.set_state('PAUSE')
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()

                # Check if the level has changed
                if current_level != P1.current_level:
                    current_level = P1.current_level
                    enemies = self.load_enemies_for_level(current_level, platforms)
                    fruits = self.load_fruits_for_level(current_level)
                    eggs = self.load_eggs_for_level(current_level)
                
                if P1.current_level == 5 and door.Check_Collision(P1):
                    self.draw_you_won_screen()
                    game_state.set_state('QUIT')  # Quit the game after the "You Won" screen


                # Update level
                lvl_sheet = os.path.join(
                    PROJECT_ROOT, 'assets', 'sprites', 'Platforms', 'generic-grassdirt-tileset', 'lavatiles.png'
                )
                level_data = LevelGeneration(
                    os.path.join(PROJECT_ROOT, 'assets', 'level_files', f'l{current_level}.csv'), 16, lvl_sheet
                )
                level_data.load_level()

                rows = len(level_data.level_data)
                scale_factor = self.SCREEN_HEIGHT / rows
                self.tile_size = int(scale_factor)
                self.level_width = int(self.tile_size * len(level_data.level_data[0]))
                level_gen = LevelGeneration(
                    os.path.join(PROJECT_ROOT, 'assets', 'level_files', f'l{current_level}.csv'),
                    self.tile_size,
                    lvl_sheet,
                )
                level_gen.load_level()

                # Update game objects
                P1.Update(level_gen, enemies, camera, self.SCREEN_HEIGHT)
                enemies.update()
                fruits.update(P1, P1.hp)
                eggs.update(P1)
                # Update enemies and check for collisions with the player
                for enemy in enemies:
                    enemy.update()  # Update enemy position and animation
                    enemy.Check_Collision(P1, self.SCREEN_HEIGHT)  # Check for collisions
                camera.update()

                if door.Check_Collision(P1):
                    if current_level == 5:  # If the player is on level 5 and collides with the door
                        self.draw_you_won_screen()  # Display the "You Won" screen
                        game_state.set_state('QUIT')  # Exit the game after showing the screen
                    else:
                        P1.increase_level()  # Increase the player's level
                        current_level = P1.current_level
                        enemies = self.load_enemies_for_level(current_level, platforms)
                        fruits = self.load_fruits_for_level(current_level)
                        eggs = self.load_eggs_for_level(current_level)

                if current_level > 5:  # Prevent loading levels beyond level 5
                    print(f"Level {current_level} does not exist. Showing 'You Won' screen.")
                    self.draw_you_won_screen()
                    game_state.set_state('QUIT')
                    return

                # Draw objects
                self.DISPLAYSURF.blit(self.bg, (camera.offset_x % self.SCREEN_WIDTH, 0))
                if camera.offset_x % self.SCREEN_WIDTH != 0:
                    self.DISPLAYSURF.blit(self.bg, (camera.offset_x % self.SCREEN_WIDTH - self.SCREEN_WIDTH, 0))
                P1.Draw(self.DISPLAYSURF, camera)
                for enemy in enemies:
                    enemy.Draw(self.DISPLAYSURF, camera)
                for fruit in fruits:
                    fruit.draw(self.DISPLAYSURF, camera)
                for egg in eggs:
                    egg.draw(self.DISPLAYSURF, camera)
                level_gen.generate_level(self.DISPLAYSURF, camera, P1)
                P1.hp.Draw(self.DISPLAYSURF, self.SCREEN_HEIGHT, self.SCREEN_WIDTH)
                door.Draw(self.DISPLAYSURF, camera)

                # Handle death
                if P1.hp.health_count <= 0:
                    self.draw_darksouls_death_screen()  # Show Dark Souls death screen
                    game_state.set_state('DEATH_SCREEN')  # Switch to the death screen
                    P1.update_score(P1.username, P1.score)

                score_text = self.font.render(f"Score: {P1.get_score()}", True, (255, 255, 255))
                level_text = self.font.render(f"Current Level: {current_level}", True, (255, 255, 255))
                self.DISPLAYSURF.blit(score_text, (50, 120))
                self.DISPLAYSURF.blit(level_text, (200, 120))
                pygame.display.flip()

            elif game_state.is_current('DEATH_SCREEN'):
                death_screen.draw()
                pygame.display.flip()

                for event in pygame.event.get():
                    result = death_screen.handle_event(event, game_state, P1)
                    if result == 'RESTART':
                        P1.hp.reset()
                        fruits = self.load_fruits_for_level(current_level)
                        eggs = self.load_eggs_for_level(current_level)
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
