import pygame

class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(300, 400, 50, 50)

    def Draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect)
    
    def Check_Collision(self, player, screen_height):
        if self.rect.colliderect(player.rect):
                player.rect.center = (160, screen_height - 300)
        else:
            pass