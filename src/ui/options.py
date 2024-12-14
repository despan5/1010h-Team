# StartScreen class manages the initial screen elements (title, buttons) for the game using pygame.

import pygame

class StartScreen:
    def __init__(self, screen):
        # initialize with the given screen
        self.screen = screen

        # define fonts for title, input, and buttons
        self.title_font = pygame.font.Font(None, 100)
        self.input_font = pygame.font.Font(None, 45)
        self.button_font = pygame.font.Font(None, 36)

        # create text elements
        self.title_text = self.title_font.render("Dino Dash", True, (29, 185, 17))
        self.start_button_text = self.button_font.render("Press Enter to Start", True, (255, 255, 255))
        self.score_button_text = self.button_font.render("Press Tab to see High Scores", True, (255, 255, 255))
        self.quit_button_text = self.button_font.render("Press Esc to Quit", True, (255, 255, 255))

        # positions for each text element
        self.title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.start_button_rect = self.start_button_text.get_rect(center=(self.screen.get_width() // 2, 400))
        self.score_button_rect = self.score_button_text.get_rect(center=(self.screen.get_width() // 2, 500))
        self.quit_button_rect = self.quit_button_text.get_rect(center=(self.screen.get_width() // 2, 600))

    def draw(self):
        """Draws the start screen, including the input box."""
        self.screen.fill((0, 0, 0))  # fill screen with black background
        self.screen.blit(self.title_text, self.title_rect)  # draw title
        self.screen.blit(self.start_button_text, self.start_button_rect)  # draw start button text
        self.screen.blit(self.score_button_text, self.score_button_rect)  # draw score button text
        self.screen.blit(self.quit_button_text, self.quit_button_rect)  # draw quit button text