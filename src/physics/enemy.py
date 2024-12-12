import pygame
import os
from constants import PROJECT_ROOT

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, movement_range, platforms, screen_height):
        super().__init__()
        sprite_sheet_path = os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'male', 'mort', 'ghost', 'move.png')

        # Load the sprite sheet
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.walking_sprites = self.load_sprites(sprite_sheet, 24, 24)
        self.current_frame = 0
        self.animation_delay = 10  # Adjust for smooth animation
        self.animation_counter = 0

        self.image = self.walking_sprites[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Movement variables
        self.velocity_x = 2  # Horizontal speed
        self.start_x = x
        self.movement_range = movement_range
        self.is_facing_right = True

        # Reference to platforms and screen height
        self.platforms = platforms
        self.screen_height = screen_height

    def load_sprites(self, sprite_sheet, frame_width, frame_height):
        # Extract frames from the sprite sheet
        sheet_width, sheet_height = sprite_sheet.get_size()
        num_frames = sheet_width // frame_width
        frames = []

        for i in range(num_frames):
            frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (100, 100))
            frames.append(frame)
        return frames

    def update(self):
        """Update the enemy's position and animation."""
        # Horizontal movement logic
        self.rect.x += self.velocity_x
        if self.rect.x <= self.start_x - self.movement_range or self.rect.x >= self.start_x + self.movement_range:
            self.velocity_x *= -1  # Reverse direction
            self.is_facing_right = not self.is_facing_right  # Flip the direction

        # Update the animation frame
        self.animation_counter += 1
        if self.animation_counter >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.walking_sprites)
            self.animation_counter = 0

        # Update the image and flip it if necessary
        self.image = self.walking_sprites[self.current_frame]
        if not self.is_facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def Check_Collision(self, player, screen_height):
        """Handle collision with the player."""
        if self.rect.colliderect(player.rect):
            # Reset player position upon collision with the enemy
            player.rect.center = (160, screen_height - 300)
            player.hp.Take_Damage()  # Assuming player has an hp attribute

    def Draw(self, surface, camera):
        """Draw the enemy sprite."""
        surface.blit(self.image, camera.apply(self.rect))
