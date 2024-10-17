import pygame



class Consumable(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        

    def update(self, player):
        # Check for collision with the player
        if self.rect.colliderect(player.rect):
            self.on_collect()

    def on_collect(self):
        # Add code to update score, remove consumable, etc.
        print("Collected!")
        self.kill()  # Remove the sprite

    def draw(self, surface, camera):
        surface.blit(self.image, camera.apply(self.rect))