import pygame
import os
import math  # Import math for trigonometric functions
from constants import PROJECT_ROOT

class Egg(pygame.sprite.Sprite):
    def __init__(self, x, y, points=50):
        super().__init__()

        # Load egg sprite
        sprite_path = os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'male', 'mort', 'egg', 'egg.png')
        self.image = pygame.image.load(sprite_path)
        self.image = pygame.transform.scale(self.image, (60, 60))  # Adjust the size as needed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Bobbing motion variables
        self.start_y = y
        self.bob_range = 5  # Range of bobbing motion
        self.bob_speed = 0.1  # Speed of bobbing
        self.bob_counter = 0

        # Points awarded for collecting the egg
        self.points = points

        # Collection state
        self.is_collected = False

    def update(self, player):
        """Update the egg's position and check for collection."""
        # Bobbing motion
        self.bob_counter += self.bob_speed
        self.rect.y = self.start_y + int(self.bob_range * math.sin(self.bob_counter))  # Use math.sin

        # Check for collision with player
        if not self.is_collected and self.rect.colliderect(player.rect):
            self.on_collect(player)

    def on_collect(self, player):
        """Handle egg collection by the player."""
        print(f"Egg collected! Awarded {self.points} points.")
        player.increase_score(self.points)  # Add points to the player's score
        self.is_collected = True
        self.kill()  # Remove the egg sprite from the game

    def draw(self, surface, camera):
        """Draw the egg on the screen."""
        if not self.is_collected:
            surface.blit(self.image, camera.apply(self.rect))
