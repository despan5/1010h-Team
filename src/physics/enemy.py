"""
Enemy Class

This script defines the `Enemy` class, representing hostile entities that move 
within a specified range and interact with the player.
"""

import pygame
import os
from constants import PROJECT_ROOT

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, movement_range, platforms, screen_height):
        """
        Initialize an Enemy object.
        Args:
            x (int): initial x-coordinate of the enemy.
            y (int): initial y-coordinate of the enemy.
            movement_range (int): maximum horizontal distance the enemy can move from its start position.
            platforms (list): list of platform objects for collision detection.
            screen_height (int): the height of the game screen.
        """
        super().__init__()

        # load sprite sheet for enemy animation
        sprite_sheet_path = os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'male', 'mort', 'ghost', 'move.png')
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()

        self.walking_sprites = self.load_sprites(sprite_sheet, 24, 24)  # load animation frames
        self.current_frame = 0  # track current frame of animation
        self.animation_delay = 10  # delay between animation frames for smoothness
        self.animation_counter = 0  # counter to manage frame updates

        self.image = self.walking_sprites[self.current_frame]  # set the initial frame
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # movement properties
        self.velocity_x = 2  # horizontal movement speed
        self.start_x = x  # initial position to calculate movement bounds
        self.movement_range = movement_range  # max range enemy can move
        self.is_facing_right = True  # direction of the enemy's facing

        # references to platforms and screen height
        self.platforms = platforms
        self.screen_height = screen_height

    def load_sprites(self, sprite_sheet, frame_width, frame_height):
        """
        Extract frames from the sprite sheet.
        Args:
            sprite_sheet (pygame.Surface): the loaded sprite sheet.
            frame_width (int): width of each animation frame.
            frame_height (int): height of each animation frame.
        Returns:
            list: list of extracted and scaled frames as pygame surfaces.
        """
        sheet_width, _ = sprite_sheet.get_size()  # get sprite sheet dimensions
        num_frames = sheet_width // frame_width  # calculate the number of frames

        frames = []
        for i in range(num_frames):
            # extract a frame and scale it for better visibility
            frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (100, 100))
            frames.append(frame)
        return frames

    def update(self):
        """
        Update the enemy's position and animation.
        Handles horizontal movement and frame animation.
        """
        # move horizontally within the defined range
        self.rect.x += self.velocity_x
        if self.rect.x <= self.start_x - self.movement_range or self.rect.x >= self.start_x + self.movement_range:
            self.velocity_x *= -1  # reverse direction
            self.is_facing_right = not self.is_facing_right  # update facing direction

        # update the animation frame
        self.animation_counter += 1
        if self.animation_counter >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.walking_sprites)  # loop through frames
            self.animation_counter = 0

        # update the displayed image and flip it if the direction changes
        self.image = self.walking_sprites[self.current_frame]
        if not self.is_facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def Check_Collision(self, player, screen_height):
        """
        Handle collision with the player.
        Args:
            player (Player): the player object to check for collisions.
            screen_height (int): the height of the game screen.
        """
        if self.rect.colliderect(player.rect):  # detect collision
            if player.bite_animation_playing:  # player attacks
                player.increase_score(100)  # award points
                self.kill()  # remove enemy
            else:
                # push the player away based on the collision direction
                if player.rect.centerx < self.rect.centerx:
                    player.rect.x -= 150  # push player left
                else:
                    player.rect.x += 150  # push player right
                player.hp.Take_Damage()  # reduce player's health

    def Draw(self, surface, camera):
        """
        Draw the enemy on the screen.
        Args:
            surface (pygame.Surface): the surface to draw the enemy on.
            camera (Camera): the camera object for scrolling.
        """
        surface.blit(self.image, camera.apply(self.rect))