"""
Consumable Class

This script defines the `Consumable` class, which represents collectible items in the game.
The consumable can be collected by the player to increase score and health.
"""

import pygame
import os
from constants import PROJECT_ROOT
from pygame.locals import *
import random

class Consumable(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        Initialize the consumable object.
        Args:
            x (int): initial x-coordinate of the consumable.
            y (int): initial y-coordinate of the consumable.
        """
        super().__init__()

        # get screen dimensions
        self.info = pygame.display.Info()
        self.SCREEN_WIDTH = self.info.current_w
        self.SCREEN_HEIGHT = self.info.current_h

        # load sprite frames for the consumable
        self.cherry_image = self.load_sprites(
            os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'fruits', '03.png'), 16, 16
        )
        self.image = self.cherry_image[0]  # default frame
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_collected = False  # tracks whether the consumable has been collected

    def update(self, player, health):
        """
        Update the state of the consumable.
        Args:
            player (Player): the player object for collision detection.
            health (Health): the health system object to manage player's health.
        """
        if not self.is_collected and self.rect.colliderect(player.rect):
            self.on_collect(health, player)  # handle collection logic

    def on_collect(self, health, player):
        """
        Handle logic when the consumable is collected.
        Args:
            health (Health): the health system object to modify player's health.
            player (Player): the player object to update score.
        """
        print(f"Before collecting: Health = {health.health_count}")
        player.increase_score(10)  # add points to player's score
        
        # increase health if it's below the maximum
        if health.health_count < 4:
            health.health_count += 1
            health.current_frame = 4 - health.health_count  # adjust health display
            health.health_image = health.health_frames[health.current_frame]
            print(f"After collecting: Health = {health.health_count}")
        else:
            print("Health is already at maximum!")
        
        self.is_collected = True  # mark as collected
        self.kill()  # remove the sprite from all groups

    def draw(self, surface, camera):
        """
        Draw the consumable on the screen.
        Args:
            surface (pygame.Surface): the display surface to draw on.
            camera (Camera): the camera object for scrolling effect.
        """
        if not self.is_collected:
            surface.blit(self.image, camera.apply(self.rect))  # draw if not collected

    def load_sprites(self, sprite_sheet_path, frame_width, frame_height):
        """
        Load frames from a sprite sheet and scale them.
        Args:
            sprite_sheet_path (str): path to the sprite sheet.
            frame_width (int): width of each frame in the sheet.
            frame_height (int): height of each frame in the sheet.
        Returns:
            list: list of scaled frames as pygame surfaces.
        """
        sprite_sheet = pygame.image.load(sprite_sheet_path)  # load sprite sheet
        sheet_width, _ = sprite_sheet.get_size()
        num_frames = sheet_width // frame_width  # calculate number of frames

        frames = []
        for i in range(num_frames):
            # extract each frame from the sprite sheet
            frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (50, 50))  # scale to uniform size
            frames.append(frame)
        return frames

    def reset(self):
        """
        Reset the consumable to its initial state.
        """
        self.is_collected = False
        # generate a new random position for the consumable
        self.rect.x = random.randint(0, self.SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, self.SCREEN_HEIGHT - self.rect.height)