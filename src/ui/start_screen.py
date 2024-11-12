import pygame
from physics.player import Player

class StartScreen:
    def __init__(self, screen):
        # Initialize Music
        pygame.mixer.init()
        self.screen = screen
        self.title_font = pygame.font.Font(None, 100)
        self.button_font = pygame.font.Font(None, 36)
        self.title_text = self.title_font.render("Dino Dash", True, (29, 185, 17))
        self.start_button_text = self.button_font.render("Press Enter to Start", True, (255, 255, 255))
        self.quit_button_text = self.button_font.render("Press Esc to Quit", True, (255, 255, 255))

        self.title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.start_button_rect = self.start_button_text.get_rect(center=(self.screen.get_width() // 2, 400))
        self.quit_button_rect = self.quit_button_text.get_rect(center=(self.screen.get_width() // 2, 500))

        # Create the player object for the cutscene
        self.player = Player(SCREEN_HEIGHT=self.screen.get_height())
        self.player.rect.x = -100  # Start off-screen (left)

        # Load Music
        pygame.mixer.music.load('assets/sound/start_song.mp3')
        pygame.mixer.music.play(-1)  # Play the music indefinitely

    def draw(self):
        """Draws the start screen and handles the cutscene animation."""
        self.screen.fill((0, 0, 0))  # Black background
        self.screen.blit(self.title_text, self.title_rect)
        self.screen.blit(self.start_button_text, self.start_button_rect)
        self.screen.blit(self.quit_button_text, self.quit_button_rect)

        # Move the player across the screen (simple cutscene)
        walk_distance = 300  # Total distance to walk
        step_size = 5  # How much to move each frame
        jump_height = 100  # How high to jump
        jump_duration = 20  # Frames to jump

        # Move the player across the screen
        while self.player.rect.x < walk_distance:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.title_text, self.title_rect)
            self.screen.blit(self.start_button_text, self.start_button_rect)
            self.screen.blit(self.quit_button_text, self.quit_button_rect)

            self.player.rect.x += step_size
            self.player.Update([], None, None, self.screen.get_height())
            self.player.Draw(self.screen, None)

            pygame.display.flip()
            pygame.time.delay(30)

        # Jump animation
        for j in range(jump_duration):
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.title_text, self.title_rect)
            self.screen.blit(self.start_button_text, self.start_button_rect)
            self.screen.blit(self.quit_button_text, self.quit_button_rect)

            if j < jump_duration // 2:  # Ascend
                self.player.rect.y -= jump_height / (jump_duration // 2)
            else:  # Descend
                self.player.rect.y += jump_height / (jump_duration // 2)

            self.player.Update([], None, None, self.screen.get_height())
            self.player.Draw(self.screen, None)

            pygame.display.flip()
            pygame.time.delay(30)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Start game when Enter is pressed
                pygame.mixer.music.stop()  # Stop the music before starting the game
                return 'START_GAME'
            elif event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                pygame.quit()
                return 'QUIT'
        return None
