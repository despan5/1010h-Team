import pygame

class Screen():
    def __init__(self, screen_width, screen_height, bg_path):
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.DISPLAY_SURF = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        bg_original = pygame.image.load('C:/Users/thoma/Documents/GitHub/1010h-Team/Sprites/game_background.jpg')
        self.bg = pygame.transform.scale(bg_original, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.DISPLAY_SURF.fill((255, 255, 255))
        pygame.display.set_caption("Game")

    def Draw_Background(self):
        self.DISPLAY_SURF.blit(self.bg, (0, 0))

    def get_surface(self):
        return self.DISPLAY_SURF