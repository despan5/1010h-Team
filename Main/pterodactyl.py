import pygame
import random
import os
import math

class PterodactylManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pterodactyls = []
        level = 0
        
        # Simple level multiplier, can be changed
        adjusted_speed = 8 + {2.5 ** level}
        adjusted_Size = 0.20 * (1.15 * {level})

        # Private speed and size (encapsulated)
        self._speed = adjusted_speed # Default speed
        self._resize_percentage = adjusted_Size  # Default resize percentage

        # Load pterodactyl image
        base_path = os.path.dirname(__file__)
        image_path = os.path.join(base_path, '..', 'Sprites', 'assets', 'pterodactyl', 'Pterodactyl_up_left.png')
        self.pterodactyl_image = pygame.image.load(image_path).convert_alpha()

        # Resize the image based on the initial size
        self._resize_image()

    def _resize_image(self):
        """Resize the pterodactyl image based on the current resize percentage."""
        original_width = self.pterodactyl_image.get_width()
        original_height = self.pterodactyl_image.get_height()

        new_width = int(original_width * self._resize_percentage)
        new_height = int(original_height * self._resize_percentage)

        if new_width > 0 and new_height > 0:
            self.pterodactyl_image = pygame.transform.scale(self.pterodactyl_image, (new_width, new_height))

    def generate_pterodactyl(self):
        """Generate a pterodactyl at a random location at the top of the screen and move it towards a random location at the bottom."""
        # Generate a random X position at the top of the screen
        x = random.randint(0, self.screen_width - self.pterodactyl_image.get_width())
        y = -self.pterodactyl_image.get_height()

        # Generate a random target position at the bottom of the screen
        target_x = random.randint(0, self.screen_width)
        target_y = self.screen_height + 50  # Extra padding below the screen

        # Calculate direction towards the random target position at the bottom
        direction_x = target_x - x
        direction_y = target_y - y

        # Normalize the direction vector
        length = math.sqrt(direction_x ** 2 + direction_y ** 2)

        # Store the pterodactyl's position and velocity vector
        self.pterodactyls.append({
            'x': x,
            'y': y,
            'velocity_x': (direction_x / length) * self._speed,  # Use internal speed
            'velocity_y': (direction_y / length) * self._speed
        })

    def update_pterodactyls(self):
        """Update the position of all pterodactyls based on their velocity."""
        for pterodactyl in self.pterodactyls:
            pterodactyl['x'] += pterodactyl['velocity_x']
            pterodactyl['y'] += pterodactyl['velocity_y']

        # Remove pterodactyls that are off-screen (below the screen)
        self.pterodactyls[:] = [p for p in self.pterodactyls if p['y'] < self.screen_height]

    def draw(self, surface):
        """Draw the pterodactyls on the surface."""
        for pterodactyl in self.pterodactyls:
            surface.blit(self.pterodactyl_image, (pterodactyl['x'], pterodactyl['y']))  # No camera offset needed

    # Getter methods to allow main.py to retrieve the values but not modify them
    def get_speed(self):
        """Return the speed of the pterodactyl."""
        return self._speed

    def get_size(self):
        """Return the resize percentage of the pterodactyl."""
        return self._resize_percentage
