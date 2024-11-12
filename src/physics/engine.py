import pygame
import sys
import random
import os
import random
from pygame.locals import *
from control.camera import Camera
from physics.player import Player
from physics.enemy import Enemy
from physics.obstacles import Obstacles, Door
from constants import TPS, MAIN_CLOCK, WHITE, PROJECT_ROOT
from physics.consumable import Consumable
from ui.start_screen import StartScreen
from ui.death_screen import DeathScreen



class GameState():
    def __init__(self):
        self.states = {
            'START_MENU': 1,
            'GAME_RUNNING': 2,
            'DEATH_SCREEN': 3,
            'QUIT': 4
        }
        self.current = self.states['START_MENU']

    def set_state(self, new_state):
        if new_state in self.states:
            self.current = self.states[new_state]

    def is_current(self, state):
        return self.current == self.states.get(state)

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

        bg_image_path = os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'background', 'background_01.png')  # Construct the path
        print(bg_image_path)

        bg_original = pygame.image.load(bg_image_path)
        self.bg = pygame.transform.scale(bg_original, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

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

        # Initialize game state
        game_state = GameState()

        # Initialize and display the start screen
        death_screen = DeathScreen(self.DISPLAYSURF)
        start_screen = StartScreen(self.DISPLAYSURF)
        

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
                        game_state.set_state('GAME_RUNNING')
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


                # Load Music
                pygame.mixer.music.load('assets/sound/song1.mp3')  

                # Play the music (-1 means loop indefinitely)
                pygame.mixer.music.play(-1)
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

                # Check if player is dead
                if P1.hp.health_count <= 0:
                    game_state.set_state('DEATH_SCREEN')

                pygame.display.flip()  # Update the full display Surface to the screen
                

            # Death Screen Loop
            elif game_state.is_current('DEATH_SCREEN'):
                death_screen.draw()
                pygame.display.flip()
                
                for event in pygame.event.get():
                    result = death_screen.handle_event(event, game_state, P1)
                    if result == 'RESTART':
                        game_state.set_state('START_MENU')
                    elif result == 'QUIT':
                        game_state.set_state('QUIT')

            # Update display and tick
        pygame.display.update()
        MAIN_CLOCK.tick(TPS)    

        pygame.quit()
