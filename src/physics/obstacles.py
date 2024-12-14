"""
Obstacles and Door Classes

These classes define static objects in the game world, such as platforms and doors. 
They handle rendering, collision detection, and interactions with the player.
"""

import pygame


class Obstacles:
    """
    Represents a static platform or obstacle in the game world.
    """

    def __init__(self, x, y, width, height):
        """
        Initialize the obstacle with a position and size.

        Args:
            x (int): X-coordinate of the top-left corner.
            y (int): Y-coordinate of the top-left corner.
            width (int): Width of the obstacle.
            height (int): Height of the obstacle.
        """
        self.rect = pygame.Rect(x, y, width, height)

    def Draw(self, surface, camera):
        """
        Draw the obstacle on the game surface.

        Args:
            surface (pygame.Surface): The surface to draw on.
            camera (Camera): The camera object for scrolling logic.
        """
        pygame.draw.rect(surface, (0, 255, 0), camera.apply(self.rect))  # green rectangle for the platform.

    def Check_Collision(self, player):
        """
        Check and handle collision between the player and the obstacle.

        Args:
            player (Player): The player object to check collision with.
        """
        # check if the player is falling and collides with the top of the platform
        if (
            player.velocity_y > 0  # player is falling
            and player.rect.bottom <= self.rect.top  # player is above the platform
            and player.rect.bottom + player.velocity_y >= self.rect.top  # player will reach the platform this frame
            and self.rect.left < player.rect.centerx < self.rect.right  # player's horizontal center is within platform bounds
        ):
            # stop the player's downward movement and reset jump state
            player.rect.bottom = self.rect.top
            player.velocity_y = 0
            player.is_jumping = False
        else:
            # if the player moves off the platform, re-enable jumping
            if not (self.rect.left < player.rect.centerx < self.rect.right) and player.rect.bottom == self.rect.top:
                player.is_jumping = True


class Door:
    """
    Represents a door that the player can interact with.
    """

    def __init__(self, x, y):
        """
        Initialize the door with a position and size.

        Args:
            x (int): X-coordinate of the top-left corner.
            y (int): Y-coordinate of the top-left corner.
        """
        self.rect = pygame.Rect(x, y, 50, 100)  # door dimensions are fixed at 50x100

    def Draw(self, surface, camera):
        """
        Draw the door on the game surface.

        Args:
            surface (pygame.Surface): The surface to draw on.
            camera (Camera): The camera object for scrolling logic.
        """
        pygame.draw.rect(surface, (255, 0, 0), camera.apply(self.rect))  # red rectangle for the door.

    def Check_Collision(self, player):
        """
        Check if the player collides with the door.

        Args:
            player (Player): The player object to check collision with.

        Returns:
            bool: True if the player collides with the door, otherwise False.
        """
        return self.rect.colliderect(player.rect)