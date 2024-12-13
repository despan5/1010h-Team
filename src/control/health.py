"""
Health Class

This script defines a `Health` class for managing a player's health in a game. It handles health states, 
health bar display, and damage effects like flashing and resetting.
"""

import os
import pygame
import time
from constants import PROJECT_ROOT

class Health:
    def __init__(self):
        """
        Initialize the health system with a health bar and flashing effect.
        """
        pygame.font.init()  # initialize font
        self.font = pygame.font.SysFont(None, 48)  # set font
        self.health_count = 4  # start with full health

        # load health bar sprite sheet
        base_path = os.path.dirname(__file__)
        health_bar_path = os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'Health', 'health_bars', 'health_bar.png')
        health_bar_sheet = pygame.image.load(health_bar_path).convert_alpha()

        # dimensions for individual health bar frames
        health_bar_image_width = 48
        health_bar_image_height = 18
        frame_count = 5  # total frames in the sprite sheet

        # extract frames from the sprite sheet
        self.health_frames = []
        for i in range(frame_count):
            # extract frame from sprite sheet
            frame = health_bar_sheet.subsurface(pygame.Rect(i * health_bar_image_width, 0, health_bar_image_width, health_bar_image_height))
            # scale frame for display
            frame = pygame.transform.scale(frame, (health_bar_image_width * 8, health_bar_image_height * 8))
            self.health_frames.append(frame)

        # set initial frame and health image
        self.current_frame = 4 - self.health_count
        self.health_image = self.health_frames[self.current_frame]

        # initialize flashing effect variables
        self.is_flasing = False
        self.flash_start_time = None
        self.flash_duration = 2  # total flash time in seconds
        self.flash_interval = 0.01  # interval between flashes
        self.last_flash_time = 0  # time of the last flash

        # initialize fade effect variables for "you died" screen
        self.alpha = 0  # initial transparency
        self.fade_speed = 0.5  # speed of fade

    def Take_Damage(self):
        """
        Decrease health by one point and start flashing effect. Print "you died" if health reaches zero.
        """
        if self.health_count > 0:
            self.health_count -= 1  # reduce health
            self.current_frame = 4 - self.health_count  # update current frame
            self.health_image = self.health_frames[self.current_frame]  # update health image
            self.is_flasing = True  # start flashing effect
        elif self.health_count == 0:
            print("you died")  # health is zero

    def Draw(self, surface, height, width):
        """
        Draw the current health bar on the screen.
        Args:
            surface (pygame.Surface): surface to draw the health bar on.
            height (int): screen height.
            width (int): screen width.
        """
        x, y = 10, 10  # position of health bar
        if self.health_count > 0:
            surface.blit(self.health_image, (x, y))  # draw health bar

    def reset(self):
        """
        Reset health to full and clear flashing or fade effects.
        """
        self.health_count = 4  # reset to full health
        self.current_frame = 4 - self.health_count  # reset frame
        self.health_image = self.health_frames[self.current_frame]  # reset health image
        self.alpha = 0  # reset alpha for fade effect
