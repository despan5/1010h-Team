import pygame
from physics.player import Player

class StartScreen:
    def __init__(self, screen):
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
        
    def draw(self):
        self.screen.fill((0, 0, 0))  # Black background
        self.screen.blit(self.title_text, self.title_rect)  # Display title centered
        self.screen.blit(self.start_button_text, self.start_button_rect)  # Display start button text centered
        self.screen.blit(self.quit_button_text, self.quit_button_rect)  # Display quit button text centered

        # Animation parameters
        walk_distance = 300  # Total distance to walk
        step_size = 5  # How much to move each frame
        jump_height = 100  # How high to jump
        jump_duration = 20  # Frames to jump

        # Move the player across the screen
        for i in range(0, walk_distance, step_size):
            self.screen.fill((0, 0, 0))  # Black background
            self.screen.blit(self.title_text, self.title_rect)  # Display title centered
            self.screen.blit(self.start_button_text, self.start_button_rect)  # Display start button text centered
            self.screen.blit(self.quit_button_text, self.quit_button_rect)  # Display quit button text centered            self.player.Update([], None, None, self.screen.get_height())  # Update player without collision detection
            self.player.rect.x += step_size  # Move right
            self.player.Draw(self.screen, None)  # Draw player

            pygame.display.flip()
            pygame.time.delay(30)  # Control speed of walking

        # Jump logic
        for j in range(jump_duration):
            self.screen.fill((0, 0, 0))  # Black background
            self.screen.blit(self.title_text, self.title_rect)  # Display title centered
            self.screen.blit(self.start_button_text, self.start_button_rect)  # Display start button text centered
            self.screen.blit(self.quit_button_text, self.quit_button_rect)  # Display quit button text centered
            if j < jump_duration // 2:  # Ascending
                self.player.rect.y -= jump_height / (jump_duration // 2)  # Move up
            else:  # Descending
                self.player.rect.y += jump_height / (jump_duration // 2)  # Move down
            
            # Update and draw the player with jumping effect
            self.player.Update([], None, None, self.screen.get_height())  # Update player without collision detection
            self.player.Draw(self.screen, None)  # Draw player
            
            pygame.display.flip()
            pygame.time.delay(30)  # Control speed of jump

        # Final display
        pygame.time.delay(1000)  # Pause before allowing interaction
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Start game when Enter is pressed
                return True
            elif event.key == pygame.K_ESCAPE:
                pygame.QUIT()
        return False
