'''
HighScore Class

This class manages the display of high scores on the screen, allowing users to view the 
top scores and return to the title or quit the game.

'''
import pygame
from database import database

class highscore:
    def __init__(self, screen):
        
        self.screen = screen

        self.title_font = pygame.font.Font(None, 100)
        self.button_font = pygame.font.Font(None, 36)
        self.title_text = self.title_font.render("high scores", True, (29, 185, 17))
        self.start_button_text = self.button_font.render("press enter to return to title", True, (255, 255, 255))
        self.quit_button_text = self.button_font.render("press esc to quit", True, (255, 255, 255))

        self.title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.start_button_rect = self.start_button_text.get_rect(center=(self.screen.get_width() // 2, 800))
        self.quit_button_rect = self.quit_button_text.get_rect(center=(self.screen.get_width() // 2, 900))

        # initialize scoremanager to fetch high scores
        # you can pass the file name here if needed  # make sure to load scores here
        self.high_scores = database().get_dict_of_all_scores_and_users()  # fetch the top scores after loading them

    def draw(self):
        self.screen.fill((0, 0, 0))  # black background
        self.screen.blit(self.title_text, self.title_rect)
        self.screen.blit(self.start_button_text, self.start_button_rect)
        self.screen.blit(self.quit_button_text, self.quit_button_rect)

        # ensure high_scores is populated correctly before drawing
        if not self.high_scores:
            print("no high scores loaded.")
        else:
            # display the top scores
            for index, (player_name, score) in enumerate(sorted(self.high_scores.items(), key=lambda item: item[1], reverse=True)[:5]):  # sort by score in descending order and get top 5
                score_text = pygame.font.Font(None, 36).render(f"{player_name}: {score}", True, (255, 255, 255))
                self.screen.blit(score_text, (self.screen.get_width() // 2 - score_text.get_width() // 2, 300 + (index * 50)))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # start game when enter is pressed                
                return 'RETURN'
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                return 'QUIT'
        return None
