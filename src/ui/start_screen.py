import pygame
from database import Database

class StartScreen:
    def __init__(self, screen):
        
        self.screen = screen

        # Fonts
        self.title_font = pygame.font.Font(None, 100)
        self.input_font = pygame.font.Font(None, 45)
        self.button_font = pygame.font.Font(None, 36)

        # Text elements
        self.title_text = self.title_font.render("Dino Dash", True, (29, 185, 17))
        self.start_button_text = self.button_font.render("Press Enter to Start", True, (255, 255, 255))
        self.score_button_text = self.button_font.render("Press Tab to see High Scores", True, (255, 255, 255))
        self.quit_button_text = self.button_font.render("Press Esc to Quit", True, (255, 255, 255))

        # Text positions
        self.title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.start_button_rect = self.start_button_text.get_rect(center=(self.screen.get_width() // 2, 400))
        self.score_button_rect = self.score_button_text.get_rect(center=(self.screen.get_width() // 2, 500))
        self.quit_button_rect = self.quit_button_text.get_rect(center=(self.screen.get_width() // 2, 600))

        # Input box attributes
        self.input_box_rect = pygame.Rect(self.screen.get_width() // 2 - 160, 300, 320, 50)
        self.input_box_color = pygame.Color("chartreuse4")
        self.input_text = ""
        self.text_surface = self.input_font.render(self.input_text, True, (255, 255, 255))  # White text
        self.active = True  # Is the input box active?

        # Blinker for cursor
        self.blink = True
        self.blink_timer = pygame.time.get_ticks()

        # Character limit
        self.max_characters = 15

        self.username = None  # To store the final username

    def draw(self):
        """Draws the start screen, including the input box."""
        self.screen.fill((0, 0, 0))  # Black background
        self.screen.blit(self.title_text, self.title_rect)
        self.screen.blit(self.start_button_text, self.start_button_rect)
        self.screen.blit(self.score_button_text, self.score_button_rect)
        self.screen.blit(self.quit_button_text, self.quit_button_rect)

        # Draw the input box
        pygame.draw.rect(self.screen, self.input_box_color, self.input_box_rect, 2)  # Border
        self.screen.blit(self.text_surface, (self.input_box_rect.x + 5, self.input_box_rect.y + 10))

        # Draw blinking cursor
        if self.active:
            if self.blink:
                cursor_x = self.input_box_rect.x + 5 + self.text_surface.get_width()
                cursor_y = self.input_box_rect.y + 10
                pygame.draw.line(self.screen, (255, 255, 255), (cursor_x, cursor_y), (cursor_x, cursor_y + 30), 2)

    def handle_event(self, event):
        """Handles events for the start screen, including text input."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle the active state of the input box if clicked
            if self.input_box_rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.input_box_color = (0, 255, 0) if self.active else pygame.Color("chartreuse4")  # Green if active

        if event.type == pygame.KEYDOWN:
            if self.active:  # Only process keypresses if the input box is active
                if event.key == pygame.K_RETURN:
                    if self.input_text.strip():  # Ensure the input box is not empty
                        self.username = self.input_text.upper()
                        print(self.username)
                        
                        exists = Database().check_user(self.username)  # Check if the user already exists
                    

                        if exists:
                            print("User already exists!")
                            return 'START_GAME'
                        else:
                            Database().add_user(self.username)  # Add the score to the database
                            return 'START_GAME'
                        
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]  # Remove last character
                elif event.key == pygame.K_TAB:
                    return 'SCORE_SCREEN'
                else:
                    if len(self.input_text) < self.max_characters:  # Check character limit
                        self.input_text += event.unicode  # Add typed character
                # Update the text surface
                self.text_surface = self.input_font.render(self.input_text, True, (255, 255, 255))

            elif event.key == pygame.K_ESCAPE:  # Quit when Esc is pressed
                pygame.mixer.music.stop()
                pygame.quit()
                return 'QUIT'
        return None

    def update(self):
        """Updates the blinking cursor."""
        if pygame.time.get_ticks() - self.blink_timer > 500:  # Toggle every 500 ms
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()
