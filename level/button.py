"""
Button Class

This script defines a reusable `Button` class using Pygame. 
It allows creating interactive buttons with click detection and scaling functionality.
"""

import pygame

# button class definition
class Button():
    def __init__(self, x, y, image, scale):
        """
        Initialize the button with position, image, and scale.

        Args:
            x (int): X-coordinate of the button's top-left corner.
            y (int): Y-coordinate of the button's top-left corner.
            image (Surface): Pygame image to display as the button.
            scale (float): Scaling factor for resizing the button.
        """
        # get original image dimensions
        width = image.get_width()
        height = image.get_height()
        # scale the image to the desired size
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        # create a rectangle for collision detection
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)  # set rectangle position
        self.clicked = False  # track whether the button was clicked

    def draw(self, surface):
        """
        Draw the button on the given surface and handle click detection.

        Args:
            surface (Surface): Pygame surface where the button is drawn.

        Returns:
            bool: True if the button is clicked, otherwise False.
        """
        action = False  # flag to track if the button was clicked

        # get the current mouse position
        pos = pygame.mouse.get_pos()

        # check if the mouse is over the button and if it is clicked
        if self.rect.collidepoint(pos):  # check if mouse is over the button
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True  # button click action triggered
                self.clicked = True  # mark button as clicked

        # reset clicked state when mouse button is released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw the button on the screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action  # return whether the button was clicked
