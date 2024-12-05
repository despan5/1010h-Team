import pygame

class StartScreen:
    def __init__(self, screen, player):
        
        self.screen = screen
        self.player = player

        self.title_font = pygame.font.Font(None, 100)
        self.button_font = pygame.font.Font(None, 36)
        self.title_text = self.title_font.render("Dino Dash", True, (29, 185, 17))
        self.start_button_text = self.button_font.render("Press Enter to Start", True, (255, 255, 255))
        self.quit_button_text = self.button_font.render("Press Esc to Quit", True, (255, 255, 255))

        self.title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.start_button_rect = self.start_button_text.get_rect(center=(self.screen.get_width() // 2, 400))
        self.quit_button_rect = self.quit_button_text.get_rect(center=(self.screen.get_width() // 2, 500))


    def draw(self):
        """Draws the start screen and handles the cutscene animation."""
        self.screen.fill((0, 0, 0))  # Black background
        self.screen.blit(self.title_text, self.title_rect)
        self.screen.blit(self.start_button_text, self.start_button_rect)
        self.screen.blit(self.quit_button_text, self.quit_button_rect)


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
