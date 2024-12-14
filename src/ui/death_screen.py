"""
DeathScreen Class

This class handles the display and management of the death screen in the game,
allowing the player to choose whether to restart the game or quit using keyboard inputs.
It includes rendering the title and action buttons (retry and quit) and handling user input.
"""
import pygame

class DeathScreen:
    def __init__(self, screen):
        """
        Initialize the death screen with necessary fonts and texts.

        Args:
            screen (pygame.Surface): The game screen surface.
        """
        self.screen = screen  # store the game screen surface
        self.title_font = pygame.font.Font(None, 100)  # font for the title text
        self.button_font = pygame.font.Font(None, 36)  # font for button texts

        # render text for title and buttons
        self.title_text = self.title_font.render("Continue?", True, (29, 185, 17))
        self.retry_button_text = self.button_font.render("Press Enter to Continue", True, (255, 255, 255))
        self.quit_button_text = self.button_font.render("Press Esc to Quit", True, (255, 255, 255))

        # calculate the rectangles for centering the text
        self.title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.retry_button_rect = self.retry_button_text.get_rect(center=(self.screen.get_width() // 2, 400))
        self.quit_button_rect = self.quit_button_text.get_rect(center=(self.screen.get_width() // 2, 500))


    def draw(self):
        """
        Draws the death screen with the title and buttons.
        """
        self.screen.fill((0, 0, 0))  # fill the screen with a black background
        self.screen.blit(self.title_text, self.title_rect)  # draw the title text centered
        self.screen.blit(self.retry_button_text, self.retry_button_rect)  # draw the retry button text centered
        self.screen.blit(self.quit_button_text, self.quit_button_rect)  # draw the quit button text centered
        pygame.display.flip()  # update the display with the drawn content


    def handle_event(self, event, game_state, P1):
        """
        Handle keyboard events for the death screen.

        Args:
            event (pygame.event.Event): The event to handle.
            game_state (str): The current game state.
            P1 (Player): The player object.

        Returns:
            str: 'RESTART' if the player chooses to continue, None otherwise.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # restart the game on Enter key press
                return 'RESTART'
            elif event.key == pygame.K_ESCAPE:  # quit the game on Escape key press
                pygame.mixer.music.stop()  # stop any background music
                pygame.quit()  # quit the game
                exit()  # exit the program
        return None  # no action if no relevant key is pressed