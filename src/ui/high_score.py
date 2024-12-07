import pygame
from ui.score_manager import ScoreManager
from database import Database

class HighScore:
    def __init__(self, screen):
        
        self.screen = screen

        self.title_font = pygame.font.Font(None, 100)
        self.button_font = pygame.font.Font(None, 36)
        self.title_text = self.title_font.render("High Scores", True, (29, 185, 17))
        self.start_button_text = self.button_font.render("Press Enter to Return to Title", True, (255, 255, 255))
        self.quit_button_text = self.button_font.render("Press Esc to Quit", True, (255, 255, 255))

        self.title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.start_button_rect = self.start_button_text.get_rect(center=(self.screen.get_width() // 2, 800))
        self.quit_button_rect = self.quit_button_text.get_rect(center=(self.screen.get_width() // 2, 900))

         # Initialize ScoreManager to fetch high scores
        self.score_manager = ScoreManager()  # You can pass the file name here if needed
        self.score_manager.load_scores()  # Make sure to load scores here
        self.high_scores = Database().get_dict_of_all_scores_and_users()  # Fetch the top scores after loading them


    def draw(self):
       
        self.screen.fill((0, 0, 0))  # Black background
        self.screen.blit(self.title_text, self.title_rect)
        self.screen.blit(self.start_button_text, self.start_button_rect)
        self.screen.blit(self.quit_button_text, self.quit_button_rect)

        # Ensure high_scores is populated correctly before drawing
        if not self.high_scores:
            print("No high scores loaded.")
        else:
            # Display the top scores
            for index, (player_name, score) in enumerate(sorted(self.high_scores.items(), key=lambda item: item[1], reverse=True)[:5]):  # Sort by score in descending order and get top 5
                score_text = pygame.font.Font(None, 36).render(f"{player_name}: {score}", True, (255, 255, 255))
                self.screen.blit(score_text, (self.screen.get_width() // 2 - score_text.get_width() // 2, 300 + (index * 50)))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Start game when Enter is pressed
                pygame.mixer.music.stop()  # Stop the music before starting the game
                return 'RETURN'
            elif event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                pygame.quit()
                return 'QUIT'
        return None