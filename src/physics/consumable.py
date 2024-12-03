import pygame
import os
from constants import PROJECT_ROOT
from pygame.locals import *


class Consumable(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()

        self.cherry_image =  self.load_sprites(os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'fruits', '03.png'), 16, 16)
        self.image = self.cherry_image[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_collected = False

    def update(self, player, health):
        # Check for collision with the player

        if not self.is_collected and self.rect.colliderect(player.rect):
            self.on_collect(health)

    def on_collect(self, health):
        # Add code to update score, remove consumable, etc.
        print(f"Before collecting: Health = {health.health_count}")
        if health.health_count < 4:  # Ensure health doesn't exceed the max
            health.health_count += 1
            health.current_frame = 4 - health.health_count
            health.health_image = health.health_frames[health.current_frame]
            print(f"After collecting: Health = {health.health_count}")
        else:
            print("Health is already at maximum!")
        self.is_collected = True
        self.kill()  # Remove the sprite
        
        

    def draw(self, surface, camera):
        if self.is_collected == False:
            surface.blit(self.image, camera.apply(self.rect))
        else:
            pass
        

    def load_sprites(self, sprite_sheet_path, frame_width, frame_height):
        # load the sprite sheet
        sprite_sheet = pygame.image.load(sprite_sheet_path)
        sheet_width, sheet_height = sprite_sheet.get_size()
        num_frames = sheet_width // frame_width  # calculate the number of frames based on the width of the sheet
        frames = []
        
        for i in range(num_frames):
            frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (50, 50))
            frames.append(frame)
        return frames
