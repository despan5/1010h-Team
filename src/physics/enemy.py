"""
Enemy Class

This script defines the `Enemy` class, representing hostile entities that move 
within a specified range and interact with the player.
"""

import pygame
import os
from constants import PROJECT_ROOT


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, movement_range, platforms, screen_height, speed=2):
        super().__init__()
        
        # Enemy attributes
        self.speed = speed
        self.start_x = x
        self.movement_range = movement_range
        self.is_facing_right = True

        # Load sprite sheet
        sprite_sheet_path = os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'male', 'mort', 'ghost', 'move.png')
        self.hit_sound = pygame.mixer.Sound(os.path.join(PROJECT_ROOT, 'assets', 'sound', 'oof.mp3'))
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.walking_sprites = self.load_sprites(sprite_sheet, 24, 24)
        self.current_frame = 0
        self.animation_delay = 10
        self.animation_counter = 0

        # Initialize sprite image and rect
        self.image = self.walking_sprites[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Movement variables
        self.velocity_x = self.speed

        # movement properties
        self.start_x = x  # initial position to calculate movement bounds
        self.movement_range = movement_range  # max range enemy can move
        self.is_facing_right = True  # direction of the enemy's facing

        # references to platforms and screen height
        self.platforms = platforms
        self.screen_height = screen_height

        # Load hit sound
        hit_sound_path = os.path.join(PROJECT_ROOT, 'assets', 'sound', 'oof.mp3')
        if os.path.exists(hit_sound_path):
            self.hit_sound = pygame.mixer.Sound(hit_sound_path)
            self.hit_sound.set_volume(0.5)  # Adjust volume if needed
        else:
            self.hit_sound = None
            print(f"Sound file not found: {hit_sound_path}")

    def load_sprites(self, sprite_sheet, frame_width, frame_height):
        """Extract frames from the sprite sheet."""
        sheet_width, sheet_height = sprite_sheet.get_size()
        num_frames = sheet_width // frame_width
        frames = []
        for i in range(num_frames):
            # extract a frame and scale it for better visibility
            frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (100, 100))  # Resize the sprite frame
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
      
        """Handle collision with the player."""
        if self.rect.colliderect(player.rect):  # Check if player collides with enemy
            if player.bite_animation_playing:  # If player is biting
                player.increase_score(100)  # Award score for defeating the enemy
                if self.hit_sound:  # Play sound only if it is loaded
                    self.hit_sound.play()
                self.kill()  # Remove the enemy
            else:  # Player hit without biting
                if self.hit_sound:  # Play sound only if it is loaded
                    self.hit_sound.play()
                # Push the player back based on the collision direction
                if player.rect.centerx < self.rect.centerx:  # Player is to the left of the enemy
                    player.rect.x -= 150  # Push the player back to the left
                else:  # Player is to the right of the enemy
                    player.rect.x += 150  # Push the player back to the right
                player.hp.Take_Damage()  # Reduce player's health

    def Draw(self, surface, camera):
        """Draw the enemy sprite."""
        surface.blit(self.image, camera.apply(self.rect))
