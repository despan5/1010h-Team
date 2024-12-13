"""
Camera Class

This script defines a simple `Camera` class that follows a player in a 2D game, 
keeping the player centered on the screen when they move beyond the center.
"""

import pygame

# camera class definition
class Camera:
    def __init__(self, player, screen_width):
        """
        Initialize the camera to follow the player.

        Args:
            player (pygame.sprite.Sprite): The player object to follow.
            screen_width (int): Width of the game screen in pixels.
        """
        self.player = player  # the player the camera follows
        self.offset_x = 0  # horizontal offset applied to objects
        self.screen_width = screen_width  # width of the screen

    def update(self):
        """
        Update the camera's offset based on the player's position.
        Keeps the player centered once they pass the screen's center.
        """
        # check if player has moved past the screen's center
        if self.player.rect.centerx > self.screen_width // 2:
            # calculate the offset to center the player
            self.offset_x = -(self.player.rect.centerx - self.screen_width // 2)
        else:
            # keep camera stationary until player reaches the center
            self.offset_x = 0

    def apply(self, obj_rect):
        """
        Apply the camera's offset to an object's rect to adjust its position.

        Args:
            obj_rect (pygame.Rect): The object's rectangle to adjust.

        Returns:
            pygame.Rect: A new rectangle adjusted for the camera's offset.
        """
        # shift the object's rectangle by the horizontal offset
        return obj_rect.move(self.offset_x, 0)
