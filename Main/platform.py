import pygame

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def Draw(self, surface, camera):
        pygame.draw.rect(surface, (0, 255, 0), camera.apply(self.rect))

    def Check_Collision(self, player):
        if player.velocity_y > 0 and player.rect.bottom <= self.rect.top and \
            player.rect.bottom + player.velocity_y >= self.rect.top and \
            self.rect.left < player.rect.centerx < self.rect.right:
            player.rect.bottom = self.rect.top
            player.velocity_y = 0
            player.is_jumping = False
        else:
            if not (self.rect.left < player.rect.centerx < self.rect.right) and player.rect.bottom == self.rect.top:
                player.is_jumping = True
