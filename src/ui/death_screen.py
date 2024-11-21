import pygame


class DeathScreen:
    def __init__(self, screen):
        # Initialize Music
        pygame.mixer.init()
        self.screen = screen
        self.title_font = pygame.font.Font(None, 100)
        self.button_font = pygame.font.Font(None, 36)
        self.title_text = self.title_font.render("Continue?", True, (29, 185, 17))
        self.retry_button_text = self.button_font.render("Press Enter to Continue", True, (255, 255, 255))
        self.quit_button_text = self.button_font.render("Press Esc to Quit", True, (255, 255, 255))

        self.title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.retry_button_rect = self.retry_button_text.get_rect(center=(self.screen.get_width() // 2, 400))
        self.quit_button_rect = self.quit_button_text.get_rect(center=(self.screen.get_width() // 2, 500))

        # Load Music
        pygame.mixer.music.load('assets/sound/start_song.mp3')  # Updated to a more fitting sound if available
        pygame.mixer.music.play(-1)  # Play the music indefinitely



    def draw(self):
        """Draws the death screen."""
        self.screen.fill((0, 0, 0))  # Black background
        self.screen.blit(self.title_text, self.title_rect)  # Display title centered
        self.screen.blit(self.retry_button_text, self.retry_button_rect)  # Display retry button text centered
        self.screen.blit(self.quit_button_text, self.quit_button_rect)  # Display quit button text centered
        pygame.display.flip()

    def handle_event(self, event, game_state, P1):
        """Handles keyboard events and updates game state accordingly."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Restart game when Enter is pressed
                P1.hp.health_count = 4  # Reset to full health or your desired initial value
                game_state.set_state('START_MENU')
                return 'RESTART'
            elif event.key == pygame.K_ESCAPE:  # Quit game when Escape is pressed
                pygame.mixer.music.stop()
                pygame.quit()
                exit()
        return None